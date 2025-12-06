import { defineStore } from 'pinia';
import { authService } from '@/services/authService';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: authService.getCurrentUser(),
        isAuthenticated: authService.isAuthenticated(),
        loading: false,
        error: null,
    }),

    getters: {
        isPlayer: (state) => state.user?.role === 'PLAYER',
        isCourtOwner: (state) => state.user?.role === 'COURT_OWNER',
        isCourtManager: (state) => state.user?.role === 'COURT_MANAGER',
        isSuperUser: (state) => state.user?.role === 'SUPER_USER',
    },

    actions: {
        async login(credentials) {
            this.loading = true;
            this.error = null;
            try {
                const data = await authService.login(credentials);
                this.user = data.user;
                this.isAuthenticated = true;
                return data;
            } catch (error) {
                this.error = error.response?.data?.detail || 'Login failed';
                throw error;
            } finally {
                this.loading = false;
            }
        },

        async register(userData) {
            this.loading = true;
            this.error = null;
            try {
                const data = await authService.register(userData);
                return data;
            } catch (error) {
                this.error = error.response?.data || 'Registration failed';
                throw error;
            } finally {
                this.loading = false;
            }
        },

        async logout() {
            this.loading = true;
            try {
                await authService.logout();
                this.user = null;
                this.isAuthenticated = false;
            } catch (error) {
                console.error('Logout error:', error);
            } finally {
                this.loading = false;
            }
        },

        async checkAuth() {
            if (!this.isAuthenticated) return;

            try {
                const data = await authService.checkAuthStatus();
                this.user = data.user;
            } catch (error) {
                this.user = null;
                this.isAuthenticated = false;
            }
        },
    },
});