from django.db import models
from user_management.models import User, UserRole


class CourtCategory(models.Model):
    """Model for court categories (User Story 9)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.ImageField(
        upload_to='category_icons/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'court_categories'
        verbose_name = 'Court Category'
        verbose_name_plural = 'Court Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class CourtRegistration(models.Model):
    """Model for court registration requests (User Story 1, 10)"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='court_registrations',
        limit_choices_to={'role': UserRole.COURT_OWNER}
    )

    # Basic court information
    court_name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)

    # Documents
    registration_documents = models.FileField(
        upload_to='court_registrations/documents/')
    court_images = models.ImageField(upload_to='court_registrations/images/')

    # Status
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='PENDING')
    rejection_reason = models.TextField(blank=True)

    # Review information
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_registrations',
        limit_choices_to={'role': UserRole.SUPER_USER}
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'court_registrations'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['owner']),
        ]

    def __str__(self):
        return f"{self.court_name} - {self.status}"


class Court(models.Model):
    """Model for approved courts (User Story 11)"""
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_courts',
        limit_choices_to={'role': UserRole.COURT_OWNER}
    )
    managers = models.ManyToManyField(
        User,
        related_name='managed_courts',
        blank=True,
        limit_choices_to={'role': UserRole.COURT_MANAGER}
    )

    # Location
    address = models.TextField()
    city = models.CharField(max_length=100)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)

    # Court details
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        CourtCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='courts'
    )
    # Basketball, Tennis, Badminton, etc.
    court_type = models.CharField(max_length=50)
    is_indoor = models.BooleanField(default=False)

    # Capacity and amenities
    capacity = models.IntegerField(default=10)
    amenities = models.TextField(
        blank=True, help_text="Comma-separated list of amenities")

    # Pricing (User Story 14)
    base_hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)

    # Operating hours
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    # Status
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    # Rating
    average_rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.IntegerField(default=0)

    # Contact
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'courts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['city', 'is_active']),
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['court_type']),
        ]

    def __str__(self):
        return f"{self.name} - {self.court_type}"


class CourtImage(models.Model):
    """Model for multiple court images"""
    court = models.ForeignKey(
        Court, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='court_images/')
    caption = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'court_images'
        ordering = ['-is_primary', '-uploaded_at']

    def __str__(self):
        return f"Image for {self.court.name}"


class DynamicPricing(models.Model):
    """Model for dynamic pricing rules (User Story 14)"""
    court = models.ForeignKey(
        Court, on_delete=models.CASCADE, related_name='pricing_rules')

    # Time range
    start_time = models.TimeField()
    end_time = models.TimeField()

    # Days of week (comma-separated: 0=Monday, 6=Sunday)
    days_of_week = models.CharField(
        max_length=20, help_text="e.g., '0,1,2,3,4' for weekdays")

    # Pricing
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)

    # Description
    # e.g., "Peak Hours", "Weekend Rate"
    description = models.CharField(max_length=100, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dynamic_pricing'
        ordering = ['start_time']

    def __str__(self):
        return f"{self.court.name} - {self.description} ({self.start_time}-{self.end_time})"


class CourtBlockedSlot(models.Model):
    """Model for blocked time slots (User Story 18)"""
    court = models.ForeignKey(
        Court, on_delete=models.CASCADE, related_name='blocked_slots')

    blocked_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    reason = models.CharField(max_length=255)
    notes = models.TextField(blank=True)

    blocked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'court_blocked_slots'
        ordering = ['blocked_date', 'start_time']
        indexes = [
            models.Index(fields=['court', 'blocked_date']),
        ]

    def __str__(self):
        return f"{self.court.name} blocked on {self.blocked_date}"


class CourtReview(models.Model):
    """Model for court reviews and ratings (User Story 19, 39)"""
    court = models.ForeignKey(
        Court, on_delete=models.CASCADE, related_name='reviews')
    player = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='court_reviews',
        limit_choices_to={'role': UserRole.PLAYER}
    )

    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    review_text = models.TextField(blank=True)

    # Owner response (User Story 19)
    owner_response = models.TextField(blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    # Moderation
    is_flagged = models.BooleanField(default=False)
    flag_reason = models.TextField(blank=True)
    is_visible = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'court_reviews'
        # One review per player per court
        unique_together = ['court', 'player']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['court', 'is_visible']),
        ]

    def __str__(self):
        return f"{self.player.full_name} - {self.court.name} ({self.rating}★)"


class EquipmentItem(models.Model):
    """Model for equipment rental tracking (User Story 29)"""
    court = models.ForeignKey(
        Court, on_delete=models.CASCADE, related_name='equipment')

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    quantity_total = models.IntegerField(default=1)
    quantity_available = models.IntegerField(default=1)

    rental_rate = models.DecimalField(max_digits=10, decimal_places=2)
    damage_penalty = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'equipment_items'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} at {self.court.name}"
