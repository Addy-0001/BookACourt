<!-- views/admin/Dashboard.vue -->
<template>
    <div class="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
            <!-- Header -->
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-6 mb-10">
                <div>
                    <h1 class="text-3xl sm:text-4xl font-bold text-gray-900">Dashboard</h1>
                    <p class="mt-2 text-lg text-gray-600">
                        Welcome back, {{ currentUser?.full_name || 'Court Manager' }} • Overview of your venues
                    </p>
                </div>

                <button @click="refreshDashboard" :disabled="loading"
                    class="px-6 py-3 bg-white border border-emerald-200 text-emerald-700 rounded-xl font-medium hover:bg-emerald-50 transition-colors flex items-center gap-2 disabled:opacity-60 shadow-sm">
                    <svg v-if="loading" class="animate-spin h-5 w-5 text-emerald-600" xmlns="http://www.w3.org/2000/svg"
                        fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4">
                        </circle>
                        <path class="opacity-75" fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                        </path>
                    </svg>
                    <span>{{ loading ? 'Refreshing...' : 'Refresh' }}</span>
                </button>
            </div>

            <!-- Error -->
            <div v-if="error"
                class="mb-8 p-5 bg-red-50 border border-red-200 rounded-xl text-red-800 flex items-center gap-3">
                <svg class="w-6 h-6 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <span>{{ error }}</span>
            </div>

            <!-- Stats Grid -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
                <StatCard title="Total Bookings" :value="stats.totalBookings.toLocaleString()" icon="📅"
                    color="emerald" />

                <StatCard title="Today's Revenue" :value="`Rs ${stats.todayRevenue.toLocaleString()}`" icon="₹"
                    color="teal" />

                <StatCard title="Occupancy Rate" :value="`${stats.occupancyRate}%`" icon="📈" color="amber" />

                <StatCard title="Pending Requests" :value="stats.pendingRegistrations" icon="📝" color="red"
                    :highlight="stats.pendingRegistrations > 0" />
            </div>

            <!-- Quick Actions -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
                <QuickActionCard title="My Courts" description="Manage venues, pricing, availability & amenities"
                    icon="🏟️" to="/my-courts" />

                <QuickActionCard title="Bookings" description="View, confirm, cancel or modify reservations" icon="📅"
                    to="/bookings" :badge="pendingBookingsCount" />

                <QuickActionCard v-if="isSuperUser" title="New Registrations"
                    description="Review & approve pending court registrations" icon="📋" to="/registrations"
                    :badge="stats.pendingRegistrations" />
            </div>

            <!-- Recent Bookings -->
            <div class="bg-white rounded-2xl shadow-md border border-emerald-100 overflow-hidden">
                <div class="p-6 border-b border-emerald-100 flex items-center justify-between">
                    <div>
                        <h2 class="text-xl font-bold text-gray-900">Recent Bookings</h2>
                        <p class="text-sm text-gray-600 mt-1">Latest 5 bookings across all your courts</p>
                    </div>
                    <router-link to="/bookings"
                        class="text-emerald-700 hover:text-emerald-800 font-medium flex items-center gap-2 hover:underline">
                        View All
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                        </svg>
                    </router-link>
                </div>

                <div v-if="loading" class="p-12 text-center">
                    <div
                        class="w-12 h-12 border-4 border-emerald-200 border-t-emerald-600 rounded-full animate-spin mx-auto">
                    </div>
                </div>

                <div v-else-if="recentBookings.length === 0" class="p-12 text-center text-gray-500">
                    No recent bookings yet
                </div>

                <div v-else class="divide-y divide-gray-100">
                    <div v-for="booking in recentBookings" :key="booking.id"
                        class="p-6 hover:bg-emerald-50/30 transition-colors cursor-pointer"
                        @click="router.push(`/bookings/${booking.id}`)">
                        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                            <div>
                                <p class="font-medium text-gray-900">{{ booking.court?.name || 'Unknown Court' }}</p>
                                <p class="text-sm text-gray-600 mt-1">
                                    {{ formatDate(booking.booking_date) }} • {{ booking.start_time }} - {{
                                        booking.end_time }}
                                </p>
                                <p class="text-xs text-gray-500 mt-1">
                                    Player: {{ booking.user?.full_name || '—' }}
                                </p>
                            </div>
                            <div class="text-right">
                                <p class="font-bold text-emerald-700 text-xl">Rs {{
                                    booking.total_amount?.toLocaleString() || '—' }}</p>
                                <span :class="getStatusBadge(booking.status)"
                                    class="inline-block px-4 py-1.5 mt-2 text-xs font-semibold rounded-full">
                                    {{ booking.status }}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useAdminStore } from '@/stores/admin'
import StatCard from '@/components/StatCard.vue'
import QuickActionCard from '@/components/QuickActionCard.vue'

const router = useRouter()
const authStore = useAuthStore()
const adminStore = useAdminStore()

const loading = ref(false)
const error = ref(null)

const stats = ref({
    totalBookings: 0,
    todayRevenue: 0,
    occupancyRate: 0,
    pendingRegistrations: 0,
})

const recentBookings = ref([])

// Role checks
const isCourtOwner = computed(() => authStore.user?.role === 'COURT_OWNER')
const isCourtManager = computed(() => authStore.user?.role === 'COURT_MANAGER')
const isCourtOwnerOrManager = computed(() => isCourtOwner.value || isCourtManager.value)
const isSuperUser = computed(() => authStore.user?.role === 'SUPER_USER')

const currentUser = computed(() => authStore.user)

// Computed pending bookings count
const pendingBookingsCount = computed(() => recentBookings.value.filter(b => b.status === 'PENDING').length)

// Fetch dashboard data
const fetchDashboard = async () => {
    if (!authStore.isAuthenticated) {
        router.push('/login')
        return
    }

    loading.value = true
    error.value = null

    try {
        // 1. Recent bookings (last 5)
        const bookingsRes = await adminStore.bookingsApi.getBookings({
            page_size: 5,
            ordering: '-created_at'
        })
        recentBookings.value = bookingsRes.results || []

        // 2. Total bookings count (for stats)
        const totalBookingsRes = await adminStore.bookingsApi.getBookings({ page_size: 1 })
        stats.value.totalBookings = totalBookingsRes.count || 0

        // 3. Today's revenue
        const today = new Date().toISOString().split('T')[0]
        const revenueRes = await adminStore.bookingsApi.getBookings({
            payment_status: 'COMPLETED',
            date_from: today,
            date_to: today
        })
        stats.value.todayRevenue = revenueRes.results?.reduce((sum, b) => sum + (Number(b.total_amount) || 0), 0) || 0

        // 4. Occupancy rate - placeholder (you can add real calculation or endpoint)
        // For real implementation, you might need a custom endpoint like /courts/occupancy/
        stats.value.occupancyRate = 68 // ← Replace with real data

        // 5. Pending registrations (super user only)
        if (isSuperUser.value) {
            const regRes = await adminStore.registrationsApi.getRegistrations({
                status: 'PENDING',
                page_size: 1
            })
            stats.value.pendingRegistrations = regRes.count || 0
        }
    } catch (err) {
        console.error('Dashboard load failed:', err)
        error.value = err.response?.data?.detail || 'Failed to load dashboard data. Please try again.'
    } finally {
        loading.value = false
    }
}

const refreshDashboard = () => {
    fetchDashboard()
}

const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
        weekday: 'short',
        month: 'short',
        day: 'numeric'
    })
}

const getStatusBadge = (status) => {
    const classes = {
        'PENDING': 'bg-amber-100 text-amber-800',
        'CONFIRMED': 'bg-emerald-100 text-emerald-800',
        'CANCELLED': 'bg-red-100 text-red-800',
        'COMPLETED': 'bg-blue-100 text-blue-800',
        'NO_SHOW': 'bg-gray-100 text-gray-800',
    }
    return classes[status] || 'bg-gray-100 text-gray-800'
}

onMounted(() => {
    fetchDashboard()
})
</script>