<!-- views/profile/PreferencesView.vue -->
<template>
    <div class="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
            <!-- Header -->
            <div class="mb-10">
                <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-2">Preferences</h1>
                <p class="text-lg text-gray-600">Customize your notifications, sports, and booking preferences</p>
            </div>

            <!-- Loading State -->
            <div v-if="loading" class="flex justify-center py-32">
                <div class="w-14 h-14 border-4 border-emerald-200 border-t-emerald-600 rounded-full animate-spin"></div>
            </div>

            <div v-else>
                <!-- Success Message -->
                <div v-if="successMessage"
                    class="mb-8 p-5 bg-emerald-50 border border-emerald-200 rounded-xl flex items-center gap-3 text-emerald-800 font-medium shadow-sm">
                    <svg class="w-6 h-6 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd"
                            d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                            clip-rule="evenodd" />
                    </svg>
                    <span>{{ successMessage }}</span>
                </div>

                <!-- Notification Preferences -->
                <div class="bg-white rounded-2xl shadow-xl border border-emerald-100 p-8 md:p-10 mb-10">
                    <h2 class="text-2xl font-bold text-gray-900 mb-6">Notification Preferences</h2>
                    <p class="text-gray-600 mb-8">Choose how you'd like to be notified about bookings and updates</p>

                    <div class="space-y-5">
                        <label
                            class="flex items-start gap-4 p-6 bg-gray-50 hover:bg-emerald-50 border border-gray-200 hover:border-emerald-300 rounded-xl transition-all cursor-pointer group">
                            <input v-model="preferences.email_notifications" type="checkbox"
                                class="mt-1.5 w-5 h-5 rounded border-gray-300 text-emerald-600 focus:ring-emerald-500" />
                            <div>
                                <p class="font-semibold text-gray-900 group-hover:text-emerald-800 transition-colors">
                                    Email Notifications</p>
                                <p class="text-sm text-gray-600 mt-1">Receive booking confirmations, reminders & updates
                                    via email</p>
                            </div>
                        </label>

                        <label
                            class="flex items-start gap-4 p-6 bg-gray-50 hover:bg-emerald-50 border border-gray-200 hover:border-emerald-300 rounded-xl transition-all cursor-pointer group">
                            <input v-model="preferences.sms_notifications" type="checkbox"
                                class="mt-1.5 w-5 h-5 rounded border-gray-300 text-emerald-600 focus:ring-emerald-500" />
                            <div>
                                <p class="font-semibold text-gray-900 group-hover:text-emerald-800 transition-colors">
                                    SMS Notifications</p>
                                <p class="text-sm text-gray-600 mt-1">Get important booking reminders & urgent updates
                                    via text message</p>
                            </div>
                        </label>

                        <label
                            class="flex items-start gap-4 p-6 bg-gray-50 hover:bg-emerald-50 border border-gray-200 hover:border-emerald-300 rounded-xl transition-all cursor-pointer group">
                            <input v-model="preferences.push_notifications" type="checkbox"
                                class="mt-1.5 w-5 h-5 rounded border-gray-300 text-emerald-600 focus:ring-emerald-500" />
                            <div>
                                <p class="font-semibold text-gray-900 group-hover:text-emerald-800 transition-colors">
                                    Push Notifications</p>
                                <p class="text-sm text-gray-600 mt-1">Real-time alerts on your phone for booking changes
                                    & reminders</p>
                            </div>
                        </label>
                    </div>
                </div>

                <!-- Sport Preferences -->
                <div class="bg-white rounded-2xl shadow-xl border border-emerald-100 p-8 md:p-10 mb-10">
                    <h2 class="text-2xl font-bold text-gray-900 mb-6">Sport Preferences</h2>
                    <p class="text-gray-600 mb-6">Tell us which sports you love — we'll help you discover great courts
                        faster</p>

                    <div class="space-y-2">
                        <label class="block text-sm font-semibold text-gray-700">Preferred Sports</label>
                        <input v-model="preferences.preferred_sports" type="text"
                            placeholder="e.g., Basketball, Futsal, Tennis, Badminton"
                            class="w-full px-5 py-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all text-lg" />
                        <p class="mt-2 text-sm text-gray-500">Separate multiple sports with commas</p>
                    </div>
                </div>

                <!-- Time Preferences -->
                <div class="bg-white rounded-2xl shadow-xl border border-emerald-100 p-8 md:p-10 mb-10">
                    <h2 class="text-2xl font-bold text-gray-900 mb-6">Preferred Playing Times</h2>
                    <p class="text-gray-600 mb-6">Help us suggest courts available when you're most likely to play</p>

                    <div class="space-y-2">
                        <label class="block text-sm font-semibold text-gray-700">Preferred Time Slots</label>
                        <input v-model="preferences.preferred_time_slots" type="text"
                            placeholder="e.g., Morning (6-10 AM), Evening (6-10 PM), Weekends"
                            class="w-full px-5 py-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all text-lg" />
                        <p class="mt-2 text-sm text-gray-500">You can write any description that suits your schedule</p>
                    </div>
                </div>

                <!-- Save Button -->
                <div class="flex justify-end">
                    <button @click="handleSave" :disabled="saving"
                        class="px-10 py-4 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all disabled:opacity-60 disabled:cursor-not-allowed flex items-center gap-3 text-lg">
                        <svg v-if="saving" class="animate-spin h-6 w-6" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4">
                            </circle>
                            <path class="opacity-75" fill="currentColor"
                                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                            </path>
                        </svg>
                        <span>{{ saving ? 'Saving...' : 'Save Preferences' }}</span>
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

onMounted(() => {
    loadPreferences()
})
</script>