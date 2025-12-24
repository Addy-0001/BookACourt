<template>
    <nav class="admin-navbar">
        <div class="navbar-container">
            <!-- Logo and Brand -->
            <div class="navbar-brand">
                <router-link to="/" class="brand-link">
                    <div class="brand-logo">🏟️</div>
                    <div class="brand-text">
                        <span class="brand-name">BookACourt</span>
                        <span class="brand-subtitle">Admin Panel</span>
                    </div>
                </router-link>
            </div>

            <!-- Desktop Navigation Links -->
            <div class="navbar-nav" :class="{ 'mobile-open': mobileMenuOpen }">
                <router-link to="/" class="nav-item" exact-active-class="active">
                    <span class="nav-icon">📊</span>
                    <span class="nav-text">Dashboard</span>
                </router-link>

                <router-link to="/admin/users" class="nav-item" active-class="active">
                    <span class="nav-icon">👥</span>
                    <span class="nav-text">Users</span>
                </router-link>

                <router-link to="/admin/courts" class="nav-item" active-class="active">
                    <span class="nav-icon">🏟️</span>
                    <span class="nav-text">Courts</span>
                </router-link>

                <router-link to="/admin/bookings" class="nav-item" active-class="active">
                    <span class="nav-icon">📅</span>
                    <span class="nav-text">Bookings</span>
                </router-link>

                <router-link to="/admin/registrations" class="nav-item" active-class="active">
                    <span class="nav-icon">📝</span>
                    <span class="nav-text">Registrations</span>
                    <span v-if="pendingCount > 0" class="nav-badge">{{ pendingCount }}</span>
                </router-link>

                <router-link to="/admin/categories" class="nav-item" active-class="active">
                    <span class="nav-icon">📂</span>
                    <span class="nav-text">Categories</span>
                </router-link>

                <router-link to="/admin/reports" class="nav-item" active-class="active">
                    <span class="nav-icon">📈</span>
                    <span class="nav-text">Reports</span>
                </router-link>
            </div>

            <!-- Right Side Actions -->
            <div class="navbar-actions">
                <!-- Notifications -->
                <div class="action-item notifications" @click="toggleNotifications">
                    <button class="action-button" :class="{ 'has-notifications': notificationCount > 0 }">
                        <span class="action-icon">🔔</span>
                        <span v-if="notificationCount > 0" class="action-badge">{{ notificationCount }}</span>
                    </button>

                    <!-- Notifications Dropdown -->
                    <div v-if="showNotifications" class="dropdown notifications-dropdown">
                        <div class="dropdown-header">
                            <h3>Notifications</h3>
                            <button class="btn-text" @click="markAllRead">Mark all read</button>
                        </div>
                        <div class="dropdown-body">
                            <div v-if="notifications.length === 0" class="empty-state">
                                <p>No new notifications</p>
                            </div>
                            <div v-else class="notification-list">
                                <div v-for="notification in notifications" :key="notification.id"
                                    class="notification-item" :class="{ unread: !notification.read }"
                                    @click="handleNotificationClick(notification)">
                                    <div class="notification-icon">{{ notification.icon }}</div>
                                    <div class="notification-content">
                                        <p class="notification-text">{{ notification.message }}</p>
                                        <span class="notification-time">{{ notification.time }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="dropdown-footer">
                            <router-link to="/admin/notifications" class="btn-view-all">
                                View All Notifications
                            </router-link>
                        </div>
                    </div>
                </div>

                <!-- User Profile -->
                <div class="action-item profile" @click="toggleProfile">
                    <button class="profile-button">
                        <div class="profile-avatar">
                            {{ userInitials }}
                        </div>
                        <div class="profile-info">
                            <span class="profile-name">{{ currentUser?.full_name || 'Admin' }}</span>
                            <span class="profile-role">{{ currentUser?.role || 'Administrator' }}</span>
                        </div>
                        <span class="profile-arrow">▼</span>
                    </button>

                    <!-- Profile Dropdown -->
                    <div v-if="showProfile" class="dropdown profile-dropdown">
                        <div class="dropdown-header user-info">
                            <div class="user-avatar-large">{{ userInitials }}</div>
                            <div class="user-details">
                                <h3>{{ currentUser?.full_name || 'Admin User' }}</h3>
                                <p>{{ currentUser?.email || 'admin@bookacourt.com' }}</p>
                            </div>
                        </div>
                        <div class="dropdown-body">
                            <router-link to="/admin/profile" class="dropdown-item">
                                <span class="item-icon">👤</span>
                                <span>My Profile</span>
                            </router-link>
                            <router-link to="/admin/settings" class="dropdown-item">
                                <span class="item-icon">⚙️</span>
                                <span>Settings</span>
                            </router-link>
                            <router-link to="/admin/help" class="dropdown-item">
                                <span class="item-icon">❓</span>
                                <span>Help & Support</span>
                            </router-link>
                            <div class="dropdown-divider"></div>
                            <button class="dropdown-item logout" @click="handleLogout">
                                <span class="item-icon">🚪</span>
                                <span>Logout</span>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Mobile Menu Toggle -->
                <button class="mobile-menu-toggle" @click="toggleMobileMenu">
                    <span class="hamburger" :class="{ open: mobileMenuOpen }">
                        <span></span>
                        <span></span>
                        <span></span>
                    </span>
                </button>
            </div>
        </div>

        <!-- Mobile Overlay -->
        <div v-if="mobileMenuOpen" class="mobile-overlay" @click="closeMobileMenu"></div>
    </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// State
const mobileMenuOpen = ref(false);
const showNotifications = ref(false);
const showProfile = ref(false);
const pendingCount = ref(3);
const notificationCount = ref(5);

// Mock current user - replace with actual auth store
const currentUser = ref({
    full_name: 'Admin User',
    email: 'admin@bookacourt.com',
    role: 'Super Admin',
});

// Mock notifications - replace with actual data
const notifications = ref([
    {
        id: 1,
        icon: '📝',
        message: 'New court registration pending approval',
        time: '5 minutes ago',
        read: false,
    },
    {
        id: 2,
        icon: '⚠️',
        message: 'Booking cancellation requires attention',
        time: '1 hour ago',
        read: false,
    },
    {
        id: 3,
        icon: '✅',
        message: 'Court "Downtown Arena" has been verified',
        time: '2 hours ago',
        read: true,
    },
    {
        id: 4,
        icon: '💰',
        message: 'Payment received for booking #12345',
        time: '3 hours ago',
        read: true,
    },
    {
        id: 5,
        icon: '👤',
        message: 'New user registered: John Doe',
        time: '5 hours ago',
        read: true,
    },
]);

// Computed
const userInitials = computed(() => {
    if (!currentUser.value?.full_name) return 'A';
    const names = currentUser.value.full_name.split(' ');
    if (names.length === 1) return names[0][0].toUpperCase();
    return (names[0][0] + names[names.length - 1][0]).toUpperCase();
});

// Methods
function toggleMobileMenu() {
    mobileMenuOpen.value = !mobileMenuOpen.value;
    if (mobileMenuOpen.value) {
        document.body.style.overflow = 'hidden';
    } else {
        document.body.style.overflow = '';
    }
}

function closeMobileMenu() {
    mobileMenuOpen.value = false;
    document.body.style.overflow = '';
}

function toggleNotifications() {
    showNotifications.value = !showNotifications.value;
    showProfile.value = false;
}

function toggleProfile() {
    showProfile.value = !showProfile.value;
    showNotifications.value = false;
}

function markAllRead() {
    notifications.value = notifications.value.map(n => ({ ...n, read: true }));
    notificationCount.value = 0;
}

function handleNotificationClick(notification) {
    // Mark as read and navigate if needed
    notification.read = true;
    notificationCount.value = notifications.value.filter(n => !n.read).length;
}

function handleLogout() {
    if (confirm('Are you sure you want to logout?')) {
        // Clear auth tokens
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');

        // Navigate to login
        router.push('/login');
    }
}

// Close dropdowns when clicking outside
function handleClickOutside(event) {
    const target = event.target;
    if (!target.closest('.notifications') && showNotifications.value) {
        showNotifications.value = false;
    }
    if (!target.closest('.profile') && showProfile.value) {
        showProfile.value = false;
    }
}

onMounted(() => {
    document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside);
    document.body.style.overflow = '';
});
</script>

<style scoped>
.admin-navbar {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
}

.navbar-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 70px;
}

/* Brand */
.navbar-brand {
    flex-shrink: 0;
}

.brand-link {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    text-decoration: none;
    color: white;
    transition: opacity 0.2s;
}

.brand-link:hover {
    opacity: 0.9;
}

.brand-logo {
    font-size: 2rem;
    line-height: 1;
}

.brand-text {
    display: flex;
    flex-direction: column;
}

.brand-name {
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: -0.5px;
}

.brand-subtitle {
    font-size: 0.75rem;
    opacity: 0.9;
    font-weight: 500;
}

/* Navigation */
.navbar-nav {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex: 1;
    justify-content: center;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.625rem 1rem;
    border-radius: 8px;
    text-decoration: none;
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.9rem;
    font-weight: 500;
    transition: all 0.2s;
    position: relative;
    white-space: nowrap;
}

.nav-item:hover {
    background: rgba(255, 255, 255, 0.15);
    color: white;
}

.nav-item.active {
    background: rgba(255, 255, 255, 0.2);
    color: white;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.nav-icon {
    font-size: 1.1rem;
}

.nav-badge {
    background: #e74c3c;
    color: white;
    padding: 0.125rem 0.375rem;
    border-radius: 10px;
    font-size: 0.7rem;
    font-weight: 600;
    min-width: 18px;
    text-align: center;
}

/* Actions */
.navbar-actions {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.action-item {
    position: relative;
}

.action-button {
    background: rgba(255, 255, 255, 0.1);
    border: none;
    padding: 0.5rem;
    border-radius: 8px;
    cursor: pointer;
    color: white;
    transition: all 0.2s;
    position: relative;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.action-button:hover {
    background: rgba(255, 255, 255, 0.2);
}

.action-button.has-notifications {
    animation: pulse 2s infinite;
}

@keyframes pulse {

    0%,
    100% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.05);
    }
}

.action-icon {
    font-size: 1.25rem;
}

.action-badge {
    position: absolute;
    top: -4px;
    right: -4px;
    background: #e74c3c;
    color: white;
    font-size: 0.65rem;
    font-weight: 600;
    padding: 0.125rem 0.375rem;
    border-radius: 10px;
    min-width: 18px;
    text-align: center;
}

/* Profile Button */
.profile-button {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: rgba(255, 255, 255, 0.1);
    border: none;
    padding: 0.375rem 0.75rem 0.375rem 0.375rem;
    border-radius: 25px;
    cursor: pointer;
    color: white;
    transition: all 0.2s;
}

.profile-button:hover {
    background: rgba(255, 255, 255, 0.2);
}

.profile-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 0.9rem;
}

.profile-info {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    text-align: left;
}

.profile-name {
    font-size: 0.9rem;
    font-weight: 600;
    line-height: 1.2;
}

.profile-role {
    font-size: 0.75rem;
    opacity: 0.9;
    line-height: 1.2;
}

.profile-arrow {
    font-size: 0.7rem;
    opacity: 0.7;
    transition: transform 0.2s;
}

.profile:hover .profile-arrow {
    transform: translateY(2px);
}

/* Dropdowns */
.dropdown {
    position: absolute;
    top: calc(100% + 0.5rem);
    right: 0;
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    min-width: 320px;
    overflow: hidden;
    animation: dropdownSlide 0.2s ease-out;
}

@keyframes dropdownSlide {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.dropdown-header {
    padding: 1rem 1.25rem;
    border-bottom: 1px solid #e9ecef;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.dropdown-header h3 {
    margin: 0;
    font-size: 1rem;
    color: #2c3e50;
    font-weight: 600;
}

.btn-text {
    background: none;
    border: none;
    color: #3498db;
    font-size: 0.85rem;
    cursor: pointer;
    padding: 0;
    font-weight: 500;
}

.btn-text:hover {
    text-decoration: underline;
}

.dropdown-body {
    max-height: 400px;
    overflow-y: auto;
}

.dropdown-footer {
    padding: 0.75rem 1.25rem;
    border-top: 1px solid #e9ecef;
}

.btn-view-all {
    display: block;
    text-align: center;
    color: #3498db;
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
}

.btn-view-all:hover {
    text-decoration: underline;
}

/* Notifications Dropdown */
.notification-list {
    display: flex;
    flex-direction: column;
}

.notification-item {
    display: flex;
    gap: 0.75rem;
    padding: 1rem 1.25rem;
    cursor: pointer;
    transition: background 0.2s;
    border-bottom: 1px solid #f8f9fa;
}

.notification-item:hover {
    background: #f8f9fa;
}

.notification-item.unread {
    background: #e3f2fd;
}

.notification-item.unread:hover {
    background: #d1e7f9;
}

.notification-icon {
    font-size: 1.5rem;
    flex-shrink: 0;
}

.notification-content {
    flex: 1;
}

.notification-text {
    margin: 0 0 0.25rem 0;
    font-size: 0.9rem;
    color: #2c3e50;
    line-height: 1.4;
}

.notification-time {
    font-size: 0.8rem;
    color: #7f8c8d;
}

/* Profile Dropdown */
.dropdown-header.user-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 1.25rem;
}

.user-avatar-large {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 1.25rem;
}

.user-details h3 {
    font-size: 1.1rem;
    margin: 0 0 0.25rem 0;
}

.user-details p {
    margin: 0;
    font-size: 0.85rem;
    color: #7f8c8d;
}

.dropdown-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.875rem 1.25rem;
    color: #2c3e50;
    text-decoration: none;
    transition: background 0.2s;
    cursor: pointer;
    border: none;
    background: none;
    width: 100%;
    font-size: 0.9rem;
    text-align: left;
}

.dropdown-item:hover {
    background: #f8f9fa;
}

.dropdown-item.logout {
    color: #e74c3c;
}

.dropdown-item.logout:hover {
    background: #fee;
}

.item-icon {
    font-size: 1.1rem;
    width: 20px;
    text-align: center;
}

.dropdown-divider {
    height: 1px;
    background: #e9ecef;
    margin: 0.5rem 0;
}

/* Empty State */
.empty-state {
    padding: 3rem 2rem;
    text-align: center;
    color: #7f8c8d;
}

/* Mobile Menu Toggle */
.mobile-menu-toggle {
    display: none;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.5rem;
}

.hamburger {
    width: 24px;
    height: 20px;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.hamburger span {
    width: 100%;
    height: 3px;
    background: white;
    border-radius: 2px;
    transition: all 0.3s;
}

.hamburger.open span:nth-child(1) {
    transform: translateY(8.5px) rotate(45deg);
}

.hamburger.open span:nth-child(2) {
    opacity: 0;
}

.hamburger.open span:nth-child(3) {
    transform: translateY(-8.5px) rotate(-45deg);
}

.mobile-overlay {
    display: none;
}

/* Responsive */
@media (max-width: 1024px) {
    .navbar-container {
        padding: 0 1rem;
    }

    .navbar-nav {
        gap: 0.25rem;
    }

    .nav-item {
        padding: 0.5rem 0.75rem;
        font-size: 0.85rem;
    }

    .profile-info {
        display: none;
    }
}

@media (max-width: 768px) {
    .navbar-container {
        height: 60px;
    }

    .brand-logo {
        font-size: 1.5rem;
    }

    .brand-name {
        font-size: 1.1rem;
    }

    .brand-subtitle {
        font-size: 0.7rem;
    }

    .navbar-nav {
        position: fixed;
        top: 60px;
        left: 0;
        right: 0;
        bottom: 0;
        background: white;
        flex-direction: column;
        justify-content: flex-start;
        padding: 1rem;
        gap: 0.5rem;
        transform: translateX(-100%);
        transition: transform 0.3s;
        overflow-y: auto;
    }

    .navbar-nav.mobile-open {
        transform: translateX(0);
    }

    .nav-item {
        width: 100%;
        color: #2c3e50;
        justify-content: flex-start;
        padding: 1rem;
        font-size: 1rem;
    }

    .nav-item:hover {
        background: #f8f9fa;
    }

    .nav-item.active {
        background: #e3f2fd;
        color: #3498db;
    }

    .mobile-menu-toggle {
        display: block;
    }

    .mobile-overlay {
        display: block;
        position: fixed;
        top: 60px;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        z-index: 999;
    }

    .dropdown {
        position: fixed;
        left: 1rem;
        right: 1rem;
        top: auto;
    }

    .notifications-dropdown {
        max-width: none;
    }
}
</style>