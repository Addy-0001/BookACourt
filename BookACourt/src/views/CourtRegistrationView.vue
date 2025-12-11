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
                        <h1 class="text-2xl font-bold text-blue-600">Court Registration</h1>
                    </div>
                </div>
            </div>
        </nav>

        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Success Message -->
            <div v-if="submitted" class="bg-white rounded-xl shadow-md p-8 text-center">
                <svg class="w-16 h-16 mx-auto text-green-500 mb-4" fill="currentColor" viewBox="0 0 24 24">
                    <path
                        d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
                </svg>
                <h2 class="text-2xl font-bold text-gray-900 mb-2">Registration Submitted!</h2>
                <p class="text-gray-600 mb-6">Your court registration has been submitted for review. We'll notify you
                    once it's approved.</p>
                <router-link to="/"
                    class="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                    Go to Home
                </router-link>
            </div>

            <!-- Registration Form -->
            <div v-else class="bg-white rounded-xl shadow-md p-8">
                <h2 class="text-2xl font-bold text-gray-900 mb-2">Register Your Court</h2>
                <p class="text-gray-600 mb-8">Fill out the form below to get your court listed on our platform.</p>

                <form @submit.prevent="handleSubmit" class="space-y-6">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Court Name *</label>
                        <input v-model="form.court_name" type="text" required
                            placeholder="e.g., Downtown Basketball Arena"
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Description *</label>
                        <textarea v-model="form.description" rows="4" required
                            placeholder="Describe your court, facilities, and what makes it special..."
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"></textarea>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">City *</label>
                            <input v-model="form.city" type="text" required placeholder="e.g., Kathmandu"
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Phone Number *</label>
                            <input v-model="form.phone_number" type="tel" required placeholder="+977 9800000000"
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
                        </div>
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Full Address *</label>
                        <textarea v-model="form.address" rows="2" required
                            placeholder="Full street address including landmarks"
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"></textarea>
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Registration Documents *</label>
                        <input @change="handleDocumentUpload" type="file" accept=".pdf,.jpg,.jpeg,.png" required
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
                        <p class="mt-1 text-sm text-gray-500">Upload business registration or ownership documents (PDF,
                            JPG, PNG)</p>
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Court Images *</label>
                        <input @change="handleImagesUpload" type="file" accept="image/*" multiple required
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
                        <p class="mt-1 text-sm text-gray-500">Upload photos of your court (multiple images allowed)</p>
                    </div>

                    <div v-if="error" class="p-4 bg-red-50 border border-red-200 rounded-lg">
                        <p class="text-sm text-red-800">{{ error }}</p>
                    </div>

                    <div class="flex gap-3 pt-4">
                        <button type="button" @click="goBack"
                            class="flex-1 px-6 py-3 border border-gray-300 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors font-medium">
                            Cancel
                        </button>
                        <button type="submit" :disabled="submitting"
                            class="flex-1 px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white rounded-lg transition-colors font-medium">
                            <span v-if="submitting">Submitting...</span>
                            <span v-else>Submit Registration</span>
                        </button>
                    </div>
                </form>
            </div>

            <!-- My Registrations -->
            <div v-if="!submitted" class="mt-8">
                <h2 class="text-xl font-bold text-gray-900 mb-4">My Registrations</h2>
                <div v-if="loadingRegistrations" class="flex justify-center py-10">
                    <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600"></div>
                </div>
                <div v-else-if="registrations.length === 0"
                    class="bg-white rounded-xl shadow-md p-6 text-center text-gray-500">
                    No previous registrations
                </div>
                <div v-else class="space-y-4">
                    <div v-for="registration in registrations" :key="registration.id"
                        class="bg-white rounded-xl shadow-md p-6">
                        <div class="flex items-start justify-between">
                            <div>
                                <h3 class="font-bold text-gray-900 text-lg">{{ registration.court_name }}</h3>
                                <p class="text-gray-600">{{ registration.city }}</p>
                                <p class="text-sm text-gray-500 mt-1">Submitted {{ formatDate(registration.created_at)
                                    }}</p>
                            </div>
                            <span :class="getStatusClass(registration.status)"
                                class="px-3 py-1 rounded-full text-sm font-medium">
                                {{ registration.status }}
                            </span>
                        </div>
                        <div v-if="registration.rejection_reason"
                            class="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                            <p class="text-sm text-red-800"><strong>Rejection Reason:</strong> {{
                                registration.rejection_reason }}</p>
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
        'PENDING': 'bg-yellow-100 text-yellow-800',
        'APPROVED': 'bg-green-100 text-green-800',
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
            // For multiple images, we append the first one (API might accept multiple)
            formData.append('court_images', form.value.court_images[0])
        }

        await courtService.submitRegistration(Object.fromEntries(formData))
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