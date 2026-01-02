<!-- views/profile/NotificationsView.vue -->
<template>
    <div class="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
            <!-- Header -->
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-6 mb-10">
                <div>
                    <h1 class="text-3xl sm:text-4xl font-bold text-gray-900">Notifications</h1>
                    <p class="mt-2 text-lg text-gray-600">Stay updated with your bookings and activities</p>
                </div>

                <button v-if="unreadCount > 0" @click="handleMarkAllRead"
                    class="px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-medium shadow-md hover:shadow-lg transition-all flex items-center gap-2">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    Mark All as Read
                </button>
            </div>

            <!-- Loading -->
            <div v-if="loading" class="flex justify-center py-32">
                <div class="w-14 h-14 border-4 border-emerald-200 border-t-emerald-600 rounded-full animate-spin"></div>
            </div>

            <!-- Error -->
            <div v-else-if="error" class="text-center py-20">
                <svg class="w-20 h-20 mx-auto text-red-500 mb-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p class="text-xl text-gray-700 font-medium">{{ error }}</p>
                <button @click="loadNotifications"
                    class="mt-6 px-8 py-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-medium transition-colors">
                    Try Again
                </button>
            </div>

            <!-- Notifications List -->
            <div v-else-if="notifications.length > 0" class="space-y-4">
                <div v-for="notification in notifications" :key="notification.id"
                    @click="handleNotificationClick(notification)"
                    class="bg-white rounded-2xl shadow-md p-6 cursor-pointer hover:shadow-xl transition-all duration-300 border border-gray-100"
                    :class="{ 'border-l-4 border-emerald-600 bg-emerald-50/30': !notification.is_read }">
                    <div class="flex items-start justify-between gap-4">
                        <div class="flex-1">
                            <!-- Type Badge + Unread Dot -->
                            <div class="flex items-center gap-3 mb-3">
                                <span :class="[
                                    'inline-flex px-3 py-1 text-xs font-semibold rounded-full',
                                    getTypeClass(notification.notification_type)
                                ]">
                                    {{ getTypeLabel(notification.notification_type) }}
                                </span>

                                <span v-if="!notification.is_read"
                                    class="w-3 h-3 bg-emerald-500 rounded-full animate-pulse"></span>
                            </div>

                            <!-- Message -->
                            <p class="text-gray-900 font-semibold text-lg mb-2 leading-tight">
                                {{ notification.message }}
                            </p>

                            <!-- Time -->
                            <p class="text-sm text-gray-500">
                                {{ formatDateTime(notification.sent_at) }}
                            </p>
                        </div>

                        <!-- Delivery Icons -->
                        <div class="flex items-center gap-3 text-gray-400">
                            <svg v-if="notification.sent_via_email" class="w-6 h-6" fill="none" stroke="currentColor"
                                viewBox="0 0 24 24" title="Sent via Email">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                            </svg>

                            <svg v-if="notification.sent_via_sms" class="w-6 h-6" fill="none" stroke="currentColor"
                                viewBox="0 0 24 24" title="Sent via SMS">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                            </svg>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Empty State -->
            <div v-else class="text-center py-32">
                <div class="inline-block p-8 bg-white rounded-2xl shadow-lg border border-emerald-100">
                    <svg class="w-24 h-24 mx-auto text-emerald-400 mb-6" fill="none" stroke="currentColor"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                    </svg>
                    <h3 class="text-2xl font-bold text-gray-900 mb-3">You're all caught up!</h3>
                    <p class="text-lg text-gray-600">No new notifications at the moment</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
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
        'CONFIRMATION': 'bg-emerald-100 text-emerald-800',
        'REMINDER': 'bg-blue-100 text-blue-800',
        'CANCELLATION': 'bg-red-100 text-red-800',
        'MODIFICATION': 'bg-amber-100 text-amber-800',
        'BOOKING_REQUEST': 'bg-purple-100 text-purple-800'
    }
    return classes[type] || 'bg-gray-100 text-gray-800'
}

const getTypeLabel = (type) => {
    const labels = {
        'CONFIRMATION': 'Confirmation',
        'REMINDER': 'Reminder',
        'CANCELLATION': 'Cancellation',
        'MODIFICATION': 'Updated',
        'BOOKING_REQUEST': 'Request'
    }
    return labels[type] || type
}

const formatDateTime = (dateString) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffMs = now - date
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMins / 60)
    const diffDays = Math.floor(diffHours / 24)

    if (diffMins < 1) return 'Just now'
    if (diffMins < 60) return `${diffMins}m ago`
    if (diffHours < 24) return `${diffHours}h ago`
    if (diffDays === 1) return 'Yesterday'
    if (diffDays < 7) return `${diffDays}d ago`

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

    // Navigate based on notification type/context
    if (notification.booking) {
        router.push(`/bookings/${notification.booking}`)
    } else if (notification.court) {
        router.push(`/courts/${notification.court}`)
    }
}

const handleMarkAllRead = async () => {
    if (confirm('Mark all notifications as read?')) {
        try {
            await markAllAsRead()
        } catch (err) {
            console.error('Failed to mark all as read:', err)
        }
    }
}

onMounted(() => {
    loadNotifications()
})
</script>