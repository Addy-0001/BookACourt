// src/services/index.js
// Central export for all services

export { authService } from './authService';
export { bookingService } from './bookingService';
export { courtService } from './courtService';
export { paymentService } from './paymentService';
export { userService } from './userService';
export { notificationService } from './notificationService';
export { cancellationPolicyService } from './cancellationPolicyService';

// Re-export the API client for direct usage if needed
export { default as apiClient } from './api';

// Service factory for convenience
export const services = {
    auth: () => import('./authService').then(m => m.authService),
    booking: () => import('./bookingService').then(m => m.bookingService),
    court: () => import('./courtService').then(m => m.courtService),
    payment: () => import('./paymentService').then(m => m.paymentService),
    user: () => import('./userService').then(m => m.userService),
    notification: () => import('./notificationService').then(m => m.notificationService),
    cancellationPolicy: () => import('./cancellationPolicyService').then(m => m.cancellationPolicyService)
};