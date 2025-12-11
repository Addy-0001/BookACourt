// src/services/userService.js
import apiClient from './api';

export const userService = {
    // ===== USER PROFILE =====
    async getProfile() {
        const response = await apiClient.get('/user/profile/');
        return response.data;
    },

    async updateProfile(data) {
        const response = await apiClient.patch('/user/profile/', data);
        return response.data;
    },

    // ===== USER PREFERENCES =====
    async getPreferences() {
        const response = await apiClient.get('/users/preferences/');
        return response.data;
    },

    async getMyPreferences() {
        const response = await apiClient.get('/users/preferences/me/');
        return response.data;
    },

    async createPreferences(data) {
        const response = await apiClient.post('/users/preferences/', data);
        return response.data;
    },

    async updatePreferences(id, data) {
        const response = await apiClient.patch(`/users/preferences/${id}/`, data);
        return response.data;
    },

    async updateMyPreferences(data) {
        const response = await apiClient.patch('/users/preferences/update_me/', data);
        return response.data;
    },

    async deletePreferences(id) {
        const response = await apiClient.delete(`/users/preferences/${id}/`);
        return response.data;
    },

    // ===== FRIENDSHIPS =====
    async getFriendships(params = {}) {
        const response = await apiClient.get('/users/friendships/', { params });
        return response.data;
    },

    async getFriendshipById(id) {
        const response = await apiClient.get(`/users/friendships/${id}/`);
        return response.data;
    },

    async sendFriendRequest(toUserId) {
        const response = await apiClient.post('/users/friendships/', {
            to_user: toUserId
        });
        return response.data;
    },

    async acceptFriendRequest(id) {
        const response = await apiClient.post(`/users/friendships/${id}/accept/`, {});
        return response.data;
    },

    async rejectFriendRequest(id) {
        const response = await apiClient.post(`/users/friendships/${id}/reject/`, {});
        return response.data;
    },

    async removeFriend(id) {
        const response = await apiClient.delete(`/users/friendships/${id}/`);
        return response.data;
    },

    async getMyFriends() {
        const response = await apiClient.get('/users/friendships/my_friends/');
        return response.data;
    },

    async getPendingRequests() {
        const response = await apiClient.get('/users/friendships/pending_requests/');
        return response.data;
    },

    async getSentRequests() {
        const response = await apiClient.get('/users/friendships/sent_requests/');
        return response.data;
    },

    // ===== PLAYER STATISTICS =====
    async getPlayerStats(params = {}) {
        const response = await apiClient.get('/users/player-stats/', { params });
        return response.data;
    },

    async getPlayerStatsById(id) {
        const response = await apiClient.get(`/users/player-stats/${id}/`);
        return response.data;
    },

    async getMyStats() {
        const response = await apiClient.get('/users/player-stats/me/');
        return response.data;
    },

    async getLeaderboard(params = {}) {
        const response = await apiClient.get('/users/player-stats/leaderboard/', { params });
        return response.data;
    }
};