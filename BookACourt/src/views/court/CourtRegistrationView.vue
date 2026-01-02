<!-- views/court/CourtRegistrationView.vue -->
<template>
    <div class="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50">

        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
            <!-- Success Message -->
            <div v-if="submitted" class="bg-white rounded-2xl shadow-xl border border-emerald-100 p-10 text-center">
                <div class="w-20 h-20 mx-auto bg-emerald-100 rounded-full flex items-center justify-center mb-6">
                    <svg class="w-12 h-12 text-emerald-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd"
                            d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                            clip-rule="evenodd" />
                    </svg>
                </div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Registration Submitted!</h2>
                <p class="text-lg text-gray-600 mb-8 max-w-xl mx-auto">
                    Your court registration has been successfully submitted for review.<br />
                    We'll notify you once it's approved — usually within 2-5 business days.
                </p>
                <router-link to="/"
                    class="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all">
                    Return to Home
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M17 8l4 4m0 0l-4 4m4-4H3" />
                    </svg>
                </router-link>
            </div>

            <!-- Registration Form -->
            <div v-else class="bg-white rounded-2xl shadow-xl border border-emerald-100 p-8 md:p-10">
                <h2 class="text-3xl font-bold text-gray-900 mb-2">Register Your Court</h2>
                <p class="text-lg text-gray-600 mb-10">
                    Add your sports venue to our platform and reach thousands of players.
                </p>

                <form @submit.prevent="handleSubmit" class="space-y-8">
                    <!-- Court Name -->
                    <div class="space-y-2">
                        <label class="block text-sm font-semibold text-gray-700">Court Name *</label>
                        <input v-model="form.court_name" type="text" required placeholder="e.g., Downtown Futsal Arena"
                            class="w-full px-5 py-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all text-lg" />
                    </div>

                    <!-- Description -->
                    <div class="space-y-2">
                        <label class="block text-sm font-semibold text-gray-700">Description *</label>
                        <textarea v-model="form.description" rows="5" required
                            placeholder="Tell players about your court — surface type, lighting, parking, amenities, atmosphere..."
                            class="w-full px-5 py-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all resize-none text-lg"></textarea>
                    </div>

                    <!-- City & Phone -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="space-y-2">
                            <label class="block text-sm font-semibold text-gray-700">City *</label>
                            <input v-model="form.city" type="text" required
                                placeholder="e.g., Kathmandu, Lalitpur, Pokhara"
                                class="w-full px-5 py-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all text-lg" />
                        </div>

                        <div class="space-y-2">
                            <label class="block text-sm font-semibold text-gray-700">Phone Number *</label>
                            <input v-model="form.phone_number" type="tel" required placeholder="+977 9800000000"
                                class="w-full px-5 py-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all text-lg" />
                        </div>
                    </div>

                    <!-- Full Address -->
                    <div class="space-y-2">
                        <label class="block text-sm font-semibold text-gray-700">Full Address *</label>
                        <textarea v-model="form.address" rows="3" required
                            placeholder="Street address, landmarks, ward number, etc."
                            class="w-full px-5 py-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all resize-none text-lg"></textarea>
                    </div>

                    <!-- Documents -->
                    <div class="space-y-2">
                        <label class="block text-sm font-semibold text-gray-700">Registration Documents * <span
                                class="text-xs text-gray-500">(PDF, JPG, PNG)</span></label>
                        <div
                            class="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-emerald-400 transition-colors cursor-pointer bg-gray-50">
                            <input @change="handleDocumentUpload" type="file" accept=".pdf,.jpg,.jpeg,.png" required
                                class="hidden" id="documents" />
                            <label for="documents" class="cursor-pointer">
                                <svg class="w-12 h-12 mx-auto text-emerald-500 mb-4" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                                </svg>
                                <p class="text-lg font-medium text-gray-700 mb-1">Click to upload or drag & drop</p>
                                <p class="text-sm text-gray-500">Business registration / Ownership proof</p>
                                <p v-if="form.registration_documents" class="mt-3 text-sm text-emerald-700 font-medium">
                                    Selected: {{ form.registration_documents.name }}
                                </p>
                            </label>
                        </div>
                    </div>

                    <!-- Court Images -->
                    <div class="space-y-2">
                        <label class="block text-sm font-semibold text-gray-700">Court Images * <span
                                class="text-xs text-gray-500">(multiple allowed)</span></label>
                        <div
                            class="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-emerald-400 transition-colors cursor-pointer bg-gray-50">
                            <input @change="handleImagesUpload" type="file" accept="image/*" multiple required
                                class="hidden" id="images" />
                            <label for="images" class="cursor-pointer">
                                <svg class="w-12 h-12 mx-auto text-emerald-500 mb-4" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                </svg>
                                <p class="text-lg font-medium text-gray-700 mb-1">Upload court photos</p>
                                <p class="text-sm text-gray-500">Show lighting, surface, surroundings — multiple images
                                    allowed</p>
                                <p v-if="form.court_images?.length" class="mt-3 text-sm text-emerald-700 font-medium">
                                    {{ form.court_images.length }} image{{ form.court_images.length !== 1 ? 's' : '' }}
                                    selected
                                </p>
                            </label>
                        </div>
                    </div>

                    <!-- Submit / Cancel -->
                    <div class="flex flex-col sm:flex-row gap-4 pt-6">
                        <button type="button" @click="goBack"
                            class="flex-1 px-8 py-4 border-2 border-gray-300 text-gray-700 hover:bg-gray-50 rounded-xl font-semibold transition-colors text-lg">
                            Cancel
                        </button>

                        <button type="submit" :disabled="submitting"
                            class="flex-1 px-8 py-4 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white rounded-xl font-bold shadow-lg hover:shadow-xl transition-all disabled:opacity-60 disabled:cursor-not-allowed text-lg">
                            {{ submitting ? 'Submitting...' : 'Submit Registration' }}
                        </button>
                    </div>
                </form>
            </div>

            <!-- My Registrations -->
            <div v-if="!submitted" class="mt-12">
                <h2 class="text-2xl font-bold text-gray-900 mb-6">My Previous Registrations</h2>

                <div v-if="loadingRegistrations" class="flex justify-center py-12">
                    <div class="w-12 h-12 border-4 border-emerald-200 border-t-emerald-600 rounded-full animate-spin">
                    </div>
                </div>

                <div v-else-if="registrations.length === 0"
                    class="bg-white rounded-2xl shadow-md border border-emerald-100 p-10 text-center">
                    <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <p class="text-xl text-gray-600">You haven't submitted any court registrations yet</p>
                </div>

                <div v-else class="space-y-6">
                    <div v-for="registration in registrations" :key="registration.id"
                        class="bg-white rounded-2xl shadow-md border border-gray-100 p-6 hover:shadow-lg transition-shadow">
                        <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
                            <div>
                                <h3 class="text-xl font-bold text-gray-900 mb-1">{{ registration.court_name }}</h3>
                                <p class="text-gray-600 mb-1">{{ registration.city }}</p>
                                <p class="text-sm text-gray-500">
                                    Submitted on {{ formatDate(registration.created_at) }}
                                </p>
                            </div>

                            <span :class="getStatusClass(registration.status)"
                                class="inline-flex px-4 py-1.5 rounded-full text-sm font-semibold self-start">
                                {{ registration.status }}
                            </span>
                        </div>

                        <div v-if="registration.rejection_reason"
                            class="mt-6 p-4 bg-red-50 border border-red-200 rounded-xl">
                            <p class="text-sm text-red-800">
                                <strong class="block mb-1">Rejection Reason:</strong>
                                {{ registration.rejection_reason }}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { courtService } from '@/services/courtService'

const router = useRouter()

const submitting = ref(false)
const submitted = ref(false)
const loadingRegistrations = ref(false)
const error = ref(null)
const registrations = ref([])

const form = ref({
    court_name: '',
    description: '',
    address: '',
    city: '',
    phone_number: '',
    registration_documents: null,
    court_images: null
})

const handleDocumentUpload = (event) => {
    const file = event.target.files[0]
    if (file) {
        form.value.registration_documents = file
    }
}

const handleImagesUpload = (event) => {
    const files = Array.from(event.target.files)
    if (files.length > 0) {
        form.value.court_images = files
    }
}

const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

const getStatusClass = (status) => {
    const classes = {
        'PENDING': 'bg-amber-100 text-amber-800',
        'APPROVED': 'bg-emerald-100 text-emerald-800',
        'REJECTED': 'bg-red-100 text-red-800'
    }
    return classes[status] || 'bg-gray-100 text-gray-800'
}

const handleSubmit = async () => {
    submitting.value = true
    error.value = null

    try {
        const formData = new FormData()
        formData.append('court_name', form.value.court_name)
        formData.append('description', form.value.description)
        formData.append('address', form.value.address)
        formData.append('city', form.value.city)
        formData.append('phone_number', form.value.phone_number)

        if (form.value.registration_documents) {
            formData.append('registration_documents', form.value.registration_documents)
        }

        if (form.value.court_images) {
            form.value.court_images.forEach((image, index) => {
                formData.append(`court_images[${index}]`, image)
            })
        }

        await courtService.submitRegistration(formData)
        submitted.value = true
    } catch (err) {
        console.error('Failed to submit registration:', err)
        error.value = err.response?.data?.detail || 'Failed to submit registration. Please try again.'
    } finally {
        submitting.value = false
    }
}

const loadMyRegistrations = async () => {
    loadingRegistrations.value = true
    try {
        const response = await courtService.getMyRegistrations()
        registrations.value = response.results || response
    } catch (err) {
        console.error('Failed to load registrations:', err)
    } finally {
        loadingRegistrations.value = false
    }
}

const goBack = () => router.go(-1)

onMounted(() => {
    loadMyRegistrations()
})
</script>