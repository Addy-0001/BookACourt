from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .user_views import (
    PlayerStatsViewSet,
    UserPreferenceViewSet,
    FriendshipViewSet
)

# Create router
router = DefaultRouter()
router.register(r'player-stats', PlayerStatsViewSet, basename='player-stats')
router.register(r'preferences', UserPreferenceViewSet,
                basename='user-preference')
router.register(r'friendships', FriendshipViewSet, basename='friendship')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
]
