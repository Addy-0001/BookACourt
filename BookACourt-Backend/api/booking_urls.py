from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .booking_views import (
    BookingViewSet,
    CancellationPolicyViewSet,
    BookingNotificationViewSet,
    EquipmentRentalViewSet,
    MatchEventViewSet,
    PlayerRatingViewSet,
    BookingShareViewSet,
    RecurringBookingViewSet
)

# Create router
router = DefaultRouter()
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'cancellation-policies',
                CancellationPolicyViewSet, basename='cancellation-policy')
router.register(r'notifications', BookingNotificationViewSet,
                basename='booking-notification')
router.register(r'equipment-rentals', EquipmentRentalViewSet,
                basename='equipment-rental')
router.register(r'match-events', MatchEventViewSet, basename='match-event')
router.register(r'player-ratings', PlayerRatingViewSet,
                basename='player-rating')
router.register(r'booking-shares', BookingShareViewSet,
                basename='booking-share')
router.register(r'recurring', RecurringBookingViewSet,
                basename='recurring-booking')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
]
