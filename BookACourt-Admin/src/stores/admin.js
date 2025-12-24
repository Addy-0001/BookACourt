// src/stores/admin.js
import { defineStore } from 'pinia';
import {
    authApi,
    userApi,
    courtApi,
    bookingApi,
    statsApi
} from '@/services/api';

export const useAdminStore = defineStore('admin', {
    state: () => ({
        // Dashboard
        dashboardStats: {
            totalUsers: 0,
            totalCourts: 0,
            totalBookings: 0,
            pendingRegistrations: 0,
        },
        dashboardLoading: false,

        // Current User
        currentUser: null,

        // Users
        users: [],
        selectedUser: null,
        usersLoading: false,
        usersPagination: {
            page: 1,
            pageSize: 20,
            total: 0,
        },

        // Courts
        courts: [],
        selectedCourt: null,
        courtsLoading: false,
        courtsPagination: {
            page: 1,
            pageSize: 20,
            total: 0,
        },

        // Categories
        categories: [],
        categoriesLoading: false,

        // Court Registrations
        registrations: [],
        selectedRegistration: null,
        registrationsLoading: false,
        registrationsPagination: {
            page: 1,
            pageSize: 20,
            total: 0,
        },

        // Bookings
        bookings: [],
        selectedBooking: null,
        bookingsLoading: false,
        bookingsPagination: {
            page: 1,
            pageSize: 20,
            total: 0,
        },

        // Notifications
        notifications: [],
        unreadNotificationsCount: 0,
        notificationsLoading: false,

        // Reviews
        reviews: [],
        reviewsLoading: false,

        // Equipment
        equipment: [],
        equipmentLoading: false,

        // Match Events
        matchEvents: [],
        matchEventsLoading: false,

        // Player Stats
        playerStats: [],
        leaderboard: [],
        playerStatsLoading: false,

        // Error handling
        error: null,
        successMessage: null,
    }),

    getters: {
        // Users
        activeUsers: (state) => state.users.filter(u => u.is_active),
        inactiveUsers: (state) => state.users.filter(u => !u.is_active),
        usersByRole: (state) => (role) => state.users.filter(u => u.role === role),
        totalUsersCount: (state) => state.usersPagination.total,

        // Courts
        activeCourts: (state) => state.courts.filter(c => c.is_active),
        verifiedCourts: (state) => state.courts.filter(c => c.is_verified),
        unverifiedCourts: (state) => state.courts.filter(c => !c.is_verified),
        totalCourtsCount: (state) => state.courtsPagination.total,

        // Registrations
        pendingRegistrations: (state) =>
            state.registrations.filter(r => r.status === 'PENDING'),
        approvedRegistrations: (state) =>
            state.registrations.filter(r => r.status === 'APPROVED'),
        rejectedRegistrations: (state) =>
            state.registrations.filter(r => r.status === 'REJECTED'),

        // Bookings
        confirmedBookings: (state) =>
            state.bookings.filter(b => b.status === 'CONFIRMED'),
        pendingBookings: (state) =>
            state.bookings.filter(b => b.status === 'PENDING'),
        cancelledBookings: (state) =>
            state.bookings.filter(b => b.status === 'CANCELLED'),
        completedBookings: (state) =>
            state.bookings.filter(b => b.status === 'COMPLETED'),

        // Categories
        activeCategories: (state) => state.categories.filter(c => c.is_active),

        // Notifications
        unreadNotifications: (state) =>
            state.notifications.filter(n => !n.is_read),
    },

    actions: {
        // ============================================
        // DASHBOARD
        // ============================================
        async fetchDashboardStats() {
            this.dashboardLoading = true;
            this.error = null;

            try {
                const stats = await statsApi.getDashboardStats();
                this.dashboardStats = stats;
            } catch (error) {
                this.handleError(error, 'Failed to fetch dashboard stats');
            } finally {
                this.dashboardLoading = false;
            }
        },

        // ============================================
        // CURRENT USER
        // ============================================
        async fetchCurrentUser() {
            try {
                const response = await userApi.getProfile();
                this.currentUser = response.data;
                return response.data;
            } catch (error) {
                this.handleError(error, 'Failed to fetch user profile');
            }
        },

        async updateCurrentUser(userData) {
            try {
                const response = await userApi.updateProfile(userData);
                this.currentUser = response.data;
                this.successMessage = 'Profile updated successfully';
                return response.data;
            } catch (error) {
                this.handleError(error, 'Failed to update profile');
                throw error;
            }
        },

        // ============================================
        // USER MANAGEMENT
        // ============================================
        async fetchUsers(params = {}) {
            this.usersLoading = true;
            this.error = null;

            try {
                const response = await userApi.getAllUsers({
                    page: this.usersPagination.page,
                    page_size: this.usersPagination.pageSize,
                    ...params,
                });

                this.users = response.data.results || response.data;
                this.usersPagination.total = response.data.count || this.users.length;
            } catch (error) {
                this.handleError(error, 'Failed to fetch users');
            } finally {
                this.usersLoading = false;
            }
        },

        async fetchUserById(userId) {
            try {
                const response = await userApi.getUserById(userId);
                this.selectedUser = response.data;
                return response.data;
            } catch (error) {
                this.handleError(error, 'Failed to fetch user');
                throw error;
            }
        },

        async updateUser(userId, userData) {
            try {
                const response = await userApi.updateUser(userId, userData);

                const index = this.users.findIndex(u => u.id === userId);
                if (index !== -1) {
                    this.users[index] = response.data;
                }

                if (this.selectedUser?.id === userId) {
                    this.selectedUser = response.data;
                }

                this.successMessage = 'User updated successfully';
                return response.data;
            } catch (error) {
                this.handleError(error, 'Failed to update user');
                throw error;
            }
        },

        async deleteUser(userId) {
            try {
                await userApi.deleteUser(userId);
                this.users = this.users.filter(u => u.id !== userId);
                this.successMessage = 'User deleted successfully';
            } catch (error) {
                this.handleError(error, 'Failed to delete user');
                throw error;
            }
        },

        // ============================================
        // COURT MANAGEMENT
        // ============================================
        async fetchCourts(params = {}) {
            this.courtsLoading = true;
            this.error = null;

            try {
                const response = await courtApi.getCourts({
                    page: this.courtsPagination.page,
                    page_size: this.courtsPagination.pageSize,
                    ...params,
                });

                this.courts = response.data.results || response.data;
                this.courtsPagination.total = response.data.count || this.courts.length;
            } catch (error) {
                this.handleError(error, 'Failed to fetch courts');
            } finally {
                this.courtsLoading = false;
            }
        },

        async fetchCourtById(courtId) {
            try {
                const response = await courtApi.getCourtById(courtId);
                this.selectedCourt = response.data;
                return response.data;
            } catch (error) {
                this.handleError(error, 'Failed to fetch court details');
                throw error;
            }
        },

        async createCourt(courtData) {
            try {
                const response = await courtApi.createCourt(courtData);
                this.courts.unshift(response.data);
                this.successMessage = 'Court created successfully';
                return response.data;
            } catch (error) {
                this.handleError(error, 'Failed to create court');
                throw error;
            }
        },

        async updateCourt(courtId, courtData) {
            try {
                const response = await courtApi.updateCourt(courtId, courtData);

                const index = this.courts.findIndex(c => c.id === courtId);
                if (index !== -1) {
                    this.courts[index] = response.data;
                }

                this.successMessage = 'Court updated successfully';
                return response.data;
            } catch (error) {
                this.handleError(error, 'Failed to update court');
                throw error;
            }
        },

        async deleteCourt(courtId) {
            try {
                await courtApi.deleteCourt(courtId);
                this.courts = this.courts.filter(c => c.id !== courtId);
                this.successMessage = 'Court deleted successfully';
            } catch (error) {
                this.handleError(error, 'Failed to delete court');
                throw error;
            }
        },

        async verifyCourt(courtId) {
            try {
                await courtApi.updateCourt(courtId, { is_verified: true });
                await this.fetchCourts();
                this.successMessage = 'Court verified successfully';
            } catch (error) {
                this.handleError(error, 'Failed to verify court');
                throw error;
            }
        },

        // ============================================
        // CATEGORIES
        // ============================================
        async fetchCategories(params = {}) {
            this.categoriesLoading = true;
            this.error = null;

            try {
                const response = await courtApi.getCategories(params);
                this.categories = response.data.results || response.data;
            } catch (error) {
                this.handleError(error, 'Failed to fetch categories');
            } finally {
                this.categoriesLoading = false;
            }
        },

        async createCategory(categoryData) {
            try {
                const response = await courtApi.createCategory(categoryData);
                this.categories.unshift(response.data);
                this.successMessage = 'Category created successfully';
                return response.data;
            } catch (error) {
                this.handleError(error, 'Failed to create category');
                throw error;
            }
        },

        async updateCategory(categoryId, categoryData) {
            try {
                const response = await courtApi.updateCategory(categoryId, categoryData);

                const index = this.categories.findIndex(c => c.id === categoryId);
                if (index !== -1) {
                    this.categories[index] = response.data;
                }

                this.successMessage = 'Category updated successfully';
                return response.data;
            } catch (error) {
                this.handleError(error, 'Failed to update category');
                throw error;
            }
        },

        async deleteCategory(categoryId) {
            try {
                await courtApi.deleteCategory(categoryId);
                this.categories = this.categories.filter(c => c.id !== categoryId);
                this.successMessage = 'Category deleted successfully';
            } catch (error) {
                this.handleError(error, 'Failed to delete category');
                throw error;
            }
        },

        // ============================================
        // COURT REGISTRATIONS
        // ============================================
        async fetchRegistrations(params = {}) {
            this.registrationsLoading = true;
            this.error = null;

            try {
                const response = await courtApi.getRegistrations({
                    page: this.registrationsPagination.page,
                    page_size: this.registrationsPagination.pageSize,
                    ...params,
                });

                this.registrations = response.data.results || response.data;
                this.registrationsPagination.total = response.data.count || this.registrations.length;
            } catch (error) {
                this.handleError(error, 'Failed to fetch registrations');
            } finally {
                this.registrationsLoading = false;
            }
        },

        async approveRegistration(registrationId) {
            try {
                await courtApi.approveRegistration(registrationId);
                await this.fetchRegistrations();
                await this.fetchDashboardStats();
                this.successMessage = 'Registration approved successfully';
            } catch (error) {
                this.handleError(error, 'Failed to approve registration');
                throw error;
            }
        },

        async rejectRegistration(registrationId, reason) {
            try {
                await courtApi.rejectRegistration(registrationId, reason);
                await this.fetchRegistrations();
                this.successMessage = 'Registration rejected';
            } catch (error) {
                this.handleError(error, 'Failed to reject registration');
                throw error;
            }
        },

        // ============================================
        // BOOKINGS
        // ============================================
        async fetchBookings(params = {}) {
            this.bookingsLoading = true;
            this.error = null;

            try {
                const response = await bookingApi.getBookings({
                    page: this.bookingsPagination.page,
                    page_size: this.bookingsPagination.pageSize,
                    ...params,
                });

                this.bookings = response.data.results || response.data;
                this.bookingsPagination.total = response.data.count || this.bookings.length;
            } catch (error) {
                this.handleError(error, 'Failed to fetch bookings');
            } finally {
                this.bookingsLoading = false;
            }
        },

        async fetchBookingById(bookingId) {
            try {
                const response = await bookingApi.getBookingById(bookingId);
                this.selectedBooking = response.data;
                return response.data;
            } catch (error) {
                this.handleError(error, 'Failed to fetch booking');
                throw error;
            }
        },

        async confirmBooking(bookingId) {
            try {
                await bookingApi.confirmBooking(bookingId);
                await this.fetchBookings();
                this.successMessage = 'Booking confirmed successfully';
            } catch (error) {
                this.handleError(error, 'Failed to confirm booking');
                throw error;
            }
        },

        async cancelBooking(bookingId, reason) {
            try {
                await bookingApi.cancelBooking(bookingId, reason);
                await this.fetchBookings();
                this.successMessage = 'Booking cancelled successfully';
            } catch (error) {
                this.handleError(error, 'Failed to cancel booking');
                throw error;
            }
        },

        // ============================================
        // NOTIFICATIONS
        // ============================================
        async fetchNotifications() {
            this.notificationsLoading = true;

            try {
                const response = await bookingApi.getNotifications({
                    ordering: '-sent_at',
                    page_size: 50,
                });

                this.notifications = response.data.results || response.data;
                this.unreadNotificationsCount = this.notifications.filter(n => !n.is_read).length;
            } catch (error) {
                this.handleError(error, 'Failed to fetch notifications');
            } finally {
                this.notificationsLoading = false;
            }
        },

        async markNotificationRead(notificationId) {
            try {
                await bookingApi.markNotificationRead(notificationId);

                const notification = this.notifications.find(n => n.id === notificationId);
                if (notification) {
                    notification.is_read = true;
                    this.unreadNotificationsCount--;
                }
            } catch (error) {
                console.error('Failed to mark notification as read:', error);
            }
        },

        async markAllNotificationsRead() {
            try {
                await bookingApi.markAllNotificationsRead();
                this.notifications.forEach(n => n.is_read = true);
                this.unreadNotificationsCount = 0;
            } catch (error) {
                this.handleError(error, 'Failed to mark all notifications as read');
            }
        },

        // ============================================
        // COURT REVIEWS
        // ============================================
        async fetchCourtReviews(courtId) {
            this.reviewsLoading = true;

            try {
                const response = await courtApi.getCourtReviews(courtId);
                this.reviews = response.data.results || response.data;
            } catch (error) {
                this.handleError(error, 'Failed to fetch reviews');
            } finally {
                this.reviewsLoading = false;
            }
        },

        async respondToReview(courtId, reviewId, responseText) {
            try {
                await courtApi.respondToReview(courtId, reviewId, responseText);
                await this.fetchCourtReviews(courtId);
                this.successMessage = 'Response posted successfully';
            } catch (error) {
                this.handleError(error, 'Failed to respond to review');
                throw error;
            }
        },

        // ============================================
        // PLAYER STATS
        // ============================================
        async fetchPlayerStats(params = {}) {
            this.playerStatsLoading = true;

            try {
                const response = await userApi.getPlayerStats(params);
                this.playerStats = response.data.results || response.data;
            } catch (error) {
                this.handleError(error, 'Failed to fetch player stats');
            } finally {
                this.playerStatsLoading = false;
            }
        },

        async fetchLeaderboard() {
            try {
                const response = await userApi.getLeaderboard();
                this.leaderboard = response.data;
            } catch (error) {
                this.handleError(error, 'Failed to fetch leaderboard');
            }
        },

        // ============================================
        // PAGINATION
        // ============================================
        setUsersPage(page) {
            this.usersPagination.page = page;
            this.fetchUsers();
        },

        setCourtsPage(page) {
            this.courtsPagination.page = page;
            this.fetchCourts();
        },

        setBookingsPage(page) {
            this.bookingsPagination.page = page;
            this.fetchBookings();
        },

        setRegistrationsPage(page) {
            this.registrationsPagination.page = page;
            this.fetchRegistrations();
        },

        // ============================================
        // UTILITIES
        // ============================================
        handleError(error, defaultMessage = 'An error occurred') {
            console.error('Store error:', error);

            if (error.response?.data) {
                const errorData = error.response.data;

                if (typeof errorData === 'string') {
                    this.error = errorData;
                } else if (errorData.detail) {
                    this.error = errorData.detail;
                } else if (errorData.message) {
                    this.error = errorData.message;
                } else {
                    const errors = [];
                    for (const [field, messages] of Object.entries(errorData)) {
                        if (Array.isArray(messages)) {
                            errors.push(...messages);
                        } else {
                            errors.push(messages);
                        }
                    }
                    this.error = errors.join('. ') || defaultMessage;
                }
            } else {
                this.error = defaultMessage;
            }
        },

        clearError() {
            this.error = null;
        },

        clearSuccess() {
            this.successMessage = null;
        },

        clearMessages() {
            this.error = null;
            this.successMessage = null;
        },

        resetState() {
            this.users = [];
            this.courts = [];
            this.bookings = [];
            this.registrations = [];
            this.categories = [];
            this.notifications = [];
            this.reviews = [];
            this.selectedUser = null;
            this.selectedCourt = null;
            this.selectedBooking = null;
            this.selectedRegistration = null;
            this.error = null;
            this.successMessage = null;
        },
    },
});