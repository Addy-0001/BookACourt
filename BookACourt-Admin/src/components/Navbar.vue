<template>
    <nav class="admin-navbar">
        <div class="navbar-container">
            <!-- Logo and Brand -->
            <div class="navbar-brand">
                <router-link to="/" class="brand-link">
                    <div class="brand-logo">🏟️</div>
                    <div class="brand-text">
                        <span class="brand-name">BookACourt</span>
                        <span class="brand-subtitle">{{ roleLabel }}</span>
                    </div>
                </router-link>
            </div>

            <!-- Desktop Navigation Links -->
            <div class="navbar-nav" :class="{ 'mobile-open': mobileMenuOpen }">
                <!-- Dashboard - Available to All -->
                <router-link to="/" class="nav-item" exact-active-class="active">
                    <span class="nav-icon">📊</span>
                    <span class="nav-text">Dashboard</span>
                </router-link>

                <!-- My Courts - Court Owners & Managers -->
                <router-link v-if="isCourtOwnerOrManager" to="/admin/my-courts" class="nav-item" active-class="active">
                    <span class="nav-icon">🏟️</span>
                    <span class="nav-text">My Courts</span>
                </router-link>

                <!-- Bookings - Available to All -->
                <router-link to="/admin/bookings" class="nav-item" active-class="active">
                    <span class="nav-icon">📅</span>
                    <span class="nav-text">Bookings</span>
                    <span v-if="pendingBookingsCount > 0" class="nav-badge">{{ pendingBookingsCount }}</span>
                </router-link>

                <!-- Court Registrations - Super Users Only -->
                <router-link v-if="isSuperUser" to="/admin/registrations" class="nav-item" active-class="active">
                    <span class="nav-icon">📝</span>
                    <span class="nav-text">Registrations</span>
                    <span v-if="pendingCount > 0" class="nav-badge">{{ pendingCount }}</span>
                </router-link>

                <!-- All Courts - Super Users Only -->
                <router-link v-if="isSuperUser" to="/admin/courts" class="nav-item" active-class="active">
                    <span class="nav-icon">🏢</span>
                    <span class="nav-text">All Courts</span>
                </router-link>

                <!-- Users Management - Super Users Only -->
                <router-link v-if="isSuperUser" to="/admin/users" class="nav-item" active-class="active">
                    <span class="nav-icon">👥</span>
                    <span class="nav-text">Users</span>
                </router-link>

                <!-- Equipment - Court Owners & Managers -->
                <router-link v-if="isCourtOwnerOrManager" to="/admin/equipment" class="nav-item" active-class="active">
                    <span class="nav-icon">🎾</span>
                    <span class="nav-text">Equipment</span>
                </router-link>

                <!-- Reviews - Court Owners & Managers -->
                <router-link v-if="isCourtOwnerOrManager" to="/admin/reviews" class="nav-item" active-class="active">
                    <span class="nav-icon">⭐</span>
                    <span class="nav-text">Reviews</span>
                    <span v-if="unansweredReviewsCount > 0" class="nav-badge">{{ unansweredReviewsCount }}</span>
                </router-link>

                <!-- Reports - Available to All -->
                <router-link to="/admin/reports" class="nav-item" active-class="active">
                    <span class="nav-icon">📈</span>
                    <span class="nav-text">Reports</span>
                </router-link>

                <!-- Categories - Super Users Only -->
                <router-link v-if="isSuperUser" to="/admin/categories" class="nav-item" active-class="active">
                    <span class="nav-icon">📂</span>
                    <span class="nav-text">Categories</span>
                </router-link>
            </div>

            <!-- Right Side Actions -->
            <div class="navbar-actions">
                <!-- Quick Actions Dropdown -->
                <div class="action-item quick-actions" @click="toggleQuickActions">
                    <button class="action-button" title="Quick Actions">
                        <span class="action-icon">⚡</span>
                    </button>

                    <!-- Quick Actions Dropdown -->
                    <div v-if="showQuickActions" class="dropdown quick-actions-dropdown">
                        <div class="dropdown-header">
                            <h3>Quick Actions</h3>
                        </div>
                        <div class="dropdown-body">
                            <!-- Court Owner/Manager Actions -->
                            <template v-if="isCourtOwnerOrManager">
                                <button class="dropdown-item" @click="handleQuickAction('new-court')">
                                    <span class="item-icon">➕</span>
                                    <span>Add New Court</span>
                                </button>
                                <button class="dropdown-item" @click="handleQuickAction('block-slot')">
                                    <span class="item-icon">🚫</span>
                                    <span>Block Time Slot</span>
                                </button>
                                <button class="dropdown-item" @click="handleQuickAction('add-equipment')">
                                    <span class="item-icon">🎾</span>
                                    <span>Add Equipment</span>
                                </button>
                                <button class="dropdown-item" @click="handleQuickAction('pricing-rule')">
                                    <span class="item-icon">💰</span>
                                    <span>Set Pricing Rule</span>
                                </button>
                                <div class="dropdown-divider"></div>
                            </template>

                            <!-- Common Actions -->
                            <button class="dropdown-item" @click="handleQuickAction('manual-booking')">
                                <span class="item-icon">📅</span>
                                <span>Create Manual Booking</span>
                            </button>
                            <button class="dropdown-item" @click="handleQuickAction('export-data')">
                                <span class="item-icon">📊</span>
                                <span>Export Data</span>
                            </button>

                            <!-- Super User Actions -->
                            <template v-if="isSuperUser">
                                <div class="dropdown-divider"></div>
                                <button class="dropdown-item" @click="handleQuickAction('system-settings')">
                                    <span class="item-icon">⚙️</span>
                                    <span>System Settings</span>
                                </button>
                            </template>
                        </div>
                    </div>
                </div>

                <!-- Notifications -->
                <div class="action-item notifications" @click="toggleNotifications">
                    <button class="action-button" :class="{ 'has-notifications': notificationCount > 0 }"
                        title="Notifications">
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
                                <span class="empty-icon">✅</span>
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

                <!-- Court Selector - For Court Managers with multiple courts -->
                <div v-if="managedCourts.length > 1" class="action-item court-selector">
                    <button class="court-selector-button" @click="toggleCourtSelector" title="Switch Court">
                        <span class="court-icon">🏟️</span>
                        <span class="court-name">{{ selectedCourt?.name || 'Select Court' }}</span>
                        <span class="arrow">▼</span>
                    </button>

                    <div v-if="showCourtSelector" class="dropdown court-dropdown">
                        <div class="dropdown-header">
                            <h3>Managed Courts</h3>
                        </div>
                        <div class="dropdown-body">
                            <button v-for="court in managedCourts" :key="court.id" class="court-item"
                                :class="{ active: selectedCourt?.id === court.id }" @click="selectCourt(court)">
                                <div class="court-item-icon">🏟️</div>
                                <div class="court-item-info">
                                    <span class="court-item-name">{{ court.name }}</span>
                                    <span class="court-item-location">{{ court.city }}</span>
                                </div>
                                <span v-if="selectedCourt?.id === court.id" class="check-icon">✓</span>
                            </button>
                        </div>
                        <div class="dropdown-footer">
                            <button class="btn-view-all" @click="viewAllCourts">
                                View All My Courts
                            </button>
                        </div>
                    </div>
                </div>

                <!-- User Profile -->
                <div class="action-item profile" @click="toggleProfile">
                    <button class="profile-button">
                        <div class="profile-avatar" :style="{ background: avatarColor }">
                            {{ userInitials }}
                        </div>
                        <div class="profile-info">
                            <span class="profile-name">{{ currentUser?.full_name || 'Admin' }}</span>
                            <span class="profile-role">{{ roleLabel }}</span>
                        </div>
                        <span class="profile-arrow">▼</span>
                    </button>

                    <!-- Profile Dropdown -->
                    <div v-if="showProfile" class="dropdown profile-dropdown">
                        <div class="dropdown-header user-info">
                            <div class="user-avatar-large" :style="{ background: avatarColor }">
                                {{ userInitials }}
                            </div>
                            <div class="user-details">
                                <h3>{{ currentUser?.full_name || 'Admin User' }}</h3>
                                <p>{{ currentUser?.email || currentUser?.phone_number }}</p>
                                <span class="user-role-badge" :class="roleClass">{{ roleLabel }}</span>
                            </div>
                        </div>
                        <div class="dropdown-body">
                            <router-link to="/admin/profile" class="dropdown-item">
                                <span class="item-icon">👤</span>
                                <span>My Profile</span>
                            </router-link>
                            <router-link v-if="isCourtOwnerOrManager" to="/admin/my-courts" class="dropdown-item">
                                <span class="item-icon">🏟️</span>
                                <span>My Courts</span>
                            </router-link>
                            <router-link to="/admin/preferences" class="dropdown-item">
                                <span class="item-icon">⚙️</span>
                                <span>Preferences</span>
                            </router-link>
                            <router-link to="/admin/security" class="dropdown-item">
                                <span class="item-icon">🔒</span>
                                <span>Security & Password</span>
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
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useAdminStore } from '@/stores/admin';

const router = useRouter();
const adminStore = useAdminStore();

// State
const mobileMenuOpen = ref(false);
const showNotifications = ref(false);
const showProfile = ref(false);
const showQuickActions = ref(false);
const showCourtSelector = ref(false);
const pendingCount = ref(0);
const pendingBookingsCount = ref(0);
const unansweredReviewsCount = ref(0);
const notificationCount = ref(0);
const selectedCourt = ref(null);
const managedCourts = ref([]);

// Get current user from store or localStorage
const currentUser = computed(() => {
    return adminStore.currentUser || JSON.parse(localStorage.getItem('user') || 'null');
});

// Role checks
const isSuperUser = computed(() => {
    return currentUser.value?.role === 'SUPER_USER';
});

const isCourtOwner = computed(() => {
    return currentUser.value?.role === 'COURT_OWNER';
});

const isCourtManager = computed(() => {
    return currentUser.value?.role === 'COURT_MANAGER';
});

const isCourtOwnerOrManager = computed(() => {
    return isCourtOwner.value || isCourtManager.value;
});

// Role label
const roleLabel = computed(() => {
    const roleMap = {
        SUPER_USER: 'Super Admin',
        COURT_OWNER: 'Court Owner',
        COURT_MANAGER: 'Court Manager',
        PLAYER: 'Player',
    };
    return roleMap[currentUser.value?.role] || 'Admin Panel';
});

// Role class for styling
const roleClass = computed(() => {
    const classMap = {
        SUPER_USER: 'role-super',
        COURT_OWNER: 'role-owner',
        COURT_MANAGER: 'role-manager',
        PLAYER: 'role-player',
    };
    return classMap[currentUser.value?.role] || 'role-default';
});

// User initials
const userInitials = computed(() => {
    if (!currentUser.value?.full_name) return 'A';
    const names = currentUser.value.full_name.split(' ');
    if (names.length === 1) return names[0][0].toUpperCase();
    return (names[0][0] + names[names.length - 1][0]).toUpperCase();
});

// Avatar color based on role
const avatarColor = computed(() => {
    const colorMap = {
        SUPER_USER: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        COURT_OWNER: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        COURT_MANAGER: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
        PLAYER: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    };
    return colorMap[currentUser.value?.role] || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
});

// Mock notifications - replace with actual data from store
const notifications = ref([
    {
        id: 1,
        icon: '📅',
        message: 'New booking for Downtown Arena - Court 1',
        time: '2 minutes ago',
        read: false,
    },
    {
        id: 2,
        icon: '⭐',
        message: 'New review posted for your court',
        time: '15 minutes ago',
        read: false,
    },
    {
        id: 3,
        icon: '💰',
        message: 'Payment received for booking #12345',
        time: '1 hour ago',
        read: true,
    },
]);

// Lifecycle
onMounted(async () => {
    await loadData();
    setupClickOutside();
});

onUnmounted(() => {
    document.body.style.overflow = '';
});

// Watch for user changes
watch(() => currentUser.value, async (newUser) => {
    if (newUser) {
        await loadUserSpecificData();
    }
});

// Methods
async function loadData() {
    try {
        // Fetch current user if not in store
        if (!adminStore.currentUser) {
            await adminStore.fetchCurrentUser();
        }

        // Load notifications
        await adminStore.fetchNotifications();
        notificationCount.value = adminStore.unreadNotificationsCount;

        // Load user-specific data
        await loadUserSpecificData();
    } catch (error) {
        console.error('Error loading navbar data:', error);
    }
}

async function loadUserSpecificData() {
    if (isSuperUser.value) {
        // Load pending registrations for super users
        await adminStore.fetchRegistrations({ status: 'PENDING' });
        pendingCount.value = adminStore.pendingRegistrations.length;
    }

    if (isCourtOwnerOrManager.value) {
        // Load managed courts
        await loadManagedCourts();

        // Load pending bookings
        await adminStore.fetchBookings({ status: 'PENDING' });
        pendingBookingsCount.value = adminStore.pendingBookings.length;

        // Load unanswered reviews count
        unansweredReviewsCount.value = 3; // Replace with actual API call
    }
}

async function loadManagedCourts() {
    try {
        // Fetch courts owned or managed by current user
        const params = isCourtOwner.value
            ? { owner: currentUser.value.id }
            : { manager: currentUser.value.id };

        await adminStore.fetchCourts(params);
        managedCourts.value = adminStore.courts;

        // Set first court as selected if none selected
        if (managedCourts.value.length > 0 && !selectedCourt.value) {
            selectedCourt.value = managedCourts.value[0];
            localStorage.setItem('selectedCourtId', selectedCourt.value.id);
        }
    } catch (error) {
        console.error('Error loading managed courts:', error);
    }
}

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
    showQuickActions.value = false;
    showCourtSelector.value = false;
}

function toggleProfile() {
    showProfile.value = !showProfile.value;
    showNotifications.value = false;
    showQuickActions.value = false;
    showCourtSelector.value = false;
}

function toggleQuickActions() {
    showQuickActions.value = !showQuickActions.value;
    showNotifications.value = false;
    showProfile.value = false;
    showCourtSelector.value = false;
}

function toggleCourtSelector() {
    showCourtSelector.value = !showCourtSelector.value;
    showNotifications.value = false;
    showProfile.value = false;
    showQuickActions.value = false;
}

function selectCourt(court) {
    selectedCourt.value = court;
    localStorage.setItem('selectedCourtId', court.id);
    showCourtSelector.value = false;

    // Optionally refresh data for selected court
    loadUserSpecificData();
}

function viewAllCourts() {
    showCourtSelector.value = false;
    router.push('/admin/my-courts');
}

async function markAllRead() {
    try {
        await adminStore.markAllNotificationsRead();
        notifications.value.forEach(n => n.read = true);
        notificationCount.value = 0;
    } catch (error) {
        console.error('Error marking all as read:', error);
    }
}

function handleNotificationClick(notification) {
    // Mark as read
    notification.read = true;
    notificationCount.value = notifications.value.filter(n => !n.read).length;

    // Navigate based on notification type
    // Add your navigation logic here
}

function handleQuickAction(action) {
    showQuickActions.value = false;

    const actionRoutes = {
        'new-court': '/admin/my-courts/create',
        'block-slot': '/admin/blocked-slots',
        'add-equipment': '/admin/equipment/create',
        'pricing-rule': '/admin/pricing',
        'manual-booking': '/admin/bookings/create',
        'export-data': '/admin/reports/export',
        'system-settings': '/admin/settings',
    };

    if (actionRoutes[action]) {
        router.push(actionRoutes[action]);
    }
}

function handleLogout() {
    if (confirm('Are you sure you want to logout?')) {
        // Clear auth tokens
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        localStorage.removeItem('selectedCourtId');

        // Reset store
        adminStore.resetState();

        // Navigate to login
        router.push('/login');
    }
}

function setupClickOutside() {
    document.addEventListener('click', handleClickOutside);
}

function handleClickOutside(event) {
    const target = event.target;
    if (!target.closest('.notifications') && showNotifications.value) {
        showNotifications.value = false;
    }
    if (!target.closest('.profile') && showProfile.value) {
        showProfile.value = false;
    }
    if (!target.closest('.quick-actions') && showQuickActions.value) {
        showQuickActions.value = false;
    }
    if (!target.closest('.court-selector') && showCourtSelector.value) {
        showCourtSelector.value = false;
    }
}
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
    max-width: 1600px;
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
    gap: 0.25rem;
    flex: 1;
    justify-content: center;
    max-width: 900px;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.625rem 0.875rem;
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
    gap: 0.75rem;
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

/* Court Selector */
.court-selector-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(255, 255, 255, 0.1);
    border: none;
    padding: 0.5rem 0.75rem;
    border-radius: 8px;
    cursor: pointer;
    color: white;
    transition: all 0.2s;
    max-width: 200px;
}

.court-selector-button:hover {
    background: rgba(255, 255, 255, 0.2);
}

.court-icon {
    font-size: 1.1rem;
}

.court-name {
    font-size: 0.85rem;
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex: 1;
}

.arrow {
    font-size: 0.7rem;
    opacity: 0.7;
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
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 0.9rem;
    color: white;
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
}

/* Dropdowns */
.dropdown {
    position: absolute;
    top: calc(100% + 0.75rem);
    right: 0;
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    min-width: 300px;
    max-width: 380px;
    overflow: hidden;
    animation: dropdownSlide 0.2s ease-out;
}

.quick-actions-dropdown {
    min-width: 260px;
}

.court-dropdown {
    min-width: 320px;
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
    width: 100%;
    text-align: center;
    color: #3498db;
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
    padding: 0.5rem;
    border-radius: 6px;
    transition: background 0.2s;
}

.btn-view-all:hover {
    background: #f8f9fa;
}

/* Court Selector Dropdown */
.court-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.875rem 1.25rem;
    cursor: pointer;
    transition: background 0.2s;
    border: none;
    background: none;
    width: 100%;
    text-align: left;
}

.court-item:hover {
    background: #f8f9fa;
}

.court-item.active {
    background: #e3f2fd;
}

.court-item-icon {
    font-size: 1.5rem;
}

.court-item-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.court-item-name {
    font-size: 0.95rem;
    font-weight: 500;
    color: #2c3e50;
}

.court-item-location {
    font-size: 0.8rem;
    color: #7f8c8d;
}

.check-icon {
    color: #27ae60;
    font-size: 1.1rem;
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
    flex-direction: row;
    align-items: center;
    gap: 1rem;
    padding: 1.25rem;
}

.user-avatar-large {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 1.25rem;
    color: white;
    flex-shrink: 0;
}

.user-details {
    flex: 1;
}

.user-details h3 {
    font-size: 1.1rem;
    margin: 0 0 0.25rem 0;
}

.user-details p {
    margin: 0 0 0.5rem 0;
    font-size: 0.85rem;
    color: #7f8c8d;
}

.user-role-badge {
    display: inline-block;
    padding: 0.25rem 0.625rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
}

.role-super {
    background: #e3f2fd;
    color: #1976d2;
}

.role-owner {
    background: #fce4ec;
    color: #c2185b;
}

.role-manager {
    background: #e0f2f1;
    color: #00796b;
}

.role-player {
    background: #f3e5f5;
    color: #7b1fa2;
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

.empty-icon {
    font-size: 3rem;
    display: block;
    margin-bottom: 0.5rem;
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
@media (max-width: 1400px) {
    .navbar-container {
        padding: 0 1.5rem;
    }

    .navbar-nav {
        gap: 0.125rem;
    }

    .nav-item {
        padding: 0.5rem 0.75rem;
        font-size: 0.85rem;
    }
}

@media (max-width: 1200px) {
    .profile-info {
        display: none;
    }

    .court-selector-button {
        max-width: 150px;
    }

    .court-name {
        font-size: 0.8rem;
    }
}

@media (max-width: 1024px) {
    .navbar-nav {
        gap: 0;
    }

    .nav-item {
        padding: 0.5rem 0.625rem;
        font-size: 0.8rem;
    }

    .nav-text {
        display: none;
    }

    .nav-icon {
        font-size: 1.25rem;
    }
}

@media (max-width: 768px) {
    .navbar-container {
        height: 60px;
        padding: 0 1rem;
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

    .nav-text {
        display: inline;
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
        max-width: none;
    }

    .court-selector-button {
        display: none;
    }

    .action-button {
        width: 36px;
        height: 36px;
    }
}

@media (max-width: 480px) {
    .navbar-actions {
        gap: 0.5rem;
    }

    .profile-button {
        padding: 0.375rem;
    }

    .profile-avatar {
        width: 28px;
        height: 28px;
        font-size: 0.8rem;
    }
}
</style>