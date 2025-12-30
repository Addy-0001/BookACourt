// src/stores/admin.js - Enhanced version with court owner functionality
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
            todayBookings: 0,
            weekRevenue: 0,
            monthRevenue: 0,
            occupancyRate: 0,
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

        // Courts - Owner's courts
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

        // Bookings - Owner's court bookings
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
        // Current user role checks
        isSuperUser: (state) => state.currentUser?.role === 'SUPER_USER',
        isCourtOwner: (state) => state.currentUser?.role === 'COURT_OWNER',
        isCourtManager: (state) => state.currentUser?.role === 'COURT_MANAGER',
        isCourtOwnerOrManager: (state) =>
            state.currentUser?.role === 'COURT_OWNER' ||
            state.currentUser?.role === 'COURT_MANAGER',

        // Users
        activeUsers: (state) => state.users.filter(u => u.is_active),
        inactiveUsers: (state) => state.users.filter(u => !u.is_active),
        usersByRole: (state) => (role) => state.users.filter(u => u.role === role),
        totalUsersCount: (state) => state.usersPagination.total,

        // Courts - filtered by owner
        activeCourts: (state) => state.courts.filter(c => c.is_active),
        inactiveCourts: (state) => state.courts.filter(c => !c.is_active),
        verifiedCourts: (state) => state.courts.filter(c => c.is_verified),
        unverifiedCourts: (state) => state.courts.filter(c => !c.is_verified),
        totalCourtsCount: (state) => state.courtsPagination.total,

        // Owner's courts IDs for filtering
        ownCourtIds: (state) => state.courts.map(c => c.id),

        // Registrations
        pendingRegistrations: (state) =>
            state.registrations.filter(r => r.status === 'PENDING'),
        approvedRegistrations: (state) =>
            state.registrations.filter(r => r.status === 'APPROVED'),
        rejectedRegistrations: (state) =>
            state.registrations.filter(r => r.status === 'REJECTED'),

        // Bookings - filtered by owner's courts
        confirmedBookings: (state) =>
            state.bookings.filter(b => b.status === 'CONFIRMED'),
        pendingBookings: (state) =>
            state.bookings.filter(b => b.status === 'PENDING'),
        cancelledBookings: (state) =>
            state.bookings.filter(b => b.status === 'CANCELLED'),
        completedBookings: (state) =>
            state.bookings.filter(b => b.status === 'COMPLETED'),
        todayBookings: (state) => {
            const today = new Date().toISOString().split('T')[0];
            return state.bookings.filter(b => b.booking_date === today);
        },

        // Revenue calculations
        totalRevenue: (state) => {
            return state.bookings
                .filter(b => b.payment_status === 'COMPLETED')
                .reduce((sum, b) => sum + parseFloat(b.total_amount || 0), 0);
        },
        weekRevenue: (state) => {
            const weekAgo = new Date();
            weekAgo.setDate(weekAgo.getDate() - 7);
            return state.bookings
                .filter(b =>
                    b.payment_status === 'COMPLETED' &&
                    new Date(b.booking_date) >= weekAgo
                )
                .reduce((sum, b) => sum + parseFloat(b.total_amount || 0), 0);
        },
        monthRevenue: (state) => {
            const monthAgo = new Date();
            monthAgo.setMonth(monthAgo.getMonth() - 1);
            return state.bookings
                .filter(b =>
                    b.payment_status === 'COMPLETED' &&
                    new Date(b.booking_date) >= monthAgo
                )
                .reduce((sum, b) => sum + parseFloat(b.total_amount || 0), 0);
        },

        // Categories
        activeCategories: (state) => state.categories.filter(c => c.is_active),

        // Notifications
        unreadNotifications: (state) =>
            state.notifications.filter(n => !n.is_read),
    },

    actions: {
        // ============================================
        // INITIALIZATION
        // ============================================
        async initialize() {
            try {
                await this.fetchCurrentUser();
                if (this.currentUser) {
                    await this.fetchDashboardStats();
                }
            } catch (error) {
                console.error('Initialization error:', error);
            }
        },

        // ============================================
        // DASHBOARD - Owner specific
        // ============================================
        async fetchDashboardStats() {
            this.dashboardLoading = true;
            this.error = null;

            try {
                // Fetch current user's courts first
                await this.fetchMyCourts();

                // Fetch bookings for owner's courts
                await this.fetchMyBookings();

                // Calculate stats
                this.dashboardStats = {
                    totalCourts: this.courts.length,
                    totalBookings: this.bookings.length,
                    todayBookings: this.todayBookings.length,
                    weekRevenue: this.weekRevenue,
                    monthRevenue: this.monthRevenue,
                    occupancyRate: this.calculateOccupancyRate(),
                };

                // Super user specific stats
                if (this.isSuperUser) {
                    const [usersRes, allCourtsRes, registrationsRes] = await Promise.all([
                        userApi.getAllUsers({ page_size: 1 }),
                        courtApi.getCourts({ page_size: 1 }),
                        courtApi.getRegistrations({ status: 'PENDING' }),
                    ]);

                    this.dashboardStats.totalUsers = usersRes.data.count || 0;
                    this.dashboardStats.totalCourts = allCourtsRes.data.count || 0;
                    this.dashboardStats.pendingRegistrations = registrationsRes.data.count || 0;
                }
            } catch (error) {
                this.handleError(error, 'Failed to fetch dashboard stats');
            } finally {
                this.dashboardLoading = false;
            }
        },

        calculateOccupancyRate() {
            if (this.courts.length === 0) return 0;

            // Simple calculation: (total bookings / (courts * 30 days * 10 hours)) * 100
            // This is a rough estimate - adjust based on your needs
            const totalPossibleSlots = this.courts.length * 30 * 10;
            const occupiedSlots = this.bookings.filter(b =>
                b.status === 'CONFIRMED' || b.status === 'COMPLETED'
            ).length;

            return Math.round((occupiedSlots / totalPossibleSlots) * 100);
        },

        // ============================================
        // CURRENT USER
        // ============================================
        async fetchCurrentUser() {
            try {
                const response = await userApi.getProfile();
                this.currentUser = response.data;

                // Store in localStorage for persistence
                localStorage.setItem('user', JSON.stringify(response.data));

                return response.data;
            } catch (error) {
                this.handleError(error, 'Failed to fetch user profile');

                // Try to get from localStorage as fallback
                const storedUser = localStorage.getItem('user');
                if (storedUser) {
                    this.currentUser = JSON.parse(storedUser);
                }
            }
        },

        async updateCurrentUser(userData) {
            try {
                const response = await userApi.updateProfile(userData);
                this.currentUser = response.data;
                localStorage.setItem('user', JSON.stringify(response.data));
                this.successMessage = 'Profile updated successfully';
                return response.data;
            } catch (error) {
                this.handleError(error, 'Failed to update profile');
                throw error;
            }
        },

        // ============================================
        // COURT MANAGEMENT - Owner specific
        // ============================================
        async fetchMyCourts(params = {}) {
            this.courtsLoading = true;
            this.error = null;

            try {
                // Filter by current user as owner or manager
                const filterParams = {
                    page: this.courtsPagination.page,
                    page_size: this.courtsPagination.pageSize,
                    ...params,
                };

                if (this.isCourtOwner) {
                    filterParams.owner = this.currentUser.id;
                } else if (this.isCourtManager) {
                    // Assuming there's a managers field - adjust based on your API
                    filterParams.managers = this.currentUser.id;
                }

                const response = await courtApi.getCourts(filterParams);

                this.courts = response.data.results || response.data;
                this.courtsPagination.total = response.data.count || this.courts.length;

                return this.courts;
            } catch (error) {
                this.handleError(error, 'Failed to fetch your courts');
            } finally {
                this.courtsLoading = false;
            }
        },

        async fetchCourtById(courtId) {
            try {
                const response = await courtApi.getCourtById(courtId);

                // Verify ownership
                if (this.isCourtOwner && response.data.owner !== this.currentUser.id) {
                    throw new Error('You do not own this court');
                }

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
                await this.fetchDashboardStats(); // Refresh stats
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
                await this.fetchDashboardStats();
            } catch (error) {
                this.handleError(error, 'Failed to delete court');
                throw error;
            }
        },

        async toggleCourtStatus(courtId, isActive) {
            try {
                await courtApi.updateCourt(courtId, { is_active: isActive });
                await this.fetchMyCourts();
                this.successMessage = `Court ${isActive ? 'activated' : 'deactivated'} successfully`;
            } catch (error) {
                this.handleError(error, 'Failed to update court status');
                throw error;
            }
        },

        // ============================================
        // BOOKINGS - Owner's courts only
        // ============================================
        async fetchMyBookings(params = {}) {
            this.bookingsLoading = true;
            this.error = null;

            try {
                // Ensure we have court IDs
                if (this.courts.length === 0) {
                    await this.fetchMyCourts();
                }

                // Filter by owner's courts
                const filterParams = {
                    page: this.bookingsPagination.page,
                    page_size: this.bookingsPagination.pageSize,
                    ordering: '-created_at',
                    ...params,
                };

                // Add court filter for owner's courts
                if (this.ownCourtIds.length > 0) {
                    filterParams.court__in = this.ownCourtIds.join(',');
                }

                const response = await bookingApi.getBookings(filterParams);

                this.bookings = response.data.results || response.data;
                this.bookingsPagination.total = response.data.count || this.bookings.length;

                return this.bookings;
            } catch (error) {
                this.handleError(error, 'Failed to fetch bookings');
            } finally {
                this.bookingsLoading = false;
            }
        },

        async fetchBookings(params = {}) {
            // Alias for fetchMyBookings to maintain compatibility
            return this.fetchMyBookings(params);
        },

        async fetchBookingById(bookingId) {
            try {
                const response = await bookingApi.getBookingById(bookingId);

                // Verify the booking is for one of owner's courts
                if (!this.ownCourtIds.includes(response.data.court)) {
                    throw new Error('This booking does not belong to your courts');
                }

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
                await this.fetchMyBookings();
                this.successMessage = 'Booking confirmed successfully';
            } catch (error) {
                this.handleError(error, 'Failed to confirm booking');
                throw error;
            }
        },

        async cancelBooking(bookingId, reason) {
            try {
                await bookingApi.cancelBooking(bookingId, reason);
                await this.fetchMyBookings();
                this.successMessage = 'Booking cancelled successfully';
            } catch (error) {
                this.handleError(error, 'Failed to cancel booking');
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
        // COURT REGISTRATIONS (Super User only)
        // ============================================
        async fetchRegistrations(params = {}) {
            if (!this.isSuperUser) return;

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
        // COURT REVIEWS - Owner's courts
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
        // PAGINATION
        // ============================================
        setUsersPage(page) {
            this.usersPagination.page = page;
            this.fetchUsers();
        },

        setCourtsPage(page) {
            this.courtsPagination.page = page;
            this.fetchMyCourts();
        },

        setBookingsPage(page) {
            this.bookingsPagination.page = page;
            this.fetchMyBookings();
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
            this.currentUser = null;
        },
    },
});