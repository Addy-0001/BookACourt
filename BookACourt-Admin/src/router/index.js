// router/index.js (admin app)
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/LoginView.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: () => import('@/views/auth/ForgotPassword.vue'), // create if needed
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/admin/DashboardView.vue'), // your dashboard
    meta: { requiresAuth: true }
  },
  {
    path: '/my-courts',
    name: 'MyCourts',
    component: () => import('@/views/admin/MyCourts.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/bookings',
    name: 'Bookings',
    component: () => import('@/views/admin/BookingsView.vue'),
    meta: { requiresAuth: true }
  },
  // Add other admin routes as needed
  {
    path: '/:pathMatch(.*)*',
    redirect: '/login'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Global guard
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // If route requires auth and not logged in → redirect to login
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next('/login')
  }

  // If logged in and trying to access login → go to dashboard
  if (to.path === '/login' && authStore.isAuthenticated) {
    return next('/dashboard')
  }

  next()
})

export default router