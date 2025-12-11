// src/utils/constants.js

// ===== USER ROLES =====
export const USER_ROLES = {
    PLAYER: 'PLAYER',
    COURT_OWNER: 'COURT_OWNER',
    COURT_MANAGER: 'COURT_MANAGER',
    SUPER_USER: 'SUPER_USER'
};

export const ROLE_LABELS = {
    [USER_ROLES.PLAYER]: 'Player',
    [USER_ROLES.COURT_OWNER]: 'Court Owner',
    [USER_ROLES.COURT_MANAGER]: 'Court Manager',
    [USER_ROLES.SUPER_USER]: 'Administrator'
};

// ===== BOOKING STATUS =====
export const BOOKING_STATUS = {
    PENDING: 'PENDING',
    CONFIRMED: 'CONFIRMED',
    CANCELLED: 'CANCELLED',
    COMPLETED: 'COMPLETED',
    NO_SHOW: 'NO_SHOW'
};

export const BOOKING_STATUS_LABELS = {
    [BOOKING_STATUS.PENDING]: 'Pending',
    [BOOKING_STATUS.CONFIRMED]: 'Confirmed',
    [BOOKING_STATUS.CANCELLED]: 'Cancelled',
    [BOOKING_STATUS.COMPLETED]: 'Completed',
    [BOOKING_STATUS.NO_SHOW]: 'No Show'
};

// ===== PAYMENT STATUS =====
export const PAYMENT_STATUS = {
    PENDING: 'PENDING',
    COMPLETED: 'COMPLETED',
    REFUNDED: 'REFUNDED',
    FAILED: 'FAILED'
};

export const PAYMENT_METHOD = {
    ONLINE: 'ONLINE',
    CASH: 'CASH',
    OFFLINE: 'OFFLINE'
};

export const PAYMENT_METHOD_LABELS = {
    [PAYMENT_METHOD.ONLINE]: 'Online Payment',
    [PAYMENT_METHOD.CASH]: 'Cash',
    [PAYMENT_METHOD.OFFLINE]: 'Offline Payment'
};

// ===== MATCH EVENT STATUS =====
export const MATCH_STATUS = {
    OPEN: 'OPEN',
    FULL: 'FULL',
    IN_PROGRESS: 'IN_PROGRESS',
    COMPLETED: 'COMPLETED',
    CANCELLED: 'CANCELLED'
};

export const MATCH_STATUS_LABELS = {
    [MATCH_STATUS.OPEN]: 'Open',
    [MATCH_STATUS.FULL]: 'Full',
    [MATCH_STATUS.IN_PROGRESS]: 'In Progress',
    [MATCH_STATUS.COMPLETED]: 'Completed',
    [MATCH_STATUS.CANCELLED]: 'Cancelled'
};

// ===== SKILL LEVELS =====
export const SKILL_LEVEL = {
    BEGINNER: 'BEGINNER',
    INTERMEDIATE: 'INTERMEDIATE',
    ADVANCED: 'ADVANCED',
    ANY: 'ANY'
};

export const SKILL_LEVEL_LABELS = {
    [SKILL_LEVEL.BEGINNER]: 'Beginner',
    [SKILL_LEVEL.INTERMEDIATE]: 'Intermediate',
    [SKILL_LEVEL.ADVANCED]: 'Advanced',
    [SKILL_LEVEL.ANY]: 'Any Level'
};

// ===== FRIENDSHIP STATUS =====
export const FRIENDSHIP_STATUS = {
    PENDING: 'PENDING',
    ACCEPTED: 'ACCEPTED',
    REJECTED: 'REJECTED'
};

// ===== NOTIFICATION TYPES =====
export const NOTIFICATION_TYPE = {
    CONFIRMATION: 'CONFIRMATION',
    REMINDER: 'REMINDER',
    CANCELLATION: 'CANCELLATION',
    MODIFICATION: 'MODIFICATION'
};

export const NOTIFICATION_TYPE_LABELS = {
    [NOTIFICATION_TYPE.CONFIRMATION]: 'Booking Confirmation',
    [NOTIFICATION_TYPE.REMINDER]: 'Reminder',
    [NOTIFICATION_TYPE.CANCELLATION]: 'Cancellation',
    [NOTIFICATION_TYPE.MODIFICATION]: 'Modification'
};

// ===== COURT REGISTRATION STATUS =====
export const REGISTRATION_STATUS = {
    PENDING: 'PENDING',
    APPROVED: 'APPROVED',
    REJECTED: 'REJECTED'
};

// ===== EQUIPMENT RENTAL STATUS =====
export const EQUIPMENT_STATUS = {
    ACTIVE: 'ACTIVE',
    RETURNED: 'RETURNED',
    DAMAGED: 'DAMAGED'
};

// ===== RATING VALUES =====
export const RATING_VALUES = [1, 2, 3, 4, 5];

export const RATING_LABELS = {
    1: 'Poor',
    2: 'Fair',
    3: 'Good',
    4: 'Very Good',
    5: 'Excellent'
};

// ===== DAYS OF WEEK =====
export const DAYS_OF_WEEK = [
    { value: 0, label: 'Sunday', short: 'Sun' },
    { value: 1, label: 'Monday', short: 'Mon' },
    { value: 2, label: 'Tuesday', short: 'Tue' },
    { value: 3, label: 'Wednesday', short: 'Wed' },
    { value: 4, label: 'Thursday', short: 'Thu' },
    { value: 5, label: 'Friday', short: 'Fri' },
    { value: 6, label: 'Saturday', short: 'Sat' }
];

// ===== COMMON SPORT TYPES =====
export const SPORT_TYPES = [
    'Basketball',
    'Tennis',
    'Badminton',
    'Volleyball',
    'Football',
    'Futsal',
    'Cricket',
    'Squash',
    'Table Tennis',
    'Other'
];

// ===== AMENITIES =====
export const COMMON_AMENITIES = [
    'Parking',
    'Restrooms',
    'Changing Rooms',
    'Showers',
    'Lockers',
    'Water Fountain',
    'First Aid',
    'Seating',
    'Lighting',
    'Scoreboard',
    'WiFi',
    'Cafeteria',
    'Pro Shop',
    'Air Conditioning',
    'Security'
];

// ===== PAGINATION =====
export const PAGINATION = {
    DEFAULT_PAGE_SIZE: 10,
    PAGE_SIZE_OPTIONS: [10, 20, 50, 100]
};

// ===== TIME SLOTS =====
export const DEFAULT_SLOT_DURATION = 1; // hours
export const MIN_BOOKING_DURATION = 0.5; // hours
export const MAX_BOOKING_DURATION = 8; // hours

// ===== VALIDATION RULES =====
export const VALIDATION = {
    PHONE_MIN_LENGTH: 10,
    PHONE_MAX_LENGTH: 15,
    PASSWORD_MIN_LENGTH: 8,
    NAME_MIN_LENGTH: 2,
    NAME_MAX_LENGTH: 100,
    DESCRIPTION_MAX_LENGTH: 1000,
    REVIEW_MIN_LENGTH: 10,
    REVIEW_MAX_LENGTH: 500
};

// ===== API ENDPOINTS (for reference) =====
export const API_ENDPOINTS = {
    AUTH: {
        LOGIN: '/api/auth/login/',
        REGISTER: '/api/auth/register/',
        LOGOUT: '/api/auth/logout/',
        STATUS: '/api/auth/status/',
        TOKEN_REFRESH: '/api/auth/token/refresh/',
        OTP_REQUEST: '/api/auth/otp/request/',
        OTP_VERIFY: '/api/auth/otp/verify/',
        PASSWORD_CHANGE: '/api/auth/password/change/',
        PASSWORD_RESET: '/api/auth/password/reset/confirm/'
    },
    USER: {
        PROFILE: '/api/user/profile/',
        PREFERENCES: '/api/users/preferences/',
        FRIENDSHIPS: '/api/users/friendships/',
        PLAYER_STATS: '/api/users/player-stats/'
    },
    COURTS: {
        COURTS: '/api/courts/courts/',
        CATEGORIES: '/api/courts/categories/',
        REGISTRATIONS: '/api/courts/registrations/'
    },
    BOOKINGS: {
        BOOKINGS: '/api/bookings/bookings/',
        BOOKING_SHARES: '/api/bookings/booking-shares/',
        MATCH_EVENTS: '/api/bookings/match-events/',
        EQUIPMENT_RENTALS: '/api/bookings/equipment-rentals/',
        PLAYER_RATINGS: '/api/bookings/player-ratings/',
        NOTIFICATIONS: '/api/bookings/notifications/',
        CANCELLATION_POLICIES: '/api/bookings/cancellation-policies/'
    }
};

// ===== UI CONSTANTS =====
export const UI = {
    TOAST_DURATION: 3000,
    DEBOUNCE_DELAY: 300,
    NOTIFICATION_POLL_INTERVAL: 30000, // 30 seconds
    MAX_FILE_SIZE: 5 * 1024 * 1024, // 5MB
    ALLOWED_IMAGE_TYPES: ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'],
    ALLOWED_DOCUMENT_TYPES: ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png']
};

// ===== ERROR MESSAGES =====
export const ERROR_MESSAGES = {
    NETWORK_ERROR: 'Network error. Please check your connection.',
    SERVER_ERROR: 'Server error. Please try again later.',
    UNAUTHORIZED: 'Authentication required. Please login again.',
    FORBIDDEN: 'You do not have permission to perform this action.',
    NOT_FOUND: 'Resource not found.',
    VALIDATION_ERROR: 'Please check your input and try again.',
    UNKNOWN_ERROR: 'An unexpected error occurred.'
};

// ===== SUCCESS MESSAGES =====
export const SUCCESS_MESSAGES = {
    BOOKING_CREATED: 'Booking created successfully!',
    BOOKING_CANCELLED: 'Booking cancelled successfully.',
    PROFILE_UPDATED: 'Profile updated successfully!',
    REVIEW_SUBMITTED: 'Review submitted successfully!',
    FRIEND_REQUEST_SENT: 'Friend request sent!',
    FRIEND_REQUEST_ACCEPTED: 'Friend request accepted!',
    MATCH_JOINED: 'Successfully joined the match!',
    MATCH_CREATED: 'Match created successfully!'
};

// Export all as a single object for convenience
export default {
    USER_ROLES,
    ROLE_LABELS,
    BOOKING_STATUS,
    BOOKING_STATUS_LABELS,
    PAYMENT_STATUS,
    PAYMENT_METHOD,
    PAYMENT_METHOD_LABELS,
    MATCH_STATUS,
    MATCH_STATUS_LABELS,
    SKILL_LEVEL,
    SKILL_LEVEL_LABELS,
    FRIENDSHIP_STATUS,
    NOTIFICATION_TYPE,
    NOTIFICATION_TYPE_LABELS,
    REGISTRATION_STATUS,
    EQUIPMENT_STATUS,
    RATING_VALUES,
    RATING_LABELS,
    DAYS_OF_WEEK,
    SPORT_TYPES,
    COMMON_AMENITIES,
    PAGINATION,
    DEFAULT_SLOT_DURATION,
    MIN_BOOKING_DURATION,
    MAX_BOOKING_DURATION,
    VALIDATION,
    API_ENDPOINTS,
    UI,
    ERROR_MESSAGES,
    SUCCESS_MESSAGES
};