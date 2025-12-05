from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'password', 'password_confirm', 'role', 'first_name', 'last_name']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already registered.")
        
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        user = authenticate(username=email, password=password)
        
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        
        data['user'] = user
        return data


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField()


class PhoneVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'phone_number', 'first_name', 'last_name', 'role', 
                  'is_email_verified', 'is_phone_verified', 'created_at', 'updated_at']
        read_only_fields = ['id', 'is_email_verified', 'is_phone_verified', 'created_at', 'updated_at']