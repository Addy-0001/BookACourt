// src/services/paymentService.js
import apiClient from './api';

export const paymentService = {
    // Payment Methods
    async getPaymentMethods() {
        const response = await apiClient.get('/payments/methods/');
        return response.data;
    },

    async getPaymentMethodById(id) {
        const response = await apiClient.get(`/payments/methods/${id}/`);
        return response.data;
    },

    async createPaymentMethod(data) {
        const response = await apiClient.post('/payments/methods/', data);
        return response.data;
    },

    async updatePaymentMethod(id, data) {
        const response = await apiClient.patch(`/payments/methods/${id}/`, data);
        return response.data;
    },

    async deletePaymentMethod(id) {
        const response = await apiClient.delete(`/payments/methods/${id}/`);
        return response.data;
    },

    async setDefaultPaymentMethod(id) {
        const response = await apiClient.post(`/payments/methods/${id}/set_default/`);
        return response.data;
    },

    // Payments
    async getPayments(params = {}) {
        const response = await apiClient.get('/payments/', { params });
        return response.data;
    },

    async getPaymentById(id) {
        const response = await apiClient.get(`/payments/${id}/`);
        return response.data;
    },

    async initiatePayment(bookingId, paymentMethodId) {
        const response = await apiClient.post('/payments/', {
            booking: bookingId,
            payment_method: paymentMethodId
        });
        return response.data;
    },

    async verifyPayment(paymentId, verificationData) {
        const response = await apiClient.post(`/payments/${paymentId}/verify/`, verificationData);
        return response.data;
    },

    async refundPayment(paymentId, amount = null, reason = '') {
        const response = await apiClient.post(`/payments/${paymentId}/refund/`, {
            amount,
            reason
        });
        return response.data;
    },

    // Wallet
    async getWallet() {
        const response = await apiClient.get('/payments/wallet/');
        return response.data;
    },

    async addWalletFunds(amount, paymentMethodId) {
        const response = await apiClient.post('/payments/wallet/add_funds/', {
            amount,
            payment_method: paymentMethodId
        });
        return response.data;
    },

    async getWalletTransactions(params = {}) {
        const response = await apiClient.get('/payments/wallet/transactions/', { params });
        return response.data;
    },

    // Loyalty & Rewards
    async getLoyaltyPoints() {
        const response = await apiClient.get('/payments/loyalty/points/');
        return response.data;
    },

    async getLoyaltyTransactions(params = {}) {
        const response = await apiClient.get('/payments/loyalty/transactions/', { params });
        return response.data;
    },

    async redeemPoints(points, bookingId) {
        const response = await apiClient.post('/payments/loyalty/redeem/', {
            points,
            booking: bookingId
        });
        return response.data;
    },

    async getAvailableRewards() {
        const response = await apiClient.get('/payments/loyalty/rewards/');
        return response.data;
    },

    async claimReward(rewardId) {
        const response = await apiClient.post(`/payments/loyalty/rewards/${rewardId}/claim/`);
        return response.data;
    },

    // Coupons
    async getCoupons(params = {}) {
        const response = await apiClient.get('/payments/coupons/', { params });
        return response.data;
    },

    async getCouponById(id) {
        const response = await apiClient.get(`/payments/coupons/${id}/`);
        return response.data;
    },

    async validateCoupon(code, bookingAmount) {
        const response = await apiClient.post('/payments/coupons/validate/', {
            code,
            booking_amount: bookingAmount
        });
        return response.data;
    },

    async applyCoupon(code, bookingId) {
        const response = await apiClient.post('/payments/coupons/apply/', {
            code,
            booking: bookingId
        });
        return response.data;
    },

    // Payment Gateway Integration
    async initializeKhaltiPayment(bookingId, amount) {
        const response = await apiClient.post('/payments/khalti/initialize/', {
            booking: bookingId,
            amount
        });
        return response.data;
    },

    async verifyKhaltiPayment(token, amount) {
        const response = await apiClient.post('/payments/khalti/verify/', {
            token,
            amount
        });
        return response.data;
    },

    async initializeEsewaPayment(bookingId, amount) {
        const response = await apiClient.post('/payments/esewa/initialize/', {
            booking: bookingId,
            amount
        });
        return response.data;
    },

    async verifyEsewaPayment(oid, amt, refId) {
        const response = await apiClient.post('/payments/esewa/verify/', {
            oid,
            amt,
            refId
        });
        return response.data;
    }
};