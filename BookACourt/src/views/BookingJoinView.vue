<template>
    <div class="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center p-4">
        <!-- Loading -->
        <div v-if="loading" class="text-center">
            <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p class="text-xl text-gray-600">Loading booking details...</p>
        </div>

        <!-- Error -->
        <div v-else-if="error" class="bg-white rounded-xl shadow-xl p-8 max-w-md w-full text-center">
            <svg class="w-16 h-16 mx-auto text-red-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h2 class="text-2xl font-bold text-gray-900 mb-2">Invalid Link</h2>
            <p class="text-gray-600 mb-6">{{ error }}</p>
            <router-link to="/"
                class="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                Go Home
            </router-link>
        </div>

        <!-- Success -->
        <div v-else-if="success" class="bg-white rounded-xl shadow-xl p-8 max-w-md w-full text-center">
            <svg class="w-16 h-16 mx-auto text-green-500 mb-4" fill="currentColor" viewBox="0 0 24 24">
                <path
                    d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
            </svg>
            <h2 class="text-2xl font-bold text-gray-900 mb-2">Joined Successfully!</h2>
            <p class="text-gray-600 mb-6">You've been added to the booking.</p>
            <router-link to="/bookings"
                class="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                View My Bookings
            </router-link>
        </div>

        <!-- Booking Details -->
        <div v-else-if="bookingShare" class="bg-white rounded-xl shadow-xl p-8 max-w-2xl w-full">
            <h2 class="text-2xl font-bold text-gray-900 mb-6">Join Booking</h2>

            <div class="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <p class="text-sm text-blue-800 font-medium">{{ bookingShare.shared_by_name }} invited you to join this
                    booking</p>
            </div>

            <div class="space-y-4 mb-6">
                <div class="flex items-center gap-3">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                    <span class="text-gray-600">Booking Ref: <span class="font-medium text-gray-900">{{
                        bookingShare.booking_reference }}</span></span>
                </div>

                <div class="flex items-center gap-3">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                    <span class="text-gray-600">{{ bookingShare.joined_count }} / {{ bookingShare.max_joins }} spots
                        filled</span>
                </div>

                <div class="flex items-center gap-3">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span class="text-gray-600">Expires: <span class="font-medium text-gray-900">{{
                        formatDateTime(bookingShare.expires_at) }}</span></span>
                </div>
            </div>

            <div v-if="!bookingShare.is_valid" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                <p class="text-sm text-red-800 font-medium">This share link is no longer valid</p>
            </div>

            <div v-else-if="alreadyJoined" class="mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <p class="text-sm text-yellow-800 font-medium">You have already joined this booking</p>
            </div>

            <div class="flex gap-3">
                <button @click="goBack"
                    class="flex-1 px-6 py-3 border border-gray-300 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors font-medium">
                    Cancel
                </button>
                <button v-if="bookingShare.is_valid && !alreadyJoined" @click="handleJoin" :disabled="joining"
                    class="flex-1 px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white rounded-lg transition-colors font-medium">
                    <span v-if="joining">Joining...</span>
                    <span v-else>Join Booking</span>
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { bookingService } from '@/services/bookingService'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const joining = ref(false)
const error = ref(null)
const success = ref(false)
const bookingShare = ref(null)

const alreadyJoined = computed(() => {
    if (!bookingShare.value) return false
    const userId = JSON.parse(localStorage.getItem('user'))?.id
    return bookingShare.value.joined_users?.includes(userId)
})

const formatDateTime = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    })
}

const loadBookingShare = async () => {
    loading.value = true
    error.value = null

    try {
        const token = route.params.token
        bookingShare.value = await bookingService.getBookingShare(token)
    } catch (err) {
        console.error('Failed to load booking share:', err)
        error.value = err.response?.data?.detail || 'This share link is invalid or has expired'
    } finally {
        loading.value = false
    }
}

const handleJoin = async () => {
    joining.value = true

    try {
        const token = route.params.token
        await bookingService.joinSharedBooking(token)
        success.value = true
    } catch (err) {
        console.error('Failed to join booking:', err)
        error.value = err.response?.data?.detail || 'Failed to join booking'
    } finally {
        joining.value = false
    }
}

const goBack = () => {
    router.go(-1)
}

onMounted(() => {
    loadBookingShare()
})
</script>