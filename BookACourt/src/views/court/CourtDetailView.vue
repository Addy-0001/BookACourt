<template>
    <div class="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50">
        <!-- Back Button -->
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6">
            <button @click="goBack"
                class="inline-flex items-center gap-2 text-gray-600 hover:text-emerald-700 font-medium">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
                Back
            </button>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="flex justify-center py-20">
            <div class="w-14 h-14 border-4 border-emerald-200 border-t-emerald-600 rounded-full animate-spin"></div>
        </div>

        <!-- Error -->
        <div v-else-if="error" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center">
            <svg class="w-16 h-16 mx-auto text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p class="mt-4 text-xl text-gray-600">{{ error }}</p>
        </div>

        <!-- Court Details -->
        <div v-else-if="court">
            <!-- Hero Image with Overlay -->
            <div class="relative h-96 overflow-hidden">
                <img v-if="court.images && court.images.length > 0" :src="court.images[currentImageIndex].image"
                    :alt="court.name" class="w-full h-full object-cover" />
                <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
                <div class="absolute bottom-0 left-0 right-0 p-8 text-white">
                    <h1 class="text-4xl font-bold mb-2">{{ court.name }}</h1>
                    <p class="flex items-center gap-2 text-lg">
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd"
                                d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z"
                                clip-rule="evenodd" />
                        </svg>
                        {{ court.city }}
                    </p>
                </div>

                <!-- Image indicators -->
                <div v-if="court.images?.length > 1" class="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2">
                    <button v-for="(img, idx) in court.images" :key="idx" @click="currentImageIndex = idx"
                        class="w-3 h-3 rounded-full bg-white/50 transition-all hover:bg-white"
                        :class="{ 'bg-white scale-110': idx === currentImageIndex }" />
                </div>
            </div>

            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <!-- Main Content -->
                    <div class="lg:col-span-2 space-y-8">
                        <!-- About Section -->
                        <div class="bg-white rounded-2xl shadow-md p-8 border border-emerald-100">
                            <h2 class="text-2xl font-bold text-gray-900 mb-6">
                                About This {{ court.category?.name || court.court_type }} Court
                            </h2>
                            <p class="text-gray-600 mb-8 leading-relaxed">{{ court.description }}</p>

                            <!-- Amenities -->
                            <div v-if="court.amenities_list?.length" class="mb-8">
                                <h3 class="text-xl font-bold text-gray-900 mb-4">Features & Amenities</h3>
                                <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
                                    <div v-for="amenity in court.amenities_list.slice(0, 6)" :key="amenity"
                                        class="flex items-center gap-3 bg-emerald-50 p-4 rounded-xl">
                                        <svg class="w-5 h-5 text-emerald-600" fill="currentColor" viewBox="0 0 20 20">
                                            <path fill-rule="evenodd"
                                                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                                clip-rule="evenodd" />
                                        </svg>
                                        <span class="font-medium text-gray-800">{{ amenity }}</span>
                                    </div>
                                </div>
                            </div>

                            <!-- Meta Info -->
                            <div class="grid grid-cols-3 gap-6 text-center">
                                <div class="p-4 bg-gray-50 rounded-xl">
                                    <p class="text-sm font-semibold text-gray-600">Type</p>
                                    <p class="mt-1 font-bold text-gray-900">{{ court.is_indoor ? 'Indoor' : 'Outdoor' }}
                                    </p>
                                </div>
                                <div class="p-4 bg-gray-50 rounded-xl">
                                    <p class="text-sm font-semibold text-gray-600">Capacity</p>
                                    <p class="mt-1 font-bold text-gray-900">{{ court.capacity }} players</p>
                                </div>
                                <div class="p-4 bg-gray-50 rounded-xl">
                                    <p class="text-sm font-semibold text-gray-600">Hours</p>
                                    <p class="mt-1 font-bold text-gray-900">
                                        {{ court.opening_time }} - {{ court.closing_time }}
                                    </p>
                                </div>
                            </div>

                            <!-- Rating -->
                            <div v-if="court.average_rating" class="mt-8 flex items-center gap-3">
                                <div class="flex">
                                    <svg v-for="i in 5" :key="i" class="w-6 h-6"
                                        :class="i <= Math.round(court.average_rating) ? 'text-amber-400 fill-current' : 'text-gray-300 fill-current'"
                                        viewBox="0 0 24 24">
                                        <path
                                            d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                                    </svg>
                                </div>
                                <span class="font-bold text-xl text-gray-900">{{ court.average_rating }}</span>
                                <span class="text-gray-600">({{ court.total_reviews || 0 }} reviews)</span>
                            </div>
                        </div>

                        <!-- Reviews Section -->
                        <div class="bg-white rounded-2xl shadow-md p-8 border border-emerald-100">
                            <div class="flex items-center justify-between mb-6">
                                <h2 class="text-2xl font-bold text-gray-900">Reviews</h2>
                                <button v-if="canReview" @click="showReviewModal = true"
                                    class="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-medium transition-colors">
                                    {{ userReview ? 'Edit Review' : 'Write Review' }}
                                </button>
                            </div>

                            <div v-if="reviews.length > 0" class="space-y-8">
                                <div v-for="review in reviews.slice(0, 3)" :key="review.id"
                                    class="border-b border-gray-200 pb-6 last:border-b-0 last:pb-0">
                                    <div class="flex justify-between items-start mb-4">
                                        <div class="flex gap-4">
                                            <div
                                                class="w-12 h-12 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-full flex items-center justify-center text-white font-bold text-xl shrink-0">
                                                {{ review.player_name.charAt(0).toUpperCase() }}
                                            </div>
                                            <div>
                                                <p class="font-bold text-gray-900">{{ review.player_name }}</p>
                                                <p class="text-sm text-gray-500 mt-1">{{ formatDate(review.created_at)
                                                }}</p>
                                            </div>
                                        </div>
                                        <div class="flex">
                                            <svg v-for="i in 5" :key="i" class="w-5 h-5"
                                                :class="i <= review.rating ? 'text-amber-400 fill-current' : 'text-gray-300 fill-current'"
                                                viewBox="0 0 24 24">
                                                <path
                                                    d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                                            </svg>
                                        </div>
                                    </div>
                                    <p class="text-gray-700 italic leading-relaxed">“{{ review.review_text }}”</p>
                                </div>
                            </div>

                            <p v-else class="text-center text-gray-600 py-8">
                                No reviews yet. Be the first to share your experience!
                            </p>
                        </div>
                    </div>

                    <!-- Booking Sidebar -->
                    <div class="lg:col-span-1">
                        <div class="sticky top-24 bg-white rounded-2xl shadow-xl p-8 border border-emerald-100">
                            <div class="text-center mb-8">
                                <p class="text-4xl font-bold text-emerald-700">
                                    ${{ displayRate }}
                                    <span class="text-xl font-normal text-gray-500">/hr</span>
                                </p>
                            </div>

                            <div v-if="bookingSuccess"
                                class="p-4 bg-emerald-50 border border-emerald-200 rounded-xl text-emerald-700 font-medium mb-6">
                                Booking created successfully! Redirecting...
                            </div>

                            <div v-if="bookingError"
                                class="p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 font-medium mb-6">
                                {{ bookingError }}
                            </div>

                            <form @submit.prevent="handleBooking" class="space-y-6">
                                <!-- Date -->
                                <div class="space-y-2">
                                    <label class="block text-sm font-semibold text-gray-700">Select Date</label>
                                    <input v-model="bookingForm.date" type="date" :min="minDate" required
                                        class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                                        @change="onDateOrTimeChange" />
                                </div>

                                <!-- Time Slots or Manual Input -->
                                <div v-if="bookingForm.date" class="space-y-4">
                                    <label class="block text-sm font-semibold text-gray-700">Time Slots</label>

                                    <div v-if="availableSlots.length || unavailableSlots.length"
                                        class="grid grid-cols-2 gap-3 max-h-64 overflow-y-auto p-4 bg-gray-50 rounded-xl border border-gray-200">
                                        <button v-for="slot in availableSlots" :key="slot.start_time" type="button"
                                            @click="toggleTimeSlot(slot)" :class="[
                                                'py-3 px-4 rounded-lg text-sm font-medium transition-all',
                                                isSlotSelected(slot)
                                                    ? 'bg-emerald-600 text-white shadow-md'
                                                    : 'bg-white border border-gray-300 hover:bg-emerald-50 hover:border-emerald-400 hover:text-emerald-700'
                                            ]">
                                            {{ slot.start_time }} – {{ slot.end_time }}
                                        </button>

                                        <button v-for="slot in unavailableSlots" :key="'unavail-' + slot.start_time"
                                            type="button" disabled
                                            class="py-3 px-4 rounded-lg bg-gray-100 text-gray-500 text-sm font-medium cursor-not-allowed opacity-70">
                                            {{ slot.start_time }} – {{ slot.end_time }}
                                            <span class="block text-xs text-gray-400 mt-1">Booked</span>
                                        </button>
                                    </div>

                                    <!-- Fallback manual time input -->
                                    <div v-else class="grid grid-cols-2 gap-4">
                                        <div class="space-y-2">
                                            <label class="block text-sm font-semibold text-gray-700">Start</label>
                                            <input v-model="bookingForm.start_time" type="time" required
                                                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                                                @change="onDateOrTimeChange" />
                                        </div>
                                        <div class="space-y-2">
                                            <label class="block text-sm font-semibold text-gray-700">End</label>
                                            <input v-model="bookingForm.end_time" type="time" required
                                                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                                                @change="onDateOrTimeChange" />
                                        </div>
                                    </div>
                                </div>

                                <!-- Total & Book Button -->
                                <button type="submit" :disabled="bookingLoading || !canBook"
                                    class="w-full py-4 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white rounded-xl font-bold shadow-lg hover:shadow-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed">
                                    {{ bookingLoading ? 'Processing...' : 'Book Now' }}
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { courtService } from '@/services/courtService'
import { bookingService } from '@/services/bookingService'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const loading = ref(true)
const error = ref(null)
const court = ref(null)
const reviews = ref([])
const availableSlots = ref([])
const unavailableSlots = ref([])
const selectedSlots = ref([])
const currentImageIndex = ref(0)

const bookingForm = ref({
    date: new Date().toISOString().split('T')[0],
    start_time: '',
    end_time: '',
    notes: '',
    equipment_rentals: []
})

const bookingLoading = ref(false)
const bookingSuccess = ref(false)
const bookingError = ref(null)
const availabilityLoading = ref(false)
const availabilityMessage = ref(null)
const isAvailable = ref(false)

const showReviewModal = ref(false)
const submittingReview = ref(false)
const reviewForm = ref({
    rating: 0,
    review_text: ''
})

const minDate = computed(() => {
    const today = new Date()
    return today.toISOString().split('T')[0]
})

const totalDuration = computed(() => {
    if (selectedSlots.value.length === 0) return 0

    return selectedSlots.value.reduce((total, slot) => {
        const start = new Date(`2000-01-01 ${slot.start_time}`)
        const end = new Date(`2000-01-01 ${slot.end_time}`)
        const hours = Math.max(0, (end - start) / (1000 * 60 * 60))
        return total + hours
    }, 0)
})

// Calculate duration in hours (for backwards compatibility)
const duration = computed(() => {
    if (selectedSlots.value.length > 0) {
        return totalDuration.value
    }
    if (!bookingForm.value.start_time || !bookingForm.value.end_time) return 0
    const start = new Date(`2000-01-01 ${bookingForm.value.start_time}`)
    const end = new Date(`2000-01-01 ${bookingForm.value.end_time}`)
    const hours = Math.max(0, (end - start) / (1000 * 60 * 60))
    return hours
})

// Find applicable pricing rule based on date and time
const applicablePricingRule = computed(() => {
    if (!court.value || !bookingForm.value.date) {
        return null
    }

    const dayOfWeek = new Date(bookingForm.value.date).getDay()
    const startTime = selectedSlots.value.length > 0 ? selectedSlots.value[0].start_time : bookingForm.value.start_time

    if (!startTime) return null

    // Find matching pricing rule
    const matchingRule = court.value.pricing_rules?.find(rule => {
        if (!rule.is_active) return false

        // Parse days of week
        const days = rule.days_of_week.split(',').map(d => parseInt(d.trim()))
        if (!days.includes(dayOfWeek)) return false

        // Check if time falls within rule's time range
        return startTime >= rule.start_time && startTime < rule.end_time
    })

    return matchingRule
})

// Get current hourly rate based on pricing rules
const currentRate = computed(() => {
    if (!court.value) return 0

    const rule = applicablePricingRule.value
    return rule ? parseFloat(rule.hourly_rate) : parseFloat(court.value.base_hourly_rate)
})

// Display rate with proper formatting
const displayRate = computed(() => {
    return currentRate.value.toFixed(2)
})

// Description of the rate being applied
const rateDescription = computed(() => {
    if (!court.value) return 'Base rate'

    const rule = applicablePricingRule.value
    if (rule) {
        return rule.description
    }

    return 'Base rate'
})

// Calculate court fee based on duration and current rate
const courtFee = computed(() => {
    const fee = totalDuration.value * currentRate.value
    return fee
})

// Calculate equipment rental fees
const equipmentFee = computed(() => {
    if (!court.value || !bookingForm.value.equipment_rentals.length) return 0
    const total = bookingForm.value.equipment_rentals.reduce((sum, equipId) => {
        const item = court.value.equipment?.find(e => e.id === equipId)
        return sum + (item ? parseFloat(item.rental_rate) : 0)
    }, 0)
    return total
})

// Calculate total estimated cost
const estimatedTotal = computed(() => {
    const total = courtFee.value + equipmentFee.value
    return total
})

// For display purposes
const courtFeeDisplay = computed(() => courtFee.value.toFixed(2))
const equipmentFeeDisplay = computed(() => equipmentFee.value.toFixed(2))
const estimatedTotalDisplay = computed(() => estimatedTotal.value.toFixed(2))

// Check if booking form is valid
const canBook = computed(() => {
    return bookingForm.value.date && selectedSlots.value.length > 0 && totalDuration.value > 0
})

// Find user's existing review
const userReview = computed(() => {
    return reviews.value.find(r => r.player === authStore.user?.id)
})

// Check if user can write a review
const canReview = computed(() => {
    return authStore.isAuthenticated && authStore.isPlayer
})

// Format date for display
const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

// Format days of week from comma-separated string
const formatDaysOfWeek = (daysStr) => {
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    const indices = daysStr.split(',').map(d => parseInt(d.trim()))
    return indices.map(i => days[i]).join(', ')
}

// Handle date or time change
const onDateOrTimeChange = () => {
    // Clear availability message when inputs change
    availabilityMessage.value = null
    isAvailable.value = false
    selectedSlots.value = []

    // Load available slots if date is selected
    if (bookingForm.value.date) {
        loadAvailableSlots()
    }
}

// Load court details
const loadCourtDetails = async () => {
    loading.value = true
    error.value = null
    try {
        court.value = await courtService.getCourtById(route.params.id)
        await loadReviews()
        if (bookingForm.value.date) {
            await loadAvailableSlots()
        }
    } catch (err) {
        console.error('Failed to load court:', err)
        error.value = 'Failed to load court details'
    } finally {
        loading.value = false
    }
}

// Load court reviews
const loadReviews = async () => {
    try {
        const response = await courtService.getCourtReviews(route.params.id)
        reviews.value = response.results || response
    } catch (err) {
        console.error('Failed to load reviews:', err)
    }
}

const loadAvailableSlots = async () => {
    if (!bookingForm.value.date) return

    try {
        const response = await courtService.getAvailableSlots(route.params.id, bookingForm.value.date)
        availableSlots.value = response.available_slots || []
        unavailableSlots.value = response.unavailable_slots || []
    } catch (err) {
        console.error('Failed to load available slots:', err)
        availableSlots.value = []
        unavailableSlots.value = []
    }
}

const toggleTimeSlot = (slot) => {
    const index = selectedSlots.value.findIndex(s =>
        s.start_time === slot.start_time && s.end_time === slot.end_time
    )

    if (index > -1) {
        selectedSlots.value.splice(index, 1)
    } else {
        selectedSlots.value.push(slot)
        // Sort by start time
        selectedSlots.value.sort((a, b) => a.start_time.localeCompare(b.start_time))
    }

    availabilityMessage.value = null
    isAvailable.value = false
}

// Check if a slot is currently selected
const isSlotSelected = (slot) => {
    return selectedSlots.value.some(s =>
        s.start_time === slot.start_time && s.end_time === slot.end_time
    )
}

// Check court availability
const checkAvailability = async () => {
    if (selectedSlots.value.length === 0) return

    availabilityLoading.value = true
    availabilityMessage.value = null
    try {
        // Check all selected slots
        for (const slot of selectedSlots.value) {
            const response = await courtService.checkAvailability(route.params.id, {
                date: bookingForm.value.date,
                start_time: slot.start_time,
                end_time: slot.end_time
            })

            if (!response.available) {
                isAvailable.value = false
                availabilityMessage.value = `Slot ${slot.start_time}-${slot.end_time} is not available: ${response.reason || response.message}`
                return
            }
        }

        isAvailable.value = true
        availabilityMessage.value = 'All selected slots are available!'
    } catch (err) {
        availabilityMessage.value = 'Failed to check availability'
        isAvailable.value = false
    } finally {
        availabilityLoading.value = false
    }
}

const handleBooking = async () => {
    if (selectedSlots.value.length === 0) {
        bookingError.value = 'Please select at least one time slot'
        return
    }

    bookingLoading.value = true
    bookingError.value = null
    bookingSuccess.value = false

    try {
        // Create bookings for each selected slot
        for (const slot of selectedSlots.value) {
            const slotDuration = (() => {
                const start = new Date(`2000-01-01 ${slot.start_time}`)
                const end = new Date(`2000-01-01 ${slot.end_time}`)
                return (end - start) / (1000 * 60 * 60)
            })()

            const slotCourtFee = slotDuration * currentRate.value
            const slotTotal = slotCourtFee + equipmentFee.value

            const bookingData = {
                court: parseInt(route.params.id),
                booking_date: bookingForm.value.date,
                start_time: slot.start_time,
                end_time: slot.end_time,
                payment_method: 'ONLINE',
                base_amount: slotCourtFee.toFixed(2),
                total_amount: slotTotal.toFixed(2),
                notes: bookingForm.value.notes || ''
            }

            const booking = await bookingService.createBooking(bookingData)

            // Handle equipment rentals for first booking only
            if (bookingForm.value.equipment_rentals.length > 0 && selectedSlots.value[0] === slot) {
                for (const equipId of bookingForm.value.equipment_rentals) {
                    await bookingService.rentEquipment(booking.id, equipId, 1)
                }
            }
        }

        bookingSuccess.value = true
        setTimeout(() => {
            router.push('/bookings')
        }, 2000)
    } catch (err) {
        console.error('Booking failed:', err)
        console.error('Error response:', err.response?.data)
        bookingError.value = err.response?.data?.detail || err.response?.data?.message || 'Failed to create booking'
    } finally {
        bookingLoading.value = false
    }
}

// Close review modal
const closeReviewModal = () => {
    showReviewModal.value = false
    reviewForm.value = {
        rating: 0,
        review_text: ''
    }
}

// Submit review
const submitReview = async () => {
    submittingReview.value = true
    try {
        if (userReview.value) {
            // Update existing review
            await courtService.updateReview(route.params.id, userReview.value.id, {
                rating: reviewForm.value.rating,
                review_text: reviewForm.value.review_text
            })
        } else {
            // Create new review
            await courtService.createReview(route.params.id, {
                rating: reviewForm.value.rating,
                review_text: reviewForm.value.review_text
            })
        }
        await loadReviews()
        closeReviewModal()
    } catch (err) {
        console.error('Failed to submit review:', err)
        alert('Failed to submit review. Please try again.')
    } finally {
        submittingReview.value = false
    }
}

// Go back to previous page
const goBack = () => router.go(-1)

// Watch for review modal opening to populate form with existing review
watch(showReviewModal, (newVal) => {
    if (newVal && userReview.value) {
        reviewForm.value = {
            rating: userReview.value.rating,
            review_text: userReview.value.review_text
        }
    }
})

// Load court details on mount
onMounted(() => {
    loadCourtDetails()
})
</script>

<style scoped>
/* Updated color scheme to green/sporty theme */
:root {
    --primary-green: #10B981;
    --dark-green: #059669;
    --light-green: #D1FAE5;
    --charcoal: #1F2937;
    --muted: #6B7280;
    --light-gray: #F3F4F6;
}

.court-detail-page {
    min-height: 100vh;
    background: #FFFFFF;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1.5rem;
}

/* Back button styling */
.back-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    background: none;
    border: none;
    color: var(--charcoal);
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 1rem;
}

.back-button:hover {
    color: var(--primary-green);
    transform: translateX(-4px);
}

.back-button .icon {
    width: 1.25rem;
    height: 1.25rem;
}

/* Loading & Error */
.loading-container {
    display: flex;
    justify-content: center;
    padding: 5rem 0;
}

.spinner {
    width: 3rem;
    height: 3rem;
    border: 3px solid #e5e7eb;
    border-top-color: var(--primary-green);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

.error-container {
    text-align: center;
    padding: 5rem 0;
}

.error-icon {
    width: 4rem;
    height: 4rem;
    margin: 0 auto 1rem;
    color: #EF4444;
}

.hero-section {
    height: 28rem;
    position: relative;
    overflow: hidden;
    margin-bottom: 2rem;
}

.hero-image-container {
    position: relative;
    width: 100%;
    height: 100%;
}

.hero-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.hero-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.1));
}

.hero-content {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 2rem;
    color: white;
}

.hero-title {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.hero-location {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.125rem;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.location-icon {
    width: 1.25rem;
    height: 1.25rem;
}

.image-indicators {
    position: absolute;
    bottom: 1rem;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 0.5rem;
}

.indicator {
    width: 0.75rem;
    height: 0.75rem;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.5);
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
}

.indicator.active {
    background: white;
    transform: scale(1.2);
}


.content-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin-bottom: 3rem;
}

@media (max-width: 1024px) {
    .content-grid {
        grid-template-columns: 1fr;
    }
}

/* Cards */
.card {
    background: white;
    border-radius: 1rem;
    padding: 2rem;
    border: 1px solid #E5E7EB;
}

.left-column {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.right-column {
    position: relative;
}

@media (max-width: 1024px) {
    .right-column {
        position: static;
    }
}

.booking-card {
    position: sticky;
    top: 2rem;
    background: white;
    border: 2px solid var(--primary-green);
}


.section-heading {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary-green);
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 3px solid var(--primary-green);
    display: inline-block;
}

.subsection-heading {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--charcoal);
    margin: 1.5rem 0 1rem 0;
}

.description-text {
    color: var(--muted);
    line-height: 1.6;
    font-size: 0.95rem;
}

/* Features Grid */
.features-section {
    margin-top: 1.5rem;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
}

.feature-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem;
    background: var(--light-green);
    border-radius: 0.5rem;
}

.feature-icon {
    width: 1.5rem;
    height: 1.5rem;
    color: var(--primary-green);
    flex-shrink: 0;
}

.feature-icon svg {
    width: 100%;
    height: 100%;
}

.feature-name {
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--dark-green);
}

/* Meta Info */
.meta-info-section {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
    padding: 1.5rem 0;
    border-top: 1px solid #E5E7EB;
    border-bottom: 1px solid #E5E7EB;
}

.meta-item {
    display: flex;
    flex-direction: column;
}

.meta-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 0.25rem;
}

.meta-value {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--charcoal);
}

/* Rating */
.rating-section {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 1rem;
}

.stars {
    display: flex;
    gap: 0.25rem;
}

.star {
    width: 1.25rem;
    height: 1.25rem;
    color: #FCD34D;
}

.star.empty {
    color: #E5E7EB;
}

.rating-value {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--charcoal);
}

/* Reviews */
.reviews-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}

.write-review-btn {
    padding: 0.5rem 1rem;
    background: var(--primary-green);
    color: white;
    border: none;
    border-radius: 0.5rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 0.875rem;
}

.write-review-btn:hover {
    background: var(--dark-green);
}

.reviews-list {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.review-item {
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #E5E7EB;
}

.review-item:last-child {
    border-bottom: none;
}

.review-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.75rem;
}

.reviewer-info {
    display: flex;
    gap: 0.75rem;
}

.reviewer-avatar {
    width: 2rem;
    height: 2rem;
    border-radius: 50%;
    background: var(--primary-green);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.875rem;
    flex-shrink: 0;
}

.reviewer-name {
    font-weight: 600;
    color: var(--charcoal);
    margin-bottom: 0.25rem;
}

.review-date {
    font-size: 0.75rem;
    color: var(--muted);
}

.review-rating {
    display: flex;
    gap: 0.125rem;
}

.star-small {
    width: 1rem;
    height: 1rem;
    color: #FCD34D;
}

.star-small.empty {
    color: #E5E7EB;
}

.review-text {
    color: var(--muted);
    font-size: 0.875rem;
    line-height: 1.5;
}

.no-reviews {
    text-align: center;
    color: var(--muted);
    padding: 1rem 0;
}

/* Booking Card */
.price-display {
    text-align: center;
    margin-bottom: 1.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 2px solid var(--light-green);
}

.price-amount {
    display: block;
    font-size: 2rem;
    font-weight: 700;
    color: var(--primary-green);
}

.price-period {
    font-size: 0.875rem;
    color: var(--muted);
}

/* Forms */
.booking-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.form-label {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--charcoal);
}

.form-input {
    padding: 0.75rem;
    border: 2px solid #E5E7EB;
    border-radius: 0.5rem;
    font-size: 0.95rem;
    transition: all 0.3s ease;
}

.form-input:focus {
    outline: none;
    border-color: var(--primary-green);
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.slots-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
    max-height: 12rem;
    overflow-y: auto;
    padding: 0.5rem;
    border: 1px solid #E5E7EB;
    border-radius: 0.5rem;
    background: var(--light-gray);
}

.slot-button {
    padding: 0.75rem 0.5rem;
    border: 2px solid #E5E7EB;
    background: white;
    border-radius: 0.5rem;
    font-size: 0.75rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    color: var(--charcoal);
}

.slot-button:not(.booked):hover {
    border-color: var(--primary-green);
    color: var(--primary-green);
}

.slot-button.selected {
    background: var(--primary-green);
    border-color: var(--primary-green);
    color: white;
}

.slot-button.booked {
    background: #F3F4F6;
    border-color: #D1D5DB;
    color: var(--muted);
    cursor: not-allowed;
    opacity: 0.6;
}

.booked-label {
    display: block;
    font-size: 0.65rem;
    margin-top: 0.25rem;
}

/* Booking Summary */
.booking-summary {
    padding: 1rem;
    background: var(--light-green);
    border-radius: 0.5rem;
    margin: 1rem 0;
}

.summary-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.875rem;
    color: var(--charcoal);
    margin-bottom: 0.5rem;
}

.summary-row.total {
    font-weight: 700;
    font-size: 1rem;
    color: var(--primary-green);
}

.summary-divider {
    height: 1px;
    background: var(--primary-green);
    margin: 0.5rem 0;
    opacity: 0.3;
}


.book-button {
    width: 100%;
    padding: 0.875rem;
    background: var(--primary-green);
    color: white;
    border: none;
    border-radius: 0.5rem;
    font-weight: 600;
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 0.5rem;
}

.book-button:hover:not(:disabled) {
    background: var(--dark-green);
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(16, 185, 129, 0.3);
}

.book-button:disabled {
    background: #D1D5DB;
    cursor: not-allowed;
    opacity: 0.6;
}

/* Alerts */
.success-alert {
    padding: 0.75rem 1rem;
    background: #D1FAE5;
    border: 1px solid #A7F3D0;
    border-radius: 0.5rem;
    color: #065F46;
    font-weight: 500;
    font-size: 0.875rem;
    margin-bottom: 1rem;
}

.error-alert {
    padding: 0.75rem 1rem;
    background: #FEE2E2;
    border: 1px solid #FECACA;
    border-radius: 0.5rem;
    color: #991B1B;
    font-weight: 500;
    font-size: 0.875rem;
    margin-bottom: 1rem;
}

.time-inputs {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
}
</style>
