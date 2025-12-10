from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from dj_rest_auth.registration.views import RegisterView
from .views import (
    LoginView,
    OTPRequestView,
    OTPVerifyView,
    PasswordResetConfirmView,
    ChangePasswordView,
    UserProfileView,
    LogoutView,
    check_auth_status,
)

app_name = 'api'

urlpatterns = [
    # Custom authentication endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),

    # JWT token refresh
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # OTP endpoints
    path('auth/otp/request/', OTPRequestView.as_view(), name='otp_request'),
    path('auth/otp/verify/', OTPVerifyView.as_view(), name='otp_verify'),

    # Password management
    path('auth/password/reset/confirm/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('auth/password/change/',
         ChangePasswordView.as_view(), name='password_change'),

    # Auth status
    path('auth/status/', check_auth_status, name='auth_status'),

    # User profile
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('courts/', include('api.court_urls'))
]
