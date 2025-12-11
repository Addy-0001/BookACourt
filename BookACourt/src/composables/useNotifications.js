// src/composables/useNotifications.js
import { ref, onMounted, onUnmounted } from 'vue';
import { notificationService } from '@/services/notificationService';

export function useNotifications() {
    const notifications = ref([]);
    const unreadCount = ref(0);
    const loading = ref(false);
    const error = ref(null);
    let pollingInterval = null;

    const loadNotifications = async () => {
        loading.value = true;
        error.value = null;
        try {
            const response = await notificationService.getNotifications();
            notifications.value = response.results || response;
        } catch (err) {
            console.error('Failed to load notifications:', err);
            error.value = 'Failed to load notifications';
        } finally {
            loading.value = false;
        }
    };

    const loadUnreadCount = async () => {
        try {
            unreadCount.value = await notificationService.getUnreadCount();
        } catch (err) {
            console.error('Failed to load unread count:', err);
        }
    };

    const markAsRead = async (id) => {
        try {
            await notificationService.markAsRead(id);
            const notif = notifications.value.find(n => n.id === id);
            if (notif) {
                notif.is_read = true;
                unreadCount.value = Math.max(0, unreadCount.value - 1);
            }
        } catch (err) {
            console.error('Failed to mark as read:', err);
            throw err;
        }
    };

    const markAllAsRead = async () => {
        try {
            await notificationService.markAllAsRead();
            notifications.value.forEach(n => n.is_read = true);
            unreadCount.value = 0;
        } catch (err) {
            console.error('Failed to mark all as read:', err);
            throw err;
        }
    };

    const startPolling = (intervalMs = 30000) => {
        if (pollingInterval) return;

        loadUnreadCount(); // Initial load
        pollingInterval = setInterval(() => {
            loadUnreadCount();
        }, intervalMs);
    };

    const stopPolling = () => {
        if (pollingInterval) {
            clearInterval(pollingInterval);
            pollingInterval = null;
        }
    };

    onMounted(() => {
        loadNotifications();
        startPolling();
    });

    onUnmounted(() => {
        stopPolling();
    });

    return {
        notifications,
        unreadCount,
        loading,
        error,
        loadNotifications,
        loadUnreadCount,
        markAsRead,
        markAllAsRead,
        startPolling,
        stopPolling
    };
}