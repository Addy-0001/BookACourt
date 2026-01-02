// src/services/adminApi.js
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance with default config
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add token to requests
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Handle token refresh on 401
// In api.js (and copy to adminApi.js)
api.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config;

        // Only attempt refresh on 401, and only once
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('refresh_token');
                if (!refreshToken) throw new Error('No refresh token available');

                const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
                    refresh: refreshToken,
                });

                const { access } = response.data;
                localStorage.setItem('access_token', access);

                // Update Authorization header and retry original request
                originalRequest.headers.Authorization = `Bearer ${access}`;
                return api(originalRequest);
            } catch (refreshError) {
                console.error('Token refresh failed:', refreshError);

                // Clean up tokens
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('user');

                // Use router for safe redirect (import at top of file)
                const router = useRouter();
                router.replace('/admin/login'); // ← Use your admin login path

                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

// ============================================
// USER MANAGEMENT APIs
// ============================================

export const userManagementApi = {
    // Get all users with filters
    getAllUsers(params = {}) {
        return api.get('/users/', { params });
    },

    // Get user by ID
    getUserById(userId) {
        return api.get(`/users/${userId}/`);
    },

    // Update user
    updateUser(userId, userData) {
        return api.patch(`/users/${userId}/`, userData);
    },

    // Delete user
    deleteUser(userId) {
        return api.delete(`/users/${userId}/`);
    },

    // Activate/Deactivate user
    toggleUserStatus(userId, isActive) {
        return api.patch(`/users/${userId}/`, { is_active: isActive });
    },

    // Verify phone number
    verifyPhone(userId) {
        return api.patch(`/users/${userId}/`, { is_phone_verified: true });
    },

    // Change user role
    changeUserRole(userId, role) {
        return api.patch(`/users/${userId}/`, { role });
    },

    // Get player statistics
    getPlayerStats(params = {}) {
        return api.get('/users/player-stats/', { params });
    },

    // Get specific player stats
    getPlayerStatsById(statsId) {
        return api.get(`/users/player-stats/${statsId}/`);
    },

    // Get friendships
    getFriendships(params = {}) {
        return api.get('/users/friendships/', { params });
    },

    // Accept/Reject friendship
    updateFriendship(friendshipId, status) {
        return api.patch(`/users/friendships/${friendshipId}/`, { status });
    },
};

// ============================================
// COURT MANAGEMENT APIs
// ============================================

export const courtManagementApi = {
    // Court Categories
    getCategories(params = {}) {
        return api.get('/courts/categories/', { params });
    },

    getCategoryById(categoryId) {
        return api.get(`/courts/categories/${categoryId}/`);
    },

    createCategory(categoryData) {
        return api.post('/courts/categories/', categoryData);
    },

    updateCategory(categoryId, categoryData) {
        return api.patch(`/courts/categories/${categoryId}/`, categoryData);
    },

    deleteCategory(categoryId) {
        return api.delete(`/courts/categories/${categoryId}/`);
    },

    // Court Registrations
    getRegistrations(params = {}) {
        return api.get('/courts/registrations/', { params });
    },

    getRegistrationById(registrationId) {
        return api.get(`/courts/registrations/${registrationId}/`);
    },

    approveRegistration(registrationId) {
        return api.post(`/courts/registrations/${registrationId}/approve/`);
    },

    rejectRegistration(registrationId, reason) {
        return api.post(`/courts/registrations/${registrationId}/reject/`, { reason });
    },

    // Courts
    getCourts(params = {}) {
        return api.get('/courts/courts/', { params });
    },

    getCourtById(courtId) {
        return api.get(`/courts/courts/${courtId}/`);
    },

    createCourt(courtData) {
        return api.post('/courts/courts/', courtData);
    },

    updateCourt(courtId, courtData) {
        return api.patch(`/courts/courts/${courtId}/`, courtData);
    },

    deleteCourt(courtId) {
        return api.delete(`/courts/courts/${courtId}/`);
    },

    toggleCourtStatus(courtId, isActive) {
        return api.patch(`/courts/courts/${courtId}/`, { is_active: isActive });
    },

    verifyCourt(courtId) {
        return api.patch(`/courts/courts/${courtId}/`, { is_verified: true });
    },

    // Court availability
    checkAvailability(courtId, date, startTime, endTime) {
        return api.post(`/courts/courts/${courtId}/check_availability/`, {
            date,
            start_time: startTime,
            end_time: endTime,
        });
    },

    getAvailableSlots(courtId, date) {
        return api.get(`/courts/courts/${courtId}/available_slots/`, {
            params: { date },
        });
    },

    // Court managers
    addCourtManager(courtId, managerId) {
        return api.post(`/courts/courts/${courtId}/add_manager/`, {
            manager_id: managerId,
        });
    },

    removeCourtManager(courtId, managerId) {
        return api.post(`/courts/courts/${courtId}/remove_manager/`, {
            manager_id: managerId,
        });
    },

    // Court Reviews
    getCourtReviews(courtId, params = {}) {
        return api.get(`/courts/courts/${courtId}/reviews/`, { params });
    },

    respondToReview(courtId, reviewId, response) {
        return api.post(`/courts/courts/${courtId}/reviews/${reviewId}/respond/`, {
            owner_response: response,
        });
    },

    flagReview(courtId, reviewId, reason) {
        return api.post(`/courts/courts/${courtId}/reviews/${reviewId}/flag/`, {
            reason,
        });
    },

    hideReview(courtId, reviewId) {
        return api.patch(`/courts/courts/${courtId}/reviews/${reviewId}/`, {
            is_visible: false,
        });
    },

    // Blocked Slots
    getBlockedSlots(courtId, params = {}) {
        return api.get(`/courts/courts/${courtId}/blocked-slots/`, { params });
    },

    createBlockedSlot(courtId, slotData) {
        return api.post(`/courts/courts/${courtId}/blocked-slots/`, slotData);
    },

    deleteBlockedSlot(courtId, slotId) {
        return api.delete(`/courts/courts/${courtId}/blocked-slots/${slotId}/`);
    },

    // Dynamic Pricing
    getPricingRules(courtId, params = {}) {
        return api.get(`/courts/courts/${courtId}/pricing/`, { params });
    },

    createPricingRule(courtId, pricingData) {
        return api.post(`/courts/courts/${courtId}/pricing/`, pricingData);
    },

    updatePricingRule(courtId, ruleId, pricingData) {
        return api.patch(`/courts/courts/${courtId}/pricing/${ruleId}/`, pricingData);
    },

    deletePricingRule(courtId, ruleId) {
        return api.delete(`/courts/courts/${courtId}/pricing/${ruleId}/`);
    },

    // Equipment
    getEquipment(courtId, params = {}) {
        return api.get(`/courts/courts/${courtId}/equipment/`, { params });
    },

    createEquipment(courtId, equipmentData) {
        return api.post(`/courts/courts/${courtId}/equipment/`, equipmentData);
    },

    updateEquipment(courtId, equipmentId, equipmentData) {
        return api.patch(`/courts/courts/${courtId}/equipment/${equipmentId}/`, equipmentData);
    },

    deleteEquipment(courtId, equipmentId) {
        return api.delete(`/courts/courts/${courtId}/equipment/${equipmentId}/`);
    },
};

// ============================================
// BOOKING MANAGEMENT APIs
// ============================================

export const bookingManagementApi = {
    // Bookings
    getBookings(params = {}) {
        return api.get('/bookings/bookings/', { params });
    },

    getBookingById(bookingId) {
        return api.get(`/bookings/bookings/${bookingId}/`);
    },

    createBooking(bookingData) {
        return api.post('/bookings/bookings/', bookingData);
    },

    updateBooking(bookingId, bookingData) {
        return api.patch(`/bookings/bookings/${bookingId}/`, bookingData);
    },

    confirmBooking(bookingId) {
        return api.post(`/bookings/bookings/${bookingId}/confirm/`);
    },

    cancelBooking(bookingId, reason) {
        return api.post(`/bookings/bookings/${bookingId}/cancel/`, {
            reason,
        });
    },

    // Cancellation Policies
    getCancellationPolicies(params = {}) {
        return api.get('/bookings/cancellation-policies/', { params });
    },

    getCancellationPolicy(policyId) {
        return api.get(`/bookings/cancellation-policies/${policyId}/`);
    },

    createCancellationPolicy(policyData) {
        return api.post('/bookings/cancellation-policies/', policyData);
    },

    updateCancellationPolicy(policyId, policyData) {
        return api.patch(`/bookings/cancellation-policies/${policyId}/`, policyData);
    },

    // Notifications
    getNotifications(params = {}) {
        return api.get('/bookings/notifications/', { params });
    },

    markNotificationRead(notificationId) {
        return api.post(`/bookings/notifications/${notificationId}/mark_read/`);
    },

    markAllNotificationsRead() {
        return api.post('/bookings/notifications/mark_all_read/');
    },

    // Equipment Rentals
    getEquipmentRentals(params = {}) {
        return api.get('/bookings/equipment-rentals/', { params });
    },

    returnEquipment(rentalId, returnData) {
        return api.post(`/bookings/equipment-rentals/${rentalId}/return_equipment/`, returnData);
    },

    // Match Events
    getMatchEvents(params = {}) {
        return api.get('/bookings/match-events/', { params });
    },

    getMatchEventById(matchId) {
        return api.get(`/bookings/match-events/${matchId}/`);
    },

    createMatchEvent(matchData) {
        return api.post('/bookings/match-events/', matchData);
    },

    cancelMatch(matchId) {
        return api.post(`/bookings/match-events/${matchId}/cancel_match/`);
    },

    // Player Ratings
    getPlayerRatings(params = {}) {
        return api.get('/bookings/player-ratings/', { params });
    },

    // Recurring Bookings
    getRecurringBookings(params = {}) {
        return api.get('/bookings/recurring/', { params });
    },

    getRecurringBookingById(recurringId) {
        return api.get(`/bookings/recurring/${recurringId}/`);
    },

    pauseRecurringBooking(recurringId) {
        return api.post(`/bookings/recurring/${recurringId}/pause/`);
    },

    resumeRecurringBooking(recurringId) {
        return api.post(`/bookings/recurring/${recurringId}/resume/`);
    },

    cancelRecurringBooking(recurringId, cancelFuture = true) {
        return api.post(`/bookings/recurring/${recurringId}/cancel/`, {
            cancel_future: cancelFuture,
        });
    },
};

// ============================================
// STATISTICS & REPORTS APIs
// ============================================

export const statisticsApi = {
    // Dashboard statistics
    getDashboardStats() {
        return Promise.all([
            userManagementApi.getAllUsers({ limit: 1 }),
            courtManagementApi.getCourts({ limit: 1 }),
            bookingManagementApi.getBookings({ limit: 1 }),
            courtManagementApi.getRegistrations({ status: 'PENDING', limit: 100 }),
        ]).then(([users, courts, bookings, registrations]) => ({
            totalUsers: users.data.count || 0,
            totalCourts: courts.data.count || 0,
            totalBookings: bookings.data.count || 0,
            pendingRegistrations: registrations.data.count || 0,
        }));
    },

    // Get booking statistics
    getBookingStats(params = {}) {
        return bookingManagementApi.getBookings(params);
    },

    // Get revenue statistics
    getRevenueStats(params = {}) {
        return bookingManagementApi.getBookings({
            ...params,
            payment_status: 'COMPLETED',
        });
    },

    // Get court performance
    getCourtPerformance(courtId, startDate, endDate) {
        return bookingManagementApi.getBookings({
            court: courtId,
            date_from: startDate,
            date_to: endDate,
        });
    },
};

// ============================================
// EXPORT APIs
// ============================================

export const exportApi = {
    // Export users
    async exportUsers(format = 'csv') {
        const response = await api.get('/users/', {
            params: { export: format },
            responseType: 'blob',
        });
        return response.data;
    },

    // Export courts
    async exportCourts(format = 'csv') {
        const response = await api.get('/courts/courts/', {
            params: { export: format },
            responseType: 'blob',
        });
        return response.data;
    },

    // Export bookings
    async exportBookings(format = 'csv', params = {}) {
        const response = await api.get('/bookings/bookings/', {
            params: { ...params, export: format },
            responseType: 'blob',
        });
        return response.data;
    },

    // Download file helper
    downloadFile(data, filename, type = 'text/csv') {
        const blob = new Blob([data], { type });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
    },
};

export default {
    userManagementApi,
    courtManagementApi,
    bookingManagementApi,
    statisticsApi,
    exportApi,
};