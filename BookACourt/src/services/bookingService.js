// src/services/bookingService.js - ENHANCED VERSION
import apiClient from './api';

export const bookingService = {
    // ===== BOOKINGS =====
    async getBookings(params = {}) {
        const response = await apiClient.get('/bookings/', { params });
        return response.data;
    },

    async getBookingById(id) {
        const response = await apiClient.get(`/bookings/${id}/`);
        return response.data;
    },

    async createBooking(data) {
        const response = await apiClient.post('/bookings/', data);
        return response.data;
    },

    async updateBooking(id, data) {
        const response = await apiClient.patch(`/bookings/${id}/`, data);
        return response.data;
    },

    async cancelBooking(id, reason) {
        const response = await apiClient.patch(`/bookings/${id}/`, {
            status: 'CANCELLED',
            cancellation_reason: reason
        });
        return response.data;
    },

    async getMyBookings(status = null) {
        const params = status ? { status } : {};
        const response = await apiClient.get('/bookings/', { params });
        return response.data;
    },

    async confirmBooking(id) {
        const response = await apiClient.post(`/bookings/${id}/confirm/`);
        return response.data;
    },

    async markAsCompleted(id) {
        const response = await apiClient.post(`/bookings/${id}/complete/`);
        return response.data;
    },

    async markAsNoShow(id) {
        const response = await apiClient.post(`/bookings/${id}/no_show/`);
        return response.data;
    },

    // ===== RECURRING BOOKINGS =====
    async createRecurringBooking(data) {
        const response = await apiClient.post('/bookings/recurring/', data);
        return response.data;
    },

    async getRecurringBookings(params = {}) {
        const response = await apiClient.get('/bookings/recurring/', { params });
        return response.data;
    },

    async getRecurringBookingById(id) {
        const response = await apiClient.get(`/bookings/recurring/${id}/`);
        return response.data;
    },

    async updateRecurringBooking(id, data) {
        const response = await apiClient.patch(`/bookings/recurring/${id}/`, data);
        return response.data;
    },

    async cancelRecurringBooking(id, cancelFuture = true) {
        const response = await apiClient.post(`/bookings/recurring/${id}/cancel/`, {
            cancel_future: cancelFuture
        });
        return response.data;
    },

    // ===== MATCH EVENTS =====
    async getMatches(params = {}) {
        const response = await apiClient.get('/matches/', { params });
        return response.data;
    },

    async getMatchById(id) {
        const response = await apiClient.get(`/matches/${id}/`);
        return response.data;
    },

    async createMatch(data) {
        const response = await apiClient.post('/matches/', data);
        return response.data;
    },

    async updateMatch(id, data) {
        const response = await apiClient.patch(`/matches/${id}/`, data);
        return response.data;
    },

    async joinMatch(id) {
        const response = await apiClient.post(`/matches/${id}/join/`);
        return response.data;
    },

    async leaveMatch(id) {
        const response = await apiClient.post(`/matches/${id}/leave/`);
        return response.data;
    },

    async cancelMatch(id, reason = '') {
        const response = await apiClient.patch(`/matches/${id}/`, {
            status: 'CANCELLED',
            cancellation_reason: reason
        });
        return response.data;
    },

    async startMatch(id) {
        const response = await apiClient.post(`/matches/${id}/start/`);
        return response.data;
    },

    async endMatch(id, winnerId = null) {
        const response = await apiClient.post(`/matches/${id}/end/`, {
            winner: winnerId
        });
        return response.data;
    },

    async getMatchParticipants(id) {
        const response = await apiClient.get(`/matches/${id}/participants/`);
        return response.data;
    },

    async inviteToMatch(matchId, userId) {
        const response = await apiClient.post(`/matches/${matchId}/invite/`, {
            user: userId
        });
        return response.data;
    },

    // ===== PLAYER RATINGS =====
    async ratePlayer(matchId, playerId, rating, feedback, misconduct = false, misconductDetails = '') {
        const response = await apiClient.post('/player-ratings/', {
            match_event: matchId,
            rated_player: playerId,
            rating,
            feedback,
            misconduct_reported: misconduct,
            misconduct_details: misconductDetails
        });
        return response.data;
    },

    async getPlayerRatings(userId) {
        const response = await apiClient.get('/player-ratings/', {
            params: { user: userId }
        });
        return response.data;
    },

    async getMyRatings() {
        const response = await apiClient.get('/player-ratings/my_ratings/');
        return response.data;
    },

    // ===== EQUIPMENT RENTALS =====
    async rentEquipment(bookingId, equipmentId, quantity) {
        const response = await apiClient.post('/equipment-rentals/', {
            booking: bookingId,
            equipment: equipmentId,
            quantity
        });
        return response.data;
    },

    async getBookingEquipment(bookingId) {
        const response = await apiClient.get('/equipment-rentals/', {
            params: { booking: bookingId }
        });
        return response.data;
    },

    async returnEquipment(rentalId, damageNotes = '', damageCharge = 0) {
        const response = await apiClient.patch(`/equipment-rentals/${rentalId}/`, {
            status: 'RETURNED',
            damage_notes: damageNotes,
            damage_charge: damageCharge
        });
        return response.data;
    },

    async reportDamage(rentalId, notes, estimatedCost) {
        const response = await apiClient.post(`/equipment-rentals/${rentalId}/report_damage/`, {
            damage_notes: notes,
            damage_charge: estimatedCost
        });
        return response.data;
    },

    // ===== BOOKING SHARES =====
    async createBookingShare(bookingId, maxJoins = 5, expiresInHours = 24) {
        const expiresAt = new Date();
        expiresAt.setHours(expiresAt.getHours() + expiresInHours);

        const response = await apiClient.post('/booking-shares/', {
            booking: bookingId,
            max_joins: maxJoins,
            expires_at: expiresAt.toISOString()
        });
        return response.data;
    },

    async getBookingShare(token) {
        const response = await apiClient.get(`/booking-shares/${token}/`);
        return response.data;
    },

    async joinSharedBooking(token) {
        const response = await apiClient.post(`/booking-shares/${token}/join/`);
        return response.data;
    },

    async revokeBookingShare(token) {
        const response = await apiClient.delete(`/booking-shares/${token}/`);
        return response.data;
    },

    // ===== BOOKING STATS & ANALYTICS =====
    async getBookingStats() {
        const response = await apiClient.get('/bookings/stats/');
        return response.data;
    },

    async getMyBookingHistory(params = {}) {
        const response = await apiClient.get('/bookings/history/', { params });
        return response.data;
    },

    async getUpcomingBookings() {
        const response = await apiClient.get('/bookings/upcoming/');
        return response.data;
    },

    async getPastBookings(params = {}) {
        const response = await apiClient.get('/bookings/past/', { params });
        return response.data;
    },

    // ===== BOOKING REMINDERS =====
    async setBookingReminder(bookingId, reminderTime) {
        const response = await apiClient.post(`/bookings/${bookingId}/reminder/`, {
            reminder_time: reminderTime
        });
        return response.data;
    },

    async cancelBookingReminder(bookingId) {
        const response = await apiClient.delete(`/bookings/${bookingId}/reminder/`);
        return response.data;
    },

    // ===== WAITLIST =====
    async joinWaitlist(courtId, date, timeSlot) {
        const response = await apiClient.post('/bookings/waitlist/', {
            court: courtId,
            date,
            time_slot: timeSlot
        });
        return response.data;
    },

    async leaveWaitlist(waitlistId) {
        const response = await apiClient.delete(`/bookings/waitlist/${waitlistId}/`);
        return response.data;
    },

    async getMyWaitlist() {
        const response = await apiClient.get('/bookings/waitlist/my/');
        return response.data;
    },

    // ===== CHECK-IN / CHECK-OUT =====
    async checkIn(bookingId, location = null) {
        const response = await apiClient.post(`/bookings/${bookingId}/check_in/`, {
            location
        });
        return response.data;
    },

    async checkOut(bookingId) {
        const response = await apiClient.post(`/bookings/${bookingId}/check_out/`);
        return response.data;
    },

    // ===== BOOKING MODIFICATIONS =====
    async requestReschedule(bookingId, newDate, newStartTime, newEndTime, reason = '') {
        const response = await apiClient.post(`/bookings/${bookingId}/reschedule/`, {
            new_date: newDate,
            new_start_time: newStartTime,
            new_end_time: newEndTime,
            reason
        });
        return response.data;
    },

    async approveReschedule(requestId) {
        const response = await apiClient.post(`/bookings/reschedule/${requestId}/approve/`);
        return response.data;
    },

    async rejectReschedule(requestId, reason) {
        const response = await apiClient.post(`/bookings/reschedule/${requestId}/reject/`, {
            reason
        });
        return response.data;
    },

    // ===== BOOKING EXTENSIONS =====
    async requestExtension(bookingId, additionalHours) {
        const response = await apiClient.post(`/bookings/${bookingId}/extend/`, {
            additional_hours: additionalHours
        });
        return response.data;
    }
};