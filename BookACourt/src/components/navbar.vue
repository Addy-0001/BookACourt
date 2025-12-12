<template>
    <nav class="bg-white shadow-md sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <!-- Logo and Brand -->
                <div class="flex items-center gap-8">
                    <router-link to="/" class="flex items-center gap-2">
                        <div
                            class="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                            </svg>
                        </div>
                        <span
                            class="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                            BookACourt
                        </span>
                    </router-link>

                    <!-- Desktop Navigation -->
                    <div class="hidden md:flex items-center gap-1">
                        <router-link v-for="link in navLinks" :key="link.path" :to="link.path" :class="[
                            'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                            isActive(link.path)
                                ? 'bg-blue-50 text-blue-600'
                                : 'text-gray-700 hover:bg-gray-100'
                        ]">
                            {{ link.label }}
                        </router-link>
                    </div>
                </div>

                <!-- Right Side Actions -->
                <div class="flex items-center gap-3">
                    <!-- Notifications -->
                    <router-link v-if="authStore.isAuthenticated" to="/notifications"
                        class="relative p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                        </svg>
                        <span v-if="unreadCount > 0"
                            class="absolute top-1 right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center font-bold">
                            {{ unreadCount > 9 ? '9+' : unreadCount }}
                        </span>
                    </router-link>

                    <!-- Friends -->
                    <router-link v-if="authStore.isAuthenticated && authStore.isPlayer" to="/friends"
                        class="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                        </svg>
                    </router-link>

                    <!-- User Menu -->
                    <div v-if="authStore.isAuthenticated" class="relative">
                        <button @click="showUserMenu = !showUserMenu"
                            class="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors">
                            <div
                                class="w-8 h-8 bg-gradient-to-br from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-sm">
                                {{ authStore.user?.full_name?.charAt(0).toUpperCase() }}
                            </div>
                            <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M19 9l-7 7-7-7" />
                            </svg>
                        </button>

                        <!-- Dropdown Menu -->
                        <div v-if="showUserMenu" v-click-outside="closeUserMenu"
                            class="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-lg border border-gray-200 py-1">
                            <div class="px-4 py-3 border-b border-gray-200">
                                <p class="text-sm font-medium text-gray-900">{{ authStore.user?.full_name }}</p>
                                <p class="text-xs text-gray-500 mt-1">{{ authStore.user?.phone_number }}</p>
                            </div>

                            <router-link v-for="item in userMenuItems" :key="item.path" :to="item.path"
                                @click="showUserMenu = false"
                                class="flex items-center gap-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors">
                                <component :is="item.icon" class="w-5 h-5 text-gray-500" />
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
                    </div>

                    <!-- Login Button (for guests) -->
                    <router-link v-else to="/login"
                        class="px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:shadow-lg transition-all font-medium">
                        Login
                    </router-link>

                    <!-- Mobile Menu Button -->
                    <button @click="showMobileMenu = !showMobileMenu"
                        class="md:hidden p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
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
        <div v-if="showMobileMenu" class="md:hidden border-t border-gray-200 bg-white">
            <div class="px-4 py-4 space-y-1">
                <router-link v-for="link in navLinks" :key="link.path" :to="link.path" @click="showMobileMenu = false"
                    :class="[
                        'block px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                        isActive(link.path)
                            ? 'bg-blue-50 text-blue-600'
                            : 'text-gray-700 hover:bg-gray-100'
                    ]">
                    {{ link.label }}
                </router-link>
            </div>
        </div>
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
            icon: 'svg'
        },
        {
            path: '/preferences',
            label: 'Preferences',
            icon: 'svg'
        }
    ]

    if (authStore.isPlayer) {
        items.push({
            path: '/leaderboard',
            label: 'Leaderboard',
            icon: 'svg'
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

// Load unread notifications count
const loadUnreadCount = async () => {
    if (!authStore.isAuthenticated) return

    try {
        unreadCount.value = await notificationService.getUnreadCount()
    } catch (err) {
        console.error('Failed to load unread count:', err)
    }
}

// Close user menu
const closeUserMenu = () => {
    showUserMenu.value = false
}

// Logout handler
const handleLogout = async () => {
    await authStore.logout()
    showUserMenu.value = false
    router.push('/login')
}

// Click outside directive
const vClickOutside = {
    mounted(el, binding) {
        el.clickOutsideEvent = (event) => {
            if (!(el === event.target || el.contains(event.target))) {
                binding.value()
            }
        }
        document.addEventListener('click', el.clickOutsideEvent)
    },
    unmounted(el) {
        document.removeEventListener('click', el.clickOutsideEvent)
    }
}

// Poll for notifications
onMounted(() => {
    if (authStore.isAuthenticated) {
        loadUnreadCount()
        notificationInterval = setInterval(loadUnreadCount, 30000) // Every 30 seconds
    }
})

onUnmounted(() => {
    if (notificationInterval) {
        clearInterval(notificationInterval)
    }
})
</script>