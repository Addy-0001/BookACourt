<!-- views/profile/FriendsView.vue -->
<template>
    <div class="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
            <!-- Header -->
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-6 mb-10">
                <div>
                    <h1 class="text-3xl sm:text-4xl font-bold text-gray-900">Friends & Players</h1>
                    <p class="mt-2 text-lg text-gray-600">Connect with other players and grow your sports circle</p>
                </div>

                <router-link to="/friends/find"
                    class="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white rounded-xl font-semibold shadow-md hover:shadow-lg transition-all">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                    </svg>
                    Find Players
                </router-link>
            </div>

            <!-- Tabs -->
            <div class="bg-white rounded-2xl shadow-md border border-emerald-100 overflow-hidden mb-10">
                <div class="flex border-b border-emerald-100 overflow-x-auto">
                    <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id" :class="[
                        'flex-1 min-w-[120px] px-6 py-5 text-center font-medium transition-all',
                        activeTab === tab.id
                            ? 'text-emerald-700 border-b-4 border-emerald-600 bg-emerald-50/50'
                            : 'text-gray-600 hover:text-emerald-700 hover:bg-emerald-50/30'
                    ]">
                        {{ tab.label }}
                        <span v-if="tab.count > 0"
                            class="ml-2 px-2.5 py-1 bg-emerald-100 text-emerald-800 rounded-full text-xs font-semibold">
                            {{ tab.count }}
                        </span>
                    </button>
                </div>
            </div>

            <!-- Loading -->
            <div v-if="loading" class="flex justify-center py-32">
                <div class="w-14 h-14 border-4 border-emerald-200 border-t-emerald-600 rounded-full animate-spin"></div>
            </div>

            <!-- My Friends Tab -->
            <div v-else-if="activeTab === 'friends'">
                <div v-if="friends.length === 0"
                    class="text-center py-20 bg-white rounded-2xl shadow-md border border-emerald-100 p-12">
                    <svg class="w-24 h-24 mx-auto text-emerald-400 mb-6" fill="none" stroke="currentColor"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                    <h3 class="text-2xl font-bold text-gray-900 mb-3">No friends yet</h3>
                    <p class="text-lg text-gray-600 mb-8">Start connecting with players to organize games together!</p>
                    <router-link to="/friends/find"
                        class="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all">
                        Find Players Now
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M17 8l4 4m0 0l-4 4m4-4H3" />
                        </svg>
                    </router-link>
                </div>

                <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div v-for="friendship in friends" :key="friendship.id"
                        class="bg-white rounded-2xl shadow-md border border-gray-100 p-6 hover:shadow-xl transition-all duration-300">
                        <div class="flex items-center gap-4 mb-5">
                            <div
                                class="w-16 h-16 rounded-full bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center text-white text-2xl font-bold shadow-md ring-2 ring-emerald-100">
                                {{ getFriendName(friendship).charAt(0).toUpperCase() }}
                            </div>
                            <div>
                                <h3 class="text-xl font-bold text-gray-900">{{ getFriendName(friendship) }}</h3>
                                <p class="text-sm text-gray-600 mt-1">{{ getFriendDetails(friendship).phone_number }}
                                </p>
                            </div>
                        </div>

                        <div class="flex gap-3">
                            <button @click="removeFriend(friendship.id)"
                                class="flex-1 px-5 py-3 bg-red-50 hover:bg-red-100 text-red-700 rounded-xl font-medium transition-colors border border-red-200">
                                Remove Friend
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Pending Requests Tab -->
            <div v-else-if="activeTab === 'pending'">
                <div v-if="pendingRequests.length === 0"
                    class="text-center py-20 bg-white rounded-2xl shadow-md border border-emerald-100 p-12">
                    <svg class="w-24 h-24 mx-auto text-emerald-400 mb-6" fill="none" stroke="currentColor"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <h3 class="text-2xl font-bold text-gray-900 mb-3">No pending requests</h3>
                    <p class="text-lg text-gray-600">When someone sends you a friend request, it will appear here.</p>
                </div>

                <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div v-for="request in pendingRequests" :key="request.id"
                        class="bg-white rounded-2xl shadow-md border border-gray-100 p-6 hover:shadow-xl transition-all duration-300">
                        <div class="flex items-center gap-4 mb-5">
                            <div
                                class="w-16 h-16 rounded-full bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center text-white text-2xl font-bold shadow-md ring-2 ring-emerald-100">
                                {{ request.from_user_details?.full_name?.charAt(0).toUpperCase() || '?' }}
                            </div>
                            <div>
                                <h3 class="text-xl font-bold text-gray-900">{{ request.from_user_details?.full_name ||
                                    'Player' }}</h3>
                                <p class="text-sm text-gray-600 mt-1">{{ request.from_user_details?.phone_number || '—'
                                    }}</p>
                                <p class="text-xs text-gray-500 mt-1">Requested {{ formatDate(request.created_at) }}</p>
                            </div>
                        </div>

                        <div class="flex gap-3">
                            <button @click="acceptRequest(request.id)"
                                class="flex-1 px-5 py-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-medium transition-colors shadow-sm">
                                Accept
                            </button>
                            <button @click="rejectRequest(request.id)"
                                class="flex-1 px-5 py-3 bg-gray-100 hover:bg-gray-200 text-gray-800 rounded-xl font-medium transition-colors">
                                Decline
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Sent Requests Tab -->
            <div v-else-if="activeTab === 'sent'">
                <div v-if="sentRequests.length === 0"
                    class="text-center py-20 bg-white rounded-2xl shadow-md border border-emerald-100 p-12">
                    <svg class="w-24 h-24 mx-auto text-emerald-400 mb-6" fill="none" stroke="currentColor"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                    </svg>
                    <h3 class="text-2xl font-bold text-gray-900 mb-3">No sent requests</h3>
                    <p class="text-lg text-gray-600">Requests you've sent will appear here until accepted or declined.
                    </p>
                </div>

                <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div v-for="request in sentRequests" :key="request.id"
                        class="bg-white rounded-2xl shadow-md border border-gray-100 p-6 hover:shadow-xl transition-all duration-300">
                        <div class="flex items-center gap-4 mb-5">
                            <div
                                class="w-16 h-16 rounded-full bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center text-white text-2xl font-bold shadow-md ring-2 ring-emerald-100">
                                {{ request.to_user_details?.full_name?.charAt(0).toUpperCase() || '?' }}
                            </div>
                            <div>
                                <h3 class="text-xl font-bold text-gray-900">{{ request.to_user_details?.full_name ||
                                    'Player' }}</h3>
                                <p class="text-sm text-gray-600 mt-1">{{ request.to_user_details?.phone_number || '—' }}
                                </p>
                                <p class="text-xs text-gray-500 mt-1">Sent {{ formatDate(request.created_at) }}</p>
                            </div>
                        </div>

                        <button @click="cancelRequest(request.id)"
                            class="w-full px-5 py-3 bg-gray-100 hover:bg-gray-200 text-gray-800 rounded-xl font-medium transition-colors">
                            Cancel Request
                        </button>
                    </div>
                </div>
            </div>

            <!-- Find Players Tab (placeholder) -->
            <div v-else-if="activeTab === 'find'"
                class="bg-white rounded-2xl shadow-xl border border-emerald-100 p-12 text-center">
                <svg class="w-24 h-24 mx-auto text-emerald-500 mb-6" fill="none" stroke="currentColor"
                    viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <h3 class="text-2xl font-bold text-gray-900 mb-4">Find New Players</h3>
                <p class="text-lg text-gray-600 mb-8">Search for players by sport, city, skill level, and more</p>
                <router-link to="/friends/find"
                    class="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all">
                    Start Searching
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M17 8l4 4m0 0l-4 4m4-4H3" />
                    </svg>
                </router-link>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useFriends } from '@/composables/useFriends'
import { userService } from '@/services/userService'
import { debounce } from '@/utils/helpers'

const router = useRouter()
const {
    friends,
    pendingRequests,
    sentRequests,
    loading,
    loadFriends,
    loadPendingRequests,
    loadSentRequests,
    acceptFriendRequest,
    rejectFriendRequest,
    removeFriend: removeFriendAction,
    sendFriendRequest,
    isFriend,
    hasPendingRequest,
    hasSentRequest
} = useFriends()

const searchQuery = ref('')
const searchResults = ref([])
const searchLoading = ref(false)
const sendingRequest = ref(null)
const activeTab = ref('friends')

const filters = ref({
    city: '',
    sport: '',
    skill_level: '',
    min_rating: ''
})

const tabs = computed(() => [
    { id: 'friends', label: 'My Friends', count: friends.value.length },
    { id: 'pending', label: 'Requests', count: pendingRequests.value.length },
    { id: 'sent', label: 'Sent', count: sentRequests.value.length },
    { id: 'find', label: 'Find Players', count: 0 }
])

const performSearch = async () => {
    searchLoading.value = true
    try {
        const params = {
            search: searchQuery.value.trim(),
            ...filters.value
        }
        Object.keys(params).forEach(key => {
            if (!params[key]) delete params[key]
        })

        const response = await userService.searchPlayers(params)
        searchResults.value = response.results || response
    } catch (err) {
        console.error('Search failed:', err)
        searchResults.value = []
    } finally {
        searchLoading.value = false
    }
}

const handleSearch = debounce(performSearch, 500)

const sendRequest = async (userId) => {
    sendingRequest.value = userId
    try {
        await sendFriendRequest(userId)
        await loadSentRequests()
    } catch (err) {
        console.error('Failed to send friend request:', err)
        alert('Failed to send friend request. Please try again.')
    } finally {
        sendingRequest.value = null
    }
}

const getFriendName = (friendship) => {
    const authUserId = JSON.parse(localStorage.getItem('user'))?.id
    if (friendship.from_user === authUserId) {
        return friendship.to_user_details.full_name
    }
    return friendship.from_user_details.full_name
}

const getFriendDetails = (friendship) => {
    const authUserId = JSON.parse(localStorage.getItem('user'))?.id
    if (friendship.from_user === authUserId) {
        return friendship.to_user_details
    }
    return friendship.from_user_details
}

const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

const acceptRequest = async (id) => {
    try {
        await acceptFriendRequest(id)
        await loadAllData()
    } catch (err) {
        console.error('Failed to accept request:', err)
    }
}

const rejectRequest = async (id) => {
    try {
        await rejectFriendRequest(id)
        await loadPendingRequests()
    } catch (err) {
        console.error('Failed to reject request:', err)
    }
}

const cancelRequest = async (id) => {
    try {
        await removeFriendAction(id)
        await loadSentRequests()
    } catch (err) {
        console.error('Failed to cancel request:', err)
    }
}

const removeFriend = async (id) => {
    if (confirm('Are you sure you want to remove this friend?')) {
        try {
            await removeFriendAction(id)
            await loadFriends()
        } catch (err) {
            console.error('Failed to remove friend:', err)
        }
    }
}

const loadAllData = async () => {
    await Promise.all([
        loadFriends(),
        loadPendingRequests(),
        loadSentRequests()
    ])
}

onMounted(() => {
    loadAllData()
})
</script>