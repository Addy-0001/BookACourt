import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/auth/LoginView.vue'),
      meta: { guest: true }
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/auth/SignupView.vue'),
      meta: { guest: true }
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/profile/ProfileView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/courts',
      name: 'courts',
      component: () => import('../views/court/CourtsView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/courts/:id',
      name: 'court-detail',
      component: () => import('../views/court/CourtDetailView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/bookings',
      name: 'bookings',
      component: () => import('../views/profile/BookingsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/bookings/:id',
      name: 'booking-detail',
      component: () => import('../views/booking/BookingDetailView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/bookings/join/:token',
      name: 'booking-join',
      component: () => import('../views/booking/BookingJoinView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/matches',
      name: 'matches',
      component: () => import('../views/profile/MatchesView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/matches/:id',
      name: 'match-detail',
      component: () => import('../views/booking/MatchDetailView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/friends',
      name: 'friends',
      component: () => import('../views/profile/FriendsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/notifications',
      name: 'notifications',
      component: () => import('../views/profile/NotificationsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/leaderboard',
      name: 'leaderboard',
      component: () => import('../views/profile/LeaderboardView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/preferences',
      name: 'preferences',
      component: () => import('../views/profile/PreferencesView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/court-registration',
      name: 'court-registration',
      component: () => import('../views/court/CourtRegistrationView.vue'),
      meta: { requiresAuth: true, requiresRole: ['COURT_OWNER'] }
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/general/AboutView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue')
    }
  ],
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Check auth status on first load
  if (authStore.isAuthenticated && !authStore.user) {
    await authStore.checkAuth()
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.guest && authStore.isAuthenticated) {
    next('/')
  } else if (to.meta.requiresRole) {
    const hasRole = to.meta.requiresRole.includes(authStore.user?.role)
    if (!hasRole) {
      next('/')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router