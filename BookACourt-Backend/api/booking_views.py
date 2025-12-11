from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.utils import timezone
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from datetime import timedelta

from booking_management.models import (
    Booking, CancellationPolicy, BookingNotification,
    EquipmentRental, MatchEvent, MatchParticipant,
    PlayerRating, BookingShare
)
from .booking_serializers import (
    BookingSerializer, BookingCreateSerializer,
    CancellationPolicySerializer, BookingNotificationSerializer,
    EquipmentRentalSerializer, MatchEventSerializer,
    MatchEventCreateSerializer, MatchParticipantSerializer,
    PlayerRatingSerializer, PlayerRatingCreateSerializer,
    BookingShareSerializer, BookingShareCreateSerializer
)


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Bookings
    Addresses User Stories: 13, 20, 22, 34, 35, 38
    """
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['booking_reference', 'court__name']
    ordering_fields = ['booking_date', 'created_at', 'total_amount']
    ordering = ['-booking_date', '-start_time']

    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        return BookingSerializer

    def get_queryset(self):
        """Filter bookings based on user role"""
        user = self.request.user
        queryset = Booking.objects.all()

        if user.is_super_user:
            # Super users see all bookings
            pass
        elif user.is_court_owner or user.is_court_manager:
            # Court staff see bookings for their courts
            from court_management.models import Court
            managed_courts = Court.objects.filter(
                Q(owner=user) | Q(managers=user)
            )
            queryset = queryset.filter(court__in=managed_courts)
        else:
            # Players see only their bookings
            queryset = queryset.filter(player=user)

        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Filter by date range
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from:
            queryset = queryset.filter(booking_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(booking_date__lte=date_to)

        return queryset.select_related('court', 'player')

    @extend_schema(
        summary="Get my bookings",
        description="Get all bookings for the current user"
    )
    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        """Get current user's bookings"""
        bookings = Booking.objects.filter(player=request.user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Cancel booking",
        description="Cancel a booking and process refund"
    )
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking"""
        booking = self.get_object()

        # Check permissions
        if booking.player != request.user and not request.user.is_super_user:
            return Response(
                {'error': 'You can only cancel your own bookings'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if already cancelled
        if booking.status == 'CANCELLED':
            return Response(
                {'error': 'Booking is already cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if booking can be cancelled
        if not booking.can_cancel():
            return Response(
                {'error': 'Booking cannot be cancelled (less than 24 hours before start time)'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate refund
        booking.status = 'CANCELLED'
        booking.cancelled_at = timezone.now()
        booking.cancellation_reason = request.data.get(
            'reason', 'Cancelled by user'
        )

        # Simple refund calculation (should use cancellation policy)
        booking.refund_amount = booking.total_amount * 0.9  # 90% refund
        booking.save()

        serializer = self.get_serializer(booking)
        return Response(serializer.data)

    @extend_schema(
        summary="Confirm booking",
        description="Confirm a pending booking (court staff only)"
    )
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm a booking"""
        booking = self.get_object()

        # Check permissions
        if not request.user.can_manage_court(booking.court):
            return Response(
                {'error': 'You do not have permission to confirm this booking'},
                status=status.HTTP_403_FORBIDDEN
            )

        if booking.status != 'PENDING':
            return Response(
                {'error': 'Only pending bookings can be confirmed'},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = 'CONFIRMED'
        booking.save()

        serializer = self.get_serializer(booking)
        return Response(serializer.data)


class CancellationPolicyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Cancellation Policies
    Addresses User Story: 15 - View and set cancellation policies
    """
    queryset = CancellationPolicy.objects.all()
    serializer_class = CancellationPolicySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Filter by court if specified"""
        queryset = CancellationPolicy.objects.all()
        court_id = self.request.query_params.get('court')
        if court_id:
            queryset = queryset.filter(court_id=court_id)
        return queryset


class BookingNotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Booking Notifications
    Addresses User Story: 41 - View booking notifications
    """
    queryset = BookingNotification.objects.all()
    serializer_class = BookingNotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering = ['-sent_at']

    def get_queryset(self):
        """Users see only their notifications"""
        return BookingNotification.objects.filter(user=self.request.user)

    @extend_schema(
        summary="Get unread notifications",
        description="Get all unread notifications for the current user"
    )
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get unread notifications"""
        notifications = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Mark as read",
        description="Mark a notification as read"
    )
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        serializer = self.get_serializer(notification)
        return Response(serializer.data)

    @extend_schema(
        summary="Mark all as read",
        description="Mark all notifications as read"
    )
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        self.get_queryset().update(is_read=True)
        return Response({'message': 'All notifications marked as read'})


class EquipmentRentalViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Equipment Rentals
    Addresses User Story: 29 - Rent equipment
    """
    queryset = EquipmentRental.objects.all()
    serializer_class = EquipmentRentalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter equipment rentals"""
        user = self.request.user
        queryset = EquipmentRental.objects.all()

        if user.is_super_user:
            pass
        elif user.is_court_owner or user.is_court_manager:
            # Court staff see rentals for their courts
            queryset = queryset.filter(
                equipment__court__owner=user
            ) | queryset.filter(
                equipment__court__managers=user
            )
        else:
            # Players see their own rentals
            queryset = queryset.filter(booking__player=user)

        return queryset

    @extend_schema(
        summary="Return equipment",
        description="Mark equipment as returned (court staff only)"
    )
    @action(detail=True, methods=['post'])
    def return_equipment(self, request, pk=None):
        """Return equipment"""
        rental = self.get_object()

        # Check permissions
        if not request.user.can_manage_court(rental.equipment.court):
            return Response(
                {'error': 'You do not have permission to process returns'},
                status=status.HTTP_403_FORBIDDEN
            )

        rental.status = 'RETURNED'
        rental.returned_at = timezone.now()
        rental.returned_by = request.user
        rental.damage_notes = request.data.get('damage_notes', '')
        rental.damage_charge = float(request.data.get('damage_charge', 0))

        if rental.damage_charge > 0:
            rental.status = 'DAMAGED'

        rental.save()

        # Update equipment availability
        rental.equipment.quantity_available += rental.quantity
        rental.equipment.save()

        serializer = self.get_serializer(rental)
        return Response(serializer.data)


class MatchEventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Match Events
    Addresses User Stories: 27, 28, 36, 37
    """
    queryset = MatchEvent.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'sport_type', 'court__name']
    ordering_fields = ['match_date', 'match_time', 'created_at']
    ordering = ['match_date', 'match_time']

    def get_serializer_class(self):
        if self.action == 'create':
            return MatchEventCreateSerializer
        return MatchEventSerializer

    def get_queryset(self):
        """Filter match events"""
        queryset = MatchEvent.objects.all()

        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Filter by date
        date_from = self.request.query_params.get('date_from')
        if date_from:
            queryset = queryset.filter(match_date__gte=date_from)

        # Filter by sport type
        sport = self.request.query_params.get('sport')
        if sport:
            queryset = queryset.filter(sport_type__icontains=sport)

        # Filter available matches (not full)
        available = self.request.query_params.get('available')
        if available == 'true':
            queryset = queryset.filter(
                current_players__lt=models.F('max_players')
            )

        return queryset.select_related('court', 'created_by', 'booking')

    @extend_schema(
        summary="Join match",
        description="Join an open match event"
    )
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join a match"""
        match = self.get_object()

        # Check if match is open
        if match.status != 'OPEN':
            return Response(
                {'error': 'Match is not open for joining'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if full
        if match.is_full():
            return Response(
                {'error': 'Match is full'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if already joined
        if MatchParticipant.objects.filter(
            match_event=match,
            player=request.user
        ).exists():
            return Response(
                {'error': 'You have already joined this match'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create participant
        MatchParticipant.objects.create(
            match_event=match,
            player=request.user
        )

        # Update player count
        match.current_players += 1
        if match.current_players >= match.max_players:
            match.status = 'FULL'
        match.save()

        serializer = self.get_serializer(match)
        return Response(serializer.data)

    @extend_schema(
        summary="Leave match",
        description="Leave a match event"
    )
    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """Leave a match"""
        match = self.get_object()

        # Cannot leave if creator
        if match.created_by == request.user:
            return Response(
                {'error': 'Match creator cannot leave. Cancel the match instead.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if participant
        try:
            participant = MatchParticipant.objects.get(
                match_event=match,
                player=request.user
            )
        except MatchParticipant.DoesNotExist:
            return Response(
                {'error': 'You are not a participant in this match'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Remove participant
        participant.delete()

        # Update player count
        match.current_players -= 1
        if match.status == 'FULL':
            match.status = 'OPEN'
        match.save()

        return Response({'message': 'Successfully left the match'})

    @extend_schema(
        summary="Cancel match",
        description="Cancel a match event (creator only)"
    )
    @action(detail=True, methods=['post'])
    def cancel_match(self, request, pk=None):
        """Cancel a match"""
        match = self.get_object()

        # Only creator can cancel
        if match.created_by != request.user:
            return Response(
                {'error': 'Only the match creator can cancel'},
                status=status.HTTP_403_FORBIDDEN
            )

        match.status = 'CANCELLED'
        match.save()

        serializer = self.get_serializer(match)
        return Response(serializer.data)


class PlayerRatingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Player Ratings
    Addresses User Story: 40 - Rate other players
    """
    queryset = PlayerRating.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return PlayerRatingCreateSerializer
        return PlayerRatingSerializer

    def get_queryset(self):
        """Filter ratings"""
        queryset = PlayerRating.objects.all()

        # Filter by match
        match_id = self.request.query_params.get('match')
        if match_id:
            queryset = queryset.filter(match_event_id=match_id)

        # Filter by player
        player_id = self.request.query_params.get('player')
        if player_id:
            queryset = queryset.filter(rated_player_id=player_id)

        return queryset


class BookingShareViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Booking Shares
    Addresses User Story: 46 - Share bookings with friends
    """
    queryset = BookingShare.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return BookingShareCreateSerializer
        return BookingShareSerializer

    def get_queryset(self):
        """Users see only their shares"""
        return BookingShare.objects.filter(shared_by=self.request.user)

    @extend_schema(
        summary="Join via share link",
        description="Join a booking using a share token"
    )
    @action(detail=False, methods=['post'])
    def join(self, request):
        """Join a booking via share link"""
        token = request.data.get('share_token')

        if not token:
            return Response(
                {'error': 'share_token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            share = BookingShare.objects.get(share_token=token)
        except BookingShare.DoesNotExist:
            return Response(
                {'error': 'Invalid share token'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if valid
        if not share.is_valid():
            return Response(
                {'error': 'Share link has expired or is full'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if already joined
        if share.joined_users.filter(id=request.user.id).exists():
            return Response(
                {'error': 'You have already joined this booking'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Add user
        share.joined_users.add(request.user)

        serializer = self.get_serializer(share)
        return Response(serializer.data)
