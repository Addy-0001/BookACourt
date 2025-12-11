// src/composables/useFriends.js
import { ref, computed } from 'vue';
import { userService } from '@/services/userService';

export function useFriends() {
    const friendships = ref([]);
    const pendingRequests = ref([]);
    const sentRequests = ref([]);
    const loading = ref(false);
    const error = ref(null);

    const friends = computed(() => {
        return friendships.value.filter(f => f.status === 'ACCEPTED');
    });

    const loadFriends = async () => {
        loading.value = true;
        error.value = null;
        try {
            const response = await userService.getMyFriends();
            friendships.value = response.results || response;
        } catch (err) {
            console.error('Failed to load friends:', err);
            error.value = 'Failed to load friends';
        } finally {
            loading.value = false;
        }
    };

    const loadPendingRequests = async () => {
        try {
            const response = await userService.getPendingRequests();
            pendingRequests.value = response.results || response;
        } catch (err) {
            console.error('Failed to load pending requests:', err);
        }
    };

    const loadSentRequests = async () => {
        try {
            const response = await userService.getSentRequests();
            sentRequests.value = response.results || response;
        } catch (err) {
            console.error('Failed to load sent requests:', err);
        }
    };

    const sendFriendRequest = async (userId) => {
        try {
            const response = await userService.sendFriendRequest(userId);
            sentRequests.value.push(response);
            return response;
        } catch (err) {
            console.error('Failed to send friend request:', err);
            throw err;
        }
    };

    const acceptFriendRequest = async (requestId) => {
        try {
            const response = await userService.acceptFriendRequest(requestId);
            // Remove from pending and add to friends
            pendingRequests.value = pendingRequests.value.filter(r => r.id !== requestId);
            friendships.value.push(response);
            return response;
        } catch (err) {
            console.error('Failed to accept friend request:', err);
            throw err;
        }
    };

    const rejectFriendRequest = async (requestId) => {
        try {
            await userService.rejectFriendRequest(requestId);
            pendingRequests.value = pendingRequests.value.filter(r => r.id !== requestId);
        } catch (err) {
            console.error('Failed to reject friend request:', err);
            throw err;
        }
    };

    const removeFriend = async (friendshipId) => {
        try {
            await userService.removeFriend(friendshipId);
            friendships.value = friendships.value.filter(f => f.id !== friendshipId);
        } catch (err) {
            console.error('Failed to remove friend:', err);
            throw err;
        }
    };

    const isFriend = (userId) => {
        return friends.value.some(f =>
            (f.from_user === userId || f.to_user === userId) && f.status === 'ACCEPTED'
        );
    };

    const hasPendingRequest = (userId) => {
        return pendingRequests.value.some(r => r.from_user === userId);
    };

    const hasSentRequest = (userId) => {
        return sentRequests.value.some(r => r.to_user === userId);
    };

    return {
        friendships,
        friends,
        pendingRequests,
        sentRequests,
        loading,
        error,
        loadFriends,
        loadPendingRequests,
        loadSentRequests,
        sendFriendRequest,
        acceptFriendRequest,
        rejectFriendRequest,
        removeFriend,
        isFriend,
        hasPendingRequest,
        hasSentRequest
    };
}