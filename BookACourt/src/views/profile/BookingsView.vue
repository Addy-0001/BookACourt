<template>
    <div class="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
            <!-- Header + Filters -->
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-6 mb-10">
                <div>
                    <h1 class="text-3xl sm:text-4xl font-bold text-gray-900">My Bookings</h1>
                    <p class="mt-2 text-lg text-gray-600">Manage your upcoming games and past reservations</p>
                </div>

                <div class="flex flex-wrap gap-3">
                    <button v-for="status in statuses" :key="status.value" @click="filterStatus = status.value" :class="[
                        'px-5 py-2.5 rounded-xl font-medium transition-all shadow-sm text-sm sm:text-base',
                        filterStatus === status.value
                            ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md'
                            : 'bg-white border border-gray-300 text-gray-700 hover:bg-emerald-50 hover:border-emerald-400'
                    ]">
                        {{ status.label }}
                    </button>
                </div>
            </div>

            <!-- Loading State -->
            <div v-if="loading" class="flex justify-center py-32">
                <div class="w-14 h-14 border-4 border-emerald-200 border-t-emerald-600 rounded-full animate-spin"></div>
            </div>

            <!-- Error State -->
            <div v-else-if="error" class="text-center py-20">
                <svg class="w-20 h-20 mx-auto text-red-500 mb-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p class="text-xl text-gray-700 font-medium mb-6">{{ error }}</p>
                <button @click="loadBookings"
                    class="px-8 py-4 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white rounded-xl font-semibold shadow-md hover:shadow-lg transition-all">
                    Try Again
                </button>
            </div>

            <!-- Bookings List -->
            <div v-else-if="filteredBookings.length > 0" class="space-y-6">
                <div v-for="booking in filteredBookings" :key="booking.id"
                    class="bg-white rounded-2xl shadow-md border border-gray-100 p-6 md:p-8 hover:shadow-xl transition-all duration-300">
                    <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-6 mb-6">
                        <div>
                            <h3 class="text-2xl font-bold text-gray-900 mb-2">
                                {{ booking.court?.name || 'Court Booking' }}
                            </h3>
                            <p class="text-gray-600 mb-1">{{ booking.court?.address || booking.court?.city || 'Location'
                            }}</p>
                            <p class="text-sm text-gray-500">
                                Ref: <span class="font-mono font-medium">{{ booking.booking_reference }}</span>
                            </p>
                        </div>

                        <span :class="getStatusClass(booking.status)"
                            class="inline-flex px-5 py-2 rounded-full text-sm font-semibold self-start whitespace-nowrap">
                            {{ booking.status }}
                        </span>
                    </div>

                    <!-- Details Grid -->
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                        <div class="flex items-center gap-3">
                            <div
                                class="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center flex-shrink-0">
                                <svg class="w-6 h-6 text-emerald-600" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                </svg>
                            </div>
                            <div>
                                <p class="text-sm text-gray-600">Date</p>
                                <p class="font-semibold text-gray-900">{{ formatDate(booking.booking_date) }}</p>
                            </div>
                        </div>

                        <div class="flex items-center gap-3">
                            <div
                                class="w-12 h-12 bg-teal-100 rounded-xl flex items-center justify-center flex-shrink-0">
                                <svg class="w-6 h-6 text-teal-600" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                            </div>
                            <div>
                                <p class="text-sm text-gray-600">Time Slot</p>
                                <p class="font-semibold text-gray-900">{{ booking.start_time }} – {{ booking.end_time }}
                                </p>
                            </div>
                        </div>

                        <div class="flex items-center gap-3">
                            <div
                                class="w-12 h-12 bg-amber-100 rounded-xl flex items-center justify-center flex-shrink-0">
                                <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                                </svg>
                            </div>
                            <div>
                                <p class="text-sm text-gray-600">Total Amount</p>
                                <p class="font-bold text-emerald-700 text-xl">Rs {{ booking.total_amount }}</p>
                            </div>
                        </div>
                    </div>

                    <!-- Payment Info -->
                    <div class="flex flex-wrap items-center gap-x-6 gap-y-2 text-sm mb-6">
                        <div>
                            <span class="font-medium text-gray-700">Payment Method:</span>
                            <span class="ml-1.5">{{ booking.payment_method || '—' }}</span>
                        </div>
                        <div>
                            <span class="font-medium text-gray-700">Payment Status:</span>
                            <span :class="getPaymentStatusClass(booking.payment_status)" class="ml-1.5 font-semibold">
                                {{ booking.payment_status || '—' }}
                            </span>
                        </div>
                    </div>

                    <!-- Action Buttons -->
                    <div class="flex flex-wrap gap-4">
                        <button v-if="canCancel(booking)" @click="showCancelModal(booking)"
                            class="px-6 py-3 bg-red-50 hover:bg-red-100 text-red-700 rounded-xl font-medium transition-colors flex items-center gap-2 border border-red-200">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M6 18L18 6M6 6l12 12" />
                            </svg>
                            Cancel Booking
                        </button>

                        <button v-if="canShare(booking)" @click="shareBooking(booking)"
                            class="px-6 py-3 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 rounded-xl font-medium transition-colors flex items-center gap-2 border border-emerald-200">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
                            </svg>
                            Share Booking
                        </button>

                        <button v-if="canReview(booking)" @click="showReviewModal(booking)"
                            class="px-6 py-3 bg-amber-50 hover:bg-amber-100 text-amber-700 rounded-xl font-medium transition-colors flex items-center gap-2 border border-amber-200">
                            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                <path
                                    d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                            </svg>
                            Leave Review
                        </button>
                    </div>
                </div>
            </div>

            <!-- Empty State -->
            <div v-else class="text-center py-32">
                <div class="inline-block p-12 bg-white rounded-2xl shadow-xl border border-emerald-100">
                    <svg class="w-24 h-24 mx-auto text-emerald-400 mb-6" fill="none" stroke="currentColor"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <h3 class="text-2xl sm:text-3xl font-bold text-gray-900 mb-4">
                        {{ filterStatus === 'all' ? 'No bookings yet' : `No ${filterStatus.toLowerCase()} bookings` }}
                    </h3>
                    <p class="text-lg text-gray-600 mb-8 max-w-md mx-auto">
                        {{ filterStatus === 'all'
                            ? 'Start exploring courts and make your first booking!'
                            : 'No bookings match the selected filter' }}
                    </p>

                    <router-link to="/courts"
                        class="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all">
                        Find & Book a Court
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M17 8l4 4m0 0l-4 4m4-4H3" />
                        </svg>
                    </router-link>
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
    { value: 'all', label: 'All Bookings' },
    { value: 'PENDING', label: 'Pending' },
    { value: 'CONFIRMED', label: 'Confirmed' },
    { value: 'COMPLETED', label: 'Completed' },
    { value: 'CANCELLED', label: 'Cancelled' },
]

const filteredBookings = computed(() => {
    if (filterStatus.value === 'all') return bookings.value
    return bookings.value.filter(b => b.status === filterStatus.value)
})

const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
        weekday: 'short',
        month: 'short',
        day: 'numeric',
        year: 'numeric'
    })
}

const getStatusClass = (status) => {
    const classes = {
        'PENDING': 'bg-amber-100 text-amber-800',
        'CONFIRMED': 'bg-emerald-100 text-emerald-800',
        'CANCELLED': 'bg-red-100 text-red-800',
        'COMPLETED': 'bg-blue-100 text-blue-800',
        'NO_SHOW': 'bg-gray-100 text-gray-800',
    }
    return classes[status] || 'bg-gray-100 text-gray-800'
}

const getPaymentStatusClass = (status) => {
    const classes = {
        'PENDING': 'text-amber-600 font-medium',
        'COMPLETED': 'text-emerald-600 font-medium',
        'REFUNDED': 'text-teal-600 font-medium',
        'FAILED': 'text-red-600 font-medium',
    }
    return classes[status] || 'text-gray-600'
}

const canCancel = (booking) => ['PENDING', 'CONFIRMED'].includes(booking.status)
const canShare = (booking) => ['PENDING', 'CONFIRMED'].includes(booking.status)
const canReview = (booking) => booking.status === 'COMPLETED' && !booking.has_review

const loadBookings = async () => {
    loading.value = true
    error.value = null
    try {
        const response = await bookingService.getMyBookings()
        bookings.value = response.results || response
    } catch (err) {
        console.error('Failed to load bookings:', err)
        error.value = 'Failed to load your bookings. Please try again later.'
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