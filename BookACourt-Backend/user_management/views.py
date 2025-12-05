from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone
from datetime import timedelta
import secrets
import string

from .models import CustomUser, EmailVerificationToken, PhoneVerificationToken, PasswordResetToken
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    EmailVerificationSerializer,
    PhoneVerificationSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    UserProfileSerializer
)
from .tasks import send_verification_email, send_password_reset_email
from .utils import generate_otp


class UserViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate and send email verification token
            token = secrets.token_urlsafe(32)
            expires_at = timezone.now() + timedelta(hours=24)
            
            EmailVerificationToken.objects.update_or_create(
                user=user,
                defaults={
                    'token': token,
                    'expires_at': expires_at,
                    'is_used': False
                }
            )
            
            # Send verification email asynchronously
            send_verification_email.delay(user.id, token)
            
            return Response(
                {
                    'message': 'User registered successfully. Please check your email for verification.',
                    'user_id': str(user.id),
                    'email': user.email
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def verify_email(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            
            try:
                verification = EmailVerificationToken.objects.get(
                    token=token,
                    is_used=False,
                    expires_at__gt=timezone.now()
                )
                
                user = verification.user
                user.is_email_verified = True
                user.save()
                
                verification.is_used = True
                verification.save()
                
                return Response(
                    {'message': 'Email verified successfully.'},
                    status=status.HTTP_200_OK
                )
            except EmailVerificationToken.DoesNotExist:
                return Response(
                    {'error': 'Invalid or expired verification token.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            if not user.is_email_verified:
                return Response(
                    {'error': 'Please verify your email before logging in.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not user.is_active:
                return Response(
                    {'error': 'Your account has been suspended.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(user)
            
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserProfileSerializer(user).data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def send_phone_verification(self, request):
        email = request.data.get('email')
        
        try:
            user = CustomUser.objects.get(email=email)
            
            if not user.phone_number:
                return Response(
                    {'error': 'Phone number not registered.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            otp = generate_otp()
            expires_at = timezone.now() + timedelta(minutes=10)
            
            PhoneVerificationToken.objects.update_or_create(
                user=user,
                defaults={
                    'token': otp,
                    'expires_at': expires_at,
                    'is_used': False,
                    'attempts': 0
                }
            )
            
            # TODO: Send OTP via SMS service
            # Example: send_sms_otp.delay(user.phone_number, otp)
            
            return Response(
                {'message': f'OTP sent to {user.phone_number}'},
                status=status.HTTP_200_OK
            )
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def verify_phone(self, request):
        serializer = PhoneVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            
            try:
                user = CustomUser.objects.get(email=email)
                verification = PhoneVerificationToken.objects.get(
                    user=user,
                    is_used=False,
                    expires_at__gt=timezone.now()
                )
                
                if verification.attempts >= 3:
                    return Response(
                        {'error': 'Too many failed attempts. Request a new OTP.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                if verification.token != otp:
                    verification.attempts += 1
                    verification.save()
                    return Response(
                        {'error': 'Invalid OTP.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                user.is_phone_verified = True
                user.save()
                
                verification.is_used = True
                verification.save()
                
                return Response(
                    {'message': 'Phone verified successfully.'},
                    status=status.HTTP_200_OK
                )
            except (CustomUser.DoesNotExist, PhoneVerificationToken.DoesNotExist):
                return Response(
                    {'error': 'Invalid email or verification token.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def request_password_reset(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                user = CustomUser.objects.get(email=email)
                
                token = secrets.token_urlsafe(32)
                expires_at = timezone.now() + timedelta(hours=1)
                
                PasswordResetToken.objects.update_or_create(
                    user=user,
                    defaults={
                        'token': token,
                        'expires_at': expires_at,
                        'is_used': False
                    }
                )
                
                send_password_reset_email.delay(user.id, token)
                
                return Response(
                    {'message': 'Password reset link sent to your email.'},
                    status=status.HTTP_200_OK
                )
            except CustomUser.DoesNotExist:
                # Return generic message for security
                return Response(
                    {'message': 'If email exists, password reset link will be sent.'},
                    status=status.HTTP_200_OK
                )

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def reset_password(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            password = serializer.validated_data['password']
            
            try:
                reset_token = PasswordResetToken.objects.get(
                    token=token,
                    is_used=False,
                    expires_at__gt=timezone.now()
                )
                
                user = reset_token.user
                user.set_password(password)
                user.save()
                
                reset_token.is_used = True
                reset_token.save()
                
                return Response(
                    {'message': 'Password reset successfully.'},
                    status=status.HTTP_200_OK
                )
            except PasswordResetToken.DoesNotExist:
                return Response(
                    {'error': 'Invalid or expired password reset token.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Profile updated successfully.', 'data': serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)