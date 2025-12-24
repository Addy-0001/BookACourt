// src/stores/admin.js
import { defineStore } from 'pinia';
import {
    userManagementApi,
    courtManagementApi,
    bookingManagementApi,
    statisticsApi,
} from '@/services/adminApi';

export const useAdminStore = defineStore('admin', {
    state: () => ({
        // Dashboard
        dashboardStats: {
            totalUsers: 0,
            totalCourts: 0,
            totalBookings: 0,
            pendingRegistrations: 0,
        },

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

        // Court Registrations
        registrations: [],
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

        // Categories
        categories: [],
        categoriesLoading: false,

        // Statistics
        statisticsLoading: false,

        // Error handling
        error: null,
    }),

    getters: {
        // Users
        activeUsers: (state) => state.users.filter((u) => u.is_active),
        inactiveUsers: (state) => state.users.filter((u) => !u.is_active),
        usersByRole: (state) => (role) => state.users.filter((u) => u.role === role),

        // Courts
        activeCourts: (state) => state.courts.filter((c) => c.is_active),
        verifiedCourts: (state) => state.courts.filter((c) => c.is_verified),

        // Registrations
        pendingRegistrations: (state) =>
            state.registrations.filter((r) => r.status === 'PENDING'),
        approvedRegistrations: (state) =>
            state.registrations.filter((r) => r.status === 'APPROVED'),
        rejectedRegistrations: (state) =>
            state.registrations.filter((r) => r.status === 'REJECTED'),

        // Bookings
        confirmedBookings: (state) =>
            state.bookings.filter((b) => b.status === 'CONFIRMED'),
        pendingBookings: (state) =>
            state.bookings.filter((b) => b.status === 'PENDING'),
        cancelledBookings: (state) =>
            state.bookings.filter((b) => b.status === 'CANCELLED'),
    },

    actions: {
        // ============================================
        // DASHBOARD ACTIONS
        // ============================================
        async fetchDashboardStats() {
            try {
                this.statisticsLoading = true;
                const stats = await statisticsApi.getDashboardStats();
                this.dashboardStats = stats;
                this.error = null;
            } catch (error) {
                this.error = error.response?.data?.message || 'Failed to fetch dashboard stats';
                console.error('Dashboard stats error:', error);
            } finally {
                this.statisticsLoading = false;
            }
        },

        // ============================================
        // USER MANAGEMENT ACTIONS
        // ============================================
        async fetchUsers(params = {}) {
            try {
                this.usersLoading = true;
                const response = await userManagementApi.getAllUsers({
                    page: this.usersPagination.page,
                    page_size: this.usersPagination.pageSize,
                    ...params,
                });

                this.users = response.data.results || response.data;
                this.usersPagination.total = response.data.count || response.data.length;
                this.error = null;
            } catch (error) {
                this.error = error.response?.data?.message || 'Failed to fetch users';
                console.error('Fetch users error:', error);
            } finally {
                this.usersLoading = false;
            }
        },

        async fetchUserById(userId) {
            try {
                const response = await userManagementApi.getUserById(userId);
                this.selectedUser = response.data;
                return response.data;
            } catch (error) {
                this.error = error.response?.data?.message || 'Failed to fetch user';
                throw error;
            }
        },

        async updateUser(userId, userData) {
            try {
                const response = await userManagementApi.updateUser(userId, userData);

                // Update in local state
                const index = this.users.findIndex((u) => u.id === userId);
                if (index !== -1) {
                    this.users[index] = response.data;
                }

                if (this.selectedUser?.id === userId) {
                    this.selectedUser = response.data;
                }

                return response.data;
            } catch (error) {
                this.error = error.response?.data?.message || 'Failed to update user';
                throw error;
            }
        },

        async toggleUserStatus(userId, isActive) {
            try {
                await userManagementApi.toggleUserStatus(userId, isActive);
                await this.fetchUsers();
            } catch (error) {
                this.error = error.response?.data?.message || 'Failed to update user status';
                throw error;
            }
        },

        async changeUserRole(userId, role) {
            try {
                await userManagementApi.changeUserRole(userId, role);
                await this.fetchUsers();
            } catch (error) {
                this.error = error.response?.data?.message || 'Failed to change user role';
                throw error;
            }
        },

        // ============================================
        // COURT MANAGEMENT ACTIONS
        // ============================================
        async fetchCourts(params = {}) {
            try {
                this.courtsLoading = true;
                const response = await courtManagementApi.getCourts({
                    page: this.courtsPagination.page,
                    page_size: this.courtsPagination.pageSize,
                    ...params,
                });

                this.courts = response.data.results || response.data;
                this.courtsPagination.total = response.data.count || response.data.length;
                this.error = null;
            } catch (error) {
                this.error = error.response?.data?.message || 'Failed to fetch courts';
                console.error('Fetch courts error:', error);
            } finally {
                this.courtsLoading = false;
            }
        },

        async fetchCourtById(courtId) {
            try {
                const response = await courtManagementApi.getCourtById(courtId);
                this.selectedCourt = response.data;
                return response.data;
            } catch (error) {
                this.error = error.response?.data?.message || 'Failed to fetch court';
                throw error;
            }
        },

        async updateCourt(courtId, courtData) {
            try {
                const response = await courtManagementApi.updateCourt(courtId, courtData);

                const index = this.courts.findIndex((c) => c.id === courtId);
                if (index !== -1) {
                    this.courts[index] = response.data;
                }

                return response.data;
            } catch (error) {
                this.error = error.response?.data?.message || 'Failed to update court';
                throw error;
            }
        },

        async toggleCourtStatus(courtId, isActive) {
            try {
                await courtManagementApi.toggleCourtStatus(courtId, isActive);
                await this.fetchCourts();
            } catch (error) {
                this.error = error.response?.data?.message || 'Failed to update court status';
                throw error;
            }
        },

        async verifyCourt(courtId) {
            try {
                await courtManagementApi.verifyCourt(courtId);
                await this.fetchCourts();
            } catch (error) {
                this.error = error.response?.data?.message || 'Failed to verify court';
                throw error;
            }
        },

        // ============================================
        // COURT REGISTRATION ACTIONS
        // ============================================
        async fetchRegistrations(params = {}) {
            try {
                this.registrationsLoading = true;
                const response = await courtManagementApi.getRegistrations({
                    page: this.registrationsPagination.page,
                    page_size: this.registrationsPagination.pageSize,
                    ...params,
                });

                this.registrations = response.data.results || response.data;
                this.registrationsPagination.total = response.data.count || response.data.length;
                this.error = null;
            } catch (error) {
                this.error = error.response?.data?.message || 'Failed to fetch registrations';
                console.error('Fetch registrations error:', error);
            } finally {
                this.registrationsLoading = false;
            }
        },

        async approveRegistration(registrationId) {
            try {
                await courtManagementApi.approveRegistration(registrationId);
                await this.fetchRegistrations();
                await this.fetchDashboardStats();
            } catch (error) {
                this.error = error.response?.data?.message || 'Failed to approve registration';
                throw error;
            }
        },

        async rejectRegistration(registrationId, reason) {
            try {
                await courtManagementApi.rejectRegistration(registrationId, reason);
                await this.fetchRegistrations();
            } catch (error) {
                this.error = error.response?.data?.message || 'Failed to reject registration';
                throw error;
            }
        },

        // ============================================
        // BOOKING MANAGEMENT ACTIONS
        // ============================================
        async fetchBookings(params = {}) {
            try {
                this.bookingsLoading = true;
                const response = await bookingManagementApi.getBookings({
                    page: this.bookingsPagination.page,
                    page_size: this.bookingsPagination.pageSize,
                    ...params,
                });

                this.bookings = response.data.results || response.data;
                this.bookingsPagination.total = response.data.count || response.data.length;
                this.error = null;
            } catch (error) {
                this.error = error.response?.data?.message || 'Failed to fetch bookings';
                console.error('Fetch bookings error:', error);
            } finally {
                this.bookingsLoading = false;
            }
        },

        async confirmBooking(bookingId) {
            try {
                await bookingManagementApi.confirmBooking(bookingId);
                await this.fetchBookings();
            } catch (error) {
                this.error = error.response?.data?.message || 'Failed to confirm booking';
                throw error;
            }
        },

        async cancelBooking(bookingId, reason) {
            try {
                await bookingManagementApi.cancelBooking(bookingId, reason);
                await this.fetchBookings();
            } catch (error) {
                this.error = error.response?.data?.message || 'Failed to cancel booking';
                throw error;
            }
        },

        // ============================================
        // CATEGORY ACTIONS
        // ============================================
        async fetchCategories() {
            try {
                this.categoriesLoading = true;
                const response = await courtManagementApi.getCategories();
                this.categories = response.data.results || response.data;
                this.error = null;
            } catch (error) {
                this.error = error.response?.data?.message || 'Failed to fetch categories';
                console.error('Fetch categories error:', error);
            } finally {
                this.categoriesLoading = false;
            }
        },

        async createCategory(categoryData) {
            try {
                await courtManagementApi.createCategory(categoryData);
                await this.fetchCategories();
            } catch (error) {
                this.error = error.response?.data?.message || 'Failed to create category';
                throw error;
            }
        },

        async updateCategory(categoryId, categoryData) {
            try {
                await courtManagementApi.updateCategory(categoryId, categoryData);
                await this.fetchCategories();
            } catch (error) {
                this.error = error.response?.data?.message || 'Failed to update category';
                throw error;
            }
        },

        async deleteCategory(categoryId) {
            try {
                await courtManagementApi.deleteCategory(categoryId);
                await this.fetchCategories();
            } catch (error) {
                this.error = error.response?.data?.message || 'Failed to delete category';
                throw error;
            }
        },

        // ============================================
        // PAGINATION ACTIONS
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
        // UTILITY ACTIONS
        // ============================================
        clearError() {
            this.error = null;
        },

        resetState() {
            this.users = [];
            this.courts = [];
            this.bookings = [];
            this.registrations = [];
            this.selectedUser = null;
            this.selectedCourt = null;
            this.selectedBooking = null;
            this.error = null;
        },
    },
});