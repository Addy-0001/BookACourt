from rest_framework import serializers
from user_management.models import PlayerStats, UserPreference, Friendship
from .serializers import UserDetailsSerializer


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
