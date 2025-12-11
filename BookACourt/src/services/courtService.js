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
    async getCourtReviews(courtId) {
        const response = await apiClient.get(`/courts/courts/${courtId}/reviews/`);
        return response.data;
    },

    async createReview(courtId, data) {
        const response = await apiClient.post(`/courts/courts/${courtId}/reviews/`, data);
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

    // Blocked Slots
    async getBlockedSlots(courtId, params = {}) {
        const response = await apiClient.get(`/courts/courts/${courtId}/blocked-slots/`, { params });
        return response.data;
    },

    async createBlockedSlot(courtId, data) {
        const response = await apiClient.post(`/courts/courts/${courtId}/blocked-slots/`, data);
        return response.data;
    },

    async deleteBlockedSlot(courtId, slotId) {
        const response = await apiClient.delete(`/courts/courts/${courtId}/blocked-slots/${slotId}/`);
        return response.data;
    },

    // Dynamic Pricing
    async getPricingRules(courtId) {
        const response = await apiClient.get(`/courts/courts/${courtId}/pricing/`);
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

    // Equipment
    async getEquipment(courtId) {
        const response = await apiClient.get(`/courts/courts/${courtId}/equipment/`);
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
    }
};