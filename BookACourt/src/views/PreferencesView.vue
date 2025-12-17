<template>
    <div class="min-h-screen bg-gray-50">

        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Loading -->
            <div v-if="loading" class="flex justify-center py-20">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>

            <div v-else>
                <div v-if="successMessage"
                    class="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg flex items-center gap-3">
                    <svg class="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd"
                            d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                            clip-rule="evenodd" />
                    </svg>
                    <p class="text-green-800 font-medium">{{ successMessage }}</p>
                </div>

                <!-- Notification Preferences -->
                <div class="bg-white rounded-xl shadow-md p-8 mb-8">
                    <h2 class="text-2xl font-bold text-gray-900 mb-6">Notification Preferences</h2>
                    <div class="space-y-4">
                        <label
                            class="flex items-start gap-4 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer">
                            <input v-model="preferences.email_notifications" type="checkbox"
                                class="mt-1 rounded text-blue-600 focus:ring-2 focus:ring-blue-500" />
                            <div>
                                <p class="font-medium text-gray-900">Email Notifications</p>
                                <p class="text-sm text-gray-600">Receive booking confirmations and updates via email</p>
                            </div>
                        </label>

                        <label
                            class="flex items-start gap-4 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer">
                            <input v-model="preferences.sms_notifications" type="checkbox"
                                class="mt-1 rounded text-blue-600 focus:ring-2 focus:ring-blue-500" />
                            <div>
                                <p class="font-medium text-gray-900">SMS Notifications</p>
                                <p class="text-sm text-gray-600">Receive booking reminders via text message</p>
                            </div>
                        </label>

                        <label
                            class="flex items-start gap-4 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer">
                            <input v-model="preferences.push_notifications" type="checkbox"
                                class="mt-1 rounded text-blue-600 focus:ring-2 focus:ring-blue-500" />
                            <div>
                                <p class="font-medium text-gray-900">Push Notifications</p>
                                <p class="text-sm text-gray-600">Receive real-time updates about your bookings</p>
                            </div>
                        </label>
                    </div>
                </div>

                <!-- Sport Preferences -->
                <div class="bg-white rounded-xl shadow-md p-8 mb-8">
                    <h2 class="text-2xl font-bold text-gray-900 mb-6">Sport Preferences</h2>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Preferred Sports</label>
                        <input v-model="preferences.preferred_sports" type="text"
                            placeholder="e.g., Basketball, Tennis, Badminton"
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
                        <p class="mt-1 text-sm text-gray-500">Separate multiple sports with commas</p>
                    </div>
                </div>

                <!-- Time Preferences -->
                <div class="bg-white rounded-xl shadow-md p-8 mb-8">
                    <h2 class="text-2xl font-bold text-gray-900 mb-6">Time Preferences</h2>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Preferred Time Slots</label>
                        <input v-model="preferences.preferred_time_slots" type="text"
                            placeholder="e.g., Morning (6-10 AM), Evening (6-10 PM)"
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
                        <p class="mt-1 text-sm text-gray-500">Help us suggest courts available at your preferred times
                        </p>
                    </div>
                </div>

                <!-- Save Button -->
                <div class="flex justify-end">
                    <button @click="handleSave" :disabled="saving"
                        class="px-8 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white rounded-lg transition-colors font-medium flex items-center gap-2">
                        <svg v-if="saving" class="animate-spin h-5 w-5" fill="none" stroke="currentColor"
                            viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                        <span v-if="saving">Saving...</span>
                        <span v-else>Save Preferences</span>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { userService } from '@/services/userService'

const router = useRouter()

const loading = ref(true)
const saving = ref(false)
const successMessage = ref('')

const preferences = ref({
    email_notifications: true,
    sms_notifications: true,
    push_notifications: true,
    preferred_sports: '',
    preferred_time_slots: ''
})

const loadPreferences = async () => {
    loading.value = true
    try {
        const data = await userService.getMyPreferences()
        if (data) {
            preferences.value = {
                email_notifications: data.email_notifications ?? true,
                sms_notifications: data.sms_notifications ?? true,
                push_notifications: data.push_notifications ?? true,
                preferred_sports: data.preferred_sports || '',
                preferred_time_slots: data.preferred_time_slots || ''
            }
        }
    } catch (err) {
        console.error('Failed to load preferences:', err)
    } finally {
        loading.value = false
    }
}

const handleSave = async () => {
    saving.value = true
    successMessage.value = ''

    try {
        await userService.updateMyPreferences(preferences.value)
        successMessage.value = 'Preferences saved successfully!'
        setTimeout(() => {
            successMessage.value = ''
        }, 3000)
    } catch (err) {
        console.error('Failed to save preferences:', err)
        alert('Failed to save preferences. Please try again.')
    } finally {
        saving.value = false
    }
}

const goBack = () => router.go(-1)

onMounted(() => {
    loadPreferences()
})
</script>