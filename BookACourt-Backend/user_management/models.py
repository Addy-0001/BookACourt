from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
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
    # Use empty string instead of null
    email = models.EmailField(blank=True, default='')
    full_name = models.CharField(max_length=255)

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.PLAYER
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)

    # OTP fields
    otp_secret = models.CharField(max_length=32, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    # Profile fields
    profile_picture = models.ImageField(
        upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)

    # Loyalty points for players (User Story 45)
    loyalty_points = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['full_name']

    # Required for allauth compatibility
    EMAIL_FIELD = 'email'

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['phone_number']),
            models.Index(fields=['role']),
            models.Index(fields=['is_active']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['email'],
                condition=~models.Q(email=''),
                name='unique_email_when_provided'
            )
        ]

    def __str__(self):
        return f"{self.full_name} ({self.phone_number})"

    # Add this property for allauth compatibility
    @property
    def username(self):
        """Return phone_number as username for allauth"""
        return str(self.phone_number)

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

    def can_manage_court(self, court):
        """Check if user can manage a specific court"""
        if self.is_super_user:
            return True
        if self.is_court_owner:
            return court.owner == self
        if self.is_court_manager:
            return court.managers.filter(id=self.id).exists()
        return False


class PasswordResetToken(models.Model):
    """Model for password reset tokens (User Story 47)"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reset_tokens')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = 'password_reset_tokens'
        ordering = ['-created_at']

    def __str__(self):
        return f"Reset token for {self.user.phone_number}"

    def is_valid(self):
        """Check if token is still valid"""
        return not self.is_used and timezone.now() < self.expires_at


class UserPreference(models.Model):
    """Model for user preferences (User Story 31)"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='preferences')

    # Notification preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)

    # Game preferences (for players)
    preferred_sports = models.CharField(
        max_length=255, blank=True)  # Comma separated
    preferred_time_slots = models.CharField(
        max_length=255, blank=True)  # e.g., "morning,evening"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_preferences'

    def __str__(self):
        return f"Preferences for {self.user.phone_number}"


class PlayerStats(models.Model):
    """Model to track player statistics (User Story 44)"""
    player = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='stats',
        limit_choices_to={'role': UserRole.PLAYER}
    )

    total_bookings = models.IntegerField(default=0)
    total_matches_played = models.IntegerField(default=0)
    matches_won = models.IntegerField(default=0)
    matches_lost = models.IntegerField(default=0)

    # Sportsmanship rating (User Story 40)
    sportsmanship_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=5.00,
        help_text="Rating out of 5.00"
    )
    total_ratings_received = models.IntegerField(default=0)

    # No-show tracking (User Story 24)
    no_show_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'player_stats'
        verbose_name = 'Player Statistics'
        verbose_name_plural = 'Player Statistics'

    def __str__(self):
        return f"Stats for {self.player.full_name}"

    @property
    def win_loss_ratio(self):
        """Calculate win/loss ratio"""
        if self.matches_lost == 0:
            return self.matches_won
        return round(self.matches_won / self.matches_lost, 2)


class Friendship(models.Model):
    """Model for friend connections (User Story 42)"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_friend_requests'
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_friend_requests'
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'friendships'
        unique_together = ['from_user', 'to_user']
        indexes = [
            models.Index(fields=['from_user', 'status']),
            models.Index(fields=['to_user', 'status']),
        ]

    def __str__(self):
        return f"{self.from_user.full_name} -> {self.to_user.full_name} ({self.status})"
