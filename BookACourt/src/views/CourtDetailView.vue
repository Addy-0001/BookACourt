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
                        <h1 class="text-2xl font-bold text-blue-600">Court Details</h1>
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
                <p class="text-xl text-red-600">{{ error }}</p>
                <button @click="loadCourtDetails" class="mt-4 px-6 py-3 bg-blue-600 text-white rounded-lg">
                    Try Again
                </button>
            </div>

            <!-- Court Details -->
            <div v-else-if="court" class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <!-- Left Column - Court Info -->
                <div class="lg:col-span-2 space-y-6">
                    <!-- Images -->
                    <div class="bg-white rounded-xl shadow-md overflow-hidden">
                        <div v-if="court.images && court.images.length > 0" class="h-96 relative">
                            <img :src="court.images[currentImageIndex].image" :alt="court.name"
                                class="w-full h-full object-cover" />
                            <div v-if="court.images.length > 1"
                                class="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex gap-2">
                                <button v-for="(img, idx) in court.images" :key="idx" @click="currentImageIndex = idx"
                                    :class="[
                                        'w-3 h-3 rounded-full transition-colors',
                                        idx === currentImageIndex ? 'bg-white' : 'bg-white/50'
                                    ]" />
                            </div>
                        </div>
                        <div v-else
                            class="h-96 bg-gradient-to-r from-blue-400 to-purple-400 flex items-center justify-center">
                            <svg class="w-32 h-32 text-white opacity-50" fill="currentColor" viewBox="0 0 24 24">
                                <path
                                    d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z" />
                            </svg>
                        </div>
                    </div>

                    <!-- Basic Info -->
                    <div class="bg-white rounded-xl shadow-md p-6">
                        <div class="flex items-start justify-between mb-4">
                            <div>
                                <h2 class="text-3xl font-bold text-gray-900">{{ court.name }}</h2>
                                <p class="text-gray-600 mt-1">{{ court.category?.name || court.court_type }}</p>
                            </div>
                            <span v-if="court.is_verified"
                                class="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                                Verified
                            </span>
                        </div>

                        <div class="flex items-center gap-4 text-gray-600 mb-4">
                            <div class="flex items-center gap-1">
                                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                    <path
                                        d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                                </svg>
                                <span>{{ court.average_rating || '0.0' }} ({{ court.total_reviews || 0 }}
                                    reviews)</span>
                            </div>
                            <span>•</span>
                            <span>{{ court.is_indoor ? 'Indoor' : 'Outdoor' }}</span>
                            <span>•</span>
                            <span>Capacity: {{ court.capacity }}</span>
                        </div>

                        <div class="border-t pt-4">
                            <h3 class="font-semibold text-gray-900 mb-2">Location</h3>
                            <p class="text-gray-600">{{ court.address }}</p>
                            <p class="text-gray-600">{{ court.city }}</p>
                        </div>

                        <div v-if="court.description" class="border-t pt-4 mt-4">
                            <h3 class="font-semibold text-gray-900 mb-2">Description</h3>
                            <p class="text-gray-600">{{ court.description }}</p>
                        </div>

                        <div v-if="court.amenities_list && court.amenities_list.length" class="border-t pt-4 mt-4">
                            <h3 class="font-semibold text-gray-900 mb-2">Amenities</h3>
                            <div class="flex flex-wrap gap-2">
                                <span v-for="amenity in court.amenities_list" :key="amenity"
                                    class="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm">
                                    {{ amenity }}
                                </span>
                            </div>
                        </div>

                        <div class="border-t pt-4 mt-4">
                            <h3 class="font-semibold text-gray-900 mb-2">Operating Hours</h3>
                            <p class="text-gray-600">{{ court.opening_time }} - {{ court.closing_time }}</p>
                        </div>

                        <!-- Dynamic Pricing -->
                        <div v-if="court.pricing_rules && court.pricing_rules.length" class="border-t pt-4 mt-4">
                            <h3 class="font-semibold text-gray-900 mb-3">Pricing Schedule</h3>
                            <div class="space-y-2">
                                <div v-for="rule in court.pricing_rules" :key="rule.id"
                                    class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                    <div>
                                        <p class="font-medium text-gray-900">{{ rule.description }}</p>
                                        <p class="text-sm text-gray-600">{{ rule.start_time }} - {{ rule.end_time }}</p>
                                        <p class="text-xs text-gray-500">{{ formatDaysOfWeek(rule.days_of_week) }}</p>
                                    </div>
                                    <span class="text-lg font-bold text-blue-600">Rs {{ rule.hourly_rate }}/hr</span>
                                </div>
                            </div>
                        </div>

                        <!-- Equipment -->
                        <div v-if="court.equipment && court.equipment.length" class="border-t pt-4 mt-4">
                            <h3 class="font-semibold text-gray-900 mb-3">Available Equipment</h3>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                                <div v-for="item in court.equipment" :key="item.id"
                                    class="p-3 border border-gray-200 rounded-lg">
                                    <div class="flex items-center justify-between mb-2">
                                        <p class="font-medium text-gray-900">{{ item.name }}</p>
                                        <span :class="item.quantity_available > 0 ? 'text-green-600' : 'text-red-600'"
                                            class="text-sm font-medium">
                                            {{ item.quantity_available }}/{{ item.quantity_total }} available
                                        </span>
                                    </div>
                                    <p class="text-sm text-gray-600 mb-2">{{ item.description }}</p>
                                    <p class="text-sm font-bold text-blue-600">Rs {{ item.rental_rate }}/session</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Reviews -->
                    <div class="bg-white rounded-xl shadow-md p-6">
                        <h3 class="text-xl font-bold text-gray-900 mb-4">Reviews</h3>
                        <div v-if="reviews.length > 0" class="space-y-4">
                            <div v-for="review in reviews" :key="review.id" class="border-b pb-4 last:border-0">
                                <div class="flex items-start gap-3">
                                    <div
                                        class="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold">
                                        {{ review.player_name.charAt(0).toUpperCase() }}
                                    </div>
                                    <div class="flex-1">
                                        <div class="flex items-center gap-2 mb-1">
                                            <span class="font-semibold">{{ review.player_name }}</span>
                                            <div class="flex">
                                                <svg v-for="i in 5" :key="i" class="w-4 h-4"
                                                    :class="i <= review.rating ? 'text-yellow-400' : 'text-gray-300'"
                                                    fill="currentColor" viewBox="0 0 24 24">
                                                    <path
                                                        d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                                                </svg>
                                            </div>
                                        </div>
                                        <p class="text-gray-600 text-sm">{{ review.review_text }}</p>
                                        <p class="text-gray-400 text-xs mt-1">{{ formatDate(review.created_at) }}</p>
                                        <div v-if="review.owner_response" class="mt-2 ml-4 p-3 bg-gray-50 rounded-lg">
                                            <p class="text-sm font-semibold text-gray-700">Owner's Response</p>
                                            <p class="text-sm text-gray-600">{{ review.owner_response }}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <p v-else class="text-gray-500 text-center py-4">No reviews yet</p>
                    </div>
                </div>

                <!-- Right Column - Booking -->
                <div class="lg:col-span-1">
                    <div class="bg-white rounded-xl shadow-md p-6 sticky top-24">
                        <div class="mb-6">
                            <div class="text-3xl font-bold text-blue-600 mb-1">
                                Rs {{ currentRate }}<span class="text-lg text-gray-600">/hour</span>
                            </div>
                            <p class="text-sm text-gray-500">{{ rateDescription }}</p>
                        </div>

                        <div v-if="bookingSuccess" class="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg">
                            <p class="text-green-800 font-medium">Booking created successfully!</p>
                        </div>

                        <div v-if="bookingError" class="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                            <p class="text-red-800">{{ bookingError }}</p>
                        </div>

                        <form @submit.prevent="handleBooking" class="space-y-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-1">Date</label>
                                <input v-model="bookingForm.date" type="date" :min="minDate" required
                                    @change="loadAvailableSlots"
                                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" />
                            </div>

                            <!-- Available Slots -->
                            <div v-if="bookingForm.date && availableSlots.length > 0">
                                <label class="block text-sm font-medium text-gray-700 mb-2">Available Time Slots</label>
                                <div class="grid grid-cols-2 gap-2 max-h-48 overflow-y-auto">
                                    <button v-for="slot in availableSlots" :key="slot.start_time" type="button"
                                        @click="selectTimeSlot(slot)" :class="[
                                            'px-3 py-2 text-sm font-medium rounded-lg border-2 transition-colors',
                                            isSlotSelected(slot)
                                                ? 'border-blue-600 bg-blue-50 text-blue-700'
                                                : 'border-gray-200 hover:border-blue-300'
                                        ]">
                                        {{ slot.start_time }} - {{ slot.end_time }}
                                    </button>
                                </div>
                            </div>

                            <!-- Manual Time Selection -->
                            <div v-else class="grid grid-cols-2 gap-4">
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">Start Time</label>
                                    <input v-model="bookingForm.start_time" type="time" required
                                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" />
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">End Time</label>
                                    <input v-model="bookingForm.end_time" type="time" required
                                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" />
                                </div>
                            </div>

                            <!-- Equipment Selection -->
                            <div v-if="court.equipment && court.equipment.length > 0">
                                <label class="block text-sm font-medium text-gray-700 mb-2">Rent Equipment
                                    (Optional)</label>
                                <div class="space-y-2 max-h-32 overflow-y-auto">
                                    <label v-for="item in court.equipment.filter(e => e.quantity_available > 0)"
                                        :key="item.id" class="flex items-center gap-2 p-2 border rounded-lg">
                                        <input type="checkbox" :value="item.id" v-model="bookingForm.equipment_rentals"
                                            class="rounded text-blue-600" />
                                        <span class="flex-1 text-sm">{{ item.name }} (Rs {{ item.rental_rate
                                            }})</span>
                                    </label>
                                </div>
                            </div>

                            <!-- Notes -->
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-1">Notes (Optional)</label>
                                <textarea v-model="bookingForm.notes" rows="2"
                                    placeholder="Any special requests or notes..."
                                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 resize-none"></textarea>
                            </div>

                            <div v-if="bookingForm.date && bookingForm.start_time && bookingForm.end_time">
                                <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                                    <p class="text-sm text-blue-800 font-medium">Booking Summary</p>
                                    <div class="mt-2 space-y-1 text-sm text-blue-900">
                                        <div class="flex justify-between">
                                            <span>Court Fee ({{ duration }} hrs)</span>
                                            <span class="font-medium">Rs {{ courtFee }}</span>
                                        </div>
                                        <div v-if="equipmentFee > 0" class="flex justify-between">
                                            <span>Equipment Rental</span>
                                            <span class="font-medium">Rs {{ equipmentFee }}</span>
                                        </div>
                                        <div class="flex justify-between pt-2 border-t border-blue-200 font-bold">
                                            <span>Total</span>
                                            <span>Rs {{ estimatedTotal }}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <button type="submit" :disabled="bookingLoading || !canBook"
                                class="w-full py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold rounded-lg transition-colors">
                                <span v-if="bookingLoading">Processing...</span>
                                <span v-else>Book Now</span>
                            </button>

                            <button v-if="bookingForm.date && bookingForm.start_time && bookingForm.end_time"
                                type="button" @click="checkAvailability" :disabled="availabilityLoading"
                                class="w-full py-2 border-2 border-blue-600 text-blue-600 hover:bg-blue-50 font-semibold rounded-lg transition-colors">
                                <span v-if="availabilityLoading">Checking...</span>
                                <span v-else>Check Availability</span>
                            </button>
                        </form>

                        <div v-if="availabilityMessage" class="mt-4 p-3 rounded-lg"
                            :class="isAvailable ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'">
                            <p class="text-sm font-medium">{{ availabilityMessage }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { courtService } from '@/services/courtService'
import { bookingService } from '@/services/bookingService'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const error = ref(null)
const court = ref(null)
const reviews = ref([])
const availableSlots = ref([])
const currentImageIndex = ref(0)

const bookingForm = ref({
    date: '',
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

const minDate = computed(() => {
    const today = new Date()
    return today.toISOString().split('T')[0]
})

const duration = computed(() => {
    if (!bookingForm.value.start_time || !bookingForm.value.end_time) return 0
    const start = new Date(`2000-01-01 ${bookingForm.value.start_time}`)
    const end = new Date(`2000-01-01 ${bookingForm.value.end_time}`)
    return Math.max(0, (end - start) / (1000 * 60 * 60))
})

const currentRate = computed(() => {
    if (!court.value || !bookingForm.value.start_time || !bookingForm.value.date) {
        return court.value?.base_hourly_rate || 0
    }

    // Check if there's a matching pricing rule
    const dayOfWeek = new Date(bookingForm.value.date).getDay()
    const startTime = bookingForm.value.start_time

    const matchingRule = court.value.pricing_rules?.find(rule => {
        if (!rule.is_active) return false
        const days = rule.days_of_week.split(',').map(d => parseInt(d.trim()))
        if (!days.includes(dayOfWeek)) return false
        return startTime >= rule.start_time && startTime < rule.end_time
    })

    return matchingRule ? matchingRule.hourly_rate : court.value.base_hourly_rate
})

const rateDescription = computed(() => {
    if (!court.value || !bookingForm.value.start_time || !bookingForm.value.date) {
        return 'Base rate'
    }

    const dayOfWeek = new Date(bookingForm.value.date).getDay()
    const startTime = bookingForm.value.start_time

    const matchingRule = court.value.pricing_rules?.find(rule => {
        if (!rule.is_active) return false
        const days = rule.days_of_week.split(',').map(d => parseInt(d.trim()))
        if (!days.includes(dayOfWeek)) return false
        return startTime >= rule.start_time && startTime < rule.end_time
    })

    return matchingRule ? matchingRule.description : 'Base rate'
})

const courtFee = computed(() => {
    return (duration.value * currentRate.value).toFixed(2)
})

const equipmentFee = computed(() => {
    if (!court.value || !bookingForm.value.equipment_rentals.length) return 0
    return bookingForm.value.equipment_rentals.reduce((total, equipId) => {
        const item = court.value.equipment?.find(e => e.id === equipId)
        return total + (item?.rental_rate || 0)
    }, 0)
})

const estimatedTotal = computed(() => {
    return (parseFloat(courtFee.value) + equipmentFee.value).toFixed(2)
})

const canBook = computed(() => {
    return bookingForm.value.date &&
        bookingForm.value.start_time &&
        bookingForm.value.end_time &&
        duration.value > 0
})

const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

const formatDaysOfWeek = (daysStr) => {
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    const indices = daysStr.split(',').map(d => parseInt(d.trim()))
    return indices.map(i => days[i]).join(', ')
}

const loadCourtDetails = async () => {
    loading.value = true
    error.value = null
    try {
        court.value = await courtService.getCourtById(route.params.id)
        await loadReviews()
    } catch (err) {
        console.error('Failed to load court:', err)
        error.value = 'Failed to load court details'
    } finally {
        loading.value = false
    }
}

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
    } catch (err) {
        console.error('Failed to load available slots:', err)
        availableSlots.value = []
    }
}

const selectTimeSlot = (slot) => {
    bookingForm.value.start_time = slot.start_time
    bookingForm.value.end_time = slot.end_time
}

const isSlotSelected = (slot) => {
    return bookingForm.value.start_time === slot.start_time &&
        bookingForm.value.end_time === slot.end_time
}

const checkAvailability = async () => {
    availabilityLoading.value = true
    availabilityMessage.value = null
    try {
        const response = await courtService.checkAvailability(route.params.id, {
            date: bookingForm.value.date,
            start_time: bookingForm.value.start_time,
            end_time: bookingForm.value.end_time
        })
        isAvailable.value = response.available
        availabilityMessage.value = response.message || (response.available ? 'Court is available!' : response.reason)
    } catch (err) {
        availabilityMessage.value = 'Failed to check availability'
        isAvailable.value = false
    } finally {
        availabilityLoading.value = false
    }
}

const handleBooking = async () => {
    bookingLoading.value = true
    bookingError.value = null
    bookingSuccess.value = false

    try {
        const bookingData = {
            court: route.params.id,
            booking_date: bookingForm.value.date,
            start_time: bookingForm.value.start_time,
            end_time: bookingForm.value.end_time,
            payment_method: 'ONLINE',
            base_amount: courtFee.value,
            total_amount: estimatedTotal.value,
            notes: bookingForm.value.notes
        }

        const booking = await bookingService.createBooking(bookingData)

        // Handle equipment rentals
        if (bookingForm.value.equipment_rentals.length > 0) {
            for (const equipId of bookingForm.value.equipment_rentals) {
                await bookingService.rentEquipment(booking.id, equipId, 1)
            }
        }

        bookingSuccess.value = true
        setTimeout(() => {
            router.push('/bookings')
        }, 2000)
    } catch (err) {
        console.error('Booking failed:', err)
        bookingError.value = err.response?.data?.detail || 'Failed to create booking'
    } finally {
        bookingLoading.value = false
    }
}

const goBack = () => router.go(-1)

onMounted(() => {
    loadCourtDetails()
})
</script>