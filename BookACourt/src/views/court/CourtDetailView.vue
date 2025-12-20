<template>
    <div class="court-detail-page">
        <div class="container">
            <!-- Back Button -->
            <button @click="goBack" class="back-button">
                <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
                <span>Back to Courts</span>
            </button>

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
            <div v-else-if="court" class="detail-grid">
                <!-- Left Column - Court Info -->
                <div class="left-column">
                    <!-- Images -->
                    <div class="image-card">
                        <div v-if="court.images && court.images.length > 0" class="image-container">
                            <img :src="court.images[currentImageIndex].image" :alt="court.name" class="court-image" />
                            <div v-if="court.images.length > 1" class="image-indicators">
                                <button v-for="(img, idx) in court.images" :key="idx" @click="currentImageIndex = idx"
                                    :class="['indicator', { active: idx === currentImageIndex }]" />
                            </div>
                        </div>
                        <div v-else class="placeholder-image">
                            <svg class="placeholder-icon" fill="currentColor" viewBox="0 0 24 24">
                                <path
                                    d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z" />
                            </svg>
                        </div>
                    </div>

                    <!-- Basic Info -->
                    <div class="info-card">
                        <div class="header-section">
                            <div>
                                <h2 class="court-title">{{ court.name }}</h2>
                                <p class="court-category">{{ court.category?.name || court.court_type }}</p>
                            </div>
                            <span v-if="court.is_verified" class="verified-badge">
                                <svg class="badge-icon" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd"
                                        d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                        clip-rule="evenodd" />
                                </svg>
                                Verified
                            </span>
                        </div>

                        <div class="meta-info">
                            <div class="rating-section">
                                <svg class="star-icon" fill="currentColor" viewBox="0 0 24 24">
                                    <path
                                        d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                                </svg>
                                <span class="rating-value">{{ court.average_rating || '0.0' }}</span>
                                <span class="review-count">({{ court.total_reviews || 0 }} reviews)</span>
                            </div>
                            <span class="separator">•</span>
                            <span>{{ court.is_indoor ? 'Indoor' : 'Outdoor' }}</span>
                            <span class="separator">•</span>
                            <span>Capacity: {{ court.capacity }}</span>
                        </div>

                        <div class="divider"></div>

                        <div class="location-section">
                            <h3 class="section-title">
                                <svg class="section-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                                </svg>
                                Location
                            </h3>
                            <p class="location-text">{{ court.address }}</p>
                            <p class="location-text">{{ court.city }}</p>
                        </div>

                        <div v-if="court.description" class="description-section">
                            <div class="divider"></div>
                            <h3 class="section-title">Description</h3>
                            <p class="description-text">{{ court.description }}</p>
                        </div>

                        <div v-if="court.amenities_list && court.amenities_list.length" class="amenities-section">
                            <div class="divider"></div>
                            <h3 class="section-title">Amenities</h3>
                            <div class="amenities-list">
                                <span v-for="amenity in court.amenities_list" :key="amenity" class="amenity-tag">
                                    {{ amenity }}
                                </span>
                            </div>
                        </div>

                        <div class="hours-section">
                            <div class="divider"></div>
                            <h3 class="section-title">
                                <svg class="section-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                Operating Hours
                            </h3>
                            <p class="hours-text">{{ court.opening_time }} - {{ court.closing_time }}</p>
                        </div>

                        <!-- Dynamic Pricing -->
                        <div v-if="court.pricing_rules && court.pricing_rules.length" class="pricing-section">
                            <div class="divider"></div>
                            <h3 class="section-title">Pricing Schedule</h3>
                            <div class="pricing-list">
                                <div v-for="rule in court.pricing_rules" :key="rule.id" class="pricing-rule">
                                    <div>
                                        <p class="rule-description">{{ rule.description }}</p>
                                        <p class="rule-time">{{ rule.start_time }} - {{ rule.end_time }}</p>
                                        <p class="rule-days">{{ formatDaysOfWeek(rule.days_of_week) }}</p>
                                    </div>
                                    <span class="rule-rate">Rs {{ rule.hourly_rate }}/hr</span>
                                </div>
                            </div>
                        </div>
                        <div v-else class="pricing-section">
                            <div class="divider"></div>
                            <h3 class="section-title">Standard Pricing</h3>
                            <div class="standard-price">
                                <span class="price-amount">Rs {{ court.base_hourly_rate }}/hr</span>
                            </div>
                        </div>

                        <!-- Equipment -->
                        <div v-if="court.equipment && court.equipment.length" class="equipment-section">
                            <div class="divider"></div>
                            <h3 class="section-title">Available Equipment</h3>
                            <div class="equipment-grid">
                                <div v-for="item in court.equipment" :key="item.id" class="equipment-item">
                                    <div class="equipment-header">
                                        <p class="equipment-name">{{ item.name }}</p>
                                        <span
                                            :class="['equipment-status', item.quantity_available > 0 ? 'available' : 'unavailable']">
                                            {{ item.quantity_available }}/{{ item.quantity_total }} available
                                        </span>
                                    </div>
                                    <p class="equipment-description">{{ item.description }}</p>
                                    <p class="equipment-price">Rs {{ item.rental_rate }}/session</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Reviews Section -->
                    <div class="reviews-card">
                        <div class="reviews-header">
                            <h3 class="reviews-title">Reviews</h3>
                            <button v-if="canReview" @click="showReviewModal = true" class="write-review-btn">
                                {{ userReview ? 'Edit Review' : 'Write Review' }}
                            </button>
                        </div>

                        <div v-if="reviews.length > 0" class="reviews-list">
                            <div v-for="review in reviews" :key="review.id" class="review-item">
                                <div class="review-content">
                                    <div class="reviewer-avatar">
                                        {{ review.player_name.charAt(0).toUpperCase() }}
                                    </div>
                                    <div class="review-body">
                                        <div class="review-header-line">
                                            <span class="reviewer-name">{{ review.player_name }}</span>
                                            <div class="review-stars">
                                                <svg v-for="i in 5" :key="i" class="star"
                                                    :class="i <= review.rating ? 'filled' : 'empty'" fill="currentColor"
                                                    viewBox="0 0 24 24">
                                                    <path
                                                        d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                                                </svg>
                                            </div>
                                            <span v-if="review.player === authStore.user?.id"
                                                class="you-badge">You</span>
                                        </div>
                                        <p class="review-text">{{ review.review_text }}</p>
                                        <p class="review-date">{{ formatDate(review.created_at) }}</p>
                                        <div v-if="review.owner_response" class="owner-response">
                                            <p class="response-label">Owner's Response</p>
                                            <p class="response-text">{{ review.owner_response }}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <p v-else class="no-reviews">No reviews yet</p>
                    </div>
                </div>

                <!-- Right Column - Booking -->
                <div class="right-column">
                    <div class="booking-card">
                        <div class="price-header">
                            <div class="price-display">
                                Rs {{ displayRate }}<span class="price-unit">/hour</span>
                            </div>
                            <p class="price-description">{{ rateDescription }}</p>
                        </div>

                        <div v-if="bookingSuccess" class="success-alert">
                            <p>Booking created successfully!</p>
                        </div>

                        <div v-if="bookingError" class="error-alert">
                            <p>{{ bookingError }}</p>
                        </div>

                        <form @submit.prevent="handleBooking" class="booking-form">
                            <div class="form-group">
                                <label class="form-label">Date</label>
                                <!-- Set default date to today and added calendar styling -->
                                <input v-model="bookingForm.date" type="date" :min="minDate" required
                                    @change="onDateOrTimeChange" class="form-input date-input" />
                            </div>

                            <!-- Redesigned slots to show available (green) and unavailable (red), allow multiple selections -->
                            <div v-if="bookingForm.date && (availableSlots.length > 0 || unavailableSlots.length > 0)">
                                <label class="form-label">Select Time Slots (Multiple allowed)</label>
                                <div class="slots-grid">
                                    <button v-for="slot in availableSlots" :key="slot.start_time" type="button"
                                        @click="toggleTimeSlot(slot)"
                                        :class="['slot-button', 'available', { selected: isSlotSelected(slot) }]">
                                        <span class="slot-time">{{ slot.start_time }} - {{ slot.end_time }}</span>
                                    </button>
                                    <button v-for="slot in unavailableSlots" :key="'unavail-' + slot.start_time"
                                        type="button" disabled :class="['slot-button', 'unavailable']">
                                        <span class="slot-time">{{ slot.start_time }} - {{ slot.end_time }}</span>
                                        <span class="unavailable-label">Booked</span>
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

                            <!-- Equipment Selection -->
                            <div v-if="court.equipment && court.equipment.length > 0" class="form-group">
                                <label class="form-label">Rent Equipment (Optional)</label>
                                <div class="equipment-options">
                                    <label v-for="item in court.equipment.filter(e => e.quantity_available > 0)"
                                        :key="item.id" class="equipment-checkbox">
                                        <input type="checkbox" :value="item.id"
                                            v-model="bookingForm.equipment_rentals" />
                                        <span class="equipment-label">{{ item.name }} (Rs {{ item.rental_rate }})</span>
                                    </label>
                                </div>
                            </div>

                            <!-- Notes -->
                            <div class="form-group">
                                <label class="form-label">Notes (Optional)</label>
                                <textarea v-model="bookingForm.notes" rows="2"
                                    placeholder="Any special requests or notes..." class="form-textarea"></textarea>
                            </div>

                            <div v-if="bookingForm.date && selectedSlots.length > 0" class="booking-summary">
                                <p class="summary-title">Booking Summary</p>
                                <div class="summary-details">
                                    <div class="summary-row">
                                        <span>Court Fee ({{ totalDuration.toFixed(1) }} hrs @ Rs {{ currentRate
                                        }}/hr)</span>
                                        <span class="summary-amount">Rs {{ courtFeeDisplay }}</span>
                                    </div>
                                    <div v-if="equipmentFee > 0" class="summary-row">
                                        <span>Equipment Rental</span>
                                        <span class="summary-amount">Rs {{ equipmentFeeDisplay }}</span>
                                    </div>
                                    <div class="summary-divider"></div>
                                    <div class="summary-row total">
                                        <span>Total</span>
                                        <span>Rs {{ estimatedTotalDisplay }}</span>
                                    </div>
                                </div>
                            </div>

                            <button type="submit" :disabled="bookingLoading || !canBook" class="book-button">
                                <span v-if="bookingLoading">Processing...</span>
                                <span v-else>Book Now</span>
                            </button>

                            <button v-if="bookingForm.date && selectedSlots.length > 0" type="button"
                                @click="checkAvailability" :disabled="availabilityLoading" class="check-button">
                                <span v-if="availabilityLoading">Checking...</span>
                                <span v-else>Check Availability</span>
                            </button>
                        </form>

                        <div v-if="availabilityMessage"
                            :class="['availability-message', isAvailable ? 'available-msg' : 'unavailable-msg']">
                            <p>{{ availabilityMessage }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Review Modal -->
        <div v-if="showReviewModal" class="modal-overlay">
            <div class="modal-content">
                <h3 class="modal-title">{{ userReview ? 'Edit Your Review' : 'Write a Review' }}</h3>

                <form @submit.prevent="submitReview" class="review-form">
                    <div class="form-group">
                        <label class="form-label">Rating</label>
                        <div class="rating-buttons">
                            <button v-for="i in 5" :key="i" type="button" @click="reviewForm.rating = i"
                                class="rating-star-button">
                                <svg class="rating-star" :class="i <= reviewForm.rating ? 'filled' : 'empty'"
                                    fill="currentColor" viewBox="0 0 24 24">
                                    <path
                                        d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                                </svg>
                            </button>
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="form-label">Your Review</label>
                        <textarea v-model="reviewForm.review_text" rows="4" placeholder="Share your experience..."
                            required class="form-textarea"></textarea>
                    </div>

                    <div class="modal-actions">
                        <button type="button" @click="closeReviewModal" class="cancel-button">
                            Cancel
                        </button>
                        <button type="submit" :disabled="submittingReview || reviewForm.rating === 0"
                            class="submit-button">
                            {{ submittingReview ? 'Submitting...' : 'Submit Review' }}
                        </button>
                    </div>
                </form>
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
/* Color Variables */
:root {
    --primary-blue: #0056B3;
    --red-cta: #EF4444;
    --purple-accent: #7C3AED;
    --success-green: #10B981;
    --warning-orange: #F59E0B;
    --charcoal: #1F2937;
    --muted: #9CA3AF;
    --orange: #FF6B35;
}

/* Base Styles */
.court-detail-page {
    min-height: 100vh;
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    padding: 2rem 0;
}

.container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 1.5rem;
}

/* Back Button */
.back-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
    padding: 0.625rem 1rem;
    background: white;
    border: 2px solid #e5e7eb;
    border-radius: 0.5rem;
    color: var(--charcoal);
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
}

.back-button:hover {
    border-color: var(--primary-blue);
    color: var(--primary-blue);
    transform: translateX(-4px);
}

.back-button .icon {
    width: 1.25rem;
    height: 1.25rem;
}

/* Loading */
.loading-container {
    display: flex;
    justify-content: center;
    padding: 5rem 0;
}

.spinner {
    width: 3rem;
    height: 3rem;
    border: 3px solid #e5e7eb;
    border-top-color: var(--primary-blue);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

/* Error */
.error-container {
    text-align: center;
    padding: 5rem 0;
}

.error-icon {
    width: 4rem;
    height: 4rem;
    margin: 0 auto 1rem;
    color: var(--red-cta);
}

.error-container p {
    font-size: 1.25rem;
    color: var(--muted);
}

/* Grid Layout */
.detail-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 2rem;
}

@media (min-width: 1024px) {
    .detail-grid {
        grid-template-columns: 2fr 1fr;
    }
}

/* Left Column */
.left-column {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

/* Cards */
.image-card,
.info-card,
.reviews-card,
.booking-card {
    background: white;
    border-radius: 1rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    overflow: hidden;
}

/* Image Section */
.image-container {
    position: relative;
    height: 24rem;
}

.court-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
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
    border: none;
    background: rgba(255, 255, 255, 0.5);
    cursor: pointer;
    transition: all 0.3s ease;
}

.indicator.active {
    background: white;
    transform: scale(1.2);
}

.placeholder-image {
    height: 24rem;
    background: linear-gradient(135deg, var(--primary-blue) 0%, var(--purple-accent) 100%);
    display: flex;
    align-items: center;
    justify-content: center;
}

.placeholder-icon {
    width: 8rem;
    height: 8rem;
    color: white;
    opacity: 0.5;
}

/* Info Card */
.info-card {
    padding: 2rem;
}

.header-section {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 1rem;
}

.court-title {
    font-size: 2rem;
    font-weight: 700;
    color: var(--charcoal);
    background: linear-gradient(135deg, var(--primary-blue) 0%, var(--purple-accent) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.court-category {
    color: var(--muted);
    margin-top: 0.25rem;
}

.verified-badge {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.5rem 0.75rem;
    background: #d1fae5;
    color: var(--success-green);
    border-radius: 9999px;
    font-size: 0.875rem;
    font-weight: 500;
}

.badge-icon {
    width: 1rem;
    height: 1rem;
}

.meta-info {
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
    color: var(--muted);
    margin-bottom: 1rem;
}

.rating-section {
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

.star-icon {
    width: 1.25rem;
    height: 1.25rem;
    color: var(--warning-orange);
}

.rating-value {
    font-weight: 500;
    color: var(--charcoal);
}

.review-count {
    color: var(--muted);
}

.separator {
    color: #d1d5db;
}

.divider {
    height: 1px;
    background: #e5e7eb;
    margin: 1.5rem 0;
}

.section-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--charcoal);
    margin-bottom: 0.75rem;
}

.section-icon {
    width: 1.25rem;
    height: 1.25rem;
    color: var(--primary-blue);
}

.location-text,
.description-text,
.hours-text {
    color: var(--muted);
    line-height: 1.6;
}

.location-text {
    margin-bottom: 0.25rem;
}

.description-text {
    margin-top: 0.5rem;
}

.description-section,
.amenities-section,
.hours-section,
.pricing-section,
.equipment-section {
    margin-top: 1.5rem;
}

.amenities-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.amenity-tag {
    padding: 0.5rem 0.75rem;
    background: #eff6ff;
    color: var(--primary-blue);
    border-radius: 9999px;
    font-size: 0.875rem;
    font-weight: 500;
}

.pricing-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.pricing-rule {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem;
    background: #f9fafb;
    border-radius: 0.5rem;
}

.rule-description {
    font-weight: 500;
    color: var(--charcoal);
    margin-bottom: 0.25rem;
}

.rule-time {
    font-size: 0.875rem;
    color: var(--muted);
    margin-bottom: 0.25rem;
}

.rule-days {
    font-size: 0.75rem;
    color: var(--muted);
}

.rule-rate {
    font-size: 1.125rem;
    font-weight: 700;
    color: var(--primary-blue);
}

.standard-price {
    padding: 1rem;
    background: #f9fafb;
    border-radius: 0.5rem;
}

.price-amount {
    font-size: 1.125rem;
    font-weight: 700;
    color: var(--primary-blue);
}

.equipment-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 0.75rem;
}

@media (min-width: 768px) {
    .equipment-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

.equipment-item {
    padding: 1rem;
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
}

.equipment-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.5rem;
}

.equipment-name {
    font-weight: 500;
    color: var(--charcoal);
}

.equipment-status {
    font-size: 0.875rem;
    font-weight: 500;
}

.equipment-status.available {
    color: var(--success-green);
}

.equipment-status.unavailable {
    color: var(--red-cta);
}

.equipment-description {
    font-size: 0.875rem;
    color: var(--muted);
    margin-bottom: 0.5rem;
}

.equipment-price {
    font-size: 0.875rem;
    font-weight: 700;
    color: var(--primary-blue);
}

/* Reviews */
.reviews-card {
    padding: 2rem;
}

.reviews-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
}

.reviews-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--charcoal);
}

.write-review-btn {
    padding: 0.625rem 1rem;
    background: linear-gradient(135deg, var(--orange) 0%, var(--red-cta) 100%);
    color: white;
    border: none;
    border-radius: 0.5rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
}

.write-review-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(255, 107, 53, 0.3);
}

.reviews-list {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.review-item {
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #e5e7eb;
}

.review-item:last-child {
    border-bottom: none;
}

.review-content {
    display: flex;
    gap: 0.75rem;
}

.reviewer-avatar {
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--primary-blue) 0%, var(--purple-accent) 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 700;
    flex-shrink: 0;
}

.review-body {
    flex: 1;
}

.review-header-line {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
    flex-wrap: wrap;
}

.reviewer-name {
    font-weight: 600;
    color: var(--charcoal);
}

.review-stars {
    display: flex;
}

.review-stars .star {
    width: 1rem;
    height: 1rem;
}

.review-stars .star.filled {
    color: var(--warning-orange);
}

.review-stars .star.empty {
    color: #d1d5db;
}

.you-badge {
    padding: 0.25rem 0.5rem;
    background: #eff6ff;
    color: var(--primary-blue);
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 500;
}

.review-text {
    color: var(--muted);
    font-size: 0.875rem;
    line-height: 1.5;
    margin-bottom: 0.5rem;
}

.review-date {
    color: #d1d5db;
    font-size: 0.75rem;
}

.owner-response {
    margin-top: 0.75rem;
    margin-left: 1rem;
    padding: 0.75rem;
    background: #f9fafb;
    border-radius: 0.5rem;
}

.response-label {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--charcoal);
    margin-bottom: 0.25rem;
}

.response-text {
    font-size: 0.875rem;
    color: var(--muted);
}

.no-reviews {
    text-align: center;
    color: var(--muted);
    padding: 1rem 0;
}

/* Right Column - Booking */
.right-column {
    position: relative;
}

.booking-card {
    padding: 1.5rem;
    position: sticky;
    top: 6rem;
}

.price-header {
    margin-bottom: 1.5rem;
}

.price-display {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--primary-blue) 0%, var(--purple-accent) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.25rem;
}

.price-unit {
    font-size: 1.125rem;
    color: var(--muted);
}

.price-description {
    font-size: 0.875rem;
    color: var(--muted);
}

/* Alerts */
.success-alert,
.error-alert {
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
}

.success-alert {
    background: #d1fae5;
    border: 1px solid #a7f3d0;
}

.success-alert p {
    color: #065f46;
    font-weight: 500;
}

.error-alert {
    background: #fee2e2;
    border: 1px solid #fecaca;
}

.error-alert p {
    color: #991b1b;
}

/* Form */
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
    font-weight: 500;
    color: var(--charcoal);
}

.form-input,
.form-textarea {
    padding: 0.75rem 1rem;
    border: 2px solid #e5e7eb;
    border-radius: 0.5rem;
    font-size: 1rem;
    transition: all 0.3s ease;
}

.form-input:focus,
.form-textarea:focus {
    outline: none;
    border-color: var(--primary-blue);
    box-shadow: 0 0 0 3px rgba(0, 86, 179, 0.1);
}

.date-input {
    cursor: pointer;
}

.time-inputs {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
}

/* Slots Grid */
.slots-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.5rem;
    max-height: 16rem;
    overflow-y: auto;
    padding: 0.5rem;
    border: 2px solid #e5e7eb;
    border-radius: 0.5rem;
}

.slot-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 0.75rem 0.5rem;
    border: 2px solid;
    border-radius: 0.5rem;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    background: white;
}

.slot-button.available {
    border-color: var(--success-green);
    color: var(--success-green);
    background: #d1fae5;
}

.slot-button.available:hover {
    background: var(--success-green);
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(16, 185, 129, 0.3);
}

.slot-button.available.selected {
    background: var(--success-green);
    color: white;
    border-color: var(--success-green);
}

.slot-button.unavailable {
    border-color: var(--red-cta);
    color: var(--red-cta);
    background: #fee2e2;
    cursor: not-allowed;
    opacity: 0.7;
}

.slot-time {
    font-weight: 600;
}

.unavailable-label {
    font-size: 0.75rem;
    margin-top: 0.25rem;
    opacity: 0.8;
}

/* Equipment Options */
.equipment-options {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    max-height: 8rem;
    overflow-y: auto;
    padding: 0.5rem;
    border: 2px solid #e5e7eb;
    border-radius: 0.5rem;
}

.equipment-checkbox {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem;
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: all 0.3s ease;
}

.equipment-checkbox:hover {
    background: #f9fafb;
}

.equipment-checkbox input[type="checkbox"] {
    width: 1.25rem;
    height: 1.25rem;
    accent-color: var(--primary-blue);
    cursor: pointer;
}

.equipment-label {
    flex: 1;
    font-size: 0.875rem;
    color: var(--charcoal);
}

/* Booking Summary */
.booking-summary {
    padding: 1rem;
    background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    border: 2px solid #bfdbfe;
    border-radius: 0.5rem;
}

.summary-title {
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--primary-blue);
    margin-bottom: 0.75rem;
}

.summary-details {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.summary-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.875rem;
    color: #1e3a8a;
}

.summary-amount {
    font-weight: 500;
}

.summary-divider {
    height: 1px;
    background: #bfdbfe;
    margin: 0.5rem 0;
}

.summary-row.total {
    font-weight: 700;
    font-size: 1rem;
}

/* Buttons */
.book-button,
.check-button {
    width: 100%;
    padding: 0.875rem;
    font-weight: 600;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: all 0.3s ease;
    border: none;
}

.book-button {
    background: linear-gradient(135deg, var(--orange) 0%, var(--red-cta) 100%);
    color: white;
}

.book-button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(255, 107, 53, 0.3);
}

.book-button:disabled {
    background: #d1d5db;
    cursor: not-allowed;
    opacity: 0.6;
}

.check-button {
    background: white;
    color: var(--primary-blue);
    border: 2px solid var(--primary-blue);
}

.check-button:hover:not(:disabled) {
    background: var(--primary-blue);
    color: white;
}

.check-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

/* Availability Message */
.availability-message {
    margin-top: 1rem;
    padding: 0.75rem;
    border-radius: 0.5rem;
}

.available-msg {
    background: #d1fae5;
    color: #065f46;
}

.unavailable-msg {
    background: #fee2e2;
    color: #991b1b;
}

.availability-message p {
    font-size: 0.875rem;
    font-weight: 500;
}

/* Modal */
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 1rem;
}

.modal-content {
    background: white;
    border-radius: 1rem;
    max-width: 28rem;
    width: 100%;
    padding: 1.5rem;
}

.modal-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--charcoal);
    margin-bottom: 1.5rem;
}

.review-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.rating-buttons {
    display: flex;
    gap: 0.5rem;
}

.rating-star-button {
    width: 2.5rem;
    height: 2.5rem;
    background: none;
    border: none;
    cursor: pointer;
    transition: transform 0.3s ease;
}

.rating-star-button:hover {
    transform: scale(1.1);
}

.rating-star {
    width: 100%;
    height: 100%;
}

.rating-star.filled {
    color: var(--warning-orange);
}

.rating-star.empty {
    color: #d1d5db;
}

.modal-actions {
    display: flex;
    gap: 0.75rem;
}

.cancel-button,
.submit-button {
    flex: 1;
    padding: 0.75rem 1rem;
    border-radius: 0.5rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
}

.cancel-button {
    background: white;
    border: 2px solid #e5e7eb;
    color: var(--charcoal);
}

.cancel-button:hover {
    background: #f9fafb;
}

.submit-button {
    background: linear-gradient(135deg, var(--primary-blue) 0%, var(--purple-accent) 100%);
    color: white;
    border: none;
}

.submit-button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(0, 86, 179, 0.3);
}

.submit-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

/* Responsive */
@media (max-width: 768px) {
    .header-section {
        flex-direction: column;
        gap: 1rem;
    }

    .meta-info {
        flex-direction: column;
        align-items: flex-start;
    }

    .slots-grid {
        grid-template-columns: 1fr;
    }
}
</style>
