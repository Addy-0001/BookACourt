<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Navigation -->
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
                        <h1 class="text-2xl font-bold text-blue-600">Matches</h1>
                    </div>
                    <div class="flex items-center gap-4">
                        <router-link to="/"
                            class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
                            Home
                        </router-link>
                        <button @click="showCreateModal = true"
                            class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium">
                            Create Match
                        </button>
                    </div>
                </div>
            </div>
        </nav>

        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Filters -->
            <div class="bg-white rounded-xl shadow-md p-6 mb-8">
                <div class="flex items-center gap-4 flex-wrap">
                    <button v-for="filter in filters" :key="filter.value" @click="activeFilter = filter.value" :class="[
                        'px-4 py-2 rounded-lg font-medium transition-colors',
                        activeFilter === filter.value
                            ? 'bg-blue-600 text-white'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    ]">
                        {{ filter.label }}
                    </button>
                </div>
            </div>

            <!-- Loading State -->
            <div v-if="loading" class="flex justify-center py-20">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>

            <!-- Error State -->
            <div v-else-if="error" class="text-center py-20">
                <svg class="w-16 h-16 mx-auto text-red-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p class="text-xl text-gray-600 mb-4">{{ error }}</p>
                <button @click="loadMatches" class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                    Try Again
                </button>
            </div>

            <!-- Matches Grid -->
            <div v-else-if="filteredMatches.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div v-for="match in filteredMatches" :key="match.id"
                    class="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-shadow">
                    <div class="p-6">
                        <div class="flex items-start justify-between mb-4">
                            <div>
                                <h3 class="text-xl font-bold text-gray-900">{{ match.title }}</h3>
                                <p class="text-gray-600 text-sm">{{ match.sport_type }}</p>
                            </div>
                            <span :class="getStatusClass(match.status)"
                                class="px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap">
                                {{ match.status }}
                            </span>
                        </div>

                        <div class="space-y-2 mb-4">
                            <div class="flex items-center gap-2 text-gray-600 text-sm">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                </svg>
                                <span>{{ formatDate(match.match_date) }} at {{ match.match_time }}</span>
                            </div>
                            <div class="flex items-center gap-2 text-gray-600 text-sm">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                                </svg>
                                <span>{{ match.court_name }}</span>
                            </div>
                            <div class="flex items-center gap-2 text-gray-600 text-sm">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                                </svg>
                                <span>{{ match.current_players }}/{{ match.max_players }} players</span>
                            </div>
                            <div class="flex items-center gap-2">
                                <span
                                    class="px-2 py-1 bg-purple-100 text-purple-800 text-xs font-medium rounded-full">{{
                                        match.skill_level }}</span>
                                <span class="text-gray-500 text-xs">• {{ match.duration_hours }}h</span>
                            </div>
                        </div>

                        <p v-if="match.description" class="text-sm text-gray-600 mb-4 line-clamp-2">{{
                            match.description }}</p>

                        <div class="flex items-center gap-2 text-xs text-gray-500 mb-4">
                            <span>Created by {{ match.creator_name }}</span>
                        </div>

                        <button v-if="canJoin(match)" @click="joinMatch(match)"
                            class="w-full py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium">
                            Join Match
                        </button>
                        <button v-else-if="isParticipant(match)" @click="leaveMatch(match)"
                            class="w-full py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium">
                            Leave Match
                        </button>
                        <button v-else-if="match.status === 'FULL'"
                            class="w-full py-2 bg-gray-400 text-white rounded-lg cursor-not-allowed font-medium"
                            disabled>
                            Match Full
                        </button>
                    </div>
                </div>
            </div>

            <!-- Empty State -->
            <div v-else class="text-center py-20">
                <svg class="w-24 h-24 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <p class="text-xl text-gray-600 mb-4">No matches found</p>
                <button @click="showCreateModal = true"
                    class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                    Create a Match
                </button>
            </div>
        </div>

        <!-- Create Match Modal -->
        <div v-if="showCreateModal"
            class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div class="bg-white rounded-xl max-w-2xl w-full p-6 max-h-[90vh] overflow-y-auto">
                <h3 class="text-2xl font-bold text-gray-900 mb-6">Create Match</h3>

                <form @submit.prevent="handleCreateMatch" class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Match Title</label>
                        <input v-model="createForm.title" type="text" required
                            placeholder="e.g., Evening Basketball Game"
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" />
                    </div>

                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Sport Type</label>
                            <select v-model="createForm.sport_type" required
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
                                <option value="">Select sport</option>
                                <option value="Basketball">Basketball</option>
                                <option value="Tennis">Tennis</option>
                                <option value="Badminton">Badminton</option>
                                <option value="Volleyball">Volleyball</option>
                                <option value="Football">Football</option>
                                <option value="Futsal">Futsal</option>
                            </select>
                        </div>

                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Skill Level</label>
                            <select v-model="createForm.skill_level" required
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
                                <option value="ANY">Any Level</option>
                                <option value="BEGINNER">Beginner</option>
                                <option value="INTERMEDIATE">Intermediate</option>
                                <option value="ADVANCED">Advanced</option>
                            </select>
                        </div>
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Court</label>
                        <select v-model="createForm.court" required
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
                            <option value="">Select court</option>
                            <option v-for="court in courts" :key="court.id" :value="court.id">{{ court.name }}</option>
                        </select>
                    </div>

                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Date</label>
                            <input v-model="createForm.match_date" type="date" :min="minDate" required
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" />
                        </div>

                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Time</label>
                            <input v-model="createForm.match_time" type="time" required
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" />
                        </div>
                    </div>

                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Max Players</label>
                            <input v-model.number="createForm.max_players" type="number" min="2" max="20" required
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" />
                        </div>

                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Duration (hours)</label>
                            <input v-model.number="createForm.duration_hours" type="number" min="1" max="8" required
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" />
                        </div>
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Description (Optional)</label>
                        <textarea v-model="createForm.description" rows="3"
                            placeholder="Additional details about the match..."
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 resize-none"></textarea>
                    </div>

                    <div class="flex gap-3 pt-4">
                        <button type="button" @click="showCreateModal = false"
                            class="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">
                            Cancel
                        </button>
                        <button type="submit" :disabled="creating"
                            class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400">
                            {{ creating ? 'Creating...' : 'Create Match' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { bookingService } from '@/services/bookingService'
import { courtService } from '@/services/courtService'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const error = ref(null)
const matches = ref([])
const courts = ref([])
const showCreateModal = ref(false)
const creating = ref(false)
const activeFilter = ref('all')

const filters = [
    { value: 'all', label: 'All Matches' },
    { value: 'open', label: 'Open' },
    { value: 'my', label: 'My Matches' },
    { value: 'joined', label: 'Joined' }
]

const createForm = ref({
    title: '',
    sport_type: '',
    skill_level: 'ANY',
    court: '',
    match_date: '',
    match_time: '',
    max_players: 10,
    duration_hours: 1,
    description: ''
})

const minDate = computed(() => {
    return new Date().toISOString().split('T')[0]
})

const filteredMatches = computed(() => {
    let filtered = matches.value

    switch (activeFilter.value) {
        case 'open':
            filtered = filtered.filter(m => m.status === 'OPEN')
            break
        case 'my':
            filtered = filtered.filter(m => m.created_by === authStore.user?.id)
            break
        case 'joined':
            filtered = filtered.filter(m => isParticipant(m))
            break
    }

    return filtered.sort((a, b) => new Date(a.match_date + ' ' + a.match_time) - new Date(b.match_date + ' ' + b.match_time))
})

const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

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

const isParticipant = (match) => {
    return match.participants?.some(p => p.player === authStore.user?.id)
}

const canJoin = (match) => {
    return match.status === 'OPEN' && !isParticipant(match) && match.created_by !== authStore.user?.id
}

const loadMatches = async () => {
    loading.value = true
    error.value = null
    try {
        const response = await bookingService.getMatches()
        matches.value = response.results || response
    } catch (err) {
        console.error('Failed to load matches:', err)
        error.value = 'Failed to load matches. Please try again.'
    } finally {
        loading.value = false
    }
}

const loadCourts = async () => {
    try {
        const response = await courtService.getCourts()
        courts.value = response.results || response
    } catch (err) {
        console.error('Failed to load courts:', err)
    }
}

const handleCreateMatch = async () => {
    creating.value = true
    try {
        await bookingService.createMatch(createForm.value)
        showCreateModal.value = false
        createForm.value = {
            title: '',
            sport_type: '',
            skill_level: 'ANY',
            court: '',
            match_date: '',
            match_time: '',
            max_players: 10,
            duration_hours: 1,
            description: ''
        }
        await loadMatches()
    } catch (err) {
        console.error('Failed to create match:', err)
        alert('Failed to create match. Please try again.')
    } finally {
        creating.value = false
    }
}

const joinMatch = async (match) => {
    try {
        await bookingService.joinMatch(match.id)
        await loadMatches()
    } catch (err) {
        console.error('Failed to join match:', err)
        alert('Failed to join match. Please try again.')
    }
}

const leaveMatch = async (match) => {
    if (!confirm('Are you sure you want to leave this match?')) return

    try {
        await bookingService.leaveMatch(match.id)
        await loadMatches()
    } catch (err) {
        console.error('Failed to leave match:', err)
        alert('Failed to leave match. Please try again.')
    }
}

const goBack = () => router.go(-1)

onMounted(() => {
    loadMatches()
    loadCourts()
})
</script>