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
                        <h1 class="text-2xl font-bold text-blue-600">Booking Details</h1>
                    </div>
                </div>
            </div>
        </nav>

        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Loading -->
            <div v-if="loading" class="flex justify-center py-20">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>

            <!-- Error -->
            <div v-else-if="error" class="text-center py-20">
                <svg class="w-16 h-16 mx-auto text-red-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p class="text-xl text-gray-600 mb-4">{{ error }}</p>
                <button @click="loadBookingDetails"
                    class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Try Again</button>
            </div>

            <!-- Booking Details -->
            <div v-else-if="booking" class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <!-- Main Content -->
                <div class="lg:col-span-2 space-y-6">
                    <!-- Booking Header -->
                    <div class="bg-white rounded-xl shadow-md p-6">
                        <div class="flex items-start justify-between mb-6">
                            <div>
                                <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ booking.court?.name || 'Court' }}
                                </h2>
                                <p class="text-gray-600">{{ booking.court?.address || booking.court?.city }}</p>
                            </div>
                            <span :class="getStatusClass(booking.status)"
                                class="px-4 py-2 rounded-full text-sm font-medium">{{ booking.status }}</span>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                            <div class="flex items-center gap-3">
                                <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                                    <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor"
                                        viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                    </svg>
                                </div>
                                <div>
                                    <p class="text-sm text-gray-600">Date</p>
                                    <p class="font-medium text-gray-900">{{ formatDate(booking.booking_date) }}</p>
                                </div>
                            </div>

                            <div class="flex items-center gap-3">
                                <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                                    <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor"
                                        viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                </div>
                                <div>
                                    <p class="text-sm text-gray-600">Time</p>
                                    <p class="font-medium text-gray-900">{{ booking.start_time }} - {{ booking.end_time
                                        }}</p>
                                </div>
                            </div>

                            <div class="flex items-center gap-3">
                                <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                                    <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor"
                                        viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                </div>
                                <div>
                                    <p class="text-sm text-gray-600">Total Amount</p>
                                    <p class="font-medium text-gray-900">Rs {{ booking.total_amount }}</p>
                                </div>
                            </div>

                            <div class="flex items-center gap-3">
                                <div class="w-10 h-10 bg-amber-100 rounded-lg flex items-center justify-center">
                                    <svg class="w-5 h-5 text-amber-600" fill="none" stroke="currentColor"
                                        viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
                                    </svg>
                                </div>
                                <div>
                                    <p class="text-sm text-gray-600">Payment Status</p>
                                    <p :class="getPaymentStatusClass(booking.payment_status)" class="font-medium">{{
                                        booking.payment_status }}</p>
                                </div>
                            </div>
                        </div>

                        <div class="border-t pt-4">
                            <div class="flex items-center gap-2 text-sm text-gray-600">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                                </svg>
                                <span>Booking Reference: <span class="font-medium text-gray-900">{{
                                        booking.booking_reference }}</span></span>
                            </div>
                            <p class="text-xs text-gray-500 mt-2">Booked on {{ formatDateTime(booking.created_at) }}</p>
                        </div>
                    </div>

                    <!-- Court Information -->
                    <div class="bg-white rounded-xl shadow-md p-6">
                        <h3 class="text-lg font-bold text-gray-900 mb-4">Court Information</h3>
                        <div class="space-y-3">
                            <div class="flex items-start gap-3">
                                <svg class="w-5 h-5 text-gray-400 mt-0.5" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                                </svg>
                                <div>
                                    <p class="text-sm text-gray-600">Location</p>
                                    <p class="text-gray-900">{{ booking.court?.address }}, {{ booking.court?.city }}</p>
                                </div>
                            </div>
                            <div class="flex items-start gap-3">
                                <svg class="w-5 h-5 text-gray-400 mt-0.5" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                                </svg>
                                <div>
                                    <p class="text-sm text-gray-600">Court Type</p>
                                    <p class="text-gray-900">{{ booking.court?.is_indoor ? 'Indoor' : 'Outdoor' }} •
                                        Capacity: {{ booking.court?.capacity }}</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Equipment Rentals -->
                    <div v-if="booking.equipment_rentals && booking.equipment_rentals.length > 0"
                        class="bg-white rounded-xl shadow-md p-6">
                        <h3 class="text-lg font-bold text-gray-900 mb-4">Equipment Rentals</h3>
                        <div class="space-y-3">
                            <div v-for="rental in booking.equipment_rentals" :key="rental.id"
                                class="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                                <div class="flex items-center gap-3">
                                    <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                                        <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor"
                                            viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
                                        </svg>
                                    </div>
                                    <div>
                                        <p class="font-medium text-gray-900">{{ rental.equipment?.name }}</p>
                                        <p class="text-sm text-gray-600">Quantity: {{ rental.quantity }}</p>
                                    </div>
                                </div>
                                <p class="font-bold text-blue-600">Rs {{ rental.rental_cost }}</p>
                            </div>
                        </div>
                    </div>

                    <!-- Notes -->
                    <div v-if="booking.notes" class="bg-white rounded-xl shadow-md p-6">
                        <h3 class="text-lg font-bold text-gray-900 mb-4">Booking Notes</h3>
                        <p class="text-gray-700">{{ booking.notes }}</p>
                    </div>

                    <!-- Cancellation Info -->
                    <div v-if="booking.status === 'CANCELLED' && booking.cancellation_reason"
                        class="bg-red-50 border border-red-200 rounded-xl p-6">
                        <h3 class="text-lg font-bold text-red-900 mb-2">Cancellation Reason</h3>
                        <p class="text-red-700">{{ booking.cancellation_reason }}</p>
                        <p v-if="booking.cancelled_at" class="text-sm text-red-600 mt-2">Cancelled on {{
                            formatDateTime(booking.cancelled_at) }}</p>
                    </div>
                </div>

                <!-- Sidebar -->
                <div class="lg:col-span-1">
                    <div class="bg-white rounded-xl shadow-md p-6 sticky top-24 space-y-6">
                        <!-- Payment Summary -->
                        <div>
                            <h3 class="text-lg font-bold text-gray-900 mb-4">Payment Summary</h3>
                            <div class="space-y-3">
                                <div class="flex justify-between text-gray-600">
                                    <span>Base Amount</span>
                                    <span class="font-medium">Rs {{ booking.base_amount }}</span>
                                </div>
                                <div v-if="booking.equipment_rentals && booking.equipment_rentals.length > 0"
                                    class="flex justify-between text-gray-600">
                                    <span>Equipment Rental</span>
                                    <span class="font-medium">Rs {{ equipmentTotal }}</span>
                                </div>
                                <div class="border-t pt-3 flex justify-between font-bold text-gray-900">
                                    <span>Total</span>
                                    <span class="text-blue-600">Rs {{ booking.total_amount }}</span>
                                </div>
                                <div class="pt-3 border-t">
                                    <p class="text-sm text-gray-600">Payment Method</p>
                                    <p class="font-medium text-gray-900">{{ booking.payment_method }}</p>
                                </div>
                            </div>
                        </div>

                        <!-- Actions -->
                        <div class="space-y-3">
                            <button v-if="canShare" @click="shareBooking"
                                class="w-full py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors font-medium flex items-center justify-center gap-2">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                                </svg>
                                Share Booking
                            </button>

                            <button v-if="canCancel" @click="showCancelModal = true"
                                class="w-full py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium flex items-center justify-center gap-2">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M6 18L18 6M6 6l12 12" />
                                </svg>
                                Cancel Booking
                            </button>

                            <button v-if="canReview" @click="showReviewModal = true"
                                class="w-full py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium flex items-center justify-center gap-2">
                                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                    <path
                                        d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                                </svg>
                                Leave Review
                            </button>

                            <button @click="goToBookings"
                                class="w-full py-3 border-2 border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 transition-colors font-medium">
                                View All Bookings
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Cancel Modal -->
        <div v-if="showCancelModal"
            class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div class="bg-white rounded-xl max-w-md w-full p-6">
                <h3 class="text-xl font-bold text-gray-900 mb-4">Cancel Booking</h3>
                <p class="text-gray-600 mb-4">Are you sure you want to cancel this booking?</p>
                <textarea v-model="cancelReason" placeholder="Reason for cancellation (optional)"
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg mb-4" rows="3"></textarea>
                <div class="flex gap-3">
                    <button @click="showCancelModal = false"
                        class="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">Keep
                        Booking</button>
                    <button @click="confirmCancel" :disabled="cancelling"
                        class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:bg-gray-400">
                        {{ cancelling ? 'Cancelling...' : 'Cancel Booking' }}
                    </button>
                </div>
            </div>
        </div>

        <!-- Share Modal -->
        <div v-if="showShareModal"
            class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div class="bg-white rounded-xl max-w-md w-full p-6">
                <h3 class="text-xl font-bold text-gray-900 mb-4">Share Booking</h3>

                <div v-if="shareLink" class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Share Link</label>
                        <div class="flex gap-2">
                            <input :value="shareLink" readonly
                                class="flex-1 px-4 py-2 border border-gray-300 rounded-lg bg-gray-50" />
                            <button @click="copyShareLink"
                                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Copy</button>
                        </div>
                        <p v-if="linkCopied" class="text-sm text-green-600 mt-1">Link copied!</p>
                    </div>

                    <div class="p-3 bg-blue-50 border border-blue-200 rounded-lg">
                        <p class="text-sm text-blue-800">
                            This link allows up to {{ shareSettings.maxJoins }} people to join your booking and expires
                            in {{ shareSettings.expiresInHours }} hours.
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
                    class="mt-4 w-full px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">Close</button>
            </div>
        </div>

        <!-- Review Modal -->
        <div v-if="showReviewModal"
            class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
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
                        <button @click="showReviewModal = false"
                            class="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">Cancel</button>
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
import { useRoute, useRouter } from 'vue-router'
import { bookingService } from '@/services/bookingService'
import { courtService } from '@/services/courtService'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const error = ref(null)
const booking = ref(null)
const showCancelModal = ref(false)
const cancelReason = ref('')
const cancelling = ref(false)
const showShareModal = ref(false)
const shareLink = ref('')
const linkCopied = ref(false)
const creatingShare = ref(false)
const shareSettings = ref({ maxJoins: 5, expiresInHours: 24 })
const showReviewModal = ref(false)
const reviewForm = ref({ rating: 0, review_text: '' })
const submittingReview = ref(false)

const equipmentTotal = computed(() => {
    if (!booking.value?.equipment_rentals) return 0
    return booking.value.equipment_rentals.reduce((sum, rental) => sum + parseFloat(rental.rental_cost), 0).toFixed(2)
})

const canCancel = computed(() => booking.value && ['PENDING', 'CONFIRMED'].includes(booking.value.status))
const canShare = computed(() => booking.value && ['PENDING', 'CONFIRMED'].includes(booking.value.status))
const canReview = computed(() => booking.value && booking.value.status === 'COMPLETED' && !booking.value.has_review)

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
        'NO_SHOW': 'bg-gray-100 text-gray-800'
    }
    return classes[status] || 'bg-gray-100 text-gray-800'
}

const getPaymentStatusClass = (status) => {
    const classes = {
        'PENDING': 'text-yellow-600',
        'COMPLETED': 'text-green-600',
        'REFUNDED': 'text-blue-600',
        'FAILED': 'text-red-600'
    }
    return classes[status] || 'text-gray-600'
}

const loadBookingDetails = async () => {
    loading.value = true
    error.value = null
    try {
        booking.value = await bookingService.getBookingById(route.params.id)
    } catch (err) {
        console.error('Failed to load booking:', err)
        error.value = 'Failed to load booking details'
    } finally {
        loading.value = false
    }
}

const confirmCancel = async () => {
    cancelling.value = true
    try {
        await bookingService.cancelBooking(booking.value.id, cancelReason.value)
        await loadBookingDetails()
        showCancelModal.value = false
        cancelReason.value = ''
    } catch (err) {
        console.error('Failed to cancel booking:', err)
        alert('Failed to cancel booking. Please try again.')
    } finally {
        cancelling.value = false
    }
}

const shareBooking = () => {
    showShareModal.value = true
    shareLink.value = ''
    linkCopied.value = false
}

const createShareLink = async () => {
    creatingShare.value = true
    try {
        const response = await bookingService.createBookingShare(
            booking.value.id,
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
    setTimeout(() => { linkCopied.value = false }, 2000)
}

const closeShareModal = () => {
    showShareModal.value = false
    shareLink.value = ''
    shareSettings.value = { maxJoins: 5, expiresInHours: 24 }
}

const submitReview = async () => {
    submittingReview.value = true
    try {
        await courtService.createReview(booking.value.court.id, {
            rating: reviewForm.value.rating,
            review_text: reviewForm.value.review_text
        })
        showReviewModal.value = false
        reviewForm.value = { rating: 0, review_text: '' }
        await loadBookingDetails()
    } catch (err) {
        console.error('Failed to submit review:', err)
        alert('Failed to submit review. Please try again.')
    } finally {
        submittingReview.value = false
    }
}

const goBack = () => router.go(-1)
const goToBookings = () => router.push('/bookings')

onMounted(() => {
    loadBookingDetails()
})
</script>