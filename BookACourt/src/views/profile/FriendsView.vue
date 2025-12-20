<template>
    <div class="min-h-screen bg-gray-50">

        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Tabs -->
            <div class="bg-white rounded-xl shadow-md mb-8">
                <div class="flex border-b border-gray-200">
                    <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id" :class="[
                        'flex-1 px-6 py-4 text-sm font-medium transition-colors',
                        activeTab === tab.id
                            ? 'text-blue-600 border-b-2 border-blue-600'
                            : 'text-gray-600 hover:text-gray-900'
                    ]">
                        {{ tab.label }}
                        <span v-if="tab.count > 0"
                            class="ml-2 px-2 py-1 bg-blue-100 text-blue-600 rounded-full text-xs">
                            {{ tab.count }}
                        </span>
                    </button>
                </div>
            </div>

            <!-- Loading -->
            <div v-if="loading" class="flex justify-center py-20">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>

            <!-- My Friends Tab -->
            <div v-else-if="activeTab === 'friends'">
                <div v-if="friends.length === 0" class="text-center py-20">
                    <svg class="w-24 h-24 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                    <p class="text-xl text-gray-600">No friends yet</p>
                </div>
                <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div v-for="friendship in friends" :key="friendship.id"
                        class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow">
                        <div class="flex items-center gap-4 mb-4">
                            <div
                                class="w-16 h-16 rounded-full bg-blue-600 flex items-center justify-center text-white text-xl font-bold">
                                {{ getFriendName(friendship).charAt(0).toUpperCase() }}
                            </div>
                            <div>
                                <h3 class="font-bold text-gray-900">{{ getFriendName(friendship) }}</h3>
                                <p class="text-sm text-gray-600">{{ getFriendDetails(friendship).phone_number }}</p>
                            </div>
                        </div>
                        <div class="flex gap-2">
                            <button @click="removeFriend(friendship.id)"
                                class="flex-1 px-4 py-2 bg-red-50 text-red-600 hover:bg-red-100 rounded-lg transition-colors text-sm font-medium">
                                Remove
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Pending Requests Tab -->
            <div v-else-if="activeTab === 'pending'">
                <div v-if="pendingRequests.length === 0" class="text-center py-20">
                    <svg class="w-24 h-24 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <p class="text-xl text-gray-600">No pending requests</p>
                </div>
                <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div v-for="request in pendingRequests" :key="request.id"
                        class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow">
                        <div class="flex items-center gap-4 mb-4">
                            <div
                                class="w-16 h-16 rounded-full bg-purple-600 flex items-center justify-center text-white text-xl font-bold">
                                {{ request.from_user_details.full_name.charAt(0).toUpperCase() }}
                            </div>
                            <div>
                                <h3 class="font-bold text-gray-900">{{ request.from_user_details.full_name }}</h3>
                                <p class="text-sm text-gray-600">{{ request.from_user_details.phone_number }}</p>
                                <p class="text-xs text-gray-500 mt-1">{{ formatDate(request.created_at) }}</p>
                            </div>
                        </div>
                        <div class="flex gap-2">
                            <button @click="acceptRequest(request.id)"
                                class="flex-1 px-4 py-2 bg-green-600 text-white hover:bg-green-700 rounded-lg transition-colors text-sm font-medium">
                                Accept
                            </button>
                            <button @click="rejectRequest(request.id)"
                                class="flex-1 px-4 py-2 bg-red-50 text-red-600 hover:bg-red-100 rounded-lg transition-colors text-sm font-medium">
                                Reject
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Sent Requests Tab -->
            <div v-else-if="activeTab === 'sent'">
                <div v-if="sentRequests.length === 0" class="text-center py-20">
                    <svg class="w-24 h-24 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                    </svg>
                    <p class="text-xl text-gray-600">No sent requests</p>
                </div>
                <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div v-for="request in sentRequests" :key="request.id"
                        class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow">
                        <div class="flex items-center gap-4 mb-4">
                            <div
                                class="w-16 h-16 rounded-full bg-amber-600 flex items-center justify-center text-white text-xl font-bold">
                                {{ request.to_user_details.full_name.charAt(0).toUpperCase() }}
                            </div>
                            <div>
                                <h3 class="font-bold text-gray-900">{{ request.to_user_details.full_name }}</h3>
                                <p class="text-sm text-gray-600">{{ request.to_user_details.phone_number }}</p>
                                <span
                                    class="inline-block mt-1 px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded-full">
                                    Pending
                                </span>
                            </div>
                        </div>
                        <button @click="cancelRequest(request.id)"
                            class="w-full px-4 py-2 bg-red-50 text-red-600 hover:bg-red-100 rounded-lg transition-colors text-sm font-medium">
                            Cancel Request
                        </button>
                    </div>
                </div>
            </div>

            <div v-else-if="activeTab === 'find'">
                <!-- Search Bar -->
                <div class="bg-white rounded-xl shadow-md p-6 mb-6">
                    <div class="flex items-center gap-4">
                        <div class="flex-1 relative">
                            <svg class="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"
                                fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                            </svg>
                            <input v-model="searchQuery" type="text" placeholder="Search players by name or phone..."
                                @input="handleSearch"
                                class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
                        </div>
                        <button @click="handleSearch" :disabled="searchLoading"
                            class="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white rounded-lg transition-colors font-medium">
                            {{ searchLoading ? 'Searching...' : 'Search' }}
                        </button>
                    </div>
                </div>

                <!-- Search Results -->
                <div v-if="searchLoading" class="flex justify-center py-20">
                    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                </div>

                <div v-else-if="searchResults.length === 0 && searchQuery"
                    class="text-center py-20 bg-white rounded-xl shadow-md">
                    <svg class="w-24 h-24 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                    <p class="text-xl text-gray-600">No players found</p>
                    <p class="text-gray-500 mt-2">Try searching with a different name or phone number</p>
                </div>

                <div v-else-if="searchResults.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div v-for="player in searchResults" :key="player.id"
                        class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow">
                        <div class="flex items-center gap-4 mb-4">
                            <div
                                class="w-16 h-16 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white text-xl font-bold">
                                {{ player.full_name.charAt(0).toUpperCase() }}
                            </div>
                            <div>
                                <h3 class="font-bold text-gray-900">{{ player.full_name }}</h3>
                                <p class="text-sm text-gray-600">{{ player.phone_number }}</p>
                                <p v-if="player.city" class="text-xs text-gray-500">{{ player.city }}</p>
                            </div>
                        </div>

                        <button v-if="isFriend(player.id)"
                            class="w-full py-2 bg-gray-100 text-gray-600 rounded-lg font-medium cursor-default"
                            disabled>
                            Already Friends
                        </button>
                        <button v-else-if="hasSentRequest(player.id)"
                            class="w-full py-2 bg-yellow-100 text-yellow-800 rounded-lg font-medium cursor-default"
                            disabled>
                            Request Sent
                        </button>
                        <button v-else-if="hasPendingRequest(player.id)"
                            class="w-full py-2 bg-blue-100 text-blue-800 rounded-lg font-medium cursor-default"
                            disabled>
                            Request Pending
                        </button>
                        <button v-else @click="sendRequest(player.id)" :disabled="sendingRequest === player.id"
                            class="w-full py-2 bg-blue-600 text-white hover:bg-blue-700 rounded-lg transition-colors font-medium disabled:bg-gray-400">
                            {{ sendingRequest === player.id ? 'Sending...' : 'Add Friend' }}
                        </button>
                    </div>
                </div>

                <div v-else class="text-center py-20 bg-white rounded-xl shadow-md">
                    <svg class="w-24 h-24 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                    <p class="text-xl text-gray-600">Find New Friends</p>
                    <p class="text-gray-500 mt-2">Search for players to connect with</p>
                </div>
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

// Filter options
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

// Search functionality
const performSearch = async () => {
    searchLoading.value = true
    try {
        const params = {
            search: searchQuery.value.trim(),
            ...filters.value
        }

        // Remove empty filter values
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

// Debounced search handler
const handleSearch = debounce(performSearch, 500)

// Send friend request
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

const clearFilters = () => {
    filters.value = {
        city: '',
        sport: '',
        skill_level: '',
        min_rating: ''
    }
    performSearch()
}

onMounted(() => {
    loadAllData()
    // Load initial player list
    if (activeTab.value === 'find') {
        performSearch()
    }
})
</script>