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
                        <h1 class="text-2xl font-bold text-blue-600">Friends</h1>
                    </div>
                    <div class="flex items-center gap-4">
                        <router-link to="/"
                            class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
                            Home
                        </router-link>
                    </div>
                </div>
            </div>
        </nav>

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
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useFriends } from '@/composables/useFriends'

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
    removeFriend: removeFriendAction
} = useFriends()

const activeTab = ref('friends')

const tabs = computed(() => [
    { id: 'friends', label: 'My Friends', count: friends.value.length },
    { id: 'pending', label: 'Requests', count: pendingRequests.value.length },
    { id: 'sent', label: 'Sent', count: sentRequests.value.length }
])

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

const goBack = () => router.go(-1)

onMounted(() => {
    loadAllData()
})
</script>