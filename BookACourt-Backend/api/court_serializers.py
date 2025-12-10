from rest_framework import serializers
from court_management.models import (
    CourtCategory, CourtRegistration, Court, CourtImage,
    DynamicPricing, CourtBlockedSlot, CourtReview, EquipmentItem
)
from user_management.models import User


class CourtCategorySerializer(serializers.ModelSerializer):
    """Serializer for court categories"""
    court_count = serializers.SerializerMethodField()

    class Meta:
        model = CourtCategory
        fields = ['id', 'name', 'description', 'icon', 'is_active',
                  'court_count', 'created_at']
        read_only_fields = ['created_at']

    def get_court_count(self, obj):
        return obj.courts.filter(is_active=True).count()


class CourtImageSerializer(serializers.ModelSerializer):
    """Serializer for court images"""

    class Meta:
        model = CourtImage
        fields = ['id', 'image', 'caption', 'is_primary', 'uploaded_at']
        read_only_fields = ['uploaded_at']


class DynamicPricingSerializer(serializers.ModelSerializer):
    """Serializer for dynamic pricing rules"""

    class Meta:
        model = DynamicPricing
        fields = ['id', 'start_time', 'end_time', 'days_of_week',
                  'hourly_rate', 'description', 'is_active']


class EquipmentItemSerializer(serializers.ModelSerializer):
    """Serializer for equipment items"""

    class Meta:
        model = EquipmentItem
        fields = ['id', 'name', 'description', 'quantity_total',
                  'quantity_available', 'rental_rate', 'damage_penalty', 'is_active']


class CourtListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for court listings"""
    owner_name = serializers.CharField(
        source='owner.full_name', read_only=True)
    category_name = serializers.CharField(
        source='category.name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    amenities_list = serializers.SerializerMethodField()

    class Meta:
        model = Court
        fields = [
            'id', 'name', 'owner_name', 'category_name', 'court_type',
            'city', 'is_indoor', 'base_hourly_rate', 'average_rating',
            'total_reviews', 'primary_image', 'amenities_list', 'is_active',
            'is_verified'
        ]

    def get_primary_image(self, obj):
        primary = obj.images.filter(is_primary=True).first()
        if primary:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(primary.image.url)
        return None

    def get_amenities_list(self, obj):
        if obj.amenities:
            return [a.strip() for a in obj.amenities.split(',')]
        return []


class CourtDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for court details"""
    owner = serializers.StringRelatedField()
    managers = serializers.StringRelatedField(many=True)
    category = CourtCategorySerializer(read_only=True)
    images = CourtImageSerializer(many=True, read_only=True)
    pricing_rules = DynamicPricingSerializer(many=True, read_only=True)
    equipment = EquipmentItemSerializer(many=True, read_only=True)
    amenities_list = serializers.SerializerMethodField()

    class Meta:
        model = Court
        fields = [
            'id', 'name', 'owner', 'managers', 'category', 'address', 'city',
            'latitude', 'longitude', 'description', 'court_type', 'is_indoor',
            'capacity', 'amenities', 'amenities_list', 'base_hourly_rate',
            'opening_time', 'closing_time', 'is_active', 'is_verified',
            'average_rating', 'total_reviews', 'phone_number', 'email',
            'images', 'pricing_rules', 'equipment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['average_rating',
                            'total_reviews', 'created_at', 'updated_at']

    def get_amenities_list(self, obj):
        if obj.amenities:
            return [a.strip() for a in obj.amenities.split(',')]
        return []


class CourtCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating courts"""

    class Meta:
        model = Court
        fields = [
            'name', 'category', 'address', 'city', 'latitude', 'longitude',
            'description', 'court_type', 'is_indoor', 'capacity', 'amenities',
            'base_hourly_rate', 'opening_time', 'closing_time', 'phone_number',
            'email', 'is_active'
        ]

    def validate_amenities(self, value):
        """Validate amenities format"""
        if value:
            # Ensure it's comma-separated
            amenities = [a.strip() for a in value.split(',')]
            if not amenities:
                raise serializers.ValidationError("Invalid amenities format")
        return value

    def validate(self, data):
        """Validate opening and closing times"""
        if 'opening_time' in data and 'closing_time' in data:
            if data['opening_time'] >= data['closing_time']:
                raise serializers.ValidationError(
                    "Closing time must be after opening time"
                )
        return data


class CourtRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for court registration requests"""
    owner_name = serializers.CharField(
        source='owner.full_name', read_only=True)
    reviewed_by_name = serializers.CharField(
        source='reviewed_by.full_name', read_only=True)

    class Meta:
        model = CourtRegistration
        fields = [
            'id', 'owner', 'owner_name', 'court_name', 'description',
            'address', 'city', 'phone_number', 'registration_documents',
            'court_images', 'status', 'rejection_reason', 'reviewed_by',
            'reviewed_by_name', 'reviewed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'status', 'rejection_reason', 'reviewed_by', 'reviewed_at',
            'created_at', 'updated_at'
        ]

    def validate(self, data):
        """Ensure owner is a court owner"""
        if 'owner' in data:
            if data['owner'].role != 'COURT_OWNER':
                raise serializers.ValidationError(
                    "Only users with Court Owner role can register courts"
                )
        return data


class CourtRegistrationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating court registration (without owner field)"""

    class Meta:
        model = CourtRegistration
        fields = [
            'court_name', 'description', 'address', 'city', 'phone_number',
            'registration_documents', 'court_images'
        ]

    def create(self, validated_data):
        """Auto-set owner to current user"""
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class CourtReviewSerializer(serializers.ModelSerializer):
    """Serializer for court reviews"""
    player_name = serializers.CharField(
        source='player.full_name', read_only=True)
    player_avatar = serializers.ImageField(
        source='player.profile_picture', read_only=True)

    class Meta:
        model = CourtReview
        fields = [
            'id', 'court', 'player', 'player_name', 'player_avatar',
            'rating', 'review_text', 'owner_response', 'responded_at',
            'is_visible', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'player', 'owner_response', 'responded_at', 'is_visible',
            'created_at', 'updated_at'
        ]

    def validate_rating(self, value):
        """Ensure rating is between 1 and 5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

    def create(self, validated_data):
        """Auto-set player to current user"""
        validated_data['player'] = self.context['request'].user
        return super().create(validated_data)


class CourtReviewResponseSerializer(serializers.Serializer):
    """Serializer for owner responding to reviews"""
    owner_response = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        """Update review with owner response"""
        from django.utils import timezone
        instance.owner_response = validated_data['owner_response']
        instance.responded_at = timezone.now()
        instance.save()
        return instance


class CourtBlockedSlotSerializer(serializers.ModelSerializer):
    """Serializer for blocked time slots"""
    blocked_by_name = serializers.CharField(
        source='blocked_by.full_name', read_only=True)

    class Meta:
        model = CourtBlockedSlot
        fields = [
            'id', 'court', 'blocked_date', 'start_time', 'end_time',
            'reason', 'notes', 'blocked_by', 'blocked_by_name', 'created_at'
        ]
        read_only_fields = ['blocked_by', 'created_at']

    def validate(self, data):
        """Validate time slot"""
        if 'start_time' in data and 'end_time' in data:
            if data['start_time'] >= data['end_time']:
                raise serializers.ValidationError(
                    "End time must be after start time"
                )
        return data

    def create(self, validated_data):
        """Auto-set blocked_by to current user"""
        validated_data['blocked_by'] = self.context['request'].user
        return super().create(validated_data)


class CourtSearchSerializer(serializers.Serializer):
    """Serializer for court search filters"""
    city = serializers.CharField(required=False)
    category = serializers.IntegerField(required=False)
    court_type = serializers.CharField(required=False)
    is_indoor = serializers.BooleanField(required=False)
    min_rating = serializers.DecimalField(
        max_digits=3, decimal_places=2, required=False)
    max_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False)
    available_date = serializers.DateField(required=False)
    available_time = serializers.TimeField(required=False)


class CourtAvailabilitySerializer(serializers.Serializer):
    """Serializer for checking court availability"""
    date = serializers.DateField(required=True)
    start_time = serializers.TimeField(required=False)
    end_time = serializers.TimeField(required=False)

    def validate(self, data):
        """Validate date and times"""
        from django.utils import timezone
        from datetime import datetime

        # Check if date is in the past
        if data['date'] < timezone.now().date():
            raise serializers.ValidationError(
                "Cannot check availability for past dates")

        # If both times provided, validate range
        if 'start_time' in data and 'end_time' in data:
            if data['start_time'] >= data['end_time']:
                raise serializers.ValidationError(
                    "End time must be after start time"
                )

        return data
