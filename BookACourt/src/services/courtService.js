// src/services/courtService.js
import apiClient from './api';

export const courtService = {
    // Court Categories
    async getCategories() {
        const response = await apiClient.get('/courts/categories/');
        return response.data;
    },

    async getCategoryById(id) {
        const response = await apiClient.get(`/courts/categories/${id}/`);
        return response.data;
    },

    // Court Registrations
    async submitRegistration(data) {
        const formData = new FormData();
        Object.keys(data).forEach(key => {
            if (data[key] !== null && data[key] !== undefined) {
                formData.append(key, data[key]);
            }
        });
        const response = await apiClient.post('/courts/registrations/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
        return response.data;
    },

    async getMyRegistrations() {
        const response = await apiClient.get('/courts/registrations/');
        return response.data;
    },

    async approveRegistration(id) {
        const response = await apiClient.post(`/courts/registrations/${id}/approve/`);
        return response.data;
    },

    async rejectRegistration(id, reason) {
        const response = await apiClient.post(`/courts/registrations/${id}/reject/`, { reason });
        return response.data;
    },

    // Courts
    async getCourts(params = {}) {
        const response = await apiClient.get('/courts/courts/', { params });
        return response.data;
    },

    async getCourtById(id) {
        const response = await apiClient.get(`/courts/courts/${id}/`);
        return response.data;
    },

    async createCourt(data) {
        const response = await apiClient.post('/courts/courts/', data);
        return response.data;
    },

    async updateCourt(id, data) {
        const response = await apiClient.patch(`/courts/courts/${id}/`, data);
        return response.data;
    },

    async checkAvailability(courtId, data) {
        const response = await apiClient.post(`/courts/courts/${courtId}/check_availability/`, data);
        return response.data;
    },

    async getAvailableSlots(courtId, date) {
        const response = await apiClient.get(`/courts/courts/${courtId}/available_slots/`, {
            params: { date }
        });
        return response.data;
    },

    async addManager(courtId, managerId) {
        const response = await apiClient.post(`/courts/courts/${courtId}/add_manager/`, {
            manager_id: managerId
        });
        return response.data;
    },

    async removeManager(courtId, managerId) {
        const response = await apiClient.post(`/courts/courts/${courtId}/remove_manager/`, {
            manager_id: managerId
        });
        return response.data;
    },

    // Court Reviews
    async getCourtReviews(courtId, params = {}) {
        const response = await apiClient.get(`/courts/courts/${courtId}/reviews/`, { params });
        return response.data;
    },

    async getReviewById(courtId, reviewId) {
        const response = await apiClient.get(`/courts/courts/${courtId}/reviews/${reviewId}/`);
        return response.data;
    },

    async createReview(courtId, data) {
        const response = await apiClient.post(`/courts/courts/${courtId}/reviews/`, data);
        return response.data;
    },

    async updateReview(courtId, reviewId, data) {
        const response = await apiClient.patch(`/courts/courts/${courtId}/reviews/${reviewId}/`, data);
        return response.data;
    },

    async deleteReview(courtId, reviewId) {
        const response = await apiClient.delete(`/courts/courts/${courtId}/reviews/${reviewId}/`);
        return response.data;
    },

    async respondToReview(courtId, reviewId, response_text) {
        const response = await apiClient.post(
            `/courts/courts/${courtId}/reviews/${reviewId}/respond/`,
            { owner_response: response_text }
        );
        return response.data;
    },

    async flagReview(courtId, reviewId, reason) {
        const response = await apiClient.post(
            `/courts/courts/${courtId}/reviews/${reviewId}/flag/`,
            { reason }
        );
        return response.data;
    },

    async getMyReviews(params = {}) {
        const response = await apiClient.get('/courts/reviews/my_reviews/', { params });
        return response.data;
    },

    // Blocked Slots
    async getBlockedSlots(courtId, params = {}) {
        const response = await apiClient.get(`/courts/courts/${courtId}/blocked-slots/`, { params });
        return response.data;
    },

    async createBlockedSlot(courtId, data) {
        const response = await apiClient.post(`/courts/courts/${courtId}/blocked-slots/`, data);
        return response.data;
    },

    async updateBlockedSlot(courtId, slotId, data) {
        const response = await apiClient.patch(`/courts/courts/${courtId}/blocked-slots/${slotId}/`, data);
        return response.data;
    },

    async deleteBlockedSlot(courtId, slotId) {
        const response = await apiClient.delete(`/courts/courts/${courtId}/blocked-slots/${slotId}/`);
        return response.data;
    },

    // Dynamic Pricing
    async getPricingRules(courtId, params = {}) {
        const response = await apiClient.get(`/courts/courts/${courtId}/pricing/`, { params });
        return response.data;
    },

    async getPricingRuleById(courtId, ruleId) {
        const response = await apiClient.get(`/courts/courts/${courtId}/pricing/${ruleId}/`);
        return response.data;
    },

    async createPricingRule(courtId, data) {
        const response = await apiClient.post(`/courts/courts/${courtId}/pricing/`, data);
        return response.data;
    },

    async updatePricingRule(courtId, ruleId, data) {
        const response = await apiClient.patch(`/courts/courts/${courtId}/pricing/${ruleId}/`, data);
        return response.data;
    },

    async deletePricingRule(courtId, ruleId) {
        const response = await apiClient.delete(`/courts/courts/${courtId}/pricing/${ruleId}/`);
        return response.data;
    },

    async togglePricingRule(courtId, ruleId) {
        const response = await apiClient.post(`/courts/courts/${courtId}/pricing/${ruleId}/toggle/`);
        return response.data;
    },

    // Equipment
    async getEquipment(courtId, params = {}) {
        const response = await apiClient.get(`/courts/courts/${courtId}/equipment/`, { params });
        return response.data;
    },

    async getEquipmentById(courtId, equipmentId) {
        const response = await apiClient.get(`/courts/courts/${courtId}/equipment/${equipmentId}/`);
        return response.data;
    },

    async createEquipment(courtId, data) {
        const response = await apiClient.post(`/courts/courts/${courtId}/equipment/`, data);
        return response.data;
    },

    async updateEquipment(courtId, equipmentId, data) {
        const response = await apiClient.patch(`/courts/courts/${courtId}/equipment/${equipmentId}/`, data);
        return response.data;
    },

    async deleteEquipment(courtId, equipmentId) {
        const response = await apiClient.delete(`/courts/courts/${courtId}/equipment/${equipmentId}/`);
        return response.data;
    },

    async updateEquipmentQuantity(courtId, equipmentId, quantity) {
        const response = await apiClient.patch(`/courts/courts/${courtId}/equipment/${equipmentId}/`, {
            quantity_total: quantity
        });
        return response.data;
    },

    // Court Images
    async uploadCourtImage(courtId, imageFile) {
        const formData = new FormData();
        formData.append('image', imageFile);
        const response = await apiClient.post(`/courts/courts/${courtId}/images/`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
        return response.data;
    },

    async deleteCourtImage(courtId, imageId) {
        const response = await apiClient.delete(`/courts/courts/${courtId}/images/${imageId}/`);
        return response.data;
    },

    async setMainImage(courtId, imageId) {
        const response = await apiClient.post(`/courts/courts/${courtId}/images/${imageId}/set_main/`);
        return response.data;
    },

    // Court Statistics
    async getCourtStatistics(courtId, params = {}) {
        const response = await apiClient.get(`/courts/courts/${courtId}/statistics/`, { params });
        return response.data;
    },

    async getCourtRevenue(courtId, params = {}) {
        const response = await apiClient.get(`/courts/courts/${courtId}/revenue/`, { params });
        return response.data;
    },

    async getCourtBookingHistory(courtId, params = {}) {
        const response = await apiClient.get(`/courts/courts/${courtId}/booking_history/`, { params });
        return response.data;
    },

    // Search and Filter
    async searchCourts(query, params = {}) {
        const response = await apiClient.get('/courts/courts/search/', {
            params: { q: query, ...params }
        });
        return response.data;
    },

    async filterCourts(filters = {}) {
        const response = await apiClient.get('/courts/courts/', { params: filters });
        return response.data;
    },

    async getNearbyCourts(latitude, longitude, radius = 5) {
        const response = await apiClient.get('/courts/courts/nearby/', {
            params: { lat: latitude, lng: longitude, radius }
        });
        return response.data;
    },

    // Court Favorites (for players)
    async addToFavorites(courtId) {
        const response = await apiClient.post(`/courts/courts/${courtId}/favorite/`);
        return response.data;
    },

    async removeFromFavorites(courtId) {
        const response = await apiClient.delete(`/courts/courts/${courtId}/favorite/`);
        return response.data;
    },

    async getFavoriteCourts(params = {}) {
        const response = await apiClient.get('/courts/courts/favorites/', { params });
        return response.data;
    },

    // Court Verification
    async requestVerification(courtId) {
        const response = await apiClient.post(`/courts/courts/${courtId}/request_verification/`);
        return response.data;
    },

    async verifyCourt(courtId, verificationData) {
        const response = await apiClient.post(`/courts/courts/${courtId}/verify/`, verificationData);
        return response.data;
    }
};