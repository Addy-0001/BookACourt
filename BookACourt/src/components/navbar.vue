<template>
    <nav class="bg-white shadow-md sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <!-- Logo and Brand -->
                <div class="flex items-center gap-8">
                    <router-link to="/" class="flex items-center gap-2">
                        <div
                            class="w-10 h-10 bg-gradient-to-br from-[#0056B3] to-[#7C3AED] rounded-lg flex items-center justify-center">
                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                            </svg>
                        </div>
                        <span
                            class="text-xl font-bold bg-gradient-to-r from-[#0056B3] to-[#7C3AED] bg-clip-text text-transparent">
                            BookACourt
                        </span>
                    </router-link>

                    <!-- Desktop Navigation -->
                    <div class="hidden md:flex items-center gap-1">
                        <router-link v-for="link in navLinks" :key="link.path" :to="link.path" :class="[
                            'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                            isActive(link.path)
                                ? 'bg-[#E3F2FD] text-[#0056B3]'
                                : 'text-gray-700 hover:bg-[#F3F4F6]'
                        ]">
                            {{ link.label }}
                        </router-link>
                    </div>
                </div>

                <!-- Right Side Actions -->
                <div class="flex items-center gap-3">
                    <!-- Notifications -->
                    <router-link v-if="authStore.isAuthenticated" to="/notifications"
                        class="relative p-2 text-gray-600 hover:bg-[#F3F4F6] rounded-lg transition-colors">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                        </svg>
                        <span v-if="unreadCount > 0"
                            class="absolute top-1 right-1 w-5 h-5 bg-[#EF4444] text-white text-xs rounded-full flex items-center justify-center font-bold">
                            {{ unreadCount > 9 ? '9+' : unreadCount }}
                        </span>
                    </router-link>

                    <!-- Friends -->
                    <router-link v-if="authStore.isAuthenticated && authStore.isPlayer" to="/friends"
                        class="p-2 text-gray-600 hover:bg-[#F3F4F6] rounded-lg transition-colors">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                        </svg>
                    </router-link>

                    <!-- User Menu -->
                    <div v-if="authStore.isAuthenticated" class="relative">
                        <button @click.stop="toggleUserMenu"
                            class="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-[#F3F4F6] transition-colors">
                            <div
                                class="w-8 h-8 bg-gradient-to-br from-[#0056B3] to-[#7C3AED] rounded-full flex items-center justify-center text-white font-bold text-sm">
                                {{ authStore.user?.full_name?.charAt(0).toUpperCase() }}
                            </div>
                            <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M19 9l-7 7-7-7" />
                            </svg>
                        </button>

                        <!-- Dropdown Menu -->
                        <transition name="dropdown">
                            <div v-if="showUserMenu"
                                class="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-lg border border-gray-200 py-1">
                                <div class="px-4 py-3 border-b border-gray-200">
                                    <p class="text-sm font-medium text-gray-900">{{ authStore.user?.full_name }}</p>
                                    <p class="text-xs text-gray-500 mt-1">{{ authStore.user?.phone_number }}</p>
                                </div>

                                <router-link v-for="item in userMenuItems" :key="item.path" :to="item.path"
                                    @click="showUserMenu = false"
                                    class="flex items-center gap-3 px-4 py-2 text-sm text-gray-700 hover:bg-[#F3F4F6] transition-colors">
                                    <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor"
                                        viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            :d="item.iconPath" />
                                    </svg>
                                    {{ item.label }}
                                </router-link>

                                <div class="border-t border-gray-200 mt-1 pt-1">
                                    <button @click="handleLogout"
                                        class="w-full flex items-center gap-3 px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                                        </svg>
                                        Logout
                                    </button>
                                </div>
                            </div>
                        </transition>
                    </div>

                    <!-- Login Button (for guests) -->
                    <router-link v-else to="/login"
                        class="px-4 py-2 bg-gradient-to-r from-[#0056B3] to-[#7C3AED] text-white rounded-lg hover:shadow-lg transition-all font-medium">
                        Login
                    </router-link>

                    <!-- Mobile Menu Button -->
                    <button @click="showMobileMenu = !showMobileMenu"
                        class="md:hidden p-2 text-gray-600 hover:bg-[#F3F4F6] rounded-lg transition-colors">
                        <svg v-if="!showMobileMenu" class="w-6 h-6" fill="none" stroke="currentColor"
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
        <transition name="mobile">
            <div v-if="showMobileMenu" class="md:hidden border-t border-gray-200 bg-white">
                <div class="px-4 py-4 space-y-1">
                    <router-link v-for="link in navLinks" :key="link.path" :to="link.path"
                        @click="showMobileMenu = false" :class="[
                            'block px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                            isActive(link.path)
                                ? 'bg-[#E3F2FD] text-[#0056B3]'
                                : 'text-gray-700 hover:bg-[#F3F4F6]'
                        ]">
                        {{ link.label }}
                    </router-link>
                </div>
            </div>
        </transition>
    </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { notificationService } from '@/services/notificationService'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const showUserMenu = ref(false)
const showMobileMenu = ref(false)
const unreadCount = ref(0)
let notificationInterval = null

// Navigation Links
const navLinks = computed(() => {
    const links = [
        { path: '/', label: 'Home' },
        { path: '/courts', label: 'Courts' },
        { path: '/bookings', label: 'My Bookings' },
    ]

    if (authStore.isPlayer) {
        links.push({ path: '/matches', label: 'Matches' })
    }

    if (authStore.isCourtOwner) {
        links.push({ path: '/court-registration', label: 'Register Court' })
    }

    return links
})

// User Menu Items
const userMenuItems = computed(() => {
    const items = [
        {
            path: '/profile',
            label: 'My Profile',
            iconPath: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z'
        },
        {
            path: '/preferences',
            label: 'Preferences',
            iconPath: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z'
        }
    ]

    if (authStore.isPlayer) {
        items.push({
            path: '/leaderboard',
            label: 'Leaderboard',
            iconPath: 'M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z'
        })
    }

    return items
})

// Check if route is active
const isActive = (path) => {
    if (path === '/') {
        return route.path === '/'
    }
    return route.path.startsWith(path)
}

// Toggle user menu
const toggleUserMenu = () => {
    showUserMenu.value = !showUserMenu.value
}

// Close user menu when clicking outside
const closeUserMenu = (e) => {
    if (!e.target.closest('.relative')) {
        showUserMenu.value = false
    }
}

// Load unread notifications count
const loadUnreadCount = async () => {
    if (!authStore.isAuthenticated) return

    try {
        unreadCount.value = await notificationService.getUnreadCount()
    } catch (err) {
        console.error('Failed to load unread count:', err)
    }
}

// Logout handler
const handleLogout = async () => {
    await authStore.logout()
    showUserMenu.value = false
    router.push('/login')
}

// Close menus on route change
router.afterEach(() => {
    showUserMenu.value = false
    showMobileMenu.value = false
})

// Poll for notifications
onMounted(() => {
    if (authStore.isAuthenticated) {
        loadUnreadCount()
        notificationInterval = setInterval(loadUnreadCount, 30000) // Every 30 seconds
    }
    document.addEventListener('click', closeUserMenu)
})

onUnmounted(() => {
    if (notificationInterval) {
        clearInterval(notificationInterval)
    }
    document.removeEventListener('click', closeUserMenu)
})
</script>

<style scoped>
/* Dropdown transitions */
.dropdown-enter-active,
.dropdown-leave-active {
    transition: all 0.2s ease;
}

.dropdown-enter-from {
    opacity: 0;
    transform: translateY(-10px);
}

.dropdown-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}

/* Mobile menu transitions */
.mobile-enter-active,
.mobile-leave-active {
    transition: all 0.3s ease;
}

.mobile-enter-from,
.mobile-leave-to {
    opacity: 0;
    max-height: 0;
    overflow: hidden;
}

.mobile-enter-to,
.mobile-leave-from {
    opacity: 1;
    max-height: 500px;
}
</style>