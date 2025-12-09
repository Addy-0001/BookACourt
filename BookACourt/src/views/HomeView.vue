<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow-sm sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-2xl font-bold text-blue-600">BookACourt</h1>
          </div>
          <div class="flex items-center gap-4">
            <router-link to="/courts"
              class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
              Courts
            </router-link>
            <router-link to="/bookings"
              class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
              My Bookings
            </router-link>
            <router-link v-if="authStore.isPlayer" to="/matches"
              class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
              Matches
            </router-link>
            <router-link to="/profile"
              class="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              Profile
            </router-link>
          </div>
        </div>
      </div>
    </nav>

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
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ authStore.user?.loyalty_points || 0 }}</p>
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
              class="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <div>
                <h3 class="font-semibold text-gray-900">{{ booking.court }}</h3>
                <p class="text-sm text-gray-600">{{ formatDate(booking.booking_date) }} at {{ booking.start_time }}</p>
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
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/services/api'

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
    // Load recent bookings (adjust endpoint as needed)
    // const bookingsResponse = await apiClient.get('/bookings/?limit=5')
    // recentBookings.value = bookingsResponse.data.results || []

    // Load stats
    // const statsResponse = await apiClient.get('/user/stats/')
    // stats.value = statsResponse.data

    // Mock data for now
    recentBookings.value = []
    stats.value = {
      upcoming: 0,
      matches: 0,
      total: 0
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