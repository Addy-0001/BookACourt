import apiClient from './api';

export const authService = {
    async register(userData) {
        const response = await apiClient.post('/auth/register/', userData);
        return response.data;
    },

    async login(credentials) {
        const response = await apiClient.post('/auth/login/', credentials);
        if (response.data.access) {
            localStorage.setItem('access_token', response.data.access);
            localStorage.setItem('refresh_token', response.data.refresh);
            localStorage.setItem('user', JSON.stringify(response.data.user));
        }
        return response.data;
    },

    async logout() {
        try {
            const refreshToken = localStorage.getItem('refresh_token');
            await apiClient.post('/auth/logout/', { refresh: refreshToken });
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user');
        }
    },

    async requestOTP(phoneNumber) {
        const response = await apiClient.post('/auth/otp/request/', {
            phone_number: phoneNumber,
        });
        return response.data;
    },

    async verifyOTP(phoneNumber, otpCode) {
        const response = await apiClient.post('/auth/otp/verify/', {
            phone_number: phoneNumber,
            otp_code: otpCode,
        });
        return response.data;
    },

    async checkAuthStatus() {
        const response = await apiClient.get('/auth/status/');
        return response.data;
    },

    getCurrentUser() {
        const userStr = localStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    },

    isAuthenticated() {
        return !!localStorage.getItem('access_token');
    },

    async updateProfile(userData) {
        const response = await apiClient.patch('/user/profile/', userData);
        // Update local storage
        localStorage.setItem('user', JSON.stringify(response.data));
        return response.data;
    },
};
