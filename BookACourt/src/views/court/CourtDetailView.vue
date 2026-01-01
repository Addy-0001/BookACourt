<template>
    <div class="court-detail-page">
        <!-- Back Button -->
        <div class="container">
            <button @click="goBack" class="back-button">
                <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
                <span>Back</span>
            </button>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="loading-container">
            <div class="spinner"></div>
        </div>

        <!-- Error -->
        <div v-else-if="error" class="error-container">
            <svg class="error-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p>{{ error }}</p>
        </div>

        <!-- Court Details -->
        <div v-else-if="court">
            <!-- Hero Image with Overlay -->
            <div class="hero-section">
                <div v-if="court.images && court.images.length > 0" class="hero-image-container">
                    <img :src="court.images[currentImageIndex].image" :alt="court.name" class="hero-image" />
                    <div class="hero-overlay"></div>
                    <div class="hero-content">
                        <h1 class="hero-title">{{ court.name }}</h1>
                        <p class="hero-location">
                            <svg class="location-icon" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd"
                                    d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z"
                                    clip-rule="evenodd" />
                            </svg>
                            {{ court.city }}
                        </p>
                    </div>
                    <!-- Image indicators for multiple images -->
                    <div v-if="court.images.length > 1" class="image-indicators">
                        <button v-for="(img, idx) in court.images" :key="idx" @click="currentImageIndex = idx"
                            :class="['indicator', { active: idx === currentImageIndex }]" />
                    </div>
                </div>
            </div>

            <div class="container">
                <!-- Main Content Grid -->
                <div class="content-grid">
                    <!-- Left Column -->
                    <div class="left-column">
                        <!-- About Section -->
                        <div class="card about-card">
                            <h2 class="section-heading">About This {{ court.category?.name || court.court_type }} Court
                            </h2>
                            <p class="description-text">{{ court.description }}</p>

                            <!-- Features & Amenities in grid layout -->
                            <div v-if="court.amenities_list && court.amenities_list.length" class="features-section">
                                <h3 class="subsection-heading">Features & Amenities</h3>
                                <div class="features-grid">
                                    <div v-for="amenity in court.amenities_list.slice(0, 4)" :key="amenity"
                                        class="feature-item">
                                        <div class="feature-icon">
                                            <svg fill="currentColor" viewBox="0 0 20 20">
                                                <path fill-rule="evenodd"
                                                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                                    clip-rule="evenodd" />
                                            </svg>
                                        </div>
                                        <span class="feature-name">{{ amenity }}</span>
                                    </div>
                                </div>
                            </div>

                            <!-- Meta Info -->
                            <div class="meta-info-section">
                                <div class="meta-item">
                                    <span class="meta-label">Type</span>
                                    <span class="meta-value">{{ court.is_indoor ? 'Indoor' : 'Outdoor' }}</span>
                                </div>
                                <div class="meta-item">
                                    <span class="meta-label">Capacity</span>
                                    <span class="meta-value">{{ court.capacity }} players</span>
                                </div>
                                <div class="meta-item">
                                    <span class="meta-label">Hours</span>
                                    <span class="meta-value">{{ court.opening_time }} - {{ court.closing_time }}</span>
                                </div>
                            </div>

                            <!-- Rating -->
                            <div v-if="court.average_rating" class="rating-section">
                                <div class="stars">
                                    <svg v-for="i in 5" :key="i" class="star"
                                        :class="i <= Math.round(court.average_rating) ? 'filled' : 'empty'"
                                        fill="currentColor" viewBox="0 0 20 20">
                                        <path
                                            d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                    </svg>
                                </div>
                                <span class="rating-value">{{ court.average_rating }} ({{ court.total_reviews || 0 }}
                                    reviews)</span>
                            </div>
                        </div>

                        <!-- Reviews Section -->
                        <div class="card reviews-card">
                            <div class="reviews-header">
                                <h3 class="section-heading">Reviews</h3>
                                <button v-if="canReview" @click="showReviewModal = true" class="write-review-btn">
                                    {{ userReview ? 'Edit' : 'Write Review' }}
                                </button>
                            </div>

                            <div v-if="reviews.length > 0" class="reviews-list">
                                <div v-for="review in reviews.slice(0, 3)" :key="review.id" class="review-item">
                                    <div class="review-header">
                                        <div class="reviewer-info">
                                            <div class="reviewer-avatar">{{ review.player_name.charAt(0).toUpperCase()
                                                }}</div>
                                            <div>
                                                <p class="reviewer-name">{{ review.player_name }}</p>
                                                <p class="review-date">{{ formatDate(review.created_at) }}</p>
                                            </div>
                                        </div>
                                        <div class="review-rating">
                                            <svg v-for="i in 5" :key="i" class="star-small"
                                                :class="i <= review.rating ? 'filled' : 'empty'" fill="currentColor"
                                                viewBox="0 0 20 20">
                                                <path
                                                    d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                            </svg>
                                        </div>
                                    </div>
                                    <p class="review-text">{{ review.review_text }}</p>
                                </div>
                            </div>
                            <p v-else class="no-reviews">No reviews yet. Be the first to review!</p>
                        </div>
                    </div>

                    <!-- Right Column - Booking -->
                    <div class="right-column">
                        <div class="card booking-card">
                            <div class="price-display">
                                <span class="price-amount">NRs. {{ displayRate }}</span>
                                <span class="price-period">/hour</span>
                            </div>

                            <div v-if="bookingSuccess" class="success-alert">
                                <p>Booking created successfully!</p>
                            </div>

                            <div v-if="bookingError" class="error-alert">
                                <p>{{ bookingError }}</p>
                            </div>

                            <form @submit.prevent="handleBooking" class="booking-form">
                                <!-- Date Selection -->
                                <div class="form-group">
                                    <label class="form-label">Select Date:</label>
                                    <input v-model="bookingForm.date" type="date" :min="minDate" required
                                        @change="onDateOrTimeChange" class="form-input date-input" />
                                </div>

                                <!-- Time Slots -->
                                <div
                                    v-if="bookingForm.date && (availableSlots.length > 0 || unavailableSlots.length > 0)">
                                    <label class="form-label">Select Time Slots:</label>
                                    <div class="slots-grid">
                                        <button v-for="slot in availableSlots" :key="slot.start_time" type="button"
                                            @click="toggleTimeSlot(slot)"
                                            :class="['slot-button', { selected: isSlotSelected(slot) }]">
                                            {{ slot.start_time }} - {{ slot.end_time }}
                                        </button>
                                        <button v-for="slot in unavailableSlots" :key="'unavail-' + slot.start_time"
                                            type="button" disabled class="slot-button booked">
                                            {{ slot.start_time }}<br><span class="booked-label">Booked</span>
                                        </button>
                                    </div>
                                </div>

                                <!-- Manual Time Selection -->
                                <div v-else-if="bookingForm.date" class="time-inputs">
                                    <div class="form-group">
                                        <label class="form-label">Start Time</label>
                                        <input v-model="bookingForm.start_time" type="time" required
                                            @change="onDateOrTimeChange" class="form-input" />
                                    </div>
                                    <div class="form-group">
                                        <label class="form-label">End Time</label>
                                        <input v-model="bookingForm.end_time" type="time" required
                                            @change="onDateOrTimeChange" class="form-input" />
                                    </div>
                                </div>

                                <!-- Booking Summary -->
                                <div v-if="bookingForm.date && selectedSlots.length > 0" class="booking-summary">
                                    <div class="summary-row">
                                        <span>Court Fee ({{ totalDuration.toFixed(1) }} hrs)</span>
                                        <span>Rs {{ courtFeeDisplay }}</span>
                                    </div>
                                    <div class="summary-divider"></div>
                                    <div class="summary-row total">
                                        <span>Total</span>
                                        <span>Rs {{ estimatedTotalDisplay }}</span>
                                    </div>
                                </div>

                                <!-- Submit Button -->
                                <button type="submit" :disabled="bookingLoading || !canBook" class="book-button">
                                    <span v-if="bookingLoading">Processing...</span>
                                    <span v-else>Book Now</span>
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
