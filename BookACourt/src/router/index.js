import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { guest: true }
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/SignupView.vue'),
      meta: { guest: true }
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/courts',
      name: 'courts',
      component: () => import('../views/CourtsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/courts/:id',
      name: 'court-detail',
      component: () => import('../views/CourtDetailView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/bookings',
      name: 'bookings',
      component: () => import('../views/BookingsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/bookings/:id',
      name: 'booking-detail',
      component: () => import('../views/BookingDetailView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/matches',
      name: 'matches',
      component: () => import('../views/MatchesView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
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
  } else {
    next()
  }
})

export default router