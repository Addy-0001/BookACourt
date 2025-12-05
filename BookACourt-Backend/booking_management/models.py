from django.db import models
from django.utils import timezone
from user_management.models import User, UserRole
from court_management.models import Court, EquipmentItem


class Booking(models.Model):
    """Model for court bookings (User Story 34, 35, 38)"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
        ('NO_SHOW', 'No Show'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('ONLINE', 'Online Payment'),
        ('CASH', 'Cash Payment'),
        ('OFFLINE', 'Offline Payment'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('REFUNDED', 'Refunded'),
        ('FAILED', 'Failed'),
    ]

    court = models.ForeignKey(
        Court, on_delete=models.CASCADE, related_name='bookings')
    player = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings',
        limit_choices_to={'role': UserRole.PLAYER}
    )

    # Booking details
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    # Status
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='PENDING')

    # Payment
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, default='ONLINE')
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')

    # Pricing
    base_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    loyalty_points_used = models.IntegerField(default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Additional info
    notes = models.TextField(blank=True)
    special_requests = models.TextField(blank=True)

    # Booking reference
    booking_reference = models.CharField(
        max_length=20, unique=True, editable=False)

    # Walk-in booking (User Story 22)
    is_walk_in = models.BooleanField(default=False)
    walk_in_guest_name = models.CharField(max_length=255, blank=True)

    # Cancellation (User Story 35)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    refund_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Tracking
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_bookings'
    )

    class Meta:
        db_table = 'bookings'
        ordering = ['-booking_date', '-start_time']
        unique_together = ['court', 'booking_date', 'start_time']
        indexes = [
            models.Index(fields=['court', 'booking_date', 'status']),
            models.Index(fields=['player', 'status']),
            models.Index(fields=['booking_reference']),
        ]

    def __str__(self):
        return f"{self.court.name} - {self.booking_date} {self.start_time}"

    def save(self, *args, **kwargs):
        # Generate booking reference if not exists
        if not self.booking_reference:
            import uuid
            self.booking_reference = f"BK{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def can_cancel(self):
        """Check if booking can be cancelled based on cancellation policy"""
        # This will reference the court's cancellation policy
        # For now, basic implementation
        from datetime import datetime, timedelta
        booking_datetime = timezone.make_aware(
            datetime.combine(self.booking_date, self.start_time)
        )
        time_until_booking = booking_datetime - timezone.now()

        # Can cancel if booking is at least 24 hours away
        return time_until_booking > timedelta(hours=24)


class CancellationPolicy(models.Model):
    """Model for court cancellation policies (User Story 15)"""
    court = models.OneToOneField(
        Court, on_delete=models.CASCADE, related_name='cancellation_policy')

    # Cancellation deadline (hours before booking)
    cancellation_deadline_hours = models.IntegerField(default=24)

    # Refund percentages based on time before booking
    full_refund_hours = models.IntegerField(
        default=48, help_text="Full refund if cancelled this many hours before")
    partial_refund_hours = models.IntegerField(
        default=24, help_text="Partial refund if cancelled this many hours before")
    partial_refund_percentage = models.IntegerField(
        default=50, help_text="Percentage of refund for partial refund")

    # No-show penalty
    no_show_penalty_percentage = models.IntegerField(
        default=100, help_text="Percentage charged for no-show")

    policy_text = models.TextField(
        help_text="Full policy description for players")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cancellation_policies'
        verbose_name = 'Cancellation Policy'
        verbose_name_plural = 'Cancellation Policies'

    def __str__(self):
        return f"Cancellation Policy for {self.court.name}"


class BookingNotification(models.Model):
    """Model for booking notifications (User Story 41)"""
    NOTIFICATION_TYPES = [
        ('CONFIRMATION', 'Booking Confirmation'),
        ('REMINDER', 'Booking Reminder'),
        ('CANCELLATION', 'Booking Cancellation'),
        ('MODIFICATION', 'Booking Modification'),
    ]

    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name='notifications')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='booking_notifications')

    notification_type = models.CharField(
        max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()

    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    # Delivery channels
    sent_via_email = models.BooleanField(default=False)
    sent_via_sms = models.BooleanField(default=False)
    sent_via_push = models.BooleanField(default=False)

    class Meta:
        db_table = 'booking_notifications'
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.notification_type} for {self.booking.booking_reference}"


class EquipmentRental(models.Model):
    """Model for equipment rentals (User Story 29)"""
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('RETURNED', 'Returned'),
        ('DAMAGED', 'Damaged'),
    ]

    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name='equipment_rentals')
    equipment = models.ForeignKey(
        EquipmentItem, on_delete=models.CASCADE, related_name='rentals')

    quantity = models.IntegerField(default=1)
    rental_cost = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='ACTIVE')

    # Return information
    returned_at = models.DateTimeField(null=True, blank=True)
    damage_notes = models.TextField(blank=True)
    damage_charge = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    # Manager who handled return
    returned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='equipment_returns'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'equipment_rentals'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.equipment.name} - {self.booking.booking_reference}"


class MatchEvent(models.Model):
    """Model for matchmaking events (User Story 36, 37, 27)"""
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('FULL', 'Full'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    court = models.ForeignKey(
        Court, on_delete=models.CASCADE, related_name='match_events')
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='match_event',
        null=True,
        blank=True
    )

    # Event details
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    sport_type = models.CharField(max_length=50)

    # Creator
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_matches',
        limit_choices_to={'role': UserRole.PLAYER}
    )

    # Capacity
    max_players = models.IntegerField()
    current_players = models.IntegerField(default=1)  # Creator is first player

    # Date and time
    match_date = models.DateField()
    match_time = models.TimeField()
    duration_hours = models.IntegerField(default=1)

    # Status
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='OPEN')

    # Skill level requirement
    skill_level = models.CharField(
        max_length=20,
        choices=[
            ('BEGINNER', 'Beginner'),
            ('INTERMEDIATE', 'Intermediate'),
            ('ADVANCED', 'Advanced'),
            ('ANY', 'Any Level'),
        ],
        default='ANY'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'match_events'
        ordering = ['-match_date', '-match_time']
        indexes = [
            models.Index(fields=['court', 'match_date', 'status']),
            models.Index(fields=['status', 'match_date']),
        ]

    def __str__(self):
        return f"{self.title} - {self.match_date}"

    def is_full(self):
        return self.current_players >= self.max_players


class MatchParticipant(models.Model):
    """Model for match event participants (User Story 37)"""
    match_event = models.ForeignKey(
        MatchEvent, on_delete=models.CASCADE, related_name='participants')
    player = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='match_participations',
        limit_choices_to={'role': UserRole.PLAYER}
    )

    joined_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=True)

    # Result tracking
    attended = models.BooleanField(default=False)

    class Meta:
        db_table = 'match_participants'
        unique_together = ['match_event', 'player']
        ordering = ['joined_at']

    def __str__(self):
        return f"{self.player.full_name} in {self.match_event.title}"


class PlayerRating(models.Model):
    """Model for player-to-player ratings (User Story 40)"""
    match_event = models.ForeignKey(
        MatchEvent, on_delete=models.CASCADE, related_name='player_ratings')
    rated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ratings_given')
    rated_player = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ratings_received')

    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    feedback = models.TextField(blank=True)

    # Misconduct reporting
    misconduct_reported = models.BooleanField(default=False)
    misconduct_details = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'player_ratings'
        unique_together = ['match_event', 'rated_by', 'rated_player']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.rated_by.full_name} rated {self.rated_player.full_name} ({self.rating}★)"


class BookingShare(models.Model):
    """Model for shared bookings (User Story 46)"""
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name='shares')

    share_token = models.CharField(max_length=100, unique=True)
    shared_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shared_bookings')

    # Who joined via this share
    joined_users = models.ManyToManyField(
        User, related_name='joined_bookings', blank=True)

    max_joins = models.IntegerField(default=5)
    expires_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'booking_shares'
        ordering = ['-created_at']

    def __str__(self):
        return f"Share for {self.booking.booking_reference}"

    def is_valid(self):
        """Check if share link is still valid"""
        return timezone.now() < self.expires_at and self.joined_users.count() < self.max_joins
