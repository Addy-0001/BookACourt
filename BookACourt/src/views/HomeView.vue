<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Section -->
    <div class="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h1 class="text-5xl font-bold mb-4">Welcome, {{ authStore.user?.full_name }}!</h1>
        <p class="text-xl mb-8">Find and book your perfect court</p>
        <router-link to="/courts"
          class="inline-flex items-center gap-2 bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          Browse Courts
        </router-link>
      </div>
    </div>

    <!-- Quick Stats (for Players) -->
    <div v-if="authStore.isPlayer" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-10">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="bg-white rounded-xl shadow-lg p-6 border-t-4 border-blue-600">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-600 text-sm font-medium">Loyalty Points</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ authStore.user?.loyalty_points || 0 }}
              </p>
            </div>
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
                <path
                  d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
              </svg>
            </div>
          </div>
        </div>

        <router-link to="/bookings"
          class="bg-white rounded-xl shadow-lg p-6 border-t-4 border-green-600 hover:shadow-xl transition-shadow">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-600 text-sm font-medium">Upcoming Bookings</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ upcomingBookingsCount }}</p>
            </div>
            <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
        </router-link>

        <router-link to="/matches"
          class="bg-white rounded-xl shadow-lg p-6 border-t-4 border-purple-600 hover:shadow-xl transition-shadow">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-600 text-sm font-medium">Active Matches</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ activeMatchesCount }}</p>
            </div>
            <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
          </div>
        </router-link>

        <div class="bg-white rounded-xl shadow-lg p-6 border-t-4 border-amber-600">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-600 text-sm font-medium">Total Bookings</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ totalBookingsCount }}</p>
            </div>
            <div class="w-12 h-12 bg-amber-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Recent Activity -->
      <div class="mb-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">Recent Activity</h2>
        <div class="bg-white rounded-xl shadow-md p-6">
          <div v-if="loading" class="flex justify-center py-8">
            <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600"></div>
          </div>
          <div v-else-if="recentBookings.length === 0" class="text-center py-8 text-gray-500">
            <svg class="w-16 h-16 mx-auto mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
            </svg>
            <p class="text-lg font-medium">No recent bookings</p>
            <router-link to="/courts" class="mt-4 inline-block text-blue-600 hover:text-blue-700 font-medium">
              Browse courts to get started
            </router-link>
          </div>
          <div v-else class="space-y-4">
            <div v-for="booking in recentBookings" :key="booking.id"
              class="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer"
              @click="router.push(`/bookings/${booking.id}`)">
              <div>
                <h3 class="font-semibold text-gray-900">{{ booking.court?.name || 'Court' }}</h3>
                <p class="text-sm text-gray-600">{{ formatDate(booking.booking_date) }} at {{
                  booking.start_time }}</p>
              </div>
              <span :class="getStatusClass(booking.status)" class="px-3 py-1 rounded-full text-sm font-medium">
                {{ booking.status }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { bookingService } from '@/services/bookingService'

const router = useRouter()
const authStore = useAuthStore()
const loading = ref(false)
const recentBookings = ref([])
const stats = ref({
  upcoming: 0,
  matches: 0,
  total: 0
})

const upcomingBookingsCount = computed(() => stats.value.upcoming || 0)
const activeMatchesCount = computed(() => stats.value.matches || 0)
const totalBookingsCount = computed(() => stats.value.total || 0)

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

const getStatusClass = (status) => {
  const classes = {
    'PENDING': 'bg-yellow-100 text-yellow-800',
    'CONFIRMED': 'bg-green-100 text-green-800',
    'CANCELLED': 'bg-red-100 text-red-800',
    'COMPLETED': 'bg-blue-100 text-blue-800',
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const loadDashboardData = async () => {
  loading.value = true
  try {
    // Load recent bookings
    const bookingsResponse = await bookingService.getMyBookings()
    const allBookings = bookingsResponse.results || bookingsResponse

    // Get recent 5 bookings
    recentBookings.value = allBookings.slice(0, 5)

    // Calculate stats
    const now = new Date()
    stats.value = {
      upcoming: allBookings.filter(b =>
        ['PENDING', 'CONFIRMED'].includes(b.status) &&
        new Date(b.booking_date + ' ' + b.start_time) > now
      ).length,
      matches: 0, // Would need to load from matches endpoint
      total: allBookings.length
    }
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadDashboardData()
})
</script>