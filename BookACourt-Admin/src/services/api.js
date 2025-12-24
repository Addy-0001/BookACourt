// src/services/api.js
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor - Add auth token
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

// Response interceptor - Handle token refresh
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('refresh_token');
                const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
                    refresh: refreshToken,
                });

                const { access } = response.data;
                localStorage.setItem('access_token', access);

                originalRequest.headers.Authorization = `Bearer ${access}`;
                return api(originalRequest);
            } catch (refreshError) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('user');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

// ============================================
// AUTH APIs
// ============================================
export const authApi = {
    login(credentials) {
        return api.post('/auth/login/', credentials);
    },

    register(userData) {
        return api.post('/auth/register/', userData);
    },

    logout(refreshToken) {
        return api.post('/auth/logout/', { refresh: refreshToken });
    },

    refreshToken(refreshToken) {
        return api.post('/auth/token/refresh/', { refresh: refreshToken });
    },

    getAuthStatus() {
        return api.get('/auth/status/');
    },

    requestOTP(phoneNumber) {
        return api.post('/auth/otp/request/', { phone_number: phoneNumber });
    },

    verifyOTP(phoneNumber, otpCode) {
        return api.post('/auth/otp/verify/', { 
            phone_number: phoneNumber, 
            otp_code: otpCode 
        });
    },

    changePassword(oldPassword, newPassword1, newPassword2) {
        return api.post('/auth/password/change/', {
            old_password: oldPassword,
            new_password1: newPassword1,
            new_password2: newPassword2,
        });
    },

    resetPasswordConfirm(phoneNumber, otpCode, newPassword1, newPassword2) {
        return api.post('/auth/password/reset/confirm/', {
            phone_number: phoneNumber,
            otp_code: otpCode,
            new_password1: newPassword1,
            new_password2: newPassword2,
        });
    },
};

// ============================================
// USER APIs
// ============================================
export const userApi = {
    // Profile
    getProfile() {
        return api.get('/user/profile/');
    },

    updateProfile(userData) {
        return api.patch('/user/profile/', userData);
    },

    // All Users (Admin)
    getAllUsers(params = {}) {
        return api.get('/users/', { params });
    },

    getUserById(userId) {
        return api.get(`/users/${userId}/`);
    },

    updateUser(userId, userData) {
        return api.patch(`/users/${userId}/`, userData);
    },

    deleteUser(userId) {
        return api.delete(`/users/${userId}/`);
    },

    // Preferences
    getMyPreferences() {
        return api.get('/users/preferences/me/');
    },

    updateMyPreferences(preferences) {
        return api.patch('/users/preferences/update_me/', preferences);
    },

    getPreferences(params = {}) {
        return api.get('/users/preferences/', { params });
    },

    getPreferenceById(preferenceId) {
        return api.get(`/users/preferences/${preferenceId}/`);
    },

    createPreference(preferenceData) {
        return api.post('/users/preferences/', preferenceData);
    },

    updatePreference(preferenceId, preferenceData) {
        return api.patch(`/users/preferences/${preferenceId}/`, preferenceData);
    },

    deletePreference(preferenceId) {
        return api.delete(`/users/preferences/${preferenceId}/`);
    },

    // Friendships
    getFriendships(params = {}) {
        return api.get('/users/friendships/', { params });
    },

    getFriendshipById(friendshipId) {
        return api.get(`/users/friendships/${friendshipId}/`);
    },

    getMyFriends() {
        return api.get('/users/friendships/my_friends/');
    },

    getPendingRequests() {
        return api.get('/users/friendships/pending_requests/');
    },

    getSentRequests() {
        return api.get('/users/friendships/sent_requests/');
    },

    sendFriendRequest(toUserId) {
        return api.post('/users/friendships/', { to_user: toUserId });
    },

    acceptFriendRequest(friendshipId) {
        return api.post(`/users/friendships/${friendshipId}/accept/`);
    },

    rejectFriendRequest(friendshipId) {
        return api.post(`/users/friendships/${friendshipId}/reject/`);
    },

    removeFriend(friendshipId) {
        return api.delete(`/users/friendships/${friendshipId}/`);
    },

    // Player Stats
    getPlayerStats(params = {}) {
        return api.get('/users/player-stats/', { params });
    },

    getPlayerStatsById(statsId) {
        return api.get(`/users/player-stats/${statsId}/`);
    },

    getMyStats() {
        return api.get('/users/player-stats/me/');
    },

    getLeaderboard() {
        return api.get('/users/player-stats/leaderboard/');
    },
};

// ============================================
// COURT APIs
// ============================================
export const courtApi = {
    // Categories
    getCategories(params = {}) {
        return api.get('/courts/categories/', { params });
    },

    getCategoryById(categoryId) {
        return api.get(`/courts/categories/${categoryId}/`);
    },

    createCategory(categoryData) {
        const formData = new FormData();
        Object.keys(categoryData).forEach(key => {
            if (categoryData[key] !== null && categoryData[key] !== undefined) {
                formData.append(key, categoryData[key]);
            }
        });
        return api.post('/courts/categories/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
    },

    updateCategory(categoryId, categoryData) {
        const formData = new FormData();
        Object.keys(categoryData).forEach(key => {
            if (categoryData[key] !== null && categoryData[key] !== undefined) {
                formData.append(key, categoryData[key]);
            }
        });
        return api.patch(`/courts/categories/${categoryId}/`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
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

    createRegistration(registrationData) {
        const formData = new FormData();
        Object.keys(registrationData).forEach(key => {
            formData.append(key, registrationData[key]);
        });
        return api.post('/courts/registrations/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
    },

    updateRegistration(registrationId, registrationData) {
        return api.patch(`/courts/registrations/${registrationId}/`, registrationData);
    },

    approveRegistration(registrationId) {
        return api.post(`/courts/registrations/${registrationId}/approve/`);
    },

    rejectRegistration(registrationId, reason) {
        return api.post(`/courts/registrations/${registrationId}/reject/`, { reason });
    },

    deleteRegistration(registrationId) {
        return api.delete(`/courts/registrations/${registrationId}/`);
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

    checkAvailability(courtId, data) {
        return api.post(`/courts/courts/${courtId}/check_availability/`, data);
    },

    getAvailableSlots(courtId, date) {
        return api.get(`/courts/courts/${courtId}/available_slots/`, { 
            params: { date } 
        });
    },

    addManager(courtId, managerId) {
        return api.post(`/courts/courts/${courtId}/add_manager/`, { 
            manager_id: managerId 
        });
    },

    removeManager(courtId, managerId) {
        return api.post(`/courts/courts/${courtId}/remove_manager/`, { 
            manager_id: managerId 
        });
    },

    // Court Reviews
    getCourtReviews(courtId, params = {}) {
        return api.get(`/courts/courts/${courtId}/reviews/`, { params });
    },

    getCourtReviewById(courtId, reviewId) {
        return api.get(`/courts/courts/${courtId}/reviews/${reviewId}/`);
    },

    createCourtReview(courtId, reviewData) {
        return api.post(`/courts/courts/${courtId}/reviews/`, reviewData);
    },

    updateCourtReview(courtId, reviewId, reviewData) {
        return api.patch(`/courts/courts/${courtId}/reviews/${reviewId}/`, reviewData);
    },

    deleteCourtReview(courtId, reviewId) {
        return api.delete(`/courts/courts/${courtId}/reviews/${reviewId}/`);
    },

    respondToReview(courtId, reviewId, response) {
        return api.post(`/courts/courts/${courtId}/reviews/${reviewId}/respond/`, {
            owner_response: response
        });
    },

    flagReview(courtId, reviewId, reason) {
        return api.post(`/courts/courts/${courtId}/reviews/${reviewId}/flag/`, { 
            reason 
        });
    },

    // Blocked Slots
    getBlockedSlots(courtId, params = {}) {
        return api.get(`/courts/courts/${courtId}/blocked-slots/`, { params });
    },

    getBlockedSlotById(courtId, slotId) {
        return api.get(`/courts/courts/${courtId}/blocked-slots/${slotId}/`);
    },

    createBlockedSlot(courtId, slotData) {
        return api.post(`/courts/courts/${courtId}/blocked-slots/`, slotData);
    },

    updateBlockedSlot(courtId, slotId, slotData) {
        return api.patch(`/courts/courts/${courtId}/blocked-slots/${slotId}/`, slotData);
    },

    deleteBlockedSlot(courtId, slotId) {
        return api.delete(`/courts/courts/${courtId}/blocked-slots/${slotId}/`);
    },

    // Dynamic Pricing
    getPricingRules(courtId, params = {}) {
        return api.get(`/courts/courts/${courtId}/pricing/`, { params });
    },

    getPricingRuleById(courtId, ruleId) {
        return api.get(`/courts/courts/${courtId}/pricing/${ruleId}/`);
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

    getEquipmentById(courtId, equipmentId) {
        return api.get(`/courts/courts/${courtId}/equipment/${equipmentId}/`);
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
// BOOKING APIs
// ============================================
export const bookingApi = {
    // Bookings
    getBookings(params = {}) {
        return api.get('/bookings/bookings/', { params });
    },

    getBookingById(bookingId) {
        return api.get(`/bookings/bookings/${bookingId}/`);
    },

    getMyBookings() {
        return api.get('/bookings/bookings/my_bookings/');
    },

    createBooking(bookingData) {
        return api.post('/bookings/bookings/', bookingData);
    },

    updateBooking(bookingId, bookingData) {
        return api.patch(`/bookings/bookings/${bookingId}/`, bookingData);
    },

    deleteBooking(bookingId) {
        return api.delete(`/bookings/bookings/${bookingId}/`);
    },

    confirmBooking(bookingId) {
        return api.post(`/bookings/bookings/${bookingId}/confirm/`);
    },

    cancelBooking(bookingId, reason) {
        return api.post(`/bookings/bookings/${bookingId}/cancel/`, { reason });
    },

    // Recurring Bookings
    getRecurringBookings(params = {}) {
        return api.get('/bookings/recurring/', { params });
    },

    getRecurringBookingById(recurringId) {
        return api.get(`/bookings/recurring/${recurringId}/`);
    },

    createRecurringBooking(bookingData) {
        return api.post('/bookings/recurring/', bookingData);
    },

    updateRecurringBooking(recurringId, bookingData) {
        return api.patch(`/bookings/recurring/${recurringId}/`, bookingData);
    },

    deleteRecurringBooking(recurringId) {
        return api.delete(`/bookings/recurring/${recurringId}/`);
    },

    pauseRecurringBooking(recurringId) {
        return api.post(`/bookings/recurring/${recurringId}/pause/`);
    },

    resumeRecurringBooking(recurringId) {
        return api.post(`/bookings/recurring/${recurringId}/resume/`);
    },

    cancelRecurringBooking(recurringId, cancelFuture = true) {
        return api.post(`/bookings/recurring/${recurringId}/cancel/`, { 
            cancel_future: cancelFuture 
        });
    },

    // Booking Shares
    getBookingShares(params = {}) {
        return api.get('/bookings/booking-shares/', { params });
    },

    getBookingShareById(shareId) {
        return api.get(`/bookings/booking-shares/${shareId}/`);
    },

    createBookingShare(shareData) {
        return api.post('/bookings/booking-shares/', shareData);
    },

    updateBookingShare(shareId, shareData) {
        return api.patch(`/bookings/booking-shares/${shareId}/`, shareData);
    },

    deleteBookingShare(shareId) {
        return api.delete(`/bookings/booking-shares/${shareId}/`);
    },

    joinBookingShare(token) {
        return api.post('/bookings/booking-shares/join/', { token });
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

    deleteCancellationPolicy(policyId) {
        return api.delete(`/bookings/cancellation-policies/${policyId}/`);
    },

    // Notifications
    getNotifications(params = {}) {
        return api.get('/bookings/notifications/', { params });
    },

    getNotificationById(notificationId) {
        return api.get(`/bookings/notifications/${notificationId}/`);
    },

    getUnreadNotifications() {
        return api.get('/bookings/notifications/unread/');
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

    getEquipmentRentalById(rentalId) {
        return api.get(`/bookings/equipment-rentals/${rentalId}/`);
    },

    createEquipmentRental(rentalData) {
        return api.post('/bookings/equipment-rentals/', rentalData);
    },

    updateEquipmentRental(rentalId, rentalData) {
        return api.patch(`/bookings/equipment-rentals/${rentalId}/`, rentalData);
    },

    deleteEquipmentRental(rentalId) {
        return api.delete(`/bookings/equipment-rentals/${rentalId}/`);
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

    updateMatchEvent(matchId, matchData) {
        return api.patch(`/bookings/match-events/${matchId}/`, matchData);
    },

    deleteMatchEvent(matchId) {
        return api.delete(`/bookings/match-events/${matchId}/`);
    },

    joinMatch(matchId) {
        return api.post(`/bookings/match-events/${matchId}/join/`);
    },

    leaveMatch(matchId) {
        return api.post(`/bookings/match-events/${matchId}/leave/`);
    },

    cancelMatch(matchId) {
        return api.post(`/bookings/match-events/${matchId}/cancel_match/`);
    },

    // Player Ratings
    getPlayerRatings(params = {}) {
        return api.get('/bookings/player-ratings/', { params });
    },

    getPlayerRatingById(ratingId) {
        return api.get(`/bookings/player-ratings/${ratingId}/`);
    },

    createPlayerRating(ratingData) {
        return api.post('/bookings/player-ratings/', ratingData);
    },

    updatePlayerRating(ratingId, ratingData) {
        return api.patch(`/bookings/player-ratings/${ratingId}/`, ratingData);
    },

    deletePlayerRating(ratingId) {
        return api.delete(`/bookings/player-ratings/${ratingId}/`);
    },
};

// ============================================
// STATISTICS & REPORTS
// ============================================
export const statsApi = {
    async getDashboardStats() {
        try {
            const [users, courts, bookings, registrations] = await Promise.all([
                userApi.getAllUsers({ page_size: 1 }),
                courtApi.getCourts({ page_size: 1 }),
                bookingApi.getBookings({ page_size: 1 }),
                courtApi.getRegistrations({ status: 'PENDING' }),
            ]);

            return {
                totalUsers: users.data.count || 0,
                totalCourts: courts.data.count || 0,
                totalBookings: bookings.data.count || 0,
                pendingRegistrations: registrations.data.count || 0,
            };
        } catch (error) {
            console.error('Error fetching dashboard stats:', error);
            throw error;
        }
    },

    getBookingStats(params = {}) {
        return bookingApi.getBookings(params);
    },

    getRevenueStats(startDate, endDate) {
        return bookingApi.getBookings({
            payment_status: 'COMPLETED',
            date_from: startDate,
            date_to: endDate,
        });
    },

    getCourtPerformance(courtId, startDate, endDate) {
        return bookingApi.getBookings({
            court: courtId,
            date_from: startDate,
            date_to: endDate,
        });
    },
};

// ============================================
// UTILITY FUNCTIONS
// ============================================
export const utilityApi = {
    uploadFile(file, path = 'uploads/') {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('path', path);
        
        return api.post('/upload/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
    },

    exportData(endpoint, format = 'csv', params = {}) {
        return api.get(endpoint, {
            params: { ...params, export: format },
            responseType: 'blob',
        });
    },

    downloadFile(blob, filename) {
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

export default api;