<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Navigation -->
        <nav class="bg-white shadow-sm sticky top-0 z-50">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex justify-between h-16">
                    <div class="flex items-center gap-4">
                        <button @click="goBack" class="text-gray-600 hover:text-gray-900">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M15 19l-7-7 7-7" />
                            </svg>
                        </button>
                        <h1 class="text-2xl font-bold text-blue-600">My Bookings</h1>
                    </div>
                    <div class="flex items-center gap-4">
                        <router-link to="/"
                            class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
                            Home
                        </router-link>
                        <router-link to="/profile"
                            class="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                            Profile
                        </router-link>
                    </div>
                </div>
            </div>
        </nav>

        <!-- Content -->
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Filters -->
            <div class="bg-white rounded-xl shadow-md p-6 mb-8">
                <div class="flex items-center gap-4">
                    <button v-for="status in statuses" :key="status.value" @click="filterStatus = status.value" :class="[
                        'px-4 py-2 rounded-lg font-medium transition-colors',
                        filterStatus === status.value
                            ? 'bg-blue-600 text-white'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    ]">
                        {{ status.label }}
                    </button>
                </div>
            </div>

            <!-- Loading State -->
            <div v-if="loading" class="flex justify-center py-20">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>

            <!-- Bookings List -->
            <div v-else-if="filteredBookings.length > 0" class="space-y-4">
                <div v-for="booking in filteredBookings" :key="booking.id"
                    class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow">
                    <div class="flex items-start justify-between mb-4">
                        <div>
                            <h3 class="text-xl font-bold text-gray-900">{{ booking.court_name }}</h3>
                            <p class="text-gray-600">{{ booking.court_address }}</p>
                        </div>
                        <span :class="getStatusClass(booking.status)"
                            class="px-3 py-1 rounded-full text-sm font-medium">
                            {{ booking.status }}
                        </span>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                        <div class="flex items-center gap-2 text-gray-600">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                            <span>{{ formatDate(booking.booking_date) }}</span>
                        </div>
                        <div class="flex items-center gap-2 text-gray-600">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <span>{{ booking.start_time }} - {{ booking.end_time }}</span>
                        </div>
                        <div class="flex items-center gap-2 text-gray-600">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <span class="font-bold">Rs {{ booking.total_amount }}</span>
                        </div>
                    </div>

                    <div class="flex items-center justify-between">
                        <span class="text-sm text-gray-500">Booking ID: {{ booking.booking_reference }}</span>
                        <div class="flex items-center gap-2">
                            <button v-if="booking.status === 'PENDING' || booking.status === 'CONFIRMED'"
                                @click="viewBookingDetail(booking.id)"
                                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                                View Details
                            </button>
                            <button v-if="booking.status === 'PENDING' || booking.status === 'CONFIRMED'"
                                @click="cancelBooking(booking)"
                                class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors">
                                Cancel
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Empty State -->
            <div v-else class="text-center py-20">
                <svg class="w-24 h-24 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <p class="text-xl text-gray-600 mb-4">No bookings found</p>
                <router-link to="/courts"
                    class="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                    Browse Courts
                </router-link>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/services/api'

const router = useRouter()
const loading = ref(false)
const bookings = ref([])
const filterStatus = ref('all')

const statuses = [
    { value: 'all', label: 'All' },
    { value: 'PENDING', label: 'Pending' },
    { value: 'CONFIRMED', label: 'Confirmed' },
    { value: 'COMPLETED', label: 'Completed' },
    { value: 'CANCELLED', label: 'Cancelled' },
]

const filteredBookings = computed(() => {
    if (filterStatus.value === 'all') {
        return bookings.value
    }
    return bookings.value.filter(b => b.status === filterStatus.value)
})

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
        'NO_SHOW': 'bg-gray-100 text-gray-800',
    }
    return classes[status] || 'bg-gray-100 text-gray-800'
}

const loadBookings = async () => {
    loading.value = true
    try {
        // API endpoint to be implemented
        // const response = await apiClient.get('/bookings/')
        // bookings.value = response.data.results || response.data

        // Mock data for now
        bookings.value = []
    } catch (error) {
        console.error('Failed to load bookings:', error)
    } finally {
        loading.value = false
    }
}

const viewBookingDetail = (bookingId) => {
    router.push(`/bookings/${bookingId}`)
}

const cancelBooking = async (booking) => {
    if (!confirm('Are you sure you want to cancel this booking?')) {
        return
    }

    try {
        // API endpoint to be implemented
        // await apiClient.patch(`/bookings/${booking.id}/`, { status: 'CANCELLED' })
        // await loadBookings()
        alert('Booking cancelled successfully')
    } catch (error) {
        console.error('Failed to cancel booking:', error)
        alert('Failed to cancel booking')
    }
}

const goBack = () => {
    router.go(-1)
}

onMounted(() => {
    loadBookings()
})
</script>