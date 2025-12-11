// src/services/cancellationPolicyService.js
import apiClient from './api';

export const cancellationPolicyService = {
    // ===== CANCELLATION POLICIES =====
    async getPolicies(params = {}) {
        const response = await apiClient.get('/bookings/cancellation-policies/', { params });
        return response.data;
    },

    async getPolicyById(id) {
        const response = await apiClient.get(`/bookings/cancellation-policies/${id}/`);
        return response.data;
    },

    async createPolicy(data) {
        const response = await apiClient.post('/bookings/cancellation-policies/', data);
        return response.data;
    },

    async updatePolicy(id, data) {
        const response = await apiClient.patch(`/bookings/cancellation-policies/${id}/`, data);
        return response.data;
    },

    async deletePolicy(id) {
        const response = await apiClient.delete(`/bookings/cancellation-policies/${id}/`);
        return response.data;
    },

    async getPolicyByCourtId(courtId) {
        const response = await apiClient.get('/bookings/cancellation-policies/', {
            params: { court: courtId }
        });
        return response.data.results?.[0] || response.data[0] || null;
    },

    // ===== POLICY HELPERS =====
    calculateRefundAmount(policy, booking, cancelTime = new Date()) {
        if (!policy || !booking) return 0;

        const bookingTime = new Date(booking.booking_date + ' ' + booking.start_time);
        const hoursUntilBooking = (bookingTime - cancelTime) / (1000 * 60 * 60);

        if (hoursUntilBooking < policy.cancellation_deadline_hours) {
            // Past deadline, no refund
            return 0;
        }

        if (hoursUntilBooking >= policy.full_refund_hours) {
            // Full refund
            return parseFloat(booking.total_amount);
        }

        if (hoursUntilBooking >= policy.partial_refund_hours) {
            // Partial refund
            return parseFloat(booking.total_amount) * (policy.partial_refund_percentage / 100);
        }

        return 0;
    },

    getRefundInfo(policy, booking, cancelTime = new Date()) {
        if (!policy || !booking) {
            return {
                canCancel: true,
                refundAmount: 0,
                refundPercentage: 0,
                message: 'No cancellation policy available'
            };
        }

        const bookingTime = new Date(booking.booking_date + ' ' + booking.start_time);
        const hoursUntilBooking = (bookingTime - cancelTime) / (1000 * 60 * 60);

        if (hoursUntilBooking < policy.cancellation_deadline_hours) {
            return {
                canCancel: false,
                refundAmount: 0,
                refundPercentage: 0,
                message: `Cancellation deadline passed (${policy.cancellation_deadline_hours} hours before booking)`
            };
        }

        if (hoursUntilBooking >= policy.full_refund_hours) {
            return {
                canCancel: true,
                refundAmount: parseFloat(booking.total_amount),
                refundPercentage: 100,
                message: `Full refund available (${policy.full_refund_hours}+ hours before booking)`
            };
        }

        if (hoursUntilBooking >= policy.partial_refund_hours) {
            const refundAmount = parseFloat(booking.total_amount) * (policy.partial_refund_percentage / 100);
            return {
                canCancel: true,
                refundAmount,
                refundPercentage: policy.partial_refund_percentage,
                message: `${policy.partial_refund_percentage}% refund available`
            };
        }

        return {
            canCancel: true,
            refundAmount: 0,
            refundPercentage: 0,
            message: 'No refund available at this time'
        };
    }
};