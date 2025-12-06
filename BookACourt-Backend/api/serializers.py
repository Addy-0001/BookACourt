from rest_framework import serializers
from dj_rest_auth.serializers import LoginSerializer as DefaultLoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer as DefaultRegisterSerializer
from dj_rest_auth.serializers import PasswordResetSerializer as DefaultPasswordResetSerializer
from dj_rest_auth.serializers import JWTSerializer as DefaultJWTSerializer
from django.contrib.auth import get_user_model
from phonenumber_field.serializerfields import PhoneNumberField
from user_management.models import UserRole

User = get_user_model()


class UserDetailsSerializer(serializers.ModelSerializer):
    """Serializer for user details"""

    class Meta:
        model = User
        fields = (
            'id', 'phone_number', 'email', 'full_name', 'role',
            'is_active', 'is_phone_verified', 'profile_picture',
            'date_of_birth', 'address', 'city', 'loyalty_points',
            'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'is_phone_verified', 'loyalty_points',
            'created_at', 'updated_at'
        )


class RegisterSerializer(DefaultRegisterSerializer):
    """Custom registration serializer using phone number"""

    phone_number = PhoneNumberField(required=True)
    full_name = serializers.CharField(required=True, max_length=255)
    role = serializers.ChoiceField(
        choices=UserRole.choices,
        default=UserRole.PLAYER
    )
    email = serializers.EmailField(required=False, allow_blank=True)

    # Remove username fields
    username = None

    class Meta:
        model = User
        fields = (
            'phone_number', 'full_name', 'email', 'password1',
            'password2', 'role'
        )

    def validate_phone_number(self, value):
        """Validate that phone number is unique"""
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(
                "A user with this phone number already exists."
            )
        return value

    def validate_email(self, value):
        """Validate email uniqueness only if provided"""
        if value and User.objects.filter(email=value).exclude(email='').exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )
        return value or ''  # Return empty string if not provided

    def validate_role(self, value):
        """Only allow registration for specific roles"""
        allowed_roles = [UserRole.PLAYER, UserRole.COURT_OWNER]
        if value not in allowed_roles:
            raise serializers.ValidationError(
                "You can only register as a Player or Court Owner."
            )
        return value

    def get_cleaned_data(self):
        """Return cleaned data for user creation"""
        return {
            'phone_number': self.validated_data.get('phone_number', ''),
            'full_name': self.validated_data.get('full_name', ''),
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'role': self.validated_data.get('role', UserRole.PLAYER),
        }

    def save(self, request):
        """Create and return new user"""
        cleaned_data = self.get_cleaned_data()
        user = User.objects.create_user(
            phone_number=cleaned_data['phone_number'],
            password=cleaned_data['password1'],
            full_name=cleaned_data['full_name'],
            email=cleaned_data.get('email', ''),
            role=cleaned_data['role'],
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Custom login serializer using phone number"""

    phone_number = PhoneNumberField(required=True)
    password = serializers.CharField(
        required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        """Validate phone number and password"""
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        if phone_number and password:
            # Get user by phone number
            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    'Unable to log in with provided credentials.'
                )

            # Check password
            if not user.check_password(password):
                raise serializers.ValidationError(
                    'Unable to log in with provided credentials.'
                )

            # Check if user is active
            if not user.is_active:
                raise serializers.ValidationError(
                    'User account is disabled.'
                )

            attrs['user'] = user
        else:
            raise serializers.ValidationError(
                'Must include "phone_number" and "password".'
            )

        return attrs


class OTPRequestSerializer(serializers.Serializer):
    """Serializer for OTP request"""
    phone_number = PhoneNumberField(required=True)

    def validate_phone_number(self, value):
        """Validate that phone number exists"""
        if not User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(
                "No user found with this phone number."
            )
        return value


class OTPVerifySerializer(serializers.Serializer):
    """Serializer for OTP verification"""
    phone_number = PhoneNumberField(required=True)
    otp_code = serializers.CharField(required=True, max_length=6)

    def validate(self, attrs):
        """Validate OTP code"""
        phone_number = attrs.get('phone_number')
        otp_code = attrs.get('otp_code')

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "No user found with this phone number."
            )

        if not user.verify_otp(otp_code):
            raise serializers.ValidationError(
                "Invalid or expired OTP code."
            )

        attrs['user'] = user
        return attrs


class PasswordResetSerializer(DefaultPasswordResetSerializer):
    """Custom password reset serializer using phone number"""

    phone_number = PhoneNumberField(required=True)
    email = None  # Remove email field

    def validate_phone_number(self, value):
        """Validate that phone number exists"""
        if not User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(
                "No user found with this phone number."
            )
        return value

    def save(self):
        """Send OTP for password reset"""
        phone_number = self.validated_data['phone_number']
        user = User.objects.get(phone_number=phone_number)

        # Generate OTP
        otp_code = user.generate_otp()

        # Send OTP via SMS (implement your SMS sending logic)
        from api.utils import send_otp_sms
        send_otp_sms(phone_number, otp_code)

        return phone_number


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for password reset confirmation"""
    phone_number = PhoneNumberField(required=True)
    otp_code = serializers.CharField(required=True, max_length=6)
    new_password1 = serializers.CharField(required=True, write_only=True)
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        """Validate OTP and passwords"""
        phone_number = attrs.get('phone_number')
        otp_code = attrs.get('otp_code')
        password1 = attrs.get('new_password1')
        password2 = attrs.get('new_password2')

        # Validate passwords match
        if password1 != password2:
            raise serializers.ValidationError(
                {"new_password2": "The two password fields didn't match."}
            )

        # Get user and verify OTP
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "No user found with this phone number."
            )

        if not user.verify_otp(otp_code):
            raise serializers.ValidationError(
                {"otp_code": "Invalid or expired OTP code."}
            )

        attrs['user'] = user
        return attrs

    def save(self):
        """Reset password"""
        user = self.validated_data['user']
        password = self.validated_data['new_password1']
        user.set_password(password)
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password1 = serializers.CharField(required=True, write_only=True)
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        """Validate old password"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, attrs):
        """Validate passwords match"""
        password1 = attrs.get('new_password1')
        password2 = attrs.get('new_password2')

        if password1 != password2:
            raise serializers.ValidationError(
                {"new_password2": "The two password fields didn't match."}
            )

        return attrs

    def save(self):
        """Change password"""
        user = self.context['request'].user
        password = self.validated_data['new_password1']
        user.set_password(password)
        user.save()
        return user


class JWTSerializer(DefaultJWTSerializer):
    """Custom JWT serializer with user details"""
    user = UserDetailsSerializer(read_only=True)
