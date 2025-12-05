from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = router.urls

# Additional custom endpoints
urlpatterns += [
    path('auth/register/', UserViewSet.as_view({'post': 'register'}), name='register'),
    path('auth/verify-email/', UserViewSet.as_view({'post': 'verify_email'}), name='verify_email'),
    path('auth/login/', UserViewSet.as_view({'post': 'login'}), name='login'),
    path('auth/send-phone-verification/', UserViewSet.as_view({'post': 'send_phone_verification'}), name='send_phone_verification'),
    path('auth/verify-phone/', UserViewSet.as_view({'post': 'verify_phone'}), name='verify_phone'),
    path('auth/request-password-reset/', UserViewSet.as_view({'post': 'request_password_reset'}), name='request_password_reset'),
    path('auth/reset-password/', UserViewSet.as_view({'post': 'reset_password'}), name='reset_password'),
    path('profile/', UserViewSet.as_view({'get': 'profile'}), name='profile'),
    path('profile/update/', UserViewSet.as_view({'put': 'update_profile'}), name='update_profile'),
]