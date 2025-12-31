// src/router/index.js
import BookingsView from '@/views/admin/BookingsView.vue';
import MyCourts from '@/views/admin/MyCourts.vue';
import LoginView from '@/views/auth/LoginView.vue';
import RegisterView from '@/views/auth/RegisterView.vue';
import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // ============================================
    // AUTH ROUTES
    // ============================================
    {
      path: '/login',
      name: 'login',
      component: () => LoginView,
      meta: { requiresGuest: true },
    },
    {
      path: '/register',
      name: 'register',
      component: () => RegisterView,
      meta: { requiresGuest: true },
    },

    // ============================================
    // DASHBOARD
    // ============================================
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      meta: { requiresAuth: true },
    },

    // ============================================
    // COURT MANAGEMENT
    // ============================================
    {
      path: '/admin/my-courts',
      name: 'my-courts',
      component: () => MyCourts,
      meta: {
        requiresAuth: true,
        requiresCourtOwnerOrManager: true
      },
    },

    // ============================================
    // BOOKING MANAGEMENT
    // ============================================
    {
      path: '/admin/bookings',
      name: 'bookings',
      component: () => BookingsView,
      meta: { requiresAuth: true },
    },
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  },
});

// ============================================
// NAVIGATION GUARDS
// ============================================
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token');
  const userStr = localStorage.getItem('user');
  const user = userStr ? JSON.parse(userStr) : null;
  const isAuthenticated = !!token;

  // Guest pages (login/register)
  if (to.meta.requiresGuest && isAuthenticated) {
    return next('/');
  }

  // Protected pages
  if (to.meta.requiresAuth && !isAuthenticated) {
    return next('/login');
  }

  // Super User only pages
  if (to.meta.requiresSuperUser && user?.role !== 'SUPER_USER') {
    console.warn('Access denied: Super User role required');
    return next('/');
  }

  // Court Owner/Manager only pages
  if (to.meta.requiresCourtOwnerOrManager) {
    const allowedRoles = ['COURT_OWNER', 'COURT_MANAGER', 'SUPER_USER'];
    if (!allowedRoles.includes(user?.role)) {
      console.warn('Access denied: Court Owner or Manager role required');
      return next('/');
    }
  }

  next();
});

// ============================================
// ERROR HANDLING
// ============================================
router.onError((error) => {
  console.error('Router error:', error);

  // Handle chunk load errors (lazy loading failures)
  if (error.message.includes('Failed to fetch dynamically imported module')) {
    window.location.reload();
  }
});

export default router;