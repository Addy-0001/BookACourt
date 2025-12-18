from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from user_management.models import PlayerStats, UserPreference, Friendship
from .user_serializers import (
    PlayerStatsSerializer, UserPreferenceSerializer,
    FriendshipSerializer, FriendshipCreateSerializer, UserDetailsSerializer
)
from .user_serializers import PlayerSearchSerializer

# Add this import at the top
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, AllowAny

# Add this new ViewSet at the end of the file


class PlayerSearchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for searching and listing players
    Allows players to find others to play with
    """
    serializer_class = PlayerSearchSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'full_name',
        'phone_number',
        'city',
        'preferences__preferred_sports'
    ]
    ordering_fields = [
        'full_name', 'created_at', 'loyalty_points',
        'stats__total_matches_played', 'stats__sportsmanship_rating'
    ]
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Return all active players except the current user
        """
        from user_management.models import User, UserRole

        queryset = User.objects.filter(
            role=UserRole.PLAYER,
            is_active=True
        ).exclude(
            id=self.request.user.id
        ).select_related('stats').prefetch_related('preferences')

        # Filter by city if provided
        city = self.request.query_params.get('city')
        if city:
            queryset = queryset.filter(city__icontains=city)

        # Filter by sport preference
        sport = self.request.query_params.get('sport')
        if sport:
            queryset = queryset.filter(
                preferences__preferred_sports__icontains=sport
            )

        # Filter by minimum rating
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            queryset = queryset.filter(
                stats__sportsmanship_rating__gte=min_rating
            )

        # Filter by skill level (based on matches played)
        skill_level = self.request.query_params.get('skill_level')
        if skill_level == 'beginner':
            queryset = queryset.filter(stats__total_matches_played__lt=10)
        elif skill_level == 'intermediate':
            queryset = queryset.filter(
                stats__total_matches_played__gte=10,
                stats__total_matches_played__lt=50
            )
        elif skill_level == 'advanced':
            queryset = queryset.filter(stats__total_matches_played__gte=50)

        return queryset.distinct()

    @extend_schema(
        summary="Search players",
        description="Search for players to play with. Supports filtering by city, sport, rating, and skill level.",
        parameters=[
            OpenApiParameter('city', str, description='Filter by city'),
            OpenApiParameter(
                'sport', str, description='Filter by preferred sport'),
            OpenApiParameter('min_rating', float,
                             description='Minimum sportsmanship rating'),
            OpenApiParameter(
                'skill_level', str, description='Skill level: beginner, intermediate, or advanced'),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Get player details",
        description="Get detailed information about a specific player"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class PlayerStatsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Player Statistics
    Addresses User Story: 44 - View player statistics
    """
    queryset = PlayerStats.objects.all()
    serializer_class = PlayerStatsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = [
        'total_bookings', 'total_matches_played',
        'matches_won', 'sportsmanship_rating'
    ]
    ordering = ['-total_bookings']

    def get_queryset(self):
        """Filter to show only relevant stats"""
        user = self.request.user

        if user.is_super_user:
            return PlayerStats.objects.all()

        # Players can see their own and their friends' stats
        if user.is_player:
            friend_ids = Friendship.objects.filter(
                from_user=user,
                status='ACCEPTED'
            ).values_list('to_user_id', flat=True)

            return PlayerStats.objects.filter(
                player__in=[user.id] + list(friend_ids)
            )

        return PlayerStats.objects.none()

    @extend_schema(
        summary="Get my stats",
        description="Get statistics for the current user"
    )
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's stats"""
        if not request.user.is_player:
            return Response(
                {'error': 'Only players have statistics'},
                status=status.HTTP_400_BAD_REQUEST
            )

        stats, created = PlayerStats.objects.get_or_create(player=request.user)
        serializer = self.get_serializer(stats)
        return Response(serializer.data)

    @extend_schema(
        summary="Get leaderboard",
        description="Get top players by various metrics"
    )
    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        """Get leaderboard of top players"""
        metric = request.query_params.get('metric', 'matches_won')
        limit = int(request.query_params.get('limit', 10))

        valid_metrics = [
            'total_bookings', 'total_matches_played',
            'matches_won', 'sportsmanship_rating'
        ]

        if metric not in valid_metrics:
            return Response(
                {'error': f'Invalid metric. Choose from: {", ".join(valid_metrics)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        stats = PlayerStats.objects.order_by(f'-{metric}')[:limit]
        serializer = self.get_serializer(stats, many=True)
        return Response(serializer.data)


class UserPreferenceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User Preferences
    Addresses User Story: 31 - Manage notification preferences
    """
    queryset = UserPreference.objects.all()
    serializer_class = UserPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Users can only access their own preferences"""
        return UserPreference.objects.filter(user=self.request.user)

    @extend_schema(
        summary="Get my preferences",
        description="Get preferences for the current user"
    )
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get or create current user's preferences"""
        preferences, created = UserPreference.objects.get_or_create(
            user=request.user
        )
        serializer = self.get_serializer(preferences)
        return Response(serializer.data)

    @extend_schema(
        summary="Update my preferences",
        description="Update preferences for the current user"
    )
    @action(detail=False, methods=['patch'])
    def update_me(self, request):
        """Update current user's preferences"""
        preferences, created = UserPreference.objects.get_or_create(
            user=request.user
        )
        serializer = self.get_serializer(
            preferences,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class FriendshipViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Friendships
    Addresses User Story: 42 - Add friends and view friend lists
    """
    queryset = Friendship.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'from_user__full_name', 'to_user__full_name',
        'from_user__phone_number', 'to_user__phone_number'
    ]
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return FriendshipCreateSerializer
        return FriendshipSerializer

    def get_queryset(self):
        """Filter friendships for current user"""
        user = self.request.user
        return Friendship.objects.filter(
            from_user=user
        ) | Friendship.objects.filter(
            to_user=user
        )

    @extend_schema(
        summary="Send friend request",
        description="Send a friend request to another user"
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Get my friends",
        description="Get list of accepted friends"
    )
    @action(detail=False, methods=['get'])
    def my_friends(self, request):
        """Get list of accepted friends"""
        user = request.user

        # Get friendships where user is either sender or receiver
        friendships = Friendship.objects.filter(
            status='ACCEPTED'
        ).filter(
            from_user=user
        ) | Friendship.objects.filter(
            status='ACCEPTED',
            to_user=user
        )

        serializer = self.get_serializer(friendships, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Get pending requests",
        description="Get friend requests pending your response"
    )
    @action(detail=False, methods=['get'])
    def pending_requests(self, request):
        """Get pending friend requests sent to user"""
        friendships = Friendship.objects.filter(
            to_user=request.user,
            status='PENDING'
        )
        serializer = self.get_serializer(friendships, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Get sent requests",
        description="Get friend requests you've sent"
    )
    @action(detail=False, methods=['get'])
    def sent_requests(self, request):
        """Get friend requests sent by user"""
        friendships = Friendship.objects.filter(
            from_user=request.user,
            status='PENDING'
        )
        serializer = self.get_serializer(friendships, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Accept friend request",
        description="Accept a pending friend request"
    )
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Accept a friend request"""
        friendship = self.get_object()

        # Only recipient can accept
        if friendship.to_user != request.user:
            return Response(
                {'error': 'You can only accept requests sent to you'},
                status=status.HTTP_403_FORBIDDEN
            )

        if friendship.status != 'PENDING':
            return Response(
                {'error': 'Only pending requests can be accepted'},
                status=status.HTTP_400_BAD_REQUEST
            )

        friendship.status = 'ACCEPTED'
        friendship.save()

        serializer = self.get_serializer(friendship)
        return Response(serializer.data)

    @extend_schema(
        summary="Reject friend request",
        description="Reject a pending friend request"
    )
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a friend request"""
        friendship = self.get_object()

        # Only recipient can reject
        if friendship.to_user != request.user:
            return Response(
                {'error': 'You can only reject requests sent to you'},
                status=status.HTTP_403_FORBIDDEN
            )

        if friendship.status != 'PENDING':
            return Response(
                {'error': 'Only pending requests can be rejected'},
                status=status.HTTP_400_BAD_REQUEST
            )

        friendship.status = 'REJECTED'
        friendship.save()

        serializer = self.get_serializer(friendship)
        return Response(serializer.data)

    @extend_schema(
        summary="Remove friend",
        description="Remove a friend or cancel a request"
    )
    def destroy(self, request, *args, **kwargs):
        """Delete friendship"""
        friendship = self.get_object()

        # Only parties involved can delete
        if request.user not in [friendship.from_user, friendship.to_user]:
            return Response(
                {'error': 'You can only remove your own friendships'},
                status=status.HTTP_403_FORBIDDEN
            )

        friendship.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
