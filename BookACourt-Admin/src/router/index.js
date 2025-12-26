import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Auth Routes
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Auth/LoginView.vue'),
      meta: { requiresGuest: true },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/Auth/RegisterView.vue'),
      meta: { requiresGuest: true },
    },

    // Admin Routes
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      meta: { requiresAuth: true },
    },
    // {
    //   path: '/admin/users',
    //   name: 'users',
    //   component: () => import('../views/Users/UsersView.vue'),
    //   meta: { requiresAuth: true, requiresSuperUser: true },
    // },
    // {
    //   path: '/admin/courts',
    //   name: 'courts',
    //   component: () => import('../views/Courts/CourtsView.vue'),
    //   meta: { requiresAuth: true },
    // },
    // {
    //   path: '/admin/courts/:id',
    //   name: 'court-detail',
    //   component: () => import('../views/Courts/CourtDetailView.vue'),
    //   meta: { requiresAuth: true },
    // },
    {
      path: '/admin/bookings',
      name: 'bookings',
      component: () => import('../views/admin/BookingsView.vue'),
      meta: { requiresAuth: true },
    },
    // {
    //   path: '/admin/registrations',
    //   name: 'registrations',
    //   component: () => import('../views/Registrations/RegistrationsView.vue'),
    //   meta: { requiresAuth: true, requiresSuperUser: true },
    // },
    // {
    //   path: '/admin/categories',
    //   name: 'categories',
    //   component: () => import('../views/Categories/CategoriesView.vue'),
    //   meta: { requiresAuth: true },
    // },
  ],
});

// Navigation Guards
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token');
  const user = JSON.parse(localStorage.getItem('user') || 'null');
  const isAuthenticated = !!token;

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  } else if (to.meta.requiresGuest && isAuthenticated) {
    next('/');
  } else if (to.meta.requiresSuperUser && user?.role !== 'SUPER_USER') {
    next('/');
  } else {
    next();
  }
});

export default router;