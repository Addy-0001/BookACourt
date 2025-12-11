// src/services/bookingService.js
import apiClient from './api';

export const bookingService = {
    // Bookings
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

    // Match Events
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

    async cancelMatch(id) {
        const response = await apiClient.patch(`/matches/${id}/`, {
            status: 'CANCELLED'
        });
        return response.data;
    },

    // Player Ratings
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

    // Equipment Rentals
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

    // Booking Shares
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

    // Booking Stats
    async getBookingStats() {
        const response = await apiClient.get('/bookings/stats/');
        return response.data;
    }
};