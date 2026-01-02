import { defineStore } from 'pinia';
import axios from 'axios';
import { useRouter } from 'vue-router';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: JSON.parse(localStorage.getItem('user') || 'null'),
        token: localStorage.getItem('access_token'),
        refreshToken: localStorage.getItem('refresh_token'),
        isAuthenticated: !!localStorage.getItem('access_token'),
    }),

    getters: {
        isAdmin: (state) => {
            return state.user && ['SUPER_USER', 'COURT_OWNER', 'COURT_MANAGER'].includes(state.user.role);
        },
        isSuperUser: (state) => {
            return state.user?.role === 'SUPER_USER';
        },
    },

    actions: {
        async login(credentials) {
            const response = await axios.post('http://localhost:8000/api/auth/login/', credentials);

            this.token = response.data.access;
            this.refreshToken = response.data.refresh;
            this.user = response.data.user;
            this.isAuthenticated = true;

            localStorage.setItem('access_token', response.data.access);
            localStorage.setItem('refresh_token', response.data.refresh);
            localStorage.setItem('user', JSON.stringify(response.data.user));

            return response.data;
        },

        async logout() {
            try {
                // Optional: Call server logout to blacklist token
                await authApi.logout(this.refreshToken);
            } catch (err) {
                console.warn('Server logout failed, clearing local data anyway');
            }

            // Clear everything
            this.user = null;
            this.token = null;
            this.refreshToken = null;
            this.isAuthenticated = false;

            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user');

            // Safe redirect
            const router = useRouter();
            router.replace('/admin/login');
        },

        async refreshAccessToken() {
            try {
                const response = await axios.post('http://localhost:8000/api/auth/token/refresh/', {
                    refresh: this.refreshToken,
                });

                this.token = response.data.access;
                localStorage.setItem('access_token', response.data.access);
            } catch (error) {
                this.logout();
                throw error;
            }
        },
    },
});