from django.db import models
# users/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
import pyotp

class UserRole(models.TextChoices):
    PLAYER = 'PLAYER', 'Player/User'
    COURT_MANAGER = 'COURT_MANAGER', 'Court Manager'
    COURT_OWNER = 'COURT_OWNER', 'Court Owner'
    SUPER_USER = 'SUPER_USER', 'Super User (Admin)'

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Phone number is required')
        
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', UserRole.SUPER_USER)
        extra_fields.setdefault('is_phone_verified', True)
        
        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    phone_number = PhoneNumberField(unique=True)
    email = models.EmailField(blank=True, null=True)
    full_name = models.CharField(max_length=255)
    
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.PLAYER
    )
    
    # For Court Owner/Manager - link to their courts
    # This will be used in related models
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    
    # OTP fields
    otp_secret = models.CharField(max_length=32, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    
    # Profile fields
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['full_name']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['phone_number']),
            models.Index(fields=['role']),
        ]
    
    def __str__(self):
        return f"{self.full_name} ({self.phone_number})"
    
    def generate_otp(self):
        """Generate a new OTP secret and return the OTP code"""
        self.otp_secret = pyotp.random_base32()
        self.otp_created_at = timezone.now()
        self.save()
        
        totp = pyotp.TOTP(self.otp_secret, interval=300)  # 5 minutes validity
        return totp.now()
    
    def verify_otp(self, otp_code):
        """Verify the provided OTP code"""
        if not self.otp_secret or not self.otp_created_at:
            return False
        
        # Check if OTP is expired (5 minutes)
        time_diff = timezone.now() - self.otp_created_at
        if time_diff.total_seconds() > 300:
            return False
        
        totp = pyotp.TOTP(self.otp_secret, interval=300)
        return totp.verify(otp_code, valid_window=1)
    
    @property
    def is_super_user(self):
        return self.role == UserRole.SUPER_USER
    
    @property
    def is_court_owner(self):
        return self.role == UserRole.COURT_OWNER
    
    @property
    def is_court_manager(self):
        return self.role == UserRole.COURT_MANAGER
    
    @property
    def is_player(self):
        return self.role == UserRole.PLAYER
    
    @property
    def role_permissions(self):
        """Return permissions based on role"""
        permissions = {
            UserRole.PLAYER: [
                'view_courts',
                'book_court',
                'view_own_bookings',
                'cancel_own_booking',
                'view_profile',
                'update_own_profile',
            ],
            UserRole.COURT_MANAGER: [
                'view_courts',
                'view_assigned_courts',
                'manage_bookings',
                'view_court_schedule',
                'update_court_availability',
                'view_revenue_reports',
                'manage_court_pricing',
            ],
            UserRole.COURT_OWNER: [
                'view_courts',
                'create_court',
                'update_own_courts',
                'delete_own_courts',
                'assign_managers',
                'view_all_bookings',
                'manage_bookings',
                'view_analytics',
                'view_revenue_reports',
                'manage_pricing',
                'manage_court_amenities',
            ],
            UserRole.SUPER_USER: [
                'all_permissions',
                'manage_all_users',
                'manage_all_courts',
                'view_platform_analytics',
                'manage_system_settings',
                'approve_court_owners',
                'suspend_users',
                'view_all_transactions',
            ]
        }
        return permissions.get(self.role, [])
    
    def can_manage_court(self, court):
        """Check if user can manage a specific court"""
        if self.is_super_user:
            return True
        if self.is_court_owner:
            return court.owner == self
        if self.is_court_manager:
            return court.managers.filter(id=self.id).exists()
        return False

