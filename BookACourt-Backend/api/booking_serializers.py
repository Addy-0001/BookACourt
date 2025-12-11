from rest_framework import serializers
from booking_management.models import (
    Booking, CancellationPolicy, BookingNotification,
    EquipmentRental, MatchEvent, MatchParticipant,
    PlayerRating, BookingShare
)
from court_management.models import Court
from django.utils import timezone
from datetime import timedelta


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for bookings"""
    court_name = serializers.CharField(source='court.name', read_only=True)
    player_name = serializers.CharField(
        source='player.full_name', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'booking_reference', 'court', 'court_name',
            'player', 'player_name', 'booking_date', 'start_time',
            'end_time', 'status', 'payment_method', 'payment_status',
            'base_amount', 'discount_amount', 'loyalty_points_used',
            'total_amount', 'notes', 'special_requests',
            'is_walk_in', 'walk_in_guest_name', 'cancelled_at',
            'cancellation_reason', 'refund_amount',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'booking_reference', 'player', 'cancelled_at',
            'cancellation_reason', 'refund_amount',
            'created_at', 'updated_at'
        ]


class BookingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating bookings"""

    class Meta:
        model = Booking
        fields = [
            'court', 'booking_date', 'start_time', 'end_time',
            'payment_method', 'notes', 'special_requests',
            'loyalty_points_used'
        ]

    def validate(self, data):
        """Validate booking"""
        court = data.get('court')
        booking_date = data.get('booking_date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        # Check if court is active
        if not court.is_active:
            raise serializers.ValidationError(
                "This court is not available for booking")

        # Check date is not in past
        if booking_date < timezone.now().date():
            raise serializers.ValidationError("Cannot book for past dates")

        # Check time validity
        if start_time >= end_time:
            raise serializers.ValidationError(
                "End time must be after start time")

        # Check operating hours
        if start_time < court.opening_time or end_time > court.closing_time:
            raise serializers.ValidationError(
                f"Court operates from {court.opening_time} to {court.closing_time}"
            )

        # Check for conflicts
        conflicts = Booking.objects.filter(
            court=court,
            booking_date=booking_date,
            status__in=['PENDING', 'CONFIRMED']
        ).filter(
            start_time__lt=end_time,
            end_time__gt=start_time
        )

        if conflicts.exists():
            raise serializers.ValidationError(
                "This time slot is already booked")

        return data

    def create(self, validated_data):
        """Create booking with calculated amounts"""
        request = self.context.get('request')
        court = validated_data['court']
        start_time = validated_data['start_time']
        end_time = validated_data['end_time']

        # Calculate hours
        duration = (
            timezone.datetime.combine(timezone.datetime.today(), end_time) -
            timezone.datetime.combine(timezone.datetime.today(), start_time)
        )
        hours = duration.total_seconds() / 3600

        # Calculate base amount
        base_amount = court.base_hourly_rate * hours

        # Apply loyalty points
        loyalty_points_used = validated_data.get('loyalty_points_used', 0)
        discount_amount = loyalty_points_used * 0.1  # 10 points = 1 unit discount

        total_amount = base_amount - discount_amount

        # Create booking
        booking = Booking.objects.create(
            player=request.user,
            base_amount=base_amount,
            discount_amount=discount_amount,
            total_amount=total_amount,
            payment_status='PENDING',
            created_by=request.user,
            **validated_data
        )

        return booking


class CancellationPolicySerializer(serializers.ModelSerializer):
    """Serializer for cancellation policies"""
    court_name = serializers.CharField(source='court.name', read_only=True)

    class Meta:
        model = CancellationPolicy
        fields = [
            'id', 'court', 'court_name', 'cancellation_deadline_hours',
            'full_refund_hours', 'partial_refund_hours',
            'partial_refund_percentage', 'no_show_penalty_percentage',
            'policy_text', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class BookingNotificationSerializer(serializers.ModelSerializer):
    """Serializer for booking notifications"""

    class Meta:
        model = BookingNotification
        fields = [
            'id', 'booking', 'user', 'notification_type',
            'message', 'is_read', 'sent_at', 'sent_via_email',
            'sent_via_sms', 'sent_via_push'
        ]
        read_only_fields = ['sent_at']


class EquipmentRentalSerializer(serializers.ModelSerializer):
    """Serializer for equipment rentals"""
    equipment_name = serializers.CharField(
        source='equipment.name', read_only=True)
    booking_reference = serializers.CharField(
        source='booking.booking_reference', read_only=True
    )

    class Meta:
        model = EquipmentRental
        fields = [
            'id', 'booking', 'booking_reference', 'equipment',
            'equipment_name', 'quantity', 'rental_cost', 'status',
            'returned_at', 'damage_notes', 'damage_charge',
            'returned_by', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'rental_cost', 'returned_at', 'returned_by',
            'created_at', 'updated_at'
        ]


class MatchParticipantSerializer(serializers.ModelSerializer):
    """Serializer for match participants"""
    player_name = serializers.CharField(
        source='player.full_name', read_only=True)

    class Meta:
        model = MatchParticipant
        fields = [
            'id', 'match_event', 'player', 'player_name',
            'joined_at', 'is_confirmed', 'attended'
        ]
        read_only_fields = ['joined_at']


class MatchEventSerializer(serializers.ModelSerializer):
    """Serializer for match events"""
    court_name = serializers.CharField(source='court.name', read_only=True)
    creator_name = serializers.CharField(
        source='created_by.full_name', read_only=True)
    participants = MatchParticipantSerializer(many=True, read_only=True)
    is_full = serializers.SerializerMethodField()

    class Meta:
        model = MatchEvent
        fields = [
            'id', 'court', 'court_name', 'booking', 'title',
            'description', 'sport_type', 'created_by', 'creator_name',
            'max_players', 'current_players', 'match_date',
            'match_time', 'duration_hours', 'status', 'skill_level',
            'participants', 'is_full', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'created_by', 'current_players', 'status',
            'created_at', 'updated_at'
        ]

    def get_is_full(self, obj):
        return obj.is_full()


class MatchEventCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating match events"""

    class Meta:
        model = MatchEvent
        fields = [
            'court', 'booking', 'title', 'description',
            'sport_type', 'max_players', 'match_date',
            'match_time', 'duration_hours', 'skill_level'
        ]

    def validate(self, data):
        """Validate match event"""
        match_date = data.get('match_date')

        # Check date is not in past
        if match_date < timezone.now().date():
            raise serializers.ValidationError(
                "Cannot create match for past dates")

        # Check max players
        if data.get('max_players', 0) < 2:
            raise serializers.ValidationError(
                "Match must allow at least 2 players")

        return data

    def create(self, validated_data):
        """Create match with current user as creator"""
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        validated_data['current_players'] = 1

        match_event = super().create(validated_data)

        # Add creator as first participant
        MatchParticipant.objects.create(
            match_event=match_event,
            player=request.user,
            is_confirmed=True
        )

        return match_event


class PlayerRatingSerializer(serializers.ModelSerializer):
    """Serializer for player ratings"""
    rated_player_name = serializers.CharField(
        source='rated_player.full_name', read_only=True
    )
    rated_by_name = serializers.CharField(
        source='rated_by.full_name', read_only=True
    )

    class Meta:
        model = PlayerRating
        fields = [
            'id', 'match_event', 'rated_by', 'rated_by_name',
            'rated_player', 'rated_player_name', 'rating',
            'feedback', 'misconduct_reported', 'misconduct_details',
            'created_at'
        ]
        read_only_fields = ['rated_by', 'created_at']


class PlayerRatingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating player ratings"""

    class Meta:
        model = PlayerRating
        fields = [
            'match_event', 'rated_player', 'rating',
            'feedback', 'misconduct_reported', 'misconduct_details'
        ]

    def validate(self, data):
        """Validate rating"""
        request = self.context.get('request')
        match_event = data.get('match_event')
        rated_player = data.get('rated_player')

        # Cannot rate yourself
        if rated_player == request.user:
            raise serializers.ValidationError("Cannot rate yourself")

        # Check if both users participated
        if not MatchParticipant.objects.filter(
            match_event=match_event,
            player=request.user
        ).exists():
            raise serializers.ValidationError(
                "You must have participated in this match to rate players"
            )

        if not MatchParticipant.objects.filter(
            match_event=match_event,
            player=rated_player
        ).exists():
            raise serializers.ValidationError(
                "This player did not participate in this match"
            )

        # Check if already rated
        if PlayerRating.objects.filter(
            match_event=match_event,
            rated_by=request.user,
            rated_player=rated_player
        ).exists():
            raise serializers.ValidationError(
                "You have already rated this player for this match"
            )

        return data

    def create(self, validated_data):
        """Create rating with current user as rater"""
        request = self.context.get('request')
        validated_data['rated_by'] = request.user

        rating = super().create(validated_data)

        # Update player stats
        rated_player = validated_data['rated_player']
        if hasattr(rated_player, 'stats'):
            stats = rated_player.stats
            total = stats.total_ratings_received
            current_rating = float(stats.sportsmanship_rating)

            # Calculate new average
            new_rating = (
                (current_rating * total +
                 validated_data['rating']) / (total + 1)
            )

            stats.sportsmanship_rating = round(new_rating, 2)
            stats.total_ratings_received += 1
            stats.save()

        return rating


class BookingShareSerializer(serializers.ModelSerializer):
    """Serializer for booking shares"""
    booking_reference = serializers.CharField(
        source='booking.booking_reference', read_only=True
    )
    shared_by_name = serializers.CharField(
        source='shared_by.full_name', read_only=True
    )
    is_valid = serializers.SerializerMethodField()
    joined_count = serializers.SerializerMethodField()

    class Meta:
        model = BookingShare
        fields = [
            'id', 'booking', 'booking_reference', 'share_token',
            'shared_by', 'shared_by_name', 'joined_users',
            'max_joins', 'expires_at', 'is_valid', 'joined_count',
            'created_at'
        ]
        read_only_fields = [
            'share_token', 'shared_by', 'joined_users',
            'created_at'
        ]

    def get_is_valid(self, obj):
        return obj.is_valid()

    def get_joined_count(self, obj):
        return obj.joined_users.count()


class BookingShareCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating booking shares"""

    class Meta:
        model = BookingShare
        fields = ['booking', 'max_joins', 'expires_at']

    def validate_booking(self, value):
        """Validate that user owns the booking"""
        request = self.context.get('request')
        if value.player != request.user:
            raise serializers.ValidationError(
                "You can only share your own bookings"
            )
        return value

    def create(self, validated_data):
        """Create share with generated token"""
        import uuid
        request = self.context.get('request')

        validated_data['shared_by'] = request.user
        validated_data['share_token'] = uuid.uuid4().hex

        # Default expiry if not provided
        if 'expires_at' not in validated_data:
            validated_data['expires_at'] = timezone.now() + timedelta(days=7)

        return super().create(validated_data)
