// src/utils/helpers.js

// ===== DATE & TIME UTILITIES =====
export const formatDate = (dateString, options = {}) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    const defaultOptions = { year: 'numeric', month: 'short', day: 'numeric' };
    return date.toLocaleDateString('en-US', { ...defaultOptions, ...options });
};

export const formatDateTime = (dateString, options = {}) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    const defaultOptions = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return date.toLocaleDateString('en-US', { ...defaultOptions, ...options });
};

export const formatTime = (timeString) => {
    if (!timeString) return 'N/A';
    return timeString.slice(0, 5); // Returns HH:MM format
};

export const getTimeFromNow = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = date - now;
    const diffMins = Math.floor(diffMs / 60000);

    if (diffMins < 0) return 'Past';
    if (diffMins < 60) return `${diffMins}m`;
    if (diffMins < 1440) return `${Math.floor(diffMins / 60)}h`;
    return `${Math.floor(diffMins / 1440)}d`;
};

export const isToday = (dateString) => {
    const date = new Date(dateString);
    const today = new Date();
    return date.toDateString() === today.toDateString();
};

export const isFuture = (dateString, timeString = null) => {
    const dateTimeStr = timeString ? `${dateString} ${timeString}` : dateString;
    return new Date(dateTimeStr) > new Date();
};

// ===== CURRENCY UTILITIES =====
export const formatCurrency = (amount, currency = 'Rs') => {
    if (amount == null) return 'N/A';
    const num = parseFloat(amount);
    return `${currency} ${num.toFixed(2)}`;
};

export const parseCurrency = (currencyString) => {
    if (!currencyString) return 0;
    const num = currencyString.toString().replace(/[^0-9.-]+/g, '');
    return parseFloat(num) || 0;
};

// ===== STATUS UTILITIES =====
export const getStatusClass = (status, type = 'booking') => {
    const statusMaps = {
        booking: {
            'PENDING': 'bg-yellow-100 text-yellow-800',
            'CONFIRMED': 'bg-green-100 text-green-800',
            'CANCELLED': 'bg-red-100 text-red-800',
            'COMPLETED': 'bg-blue-100 text-blue-800',
            'NO_SHOW': 'bg-gray-100 text-gray-800'
        },
        payment: {
            'PENDING': 'text-yellow-600',
            'COMPLETED': 'text-green-600',
            'REFUNDED': 'text-blue-600',
            'FAILED': 'text-red-600'
        },
        match: {
            'OPEN': 'bg-green-100 text-green-800',
            'FULL': 'bg-blue-100 text-blue-800',
            'IN_PROGRESS': 'bg-purple-100 text-purple-800',
            'COMPLETED': 'bg-gray-100 text-gray-800',
            'CANCELLED': 'bg-red-100 text-red-800'
        }
    };
    return statusMaps[type]?.[status] || 'bg-gray-100 text-gray-800';
};

export const getStatusLabel = (status) => {
    return status.replace(/_/g, ' ').toLowerCase()
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
};

// ===== VALIDATION UTILITIES =====
export const validatePhone = (phone) => {
    const phoneRegex = /^(\+977)?[0-9]{10}$/;
    return phoneRegex.test(phone.replace(/\s/g, ''));
};

export const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
};

export const validateTime = (startTime, endTime) => {
    if (!startTime || !endTime) return false;
    const start = new Date(`2000-01-01 ${startTime}`);
    const end = new Date(`2000-01-01 ${endTime}`);
    return end > start;
};

// ===== STRING UTILITIES =====
export const truncate = (str, length = 50) => {
    if (!str) return '';
    return str.length > length ? str.substring(0, length) + '...' : str;
};

export const capitalize = (str) => {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
};

export const slugify = (str) => {
    return str
        .toLowerCase()
        .replace(/[^\w\s-]/g, '')
        .replace(/\s+/g, '-')
        .replace(/-+/g, '-')
        .trim();
};

// ===== ARRAY UTILITIES =====
export const groupBy = (array, key) => {
    return array.reduce((result, item) => {
        const group = item[key];
        if (!result[group]) result[group] = [];
        result[group].push(item);
        return result;
    }, {});
};

export const sortBy = (array, key, order = 'asc') => {
    return [...array].sort((a, b) => {
        const aVal = a[key];
        const bVal = b[key];
        if (aVal < bVal) return order === 'asc' ? -1 : 1;
        if (aVal > bVal) return order === 'asc' ? 1 : -1;
        return 0;
    });
};

// ===== OBJECT UTILITIES =====
export const isEmpty = (obj) => {
    return obj == null || Object.keys(obj).length === 0;
};

export const pick = (obj, keys) => {
    return keys.reduce((result, key) => {
        if (key in obj) result[key] = obj[key];
        return result;
    }, {});
};

export const omit = (obj, keys) => {
    const result = { ...obj };
    keys.forEach(key => delete result[key]);
    return result;
};

// ===== DEBOUNCE & THROTTLE =====
export const debounce = (func, wait = 300) => {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

export const throttle = (func, limit = 300) => {
    let inThrottle;
    return function executedFunction(...args) {
        if (!inThrottle) {
            func(...args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
};

// ===== STORAGE UTILITIES =====
export const storage = {
    get(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch {
            return defaultValue;
        }
    },

    set(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch {
            return false;
        }
    },

    remove(key) {
        try {
            localStorage.removeItem(key);
            return true;
        } catch {
            return false;
        }
    },

    clear() {
        try {
            localStorage.clear();
            return true;
        } catch {
            return false;
        }
    }
};

// ===== ERROR HANDLING =====
export const handleApiError = (error) => {
    if (error.response) {
        const { status, data } = error.response;

        if (status === 401) {
            return 'Authentication required. Please login again.';
        } else if (status === 403) {
            return 'You do not have permission to perform this action.';
        } else if (status === 404) {
            return 'Resource not found.';
        } else if (status === 422 || status === 400) {
            if (typeof data === 'object') {
                const firstError = Object.values(data)[0];
                return Array.isArray(firstError) ? firstError[0] : firstError;
            }
            return data.detail || data.message || 'Invalid request.';
        } else if (status >= 500) {
            return 'Server error. Please try again later.';
        }

        return data.detail || data.message || 'An error occurred.';
    } else if (error.request) {
        return 'Network error. Please check your connection.';
    }

    return error.message || 'An unexpected error occurred.';
};

// ===== BOOKING UTILITIES =====
export const calculateDuration = (startTime, endTime) => {
    if (!startTime || !endTime) return 0;
    const start = new Date(`2000-01-01 ${startTime}`);
    const end = new Date(`2000-01-01 ${endTime}`);
    return Math.max(0, (end - start) / (1000 * 60 * 60));
};

export const generateTimeSlots = (openTime, closeTime, slotDuration = 1) => {
    const slots = [];
    let current = new Date(`2000-01-01 ${openTime}`);
    const end = new Date(`2000-01-01 ${closeTime}`);

    while (current < end) {
        const next = new Date(current.getTime() + slotDuration * 60 * 60 * 1000);
        if (next <= end) {
            slots.push({
                start_time: current.toTimeString().slice(0, 5),
                end_time: next.toTimeString().slice(0, 5)
            });
        }
        current = next;
    }

    return slots;
};

// ===== RATING UTILITIES =====
export const getRatingStars = (rating) => {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);

    return {
        full: fullStars,
        half: hasHalfStar ? 1 : 0,
        empty: emptyStars
    };
};

export const calculateAverageRating = (reviews) => {
    if (!reviews || reviews.length === 0) return 0;
    const sum = reviews.reduce((acc, review) => acc + review.rating, 0);
    return (sum / reviews.length).toFixed(1);
};