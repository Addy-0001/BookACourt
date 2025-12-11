// src/services/notificationService.js
import apiClient from './api';

export const notificationService = {
    // ===== NOTIFICATIONS =====
    async getNotifications(params = {}) {
        const response = await apiClient.get('/bookings/notifications/', { params });
        return response.data;
    },

    async getNotificationById(id) {
        const response = await apiClient.get(`/bookings/notifications/${id}/`);
        return response.data;
    },

    async getUnreadNotifications() {
        const response = await apiClient.get('/bookings/notifications/unread/');
        return response.data;
    },

    async getUnreadCount() {
        const response = await apiClient.get('/bookings/notifications/unread/');
        const data = response.data;
        return Array.isArray(data) ? data.filter(n => !n.is_read).length : 0;
    },

    async markAsRead(id) {
        const response = await apiClient.post(`/bookings/notifications/${id}/mark_read/`, {});
        return response.data;
    },

    async markAllAsRead() {
        const response = await apiClient.post('/bookings/notifications/mark_all_read/', {});
        return response.data;
    }
};