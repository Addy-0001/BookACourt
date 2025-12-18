from rest_framework import serializers
from user_management.models import PlayerStats, UserPreference, Friendship
from .serializers import UserDetailsSerializer
# import user
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, AllowAny


User = get_user_model()


class PlayerStatsSerializer(serializers.ModelSerializer):
    """Serializer for player statistics"""
    player_name = serializers.CharField(
        source='player.full_name', read_only=True)
    win_loss_ratio = serializers.ReadOnlyField()

    class Meta:
        model = PlayerStats
        fields = [
            'id', 'player', 'player_name', 'total_bookings',
            'total_matches_played', 'matches_won', 'matches_lost',
            'win_loss_ratio', 'sportsmanship_rating',
            'total_ratings_received', 'no_show_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'total_bookings', 'total_matches_played', 'matches_won',
            'matches_lost', 'sportsmanship_rating',
            'total_ratings_received', 'no_show_count',
            'created_at', 'updated_at'
        ]


class UserPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for user preferences"""

    class Meta:
        model = UserPreference
        fields = [
            'id', 'user', 'email_notifications', 'sms_notifications',
            'push_notifications', 'preferred_sports',
            'preferred_time_slots', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']


class FriendshipSerializer(serializers.ModelSerializer):
    """Serializer for friendships"""
    from_user_details = UserDetailsSerializer(
        source='from_user', read_only=True)
    to_user_details = UserDetailsSerializer(source='to_user', read_only=True)

    class Meta:
        model = Friendship
        fields = [
            'id', 'from_user', 'from_user_details', 'to_user',
            'to_user_details', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['from_user', 'status', 'created_at', 'updated_at']


class FriendshipCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating friend requests"""

    class Meta:
        model = Friendship
        fields = ['to_user']

    def validate_to_user(self, value):
        """Validate friend request"""
        request = self.context.get('request')

        # Cannot send request to self
        if value == request.user:
            raise serializers.ValidationError(
                "Cannot send friend request to yourself")

        # Check if friendship already exists
        if Friendship.objects.filter(
            from_user=request.user,
            to_user=value
        ).exists():
            raise serializers.ValidationError("Friend request already sent")

        # Check reverse friendship
        if Friendship.objects.filter(
            from_user=value,
            to_user=request.user
        ).exists():
            raise serializers.ValidationError(
                "This user has already sent you a friend request")

        return value

    def create(self, validated_data):
        """Create friendship with current user as from_user"""
        validated_data['from_user'] = self.context['request'].user
        return super().create(validated_data)


class PlayerSearchSerializer(serializers.ModelSerializer):
    """Enhanced serializer for player search results"""
    player_stats = PlayerStatsSerializer(source='stats', read_only=True)
    preferences = serializers.SerializerMethodField()
    friendship_status = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'phone_number', 'full_name', 'city',
            'profile_picture', 'loyalty_points',
            'player_stats', 'preferences', 'friendship_status'
        ]

    def get_preferences(self, obj):
        """Get user preferences if they exist"""
        try:
            return {
                'preferred_sports': obj.preferences.preferred_sports,
                'preferred_time_slots': obj.preferences.preferred_time_slots
            }
        except:
            return None

    def get_friendship_status(self, obj):
        """Check friendship status with current user"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return None

        from user_management.models import Friendship

        # Check if already friends
        friendship = Friendship.objects.filter(
            Q(from_user=request.user, to_user=obj) |
            Q(from_user=obj, to_user=request.user)
        ).first()

        if friendship:
            if friendship.status == 'ACCEPTED':
                return 'friends'
            elif friendship.from_user == request.user:
                return 'request_sent'
            else:
                return 'request_received'

        return 'none'
