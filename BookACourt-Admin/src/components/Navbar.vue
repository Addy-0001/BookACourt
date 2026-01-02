<template>
    <nav class="bg-white shadow-sm sticky top-0 z-50 border-b border-emerald-100">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <!-- Logo & Brand -->
                <div class="flex items-center gap-4">
                    <router-link to="/dashboard" class="flex items-center gap-3">
                        <div
                            class="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-600 to-teal-600 flex items-center justify-center text-white text-2xl shadow-md">
                            🏟️
                        </div>
                        <div class="hidden sm:block">
                            <span
                                class="text-xl font-bold bg-gradient-to-r from-emerald-700 to-teal-700 bg-clip-text text-transparent">
                                Court Manager
                            </span>
                            <p class="text-xs text-emerald-700 font-medium">Venue Dashboard</p>
                        </div>
                    </router-link>
                </div>

                <!-- Desktop Navigation -->
                <div class="hidden lg:flex items-center gap-2">
                    <!-- Dashboard (always visible) -->
                    <router-link to="/dashboard"
                        class="px-5 py-2.5 rounded-xl font-medium transition-all hover:bg-emerald-50 hover:text-emerald-700"
                        :class="{ 'bg-emerald-50 text-emerald-700 font-semibold': $route.path === '/dashboard' }">
                        Dashboard
                    </router-link>

                    <!-- My Courts -->
                    <router-link v-if="isCourtOwnerOrManager" to="/my-courts"
                        class="px-5 py-2.5 rounded-xl font-medium transition-all hover:bg-emerald-50 hover:text-emerald-700"
                        :class="{ 'bg-emerald-50 text-emerald-700 font-semibold': $route.path.startsWith('/my-courts') }">
                        My Courts
                    </router-link>

                    <!-- Bookings -->
                    <router-link to="/bookings"
                        class="px-5 py-2.5 rounded-xl font-medium transition-all hover:bg-emerald-50 hover:text-emerald-700 relative"
                        :class="{ 'bg-emerald-50 text-emerald-700 font-semibold': $route.path.startsWith('/bookings') }">
                        Bookings
                        <span v-if="pendingBookingsCount > 0"
                            class="absolute -top-1 -right-1 px-2 py-1 bg-red-500 text-white text-xs rounded-full min-w-[20px] h-5 flex items-center justify-center">
                            {{ pendingBookingsCount }}
                        </span>
                    </router-link>

                    <!-- Registrations (Super User only) -->
                    <router-link v-if="isSuperUser" to="/registrations"
                        class="px-5 py-2.5 rounded-xl font-medium transition-all hover:bg-emerald-50 hover:text-emerald-700 relative"
                        :class="{ 'bg-emerald-50 text-emerald-700 font-semibold': $route.path.startsWith('/registrations') }">
                        Registrations
                        <span v-if="pendingRegistrationsCount > 0"
                            class="absolute -top-1 -right-1 px-2 py-1 bg-amber-500 text-white text-xs rounded-full min-w-[20px] h-5 flex items-center justify-center">
                            {{ pendingRegistrationsCount }}
                        </span>
                    </router-link>

                    <!-- All Courts (Super User only) -->
                    <router-link v-if="isSuperUser" to="/courts"
                        class="px-5 py-2.5 rounded-xl font-medium transition-all hover:bg-emerald-50 hover:text-emerald-700"
                        :class="{ 'bg-emerald-50 text-emerald-700 font-semibold': $route.path.startsWith('/courts') }">
                        All Courts
                    </router-link>
                </div>

                <!-- Right Side: Notifications + Profile -->
                <div class="flex items-center gap-4">
                    <!-- Notifications Bell -->
                    <button @click="showNotifications = !showNotifications"
                        class="relative p-2 rounded-full hover:bg-emerald-50 transition-colors">
                        <svg class="w-6 h-6 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                        </svg>
                        <span v-if="unreadNotificationsCount > 0"
                            class="absolute top-0 right-0 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                            {{ unreadNotificationsCount > 9 ? '9+' : unreadNotificationsCount }}
                        </span>
                    </button>

                    <!-- Profile Dropdown -->
                    <div class="relative">
                        <button @click="showProfileMenu = !showProfileMenu"
                            class="flex items-center gap-3 p-2 rounded-xl hover:bg-emerald-50 transition-colors">
                            <div
                                class="w-10 h-10 rounded-full bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center text-white font-bold text-lg shadow-md">
                                {{ currentUser?.full_name?.charAt(0)?.toUpperCase() || '?' }}
                            </div>
                            <div class="hidden md:block text-left">
                                <p class="text-sm font-semibold text-gray-900">{{ currentUser?.full_name || 'Court Owner' }}</p>
                                <p class="text-xs text-gray-600">{{ roleLabel }}</p>
                            </div>
                        </button>

                        <!-- Profile Dropdown Menu -->
                        <div v-if="showProfileMenu"
                            class="absolute right-0 mt-3 w-64 bg-white rounded-2xl shadow-2xl border border-emerald-100 py-2 z-50">
                            <div class="px-5 py-4 border-b border-emerald-100">
                                <p class="font-semibold text-gray-900">{{ currentUser?.full_name }}</p>
                                <p class="text-sm text-gray-600">{{ currentUser?.phone_number }}</p>
                            </div>

                            <router-link to="/profile"
                                class="block px-5 py-3 hover:bg-emerald-50 text-gray-800 transition-colors"
                                @click="showProfileMenu = false">
                                My Profile
                            </router-link>

                            <button @click="handleLogout"
                                class="w-full text-left px-5 py-3 hover:bg-red-50 text-red-700 font-medium transition-colors">
                                Sign Out
                            </button>
                        </div>
                    </div>

                    <!-- Mobile Menu Toggle -->
                    <button class="lg:hidden p-2 rounded-full hover:bg-emerald-50 text-gray-700"
                        @click="mobileMenuOpen = !mobileMenuOpen">
                        <svg v-if="!mobileMenuOpen" class="w-6 h-6" fill="none" stroke="currentColor"
                            viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M4 6h16M4 12h16M4 18h16" />
                        </svg>
                        <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
            </div>
        </div>

        <!-- Mobile Menu -->
        <div v-if="mobileMenuOpen" class="lg:hidden fixed inset-0 bg-black/50 z-40" @click="mobileMenuOpen = false">
            <div class="absolute top-16 left-0 right-0 bg-white shadow-xl rounded-b-2xl overflow-hidden" @click.stop>
                <div class="p-6 space-y-2">
                    <!-- Mobile Nav Links -->
                    <router-link to="/dashboard"
                        class="block px-5 py-4 rounded-xl hover:bg-emerald-50 text-gray-800 font-medium transition-colors"
                        :class="{ 'bg-emerald-50 text-emerald-700': $route.path === '/dashboard' }"
                        @click="mobileMenuOpen = false">
                        Dashboard
                    </router-link>

                    <router-link v-if="isCourtOwnerOrManager" to="/my-courts"
                        class="block px-5 py-4 rounded-xl hover:bg-emerald-50 text-gray-800 font-medium transition-colors"
                        :class="{ 'bg-emerald-50 text-emerald-700': $route.path.startsWith('/my-courts') }"
                        @click="mobileMenuOpen = false">
                        My Courts
                    </router-link>

                    <router-link to="/bookings"
                        class="block px-5 py-4 rounded-xl hover:bg-emerald-50 text-gray-800 font-medium transition-colors"
                        :class="{ 'bg-emerald-50 text-emerald-700': $route.path.startsWith('/bookings') }"
                        @click="mobileMenuOpen = false">
                        Bookings
                    </router-link>

                    <router-link v-if="isSuperUser" to="/registrations"
                        class="block px-5 py-4 rounded-xl hover:bg-emerald-50 text-gray-800 font-medium transition-colors"
                        :class="{ 'bg-emerald-50 text-emerald-700': $route.path.startsWith('/registrations') }"
                        @click="mobileMenuOpen = false">
                        Registrations
                    </router-link>

                    <router-link v-if="isSuperUser" to="/courts"
                        class="block px-5 py-4 rounded-xl hover:bg-emerald-50 text-gray-800 font-medium transition-colors"
                        :class="{ 'bg-emerald-50 text-emerald-700': $route.path.startsWith('/courts') }"
                        @click="mobileMenuOpen = false">
                        All Courts
                    </router-link>
                </div>
            </div>
        </div>
    </nav>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const mobileMenuOpen = ref(false)
const showProfileMenu = ref(false)

// Computed role checks
const isCourtOwner = computed(() => authStore.user?.role === 'COURT_OWNER')
const isCourtManager = computed(() => authStore.user?.role === 'COURT_MANAGER')
const isCourtOwnerOrManager = computed(() => isCourtOwner.value || isCourtManager.value)
const isSuperUser = computed(() => authStore.user?.role === 'SUPER_USER')

// Current user
const currentUser = computed(() => authStore.user)

// Role label
const roleLabel = computed(() => {
    const role = authStore.user?.role
    if (role === 'COURT_OWNER') return 'Court Owner'
    if (role === 'COURT_MANAGER') return 'Court Manager'
    if (role === 'SUPER_USER') return 'Administrator'
    return 'User'
})

// Placeholder counts (replace with real data from store)
const pendingBookingsCount = ref(0) // Fetch from store or API
const pendingRegistrationsCount = ref(0) // Fetch from store or API
const unreadNotificationsCount = ref(0) // Fetch from store or API

const handleLogout = async () => {
    try {
        await authStore.logout()
        router.push('/login')
    } catch (err) {
        console.error('Logout failed:', err)
    }
}

// Close dropdowns on outside click
onMounted(() => {
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.profile-dropdown')) {
            showProfileMenu.value = false
        }
    })
})
</script>

<style scoped>
.admin-navbar {
  background: white;
  border-bottom: 1px solid #d1fae5; /* emerald-100 */
}

.nav-item.active {
  background: #ecfdf5; /* emerald-50 */
  color: #059669; /* emerald-600 */
  font-weight: 600;
}

.nav-badge {
  background: #ef4444; /* red-500 */
  color: white;
}

.profile-dropdown {
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
}


.admin-navbar {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
}

.navbar-container {
    max-width: 1600px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 70px;
}

/* Brand */
.navbar-brand {
    flex-shrink: 0;
}

.brand-link {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    text-decoration: none;
    color: white;
    transition: opacity 0.2s;
}

.brand-link:hover {
    opacity: 0.9;
}

.brand-logo {
    font-size: 2rem;
    line-height: 1;
}

.brand-text {
    display: flex;
    flex-direction: column;
}

.brand-name {
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: -0.5px;
}

.brand-subtitle {
    font-size: 0.75rem;
    opacity: 0.9;
    font-weight: 500;
}

/* Navigation */
.navbar-nav {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    flex: 1;
    justify-content: center;
    max-width: 900px;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.625rem 0.875rem;
    border-radius: 8px;
    text-decoration: none;
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.9rem;
    font-weight: 500;
    transition: all 0.2s;
    position: relative;
    white-space: nowrap;
}

.nav-item:hover {
    background: rgba(255, 255, 255, 0.15);
    color: white;
}

.nav-item.active {
    background: rgba(255, 255, 255, 0.2);
    color: white;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.nav-icon {
    font-size: 1.1rem;
}

.nav-badge {
    background: #e74c3c;
    color: white;
    padding: 0.125rem 0.375rem;
    border-radius: 10px;
    font-size: 0.7rem;
    font-weight: 600;
    min-width: 18px;
    text-align: center;
}

/* Actions */
.navbar-actions {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.action-item {
    position: relative;
}

.action-button {
    background: rgba(255, 255, 255, 0.1);
    border: none;
    padding: 0.5rem;
    border-radius: 8px;
    cursor: pointer;
    color: white;
    transition: all 0.2s;
    position: relative;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.action-button:hover {
    background: rgba(255, 255, 255, 0.2);
}

.action-button.has-notifications {
    animation: pulse 2s infinite;
}

@keyframes pulse {

    0%,
    100% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.05);
    }
}

.action-icon {
    font-size: 1.25rem;
}

.action-badge {
    position: absolute;
    top: -4px;
    right: -4px;
    background: #e74c3c;
    color: white;
    font-size: 0.65rem;
    font-weight: 600;
    padding: 0.125rem 0.375rem;
    border-radius: 10px;
    min-width: 18px;
    text-align: center;
}

/* Court Selector */
.court-selector-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(255, 255, 255, 0.1);
    border: none;
    padding: 0.5rem 0.75rem;
    border-radius: 8px;
    cursor: pointer;
    color: white;
    transition: all 0.2s;
    max-width: 200px;
}

.court-selector-button:hover {
    background: rgba(255, 255, 255, 0.2);
}

.court-icon {
    font-size: 1.1rem;
}

.court-name {
    font-size: 0.85rem;
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex: 1;
}

.arrow {
    font-size: 0.7rem;
    opacity: 0.7;
}

/* Profile Button */
.profile-button {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: rgba(255, 255, 255, 0.1);
    border: none;
    padding: 0.375rem 0.75rem 0.375rem 0.375rem;
    border-radius: 25px;
    cursor: pointer;
    color: white;
    transition: all 0.2s;
}

.profile-button:hover {
    background: rgba(255, 255, 255, 0.2);
}

.profile-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 0.9rem;
    color: white;
}

.profile-info {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    text-align: left;
}

.profile-name {
    font-size: 0.9rem;
    font-weight: 600;
    line-height: 1.2;
}

.profile-role {
    font-size: 0.75rem;
    opacity: 0.9;
    line-height: 1.2;
}

.profile-arrow {
    font-size: 0.7rem;
    opacity: 0.7;
}

/* Dropdowns */
.dropdown {
    position: absolute;
    top: calc(100% + 0.75rem);
    right: 0;
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    min-width: 300px;
    max-width: 380px;
    overflow: hidden;
    animation: dropdownSlide 0.2s ease-out;
}

.quick-actions-dropdown {
    min-width: 260px;
}

.court-dropdown {
    min-width: 320px;
}

@keyframes dropdownSlide {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.dropdown-header {
    padding: 1rem 1.25rem;
    border-bottom: 1px solid #e9ecef;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.dropdown-header h3 {
    margin: 0;
    font-size: 1rem;
    color: #2c3e50;
    font-weight: 600;
}

.btn-text {
    background: none;
    border: none;
    color: #3498db;
    font-size: 0.85rem;
    cursor: pointer;
    padding: 0;
    font-weight: 500;
}

.btn-text:hover {
    text-decoration: underline;
}

.dropdown-body {
    max-height: 400px;
    overflow-y: auto;
}

.dropdown-footer {
    padding: 0.75rem 1.25rem;
    border-top: 1px solid #e9ecef;
}

.btn-view-all {
    display: block;
    width: 100%;
    text-align: center;
    color: #3498db;
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
    padding: 0.5rem;
    border-radius: 6px;
    transition: background 0.2s;
}

.btn-view-all:hover {
    background: #f8f9fa;
}

/* Court Selector Dropdown */
.court-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.875rem 1.25rem;
    cursor: pointer;
    transition: background 0.2s;
    border: none;
    background: none;
    width: 100%;
    text-align: left;
}

.court-item:hover {
    background: #f8f9fa;
}

.court-item.active {
    background: #e3f2fd;
}

.court-item-icon {
    font-size: 1.5rem;
}

.court-item-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.court-item-name {
    font-size: 0.95rem;
    font-weight: 500;
    color: #2c3e50;
}

.court-item-location {
    font-size: 0.8rem;
    color: #7f8c8d;
}

.check-icon {
    color: #27ae60;
    font-size: 1.1rem;
}

/* Notifications Dropdown */
.notification-list {
    display: flex;
    flex-direction: column;
}

.notification-item {
    display: flex;
    gap: 0.75rem;
    padding: 1rem 1.25rem;
    cursor: pointer;
    transition: background 0.2s;
    border-bottom: 1px solid #f8f9fa;
}

.notification-item:hover {
    background: #f8f9fa;
}

.notification-item.unread {
    background: #e3f2fd;
}

.notification-item.unread:hover {
    background: #d1e7f9;
}

.notification-icon {
    font-size: 1.5rem;
    flex-shrink: 0;
}

.notification-content {
    flex: 1;
}

.notification-text {
    margin: 0 0 0.25rem 0;
    font-size: 0.9rem;
    color: #2c3e50;
    line-height: 1.4;
}

.notification-time {
    font-size: 0.8rem;
    color: #7f8c8d;
}

/* Profile Dropdown */
.dropdown-header.user-info {
    flex-direction: row;
    align-items: center;
    gap: 1rem;
    padding: 1.25rem;
}

.user-avatar-large {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 1.25rem;
    color: white;
    flex-shrink: 0;
}

.user-details {
    flex: 1;
}

.user-details h3 {
    font-size: 1.1rem;
    margin: 0 0 0.25rem 0;
}

.user-details p {
    margin: 0 0 0.5rem 0;
    font-size: 0.85rem;
    color: #7f8c8d;
}

.user-role-badge {
    display: inline-block;
    padding: 0.25rem 0.625rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
}

.role-super {
    background: #e3f2fd;
    color: #1976d2;
}

.role-owner {
    background: #fce4ec;
    color: #c2185b;
}

.role-manager {
    background: #e0f2f1;
    color: #00796b;
}

.role-player {
    background: #f3e5f5;
    color: #7b1fa2;
}

.dropdown-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.875rem 1.25rem;
    color: #2c3e50;
    text-decoration: none;
    transition: background 0.2s;
    cursor: pointer;
    border: none;
    background: none;
    width: 100%;
    font-size: 0.9rem;
    text-align: left;
}

.dropdown-item:hover {
    background: #f8f9fa;
}

.dropdown-item.logout {
    color: #e74c3c;
}

.dropdown-item.logout:hover {
    background: #fee;
}

.item-icon {
    font-size: 1.1rem;
    width: 20px;
    text-align: center;
}

.dropdown-divider {
    height: 1px;
    background: #e9ecef;
    margin: 0.5rem 0;
}

/* Empty State */
.empty-state {
    padding: 3rem 2rem;
    text-align: center;
    color: #7f8c8d;
}

.empty-icon {
    font-size: 3rem;
    display: block;
    margin-bottom: 0.5rem;
}

/* Mobile Menu Toggle */
.mobile-menu-toggle {
    display: none;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.5rem;
}

.hamburger {
    width: 24px;
    height: 20px;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.hamburger span {
    width: 100%;
    height: 3px;
    background: white;
    border-radius: 2px;
    transition: all 0.3s;
}

.hamburger.open span:nth-child(1) {
    transform: translateY(8.5px) rotate(45deg);
}

.hamburger.open span:nth-child(2) {
    opacity: 0;
}

.hamburger.open span:nth-child(3) {
    transform: translateY(-8.5px) rotate(-45deg);
}

.mobile-overlay {
    display: none;
}

/* Responsive */
@media (max-width: 1400px) {
    .navbar-container {
        padding: 0 1.5rem;
    }

    .navbar-nav {
        gap: 0.125rem;
    }

    .nav-item {
        padding: 0.5rem 0.75rem;
        font-size: 0.85rem;
    }
}

@media (max-width: 1200px) {
    .profile-info {
        display: none;
    }

    .court-selector-button {
        max-width: 150px;
    }

    .court-name {
        font-size: 0.8rem;
    }
}

@media (max-width: 1024px) {
    .navbar-nav {
        gap: 0;
    }

    .nav-item {
        padding: 0.5rem 0.625rem;
        font-size: 0.8rem;
    }

    .nav-text {
        display: none;
    }

    .nav-icon {
        font-size: 1.25rem;
    }
}

@media (max-width: 768px) {
    .navbar-container {
        height: 60px;
        padding: 0 1rem;
    }

    .brand-logo {
        font-size: 1.5rem;
    }

    .brand-name {
        font-size: 1.1rem;
    }

    .brand-subtitle {
        font-size: 0.7rem;
    }

    .navbar-nav {
        position: fixed;
        top: 60px;
        left: 0;
        right: 0;
        bottom: 0;
        background: white;
        flex-direction: column;
        justify-content: flex-start;
        padding: 1rem;
        gap: 0.5rem;
        transform: translateX(-100%);
        transition: transform 0.3s;
        overflow-y: auto;
    }

    .navbar-nav.mobile-open {
        transform: translateX(0);
    }

    .nav-item {
        width: 100%;
        color: #2c3e50;
        justify-content: flex-start;
        padding: 1rem;
        font-size: 1rem;
    }

    .nav-text {
        display: inline;
    }

    .nav-item:hover {
        background: #f8f9fa;
    }

    .nav-item.active {
        background: #e3f2fd;
        color: #3498db;
    }

    .mobile-menu-toggle {
        display: block;
    }

    .mobile-overlay {
        display: block;
        position: fixed;
        top: 60px;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        z-index: 999;
    }

    .dropdown {
        position: fixed;
        left: 1rem;
        right: 1rem;
        top: auto;
        max-width: none;
    }

    .court-selector-button {
        display: none;
    }

    .action-button {
        width: 36px;
        height: 36px;
    }
}

@media (max-width: 480px) {
    .navbar-actions {
        gap: 0.5rem;
    }

    .profile-button {
        padding: 0.375rem;
    }

    .profile-avatar {
        width: 28px;
        height: 28px;
        font-size: 0.8rem;
    }
}
</style>