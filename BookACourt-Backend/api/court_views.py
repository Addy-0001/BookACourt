from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from django.db.models import Q, Avg, Count
from django.utils import timezone
from datetime import datetime, timedelta
from drf_spectacular.utils import extend_schema, OpenApiParameter

from court_management.models import (
    CourtCategory, CourtRegistration, Court, CourtImage,
    DynamicPricing, CourtBlockedSlot, CourtReview, EquipmentItem
)
from .court_serializers import (
    CourtCategorySerializer, CourtRegistrationSerializer,
    CourtRegistrationCreateSerializer, CourtListSerializer,
    CourtDetailSerializer, CourtCreateUpdateSerializer,
    CourtReviewSerializer, CourtReviewResponseSerializer,
    CourtBlockedSlotSerializer, CourtImageSerializer,
    DynamicPricingSerializer, EquipmentItemSerializer,
    CourtSearchSerializer, CourtAvailabilitySerializer
)
from .court_permissions import (
    IsCourtOwnerOrReadOnly, IsCourtOwnerOrManager,
    IsPlayerOrReadOnly, IsSuperUserOrReadOnly
)


class CourtCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Court Categories
    Addresses User Story: 9 - Browse courts by categories
    """
    queryset = CourtCategory.objects.filter(is_active=True)
    serializer_class = CourtCategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @extend_schema(
        summary="List all active court categories",
        description="Get a list of all active court categories with court counts"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Get category details",
        description="Get detailed information about a specific court category"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class CourtRegistrationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Court Registration
    Addresses User Story: 1, 10 - Register and manage court registrati
    """
    queryset = CourtRegistration.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['court_name', 'city', 'owner__full_name']
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return CourtRegistrationCreateSerializer
        return CourtRegistrationSerializer

    def get_queryset(self):
        """Filter based on user role"""
        user = self.request.user

        if user.is_super_user:
            # Super users see all registrations
            return CourtRegistration.objects.all()
        elif user.is_court_owner:
            # Court owners see only their registrations
            return CourtRegistration.objects.filter(owner=user)

        return CourtRegistration.objects.none()

    @extend_schema(
        summary="Submit court registration",
        description="Court owners can submit a registration request for a new court"
    )
    def create(self, request, *args, **kwargs):
        # Ensure user is a court owner
        if not request.user.is_court_owner:
            return Response(
                {'error': 'Only court owners can register courts'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Approve registration",
        description="Super users can approve pending court registrations"
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def approve(self, request, pk=None):
        """Approve a court registration and create the court"""
        if not request.user.is_super_user:
            return Response(
                {'error': 'Only super users can approve registrations'},
                status=status.HTTP_403_FORBIDDEN
            )

        registration = self.get_object()

        if registration.status != 'PENDING':
            return Response(
                {'error': 'Only pending registrations can be approved'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the court
        court = Court.objects.create(
            name=registration.court_name,
            owner=registration.owner,
            address=registration.address,
            city=registration.city,
            description=registration.description,
            phone_number=registration.phone_number,
            court_type='General',
            base_hourly_rate=0,
            opening_time='06:00',
            closing_time='22:00',
            is_active=True,
            is_verified=True
        )

        # Update registration
        registration.status = 'APPROVED'
        registration.reviewed_by = request.user
        registration.reviewed_at = timezone.now()
        registration.save()

        return Response({
            'message': 'Registration approved successfully',
            'court_id': court.id
        }, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Reject registration",
        description="Super users can reject pending court registrations"
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        """Reject a court registration"""
        if not request.user.is_super_user:
            return Response(
                {'error': 'Only super users can reject registrations'},
                status=status.HTTP_403_FORBIDDEN
            )

        registration = self.get_object()

        if registration.status != 'PENDING':
            return Response(
                {'error': 'Only pending registrations can be rejected'},
                status=status.HTTP_400_BAD_REQUEST
            )

        reason = request.data.get('reason', 'Rejected by admin')

        registration.status = 'REJECTED'
        registration.rejection_reason = reason
        registration.reviewed_by = request.user
        registration.reviewed_at = timezone.now()
        registration.save()

        return Response({
            'message': 'Registration rejected'
        }, status=status.HTTP_200_OK)


class CourtViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Courts
    Addresses User Stories: 11, 13, 14, 16, 18, 32, 33
    """
    queryset = Court.objects.filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'city', 'court_type', 'description']
    ordering_fields = ['name', 'city', 'base_hourly_rate',
                       'average_rating', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return CourtListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CourtCreateUpdateSerializer
        return CourtDetailSerializer

    def get_queryset(self):
        """Filter courts based on various criteria"""
        queryset = Court.objects.filter(is_active=True)

        # Apply filters from query params
        city = self.request.query_params.get('city')
        category = self.request.query_params.get('category')
        court_type = self.request.query_params.get('court_type')
        is_indoor = self.request.query_params.get('is_indoor')
        min_rating = self.request.query_params.get('min_rating')
        max_price = self.request.query_params.get('max_price')

        if city:
            queryset = queryset.filter(city__icontains=city)
        if category:
            queryset = queryset.filter(category_id=category)
        if court_type:
            queryset = queryset.filter(court_type__icontains=court_type)
        if is_indoor is not None:
            queryset = queryset.filter(is_indoor=is_indoor.lower() == 'true')
        if min_rating:
            queryset = queryset.filter(average_rating__gte=min_rating)
        if max_price:
            queryset = queryset.filter(base_hourly_rate__lte=max_price)

        return queryset.select_related('owner', 'category').prefetch_related('images')

    @extend_schema(
        summary="List all courts",
        description="Get a list of all active courts with filtering options",
        parameters=[
            OpenApiParameter('city', str, description='Filter by city'),
            OpenApiParameter(
                'category', int, description='Filter by category ID'),
            OpenApiParameter('court_type', str,
                             description='Filter by court type'),
            OpenApiParameter('is_indoor', bool,
                             description='Filter by indoor/outdoor'),
            OpenApiParameter('min_rating', float,
                             description='Minimum rating'),
            OpenApiParameter('max_price', float,
                             description='Maximum hourly rate'),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create new court",
        description="Court owners can create a new court (must have approved registration)"
    )
    def create(self, request, *args, **kwargs):
        if not request.user.is_court_owner:
            return Response(
                {'error': 'Only court owners can create courts'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Update court",
        description="Court owners can update their courts"
    )
    def update(self, request, *args, **kwargs):
        court = self.get_object()
        if not request.user.can_manage_court(court):
            return Response(
                {'error': 'You do not have permission to update this court'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Check court availability",
        description="Check if a court is available for a specific date/time"
    )
    @action(detail=True, methods=['post'])
    def check_availability(self, request, pk=None):
        """Check court availability for a specific date/time"""
        court = self.get_object()
        serializer = CourtAvailabilitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        date = serializer.validated_data['date']
        start_time = serializer.validated_data.get('start_time')
        end_time = serializer.validated_data.get('end_time')

        # Check if date is within operating hours
        if start_time and end_time:
            if start_time < court.opening_time or end_time > court.closing_time:
                return Response({
                    'available': False,
                    'reason': 'Outside operating hours',
                    'operating_hours': {
                        'opening': str(court.opening_time),
                        'closing': str(court.closing_time)
                    }
                })

        # Check for blocked slots
        blocked_slots = CourtBlockedSlot.objects.filter(
            court=court,
            blocked_date=date
        )

        if start_time and end_time:
            blocked_slots = blocked_slots.filter(
                Q(start_time__lt=end_time) & Q(end_time__gt=start_time)
            )

        if blocked_slots.exists():
            return Response({
                'available': False,
                'reason': 'Time slot is blocked',
                'blocked_slots': CourtBlockedSlotSerializer(blocked_slots, many=True).data
            })

        # Check for existing bookings
        from booking_management.models import Booking
        bookings = Booking.objects.filter(
            court=court,
            booking_date=date,
            status__in=['PENDING', 'CONFIRMED']
        )

        if start_time and end_time:
            bookings = bookings.filter(
                Q(start_time__lt=end_time) & Q(end_time__gt=start_time)
            )

        if bookings.exists():
            return Response({
                'available': False,
                'reason': 'Time slot already booked',
                'booked_slots': [{
                    'start_time': str(b.start_time),
                    'end_time': str(b.end_time)
                } for b in bookings]
            })

        return Response({
            'available': True,
            'message': 'Court is available for booking'
        })

    @extend_schema(
        summary="Get available time slots",
        description="Get all available time slots for a specific date"
    )
    @action(detail=True, methods=['get'])
    def available_slots(self, request, pk=None):
        """Get available time slots for a specific date"""
        court = self.get_object()
        date_str = request.query_params.get('date')

        if not date_str:
            return Response(
                {'error': 'Date parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get all bookings and blocked slots for the date
        from booking_management.models import Booking
        bookings = Booking.objects.filter(
            court=court,
            booking_date=date,
            status__in=['PENDING', 'CONFIRMED']
        ).values_list('start_time', 'end_time')

        blocked_slots = CourtBlockedSlot.objects.filter(
            court=court,
            blocked_date=date
        ).values_list('start_time', 'end_time')

        # Combine all unavailable slots
        unavailable_slots = list(bookings) + list(blocked_slots)

        # Generate available slots (hourly intervals)
        available_slots = []
        current_time = court.opening_time

        while current_time < court.closing_time:
            next_time = (datetime.combine(date, current_time) +
                         timedelta(hours=1)).time()

            # Check if slot overlaps with any unavailable slot
            is_available = True
            for start, end in unavailable_slots:
                if current_time < end and next_time > start:
                    is_available = False
                    break

            if is_available:
                available_slots.append({
                    'start_time': str(current_time),
                    'end_time': str(next_time)
                })

            current_time = next_time

        return Response({
            'date': date_str,
            'available_slots': available_slots
        })

    @extend_schema(
        summary="Add court manager",
        description="Court owners can add managers to their courts"
    )
    @action(detail=True, methods=['post'])
    def add_manager(self, request, pk=None):
        """Add a manager to the court"""
        court = self.get_object()

        if not request.user.is_court_owner or court.owner != request.user:
            return Response(
                {'error': 'Only the court owner can add managers'},
                status=status.HTTP_403_FORBIDDEN
            )

        manager_id = request.data.get('manager_id')
        if not manager_id:
            return Response(
                {'error': 'manager_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            from user_management.models import User, UserRole
            manager = User.objects.get(id=manager_id)

            if manager.role != UserRole.COURT_MANAGER:
                return Response(
                    {'error': 'User must have Court Manager role'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            court.managers.add(manager)
            return Response({
                'message': f'Manager {manager.full_name} added successfully'
            })
        except User.DoesNotExist:
            return Response(
                {'error': 'Manager not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @extend_schema(
        summary="Remove court manager",
        description="Court owners can remove managers from their courts"
    )
    @action(detail=True, methods=['post'])
    def remove_manager(self, request, pk=None):
        """Remove a manager from the court"""
        court = self.get_object()

        if not request.user.is_court_owner or court.owner != request.user:
            return Response(
                {'error': 'Only the court owner can remove managers'},
                status=status.HTTP_403_FORBIDDEN
            )

        manager_id = request.data.get('manager_id')
        if not manager_id:
            return Response(
                {'error': 'manager_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            from user_management.models import User
            manager = User.objects.get(id=manager_id)
            court.managers.remove(manager)
            return Response({
                'message': f'Manager {manager.full_name} removed successfully'
            })
        except User.DoesNotExist:
            return Response(
                {'error': 'Manager not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class CourtReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Court Reviews
    Addresses User Story: 19, 39 - Review courts and respond to reviews
    """
    queryset = CourtReview.objects.filter(is_visible=True)
    serializer_class = CourtReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = CourtReview.objects.filter(is_visible=True)

        court_pk = self.kwargs.get('court_pk')
        if court_pk:
            queryset = queryset.filter(court_id=court_pk)

        return queryset.select_related('player', 'court')

    @extend_schema(
        summary="Create court review",
        description="Players can review courts they have booked"
    )
    def create(self, request, *args, **kwargs):
        if not request.user.is_player:
            return Response(
                {'error': 'Only players can create reviews'},
                status=status.HTTP_403_FORBIDDEN
            )

    # Check if user has already reviewed this court
        court_id = request.data.get('court')
        if CourtReview.objects.filter(court_id=court_id, player=request.user).exists():
            return Response(
                {'error': 'You have already reviewed this court'},
                status=status.HTTP_400_BAD_REQUEST
            )

    # Create review - signals will handle updating court stats
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Respond to review",
        description="Court owners can respond to reviews of their courts"
    )
    @action(detail=True, methods=['post'])
    def respond(self, request, pk=None):
        """Court owner responds to a review"""
        review = self.get_object()
        court = review.court

        if not request.user.can_manage_court(court):
            return Response(
                {'error': 'Only court owner/manager can respond to reviews'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CourtReviewResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(review, serializer.validated_data)

        return Response(CourtReviewSerializer(review).data)

    @extend_schema(
        summary="Flag review",
        description="Flag inappropriate reviews for moderation"
    )
    @action(detail=True, methods=['post'])
    def flag(self, request, pk=None):
        """Flag a review for moderation"""
        review = self.get_object()
        reason = request.data.get('reason', 'Inappropriate content')

        review.is_flagged = True
        review.flag_reason = reason
        review.save()

        return Response({
            'message': 'Review flagged for moderation'
        })

    # Create queryset
    def perform_create(self, serializer):
        serializer.save(
            player=self.request.user,
            court_id=self.kwargs.get('court_pk')
        )


class CourtBlockedSlotViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Blocked Time Slots
    Addresses User Story: 18 - Block time slots for maintenance
    """
    queryset = CourtBlockedSlot.objects.all()
    serializer_class = CourtBlockedSlotSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering = ['blocked_date', 'start_time']

    def get_queryset(self):
        """Filter by court and date range"""
        queryset = CourtBlockedSlot.objects.all()
        court_id = self.request.query_params.get('court')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if court_id:
            queryset = queryset.filter(court_id=court_id)
        if date_from:
            queryset = queryset.filter(blocked_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(blocked_date__lte=date_to)

        return queryset

    def create(self, request, *args, **kwargs):
        """Create blocked slot"""
        court_id = request.data.get('court')

        try:
            court = Court.objects.get(id=court_id)
            if not request.user.can_manage_court(court):
                return Response(
                    {'error': 'You do not have permission to block slots for this court'},
                    status=status.HTTP_403_FORBIDDEN
                )
        except Court.DoesNotExist:
            return Response(
                {'error': 'Court not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        return super().create(request, *args, **kwargs)


class DynamicPricingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Dynamic Pricing
    Addresses User Story: 14 - Set different rates for peak/off-peak times
    """
    queryset = DynamicPricing.objects.all()
    serializer_class = DynamicPricingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter by court"""
        queryset = DynamicPricing.objects.all()
        court_id = self.request.query_params.get('court')

        if court_id:
            queryset = queryset.filter(court_id=court_id)

        return queryset

    def create(self, request, *args, **kwargs):
        """Create pricing rule"""
        court_id = request.data.get('court')

        try:
            court = Court.objects.get(id=court_id)
            if not request.user.can_manage_court(court):
                return Response(
                    {'error': 'You do not have permission to set pricing for this court'},
                    status=status.HTTP_403_FORBIDDEN
                )
        except Court.DoesNotExist:
            return Response(
                {'error': 'Court not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        return super().create(request, *args, **kwargs)


class EquipmentItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Equipment Items
    Addresses User Story: 29 - Rent equipment
    """
    queryset = EquipmentItem.objects.filter(is_active=True)
    serializer_class = EquipmentItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Filter by court"""
        queryset = EquipmentItem.objects.filter(is_active=True)
        court_id = self.request.query_params.get('court')

        if court_id:
            queryset = queryset.filter(court_id=court_id)

        return queryset

    def create(self, request, *args, **kwargs):
        """Create equipment item"""
        court_id = request.data.get('court')

        try:
            court = Court.objects.get(id=court_id)
            if not request.user.can_manage_court(court):
                return Response(
                    {'error': 'You do not have permission to add equipment for this court'},
                    status=status.HTTP_403_FORBIDDEN
                )
        except Court.DoesNotExist:
            return Response(
                {'error': 'Court not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        return super().create(request, *args, **kwargs)
