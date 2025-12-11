<template>
    <div class="min-h-screen bg-gray-50">
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

        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Filters -->
            <div class="bg-white rounded-xl shadow-md p-6 mb-8">
                <div class="flex items-center gap-4 flex-wrap">
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

            <!-- Error State -->
            <div v-else-if="error" class="text-center py-20">
                <svg class="w-16 h-16 mx-auto text-red-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p class="text-xl text-gray-600 mb-4">{{ error }}</p>
                <button @click="loadBookings" class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                    Try Again
                </button>
            </div>

            <!-- Bookings List -->
            <div v-else-if="filteredBookings.length > 0" class="space-y-4">
                <div v-for="booking in filteredBookings" :key="booking.id"
                    class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow">
                    <div class="flex items-start justify-between mb-4">
                        <div>
                            <h3 class="text-xl font-bold text-gray-900">{{ booking.court?.name || 'Court' }}</h3>
                            <p class="text-gray-600">{{ booking.court?.address || booking.court?.city }}</p>
                            <p class="text-sm text-gray-500 mt-1">Ref: {{ booking.booking_reference }}</p>
                        </div>
                        <span :class="getStatusClass(booking.status)"
                            class="px-3 py-1 rounded-full text-sm font-medium whitespace-nowrap">
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

                    <div class="flex items-center gap-2 text-sm text-gray-500 mb-4">
                        <span>Payment: {{ booking.payment_method }}</span>
                        <span>•</span>
                        <span :class="getPaymentStatusClass(booking.payment_status)">
                            {{ booking.payment_status }}
                        </span>
                    </div>

                    <!-- Equipment Rentals -->
                    <div v-if="booking.equipment_rentals && booking.equipment_rentals.length > 0"
                        class="mb-4 p-3 bg-blue-50 rounded-lg">
                        <p class="font-medium text-blue-900 mb-2">Equipment Rented:</p>
                        <div class="space-y-1">
                            <div v-for="rental in booking.equipment_rentals" :key="rental.id"
                                class="text-sm text-blue-800 flex items-center justify-between">
                                <span>{{ rental.equipment?.name }} (x{{ rental.quantity }})</span>
                                <span class="font-medium">Rs {{ rental.rental_cost }}</span>
                            </div>
                        </div>
                    </div>

                    <div v-if="booking.notes" class="text-sm text-gray-600 mb-4 p-3 bg-gray-50 rounded-lg">
                        <p class="font-medium text-gray-700">Notes:</p>
                        <p>{{ booking.notes }}</p>
                    </div>

                    <div class="flex items-center justify-between border-t pt-4">
                        <span class="text-xs text-gray-400">
                            Booked {{ formatDateTime(booking.created_at) }}
                        </span>
                        <div class="flex items-center gap-2">
                            <button v-if="canShare(booking)" @click="shareBooking(booking)"
                                class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors text-sm font-medium">
                                Share
                            </button>
                            <button v-if="canCancel(booking)" @click="showCancelModal(booking)"
                                class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors text-sm font-medium">
                                Cancel
                            </button>
                            <button v-if="canReview(booking)" @click="showReviewModal(booking)"
                                class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm font-medium">
                                Leave Review
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

        <!-- Cancel Modal -->
        <div v-if="cancelModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div class="bg-white rounded-xl max-w-md w-full p-6">
                <h3 class="text-xl font-bold text-gray-900 mb-4">Cancel Booking</h3>
                <p class="text-gray-600 mb-4">Are you sure you want to cancel this booking?</p>
                <textarea v-model="cancelReason" placeholder="Reason for cancellation (optional)"
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg mb-4" rows="3"></textarea>
                <div class="flex gap-3">
                    <button @click="cancelModal = null"
                        class="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">
                        Keep Booking
                    </button>
                    <button @click="confirmCancel" :disabled="cancelling"
                        class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:bg-gray-400">
                        {{ cancelling ? 'Cancelling...' : 'Cancel Booking' }}
                    </button>
                </div>
            </div>
        </div>

        <!-- Share Modal -->
        <div v-if="shareModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div class="bg-white rounded-xl max-w-md w-full p-6">
                <h3 class="text-xl font-bold text-gray-900 mb-4">Share Booking</h3>

                <div v-if="shareLink" class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Share Link</label>
                        <div class="flex gap-2">
                            <input :value="shareLink" readonly
                                class="flex-1 px-4 py-2 border border-gray-300 rounded-lg bg-gray-50" />
                            <button @click="copyShareLink"
                                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                                Copy
                            </button>
                        </div>
                        <p v-if="linkCopied" class="text-sm text-green-600 mt-1">Link copied!</p>
                    </div>

                    <div class="p-3 bg-blue-50 border border-blue-200 rounded-lg">
                        <p class="text-sm text-blue-800">
                            This link allows up to {{ shareSettings.maxJoins }} people to join your booking
                            and expires in {{ shareSettings.expiresInHours }} hours.
                        </p>
                    </div>
                </div>

                <div v-else class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Maximum Participants</label>
                        <input v-model.number="shareSettings.maxJoins" type="number" min="1" max="10"
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg" />
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Link Expires In (hours)</label>
                        <input v-model.number="shareSettings.expiresInHours" type="number" min="1" max="72"
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg" />
                    </div>

                    <button @click="createShareLink" :disabled="creatingShare"
                        class="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400">
                        {{ creatingShare ? 'Creating...' : 'Create Share Link' }}
                    </button>
                </div>

                <button @click="closeShareModal"
                    class="mt-4 w-full px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">
                    Close
                </button>
            </div>
        </div>

        <!-- Review Modal -->
        <div v-if="reviewModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div class="bg-white rounded-xl max-w-md w-full p-6">
                <h3 class="text-xl font-bold text-gray-900 mb-4">Leave a Review</h3>

                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Rating</label>
                        <div class="flex gap-2">
                            <button v-for="i in 5" :key="i" type="button" @click="reviewForm.rating = i"
                                class="w-10 h-10">
                                <svg class="w-full h-full"
                                    :class="i <= reviewForm.rating ? 'text-yellow-400' : 'text-gray-300'"
                                    fill="currentColor" viewBox="0 0 24 24">
                                    <path
                                        d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                                </svg>
                            </button>
                        </div>
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Your Review</label>
                        <textarea v-model="reviewForm.review_text" rows="4" placeholder="Share your experience..."
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg resize-none"></textarea>
                    </div>

                    <div class="flex gap-3">
                        <button @click="reviewModal = null"
                            class="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">
                            Cancel
                        </button>
                        <button @click="submitReview" :disabled="submittingReview || reviewForm.rating === 0"
                            class="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400">
                            {{ submittingReview ? 'Submitting...' : 'Submit Review' }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { bookingService } from '@/services/bookingService'
import { courtService } from '@/services/courtService'

const router = useRouter()
const loading = ref(false)
const error = ref(null)
const bookings = ref([])
const filterStatus = ref('all')
const cancelModal = ref(null)
const cancelReason = ref('')
const cancelling = ref(false)
const shareModal = ref(null)
const shareLink = ref('')
const linkCopied = ref(false)
const creatingShare = ref(false)
const shareSettings = ref({
    maxJoins: 5,
    expiresInHours: 24
})
const reviewModal = ref(null)
const reviewForm = ref({
    rating: 0,
    review_text: ''
})
const submittingReview = ref(false)

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

const formatDateTime = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit' })
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

const getPaymentStatusClass = (status) => {
    const classes = {
        'PENDING': 'text-yellow-600',
        'COMPLETED': 'text-green-600',
        'REFUNDED': 'text-blue-600',
        'FAILED': 'text-red-600',
    }
    return classes[status] || 'text-gray-600'
}

const canCancel = (booking) => {
    return ['PENDING', 'CONFIRMED'].includes(booking.status)
}

const canShare = (booking) => {
    return ['PENDING', 'CONFIRMED'].includes(booking.status)
}

const canReview = (booking) => {
    return booking.status === 'COMPLETED' && !booking.has_review
}

const loadBookings = async () => {
    loading.value = true
    error.value = null
    try {
        const response = await bookingService.getMyBookings()
        bookings.value = response.results || response
    } catch (err) {
        console.error('Failed to load bookings:', err)
        error.value = 'Failed to load bookings. Please try again.'
    } finally {
        loading.value = false
    }
}

const showCancelModal = (booking) => {
    cancelModal.value = booking
    cancelReason.value = ''
}

const confirmCancel = async () => {
    if (!cancelModal.value) return

    cancelling.value = true
    try {
        await bookingService.cancelBooking(cancelModal.value.id, cancelReason.value)
        await loadBookings()
        cancelModal.value = null
        cancelReason.value = ''
    } catch (err) {
        console.error('Failed to cancel booking:', err)
        alert('Failed to cancel booking. Please try again.')
    } finally {
        cancelling.value = false
    }
}

const shareBooking = (booking) => {
    shareModal.value = booking
    shareLink.value = ''
    linkCopied.value = false
}

const createShareLink = async () => {
    if (!shareModal.value) return

    creatingShare.value = true
    try {
        const response = await bookingService.createBookingShare(
            shareModal.value.id,
            shareSettings.value.maxJoins,
            shareSettings.value.expiresInHours
        )
        shareLink.value = `${window.location.origin}/bookings/join/${response.share_token}`
    } catch (err) {
        console.error('Failed to create share link:', err)
        alert('Failed to create share link. Please try again.')
    } finally {
        creatingShare.value = false
    }
}

const copyShareLink = () => {
    navigator.clipboard.writeText(shareLink.value)
    linkCopied.value = true
    setTimeout(() => {
        linkCopied.value = false
    }, 2000)
}

const closeShareModal = () => {
    shareModal.value = null
    shareLink.value = ''
    shareSettings.value = {
        maxJoins: 5,
        expiresInHours: 24
    }
}

const showReviewModal = (booking) => {
    reviewModal.value = booking
    reviewForm.value = {
        rating: 0,
        review_text: ''
    }
}

const submitReview = async () => {
    if (!reviewModal.value || reviewForm.value.rating === 0) return

    submittingReview.value = true
    try {
        await courtService.createReview(reviewModal.value.court.id, {
            rating: reviewForm.value.rating,
            review_text: reviewForm.value.review_text
        })
        await loadBookings()
        reviewModal.value = null
    } catch (err) {
        console.error('Failed to submit review:', err)
        alert('Failed to submit review. Please try again.')
    } finally {
        submittingReview.value = false
    }
}

const goBack = () => {
    router.go(-1)
}

onMounted(() => {
    loadBookings()
})
</script>