from requests import request
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.contrib.auth import get_user_model


from .serializers import (
    UserDetailsSerializer,
    OTPRequestSerializer,
    OTPVerifySerializer,
    PasswordResetConfirmSerializer,
    ChangePasswordSerializer,
    LoginSerializer,
)
from .utils import send_otp_sms, send_welcome_sms

User = get_user_model()


class LoginView(APIView):
    """
    Custom login view using phone number
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @extend_schema(
        request=LoginSerializer,
        responses={200: {'description': 'Login successful'}},
        description='Login using phone number and password'
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserDetailsSerializer(
                user,
                context={'request': request}
            ).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)


class OTPRequestView(APIView):
    """
    Request OTP for phone verification or password reset
    """
    permission_classes = [AllowAny]
    serializer_class = OTPRequestSerializer

    @extend_schema(
        request=OTPRequestSerializer,
        responses={200: {'description': 'OTP sent successfully'}},
        description='Request OTP code for phone verification'
    )
    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        user = User.objects.get(phone_number=phone_number)

        # Generate and send OTP
        otp_code = user.generate_otp()
        send_otp_sms(phone_number, otp_code)

        return Response({
            'message': 'OTP sent successfully',
            'phone_number': str(phone_number)
        }, status=status.HTTP_200_OK)


class OTPVerifyView(APIView):
    """
    Verify OTP and mark phone as verified
    """
    permission_classes = [AllowAny]
    serializer_class = OTPVerifySerializer

    @extend_schema(
        request=OTPVerifySerializer,
        responses={200: {'description': 'Phone verified successfully'}},
        description='Verify OTP code and mark phone as verified'
    )
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        user.is_phone_verified = True
        user.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Phone verified successfully',
            'user': UserDetailsSerializer(
                user,
                context={'request': request}
            ).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """
    Confirm password reset with OTP
    """
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    @extend_schema(
        request=PasswordResetConfirmSerializer,
        responses={200: {'description': 'Password reset successfully'}},
        description='Reset password using OTP verification'
    )
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response({
            'message': 'Password reset successfully',
        }, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    """
    Change password for authenticated user
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={200: {'description': 'Password changed successfully'}},
        description='Change password for authenticated user'
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Password changed successfully',
        }, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    """
    Get and update user profile
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailsSerializer

    @extend_schema(
        responses={200: UserDetailsSerializer},
        description='Get current user profile'
    )
    def get(self, request):
        serializer = UserDetailsSerializer(
            request.user,
            context={'request': request}
        )
        return Response(serializer.data)

    @extend_schema(
        request=UserDetailsSerializer,
        responses={200: UserDetailsSerializer},
        description='Update current user profile'
    )
    def patch(self, request):
        serializer = UserDetailsSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LogoutView(APIView):
    """
    Logout user by blacklisting refresh token
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request={'refresh': 'string'},
        responses={200: {'description': 'Logout successful'}},
        description='Logout user by blacklisting refresh token'
    )
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_auth_status(request):
    """
    Check if user is authenticated and return user details
    """
    return Response({
        'authenticated': True,
        'user': UserDetailsSerializer(
            request.user,
            context={'request': request}
        ).data
    })
