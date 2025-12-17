<template>
    <div class="min-h-screen bg-gray-50">

        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
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

            <!-- Notifications List -->
            <div v-else-if="notifications.length > 0" class="space-y-2">
                <div v-for="notification in notifications" :key="notification.id"
                    @click="handleNotificationClick(notification)" :class="[
                        'bg-white rounded-xl shadow-md p-6 cursor-pointer hover:shadow-lg transition-all',
                        !notification.is_read && 'border-l-4 border-blue-600'
                    ]">
                    <div class="flex items-start justify-between gap-4">
                        <div class="flex-1">
                            <div class="flex items-center gap-2 mb-2">
                                <span :class="[
                                    'px-2 py-1 text-xs font-medium rounded-full',
                                    getTypeClass(notification.notification_type)
                                ]">
                                    {{ getTypeLabel(notification.notification_type) }}
                                </span>
                                <span v-if="!notification.is_read" class="w-2 h-2 bg-blue-600 rounded-full"></span>
                            </div>
                            <p class="text-gray-900 font-medium mb-1">{{ notification.message }}</p>
                            <p class="text-sm text-gray-500">{{ formatDateTime(notification.sent_at) }}</p>
                        </div>
                        <div class="flex items-center gap-2">
                            <svg v-if="notification.sent_via_email" class="w-5 h-5 text-gray-400" fill="none"
                                stroke="currentColor" viewBox="0 0 24 24" title="Sent via email">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                            </svg>
                            <svg v-if="notification.sent_via_sms" class="w-5 h-5 text-gray-400" fill="none"
                                stroke="currentColor" viewBox="0 0 24 24" title="Sent via SMS">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                            </svg>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Empty State -->
            <div v-else class="text-center py-20">
                <svg class="w-24 h-24 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
                <p class="text-xl text-gray-600 mb-2">No notifications</p>
                <p class="text-gray-500">You're all caught up!</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useNotifications } from '@/composables/useNotifications'

const router = useRouter()
const {
    notifications,
    unreadCount,
    loading,
    error,
    loadNotifications,
    markAsRead,
    markAllAsRead
} = useNotifications()

const getTypeClass = (type) => {
    const classes = {
        'CONFIRMATION': 'bg-green-100 text-green-800',
        'REMINDER': 'bg-blue-100 text-blue-800',
        'CANCELLATION': 'bg-red-100 text-red-800',
        'MODIFICATION': 'bg-amber-100 text-amber-800'
    }
    return classes[type] || 'bg-gray-100 text-gray-800'
}

const getTypeLabel = (type) => {
    const labels = {
        'CONFIRMATION': 'Confirmation',
        'REMINDER': 'Reminder',
        'CANCELLATION': 'Cancellation',
        'MODIFICATION': 'Modified'
    }
    return labels[type] || type
}

const formatDateTime = (dateString) => {
    const date = new Date(dateString)
    const now = new Date()
    const diff = now - date
    const hours = Math.floor(diff / (1000 * 60 * 60))

    if (hours < 1) {
        const mins = Math.floor(diff / (1000 * 60))
        return mins < 1 ? 'Just now' : `${mins}m ago`
    }
    if (hours < 24) return `${hours}h ago`

    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    })
}

const handleNotificationClick = async (notification) => {
    if (!notification.is_read) {
        await markAsRead(notification.id)
    }
    // Navigate to booking if available
    if (notification.booking) {
        router.push(`/bookings/${notification.booking}`)
    }
}

const handleMarkAllRead = async () => {
    try {
        await markAllAsRead()
    } catch (err) {
        console.error('Failed to mark all as read:', err)
    }
}

const goBack = () => router.go(-1)

onMounted(() => {
    loadNotifications()
})
</script>