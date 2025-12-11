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
                        <h1 class="text-2xl font-bold text-blue-600">Match Details</h1>
                    </div>
                </div>
            </div>
        </nav>

        <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
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
                <p class="text-xl text-gray-600">{{ error }}</p>
            </div>

            <!-- Match Details -->
            <div v-else-if="match">
                <!-- Match Header -->
                <div class="bg-white rounded-xl shadow-md p-8 mb-8">
                    <div class="flex items-start justify-between mb-6">
                        <div>
                            <h2 class="text-3xl font-bold text-gray-900 mb-2">{{ match.title }}</h2>
                            <p class="text-gray-600">{{ match.sport_type }}</p>
                        </div>
                        <span :class="getStatusClass(match.status)" class="px-4 py-2 rounded-full text-sm font-medium">
                            {{ match.status }}
                        </span>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                        <div class="flex items-center gap-3">
                            <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                            <div>
                                <p class="text-sm text-gray-600">Date</p>
                                <p class="font-medium text-gray-900">{{ formatDate(match.match_date) }}</p>
                            </div>
                        </div>

                        <div class="flex items-center gap-3">
                            <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <div>
                                <p class="text-sm text-gray-600">Time</p>
                                <p class="font-medium text-gray-900">{{ match.match_time }}</p>
                            </div>
                        </div>

                        <div class="flex items-center gap-3">
                            <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                            </svg>
                            <div>
                                <p class="text-sm text-gray-600">Players</p>
                                <p class="font-medium text-gray-900">{{ match.current_players }}/{{ match.max_players }}
                                </p>
                            </div>
                        </div>
                    </div>

                    <div class="flex items-center gap-4 mb-6">
                        <span class="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-medium">
                            {{ match.skill_level || 'Any Level' }}
                        </span>
                        <span class="text-gray-600">
                            Court: <span class="font-medium text-gray-900">{{ match.court_name }}</span>
                        </span>
                    </div>

                    <div v-if="match.description" class="mb-6 p-4 bg-gray-50 rounded-lg">
                        <p class="text-gray-700">{{ match.description }}</p>
                    </div>

                    <!-- Actions -->
                    <div class="flex gap-3">
                        <button v-if="canJoin" @click="handleJoin" :disabled="actionLoading"
                            class="flex-1 px-6 py-3 bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white rounded-lg transition-colors font-medium">
                            {{ actionLoading ? 'Joining...' : 'Join Match' }}
                        </button>
                        <button v-if="canLeave" @click="handleLeave" :disabled="actionLoading"
                            class="flex-1 px-6 py-3 bg-red-600 hover:bg-red-700 disabled:bg-gray-400 text-white rounded-lg transition-colors font-medium">
                            {{ actionLoading ? 'Leaving...' : 'Leave Match' }}
                        </button>
                        <button v-if="canCancel" @click="showCancelModal = true"
                            class="px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors font-medium">
                            Cancel Match
                        </button>
                    </div>
                </div>

                <!-- Participants -->
                <div class="bg-white rounded-xl shadow-md p-8">
                    <h3 class="text-xl font-bold text-gray-900 mb-6">Participants</h3>
                    <div class="space-y-3">
                        <div v-for="participant in match.participants" :key="participant.id"
                            class="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                            <div class="flex items-center gap-3">
                                <div
                                    class="w-12 h-12 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold">
                                    {{ participant.player_name.charAt(0).toUpperCase() }}
                                </div>
                                <div>
                                    <p class="font-medium text-gray-900">{{ participant.player_name }}</p>
                                    <p class="text-sm text-gray-600">Joined {{ formatDateTime(participant.joined_at) }}
                                    </p>
                                </div>
                            </div>
                            <div class="flex items-center gap-2">
                                <span v-if="participant.player === match.created_by"
                                    class="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-medium">
                                    Organizer
                                </span>
                                <span v-if="participant.is_confirmed"
                                    class="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                                    Confirmed
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Cancel Modal -->
        <div v-if="showCancelModal"
            class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div class="bg-white rounded-xl max-w-md w-full p-6">
                <h3 class="text-xl font-bold text-gray-900 mb-4">Cancel Match</h3>
                <p class="text-gray-600 mb-4">Are you sure you want to cancel this match? All participants will be
                    notified.</p>
                <textarea v-model="cancelReason" placeholder="Reason for cancellation (optional)"
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg mb-4" rows="3"></textarea>
                <div class="flex gap-3">
                    <button @click="showCancelModal = false"
                        class="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">
                        Keep Match
                    </button>
                    <button @click="handleCancel" :disabled="actionLoading"
                        class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:bg-gray-400">
                        {{ actionLoading ? 'Cancelling...' : 'Cancel Match' }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { bookingService } from '@/services/bookingService'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const actionLoading = ref(false)
const error = ref(null)
const match = ref(null)
const showCancelModal = ref(false)
const cancelReason = ref('')

const currentUserId = computed(() => JSON.parse(localStorage.getItem('user'))?.id)

const isParticipant = computed(() => {
    if (!match.value || !currentUserId.value) return false
    return match.value.participants?.some(p => p.player === currentUserId.value)
})

const isCreator = computed(() => {
    return match.value?.created_by === currentUserId.value
})

const canJoin = computed(() => {
    return match.value?.status === 'OPEN' && !isParticipant.value && !match.value.is_full
})

const canLeave = computed(() => {
    return isParticipant.value && !isCreator.value && ['OPEN', 'FULL'].includes(match.value?.status)
})

const canCancel = computed(() => {
    return isCreator.value && ['OPEN', 'FULL'].includes(match.value?.status)
})

const getStatusClass = (status) => {
    const classes = {
        'OPEN': 'bg-green-100 text-green-800',
        'FULL': 'bg-blue-100 text-blue-800',
        'IN_PROGRESS': 'bg-purple-100 text-purple-800',
        'COMPLETED': 'bg-gray-100 text-gray-800',
        'CANCELLED': 'bg-red-100 text-red-800'
    }
    return classes[status] || 'bg-gray-100 text-gray-800'
}

const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

const formatDateTime = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

const loadMatch = async () => {
    loading.value = true
    error.value = null

    try {
        match.value = await bookingService.getMatchById(route.params.id)
    } catch (err) {
        console.error('Failed to load match:', err)
        error.value = 'Failed to load match details'
    } finally {
        loading.value = false
    }
}

const handleJoin = async () => {
    actionLoading.value = true

    try {
        await bookingService.joinMatch(route.params.id)
        await loadMatch()
    } catch (err) {
        console.error('Failed to join match:', err)
        alert(err.response?.data?.detail || 'Failed to join match')
    } finally {
        actionLoading.value = false
    }
}

const handleLeave = async () => {
    if (!confirm('Are you sure you want to leave this match?')) return

    actionLoading.value = true

    try {
        await bookingService.leaveMatch(route.params.id)
        await loadMatch()
    } catch (err) {
        console.error('Failed to leave match:', err)
        alert(err.response?.data?.detail || 'Failed to leave match')
    } finally {
        actionLoading.value = false
    }
}

const handleCancel = async () => {
    actionLoading.value = true

    try {
        await bookingService.cancelMatch(route.params.id, cancelReason.value)
        showCancelModal.value = false
        router.push('/matches')
    } catch (err) {
        console.error('Failed to cancel match:', err)
        alert(err.response?.data?.detail || 'Failed to cancel match')
    } finally {
        actionLoading.value = false
    }
}

const goBack = () => router.go(-1)

onMounted(() => {
    loadMatch()
})
</script>