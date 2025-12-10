from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    CourtCategory, CourtRegistration, Court, CourtImage,
    DynamicPricing, CourtBlockedSlot, CourtReview, EquipmentItem
)


@admin.register(CourtCategory)
class CourtCategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for Court Categories
    Addresses User Story: 9
    """
    list_display = ('name', 'is_active', 'court_count', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'description', 'icon', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def court_count(self, obj):
        """Display number of courts in this category"""
        count = obj.courts.filter(is_active=True).count()
        return format_html(
            '<span style="font-weight: bold; color: blue;">{}</span>',
            count
        )
    court_count.short_description = 'Active Courts'

    actions = ['activate_categories', 'deactivate_categories']

    def activate_categories(self, request, queryset):
        """Activate selected categories"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} categor(y/ies) activated.')
    activate_categories.short_description = 'Activate selected categories'

    def deactivate_categories(self, request, queryset):
        """Deactivate selected categories"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} categor(y/ies) deactivated.')
    deactivate_categories.short_description = 'Deactivate selected categories'


@admin.register(CourtRegistration)
class CourtRegistrationAdmin(admin.ModelAdmin):
    """
    Admin interface for Court Registration Requests
    Addresses User Story: 1, 10
    """
    list_display = (
        'court_name', 'owner', 'city', 'status_badge',
        'created_at', 'reviewed_by'
    )
    list_filter = ('status', 'city', 'created_at')
    search_fields = (
        'court_name', 'owner__full_name',
        'owner__phone_number', 'city', 'address'
    )
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at', 'reviewed_at')

    fieldsets = (
        ('Court Information', {
            'fields': (
                'owner', 'court_name', 'description',
                'address', 'city', 'phone_number'
            )
        }),
        ('Documents', {
            'fields': ('registration_documents', 'court_images')
        }),
        ('Review Status', {
            'fields': ('status', 'rejection_reason', 'reviewed_by', 'reviewed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        """Display status with color badge"""
        colors = {
            'PENDING': 'orange',
            'APPROVED': 'green',
            'REJECTED': 'red',
        }
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    actions = ['approve_registrations', 'reject_registrations']

    def approve_registrations(self, request, queryset):
        """
        User Story 1: Approve court registrations
        This creates the actual Court object
        """
        from django.utils import timezone
        approved_count = 0

        for registration in queryset.filter(status='PENDING'):
            # Create the court from registration
            court = Court.objects.create(
                name=registration.court_name,
                owner=registration.owner,
                address=registration.address,
                city=registration.city,
                description=registration.description,
                phone_number=registration.phone_number,
                court_type='General',  # Default, can be updated
                base_hourly_rate=0,  # Default, needs to be set
                opening_time='06:00',
                closing_time='22:00',
                is_active=True,
                is_verified=True
            )

            # Update registration status
            registration.status = 'APPROVED'
            registration.reviewed_by = request.user
            registration.reviewed_at = timezone.now()
            registration.save()

            approved_count += 1

        self.message_user(
            request,
            f'{approved_count} registration(s) approved and court(s) created.'
        )
    approve_registrations.short_description = 'Approve selected registrations'

    def reject_registrations(self, request, queryset):
        """User Story 1: Reject court registrations"""
        from django.utils import timezone

        for registration in queryset.filter(status='PENDING'):
            registration.status = 'REJECTED'
            registration.reviewed_by = request.user
            registration.reviewed_at = timezone.now()
            if not registration.rejection_reason:
                registration.rejection_reason = 'Rejected by admin'
            registration.save()

        count = queryset.filter(status='REJECTED').count()
        self.message_user(request, f'{count} registration(s) rejected.')
    reject_registrations.short_description = 'Reject selected registrations'

    def get_queryset(self, request):
        """User Story 1: See pending court registrations"""
        qs = super().get_queryset(request)
        return qs.select_related('owner', 'reviewed_by')


class CourtImageInline(admin.TabularInline):
    """Inline for court images"""
    model = CourtImage
    extra = 1
    fields = ('image', 'caption', 'is_primary')


class DynamicPricingInline(admin.TabularInline):
    """Inline for dynamic pricing rules"""
    model = DynamicPricing
    extra = 1
    fields = ('description', 'start_time', 'end_time',
              'days_of_week', 'hourly_rate', 'is_active')


@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    """
    Admin interface for Courts
    Addresses User Stories: 11, 13, 14, 18, 32, 33
    """
    list_display = (
        'name', 'owner', 'court_type', 'category', 'city',
        'rating_display', 'is_active', 'is_verified',
        'base_hourly_rate', 'booking_count'
    )
    list_filter = (
        'is_active', 'is_verified', 'is_indoor',
        'category', 'court_type', 'city'
    )
    search_fields = (
        'name', 'owner__full_name', 'city',
        'address', 'court_type'
    )
    readonly_fields = (
        'average_rating', 'total_reviews',
        'created_at', 'updated_at'
    )

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name', 'owner', 'category', 'court_type',
                'is_indoor', 'description'
            )
        }),
        ('Location', {
            'fields': ('address', 'city', 'latitude', 'longitude')
        }),
        ('Capacity & Amenities', {
            'fields': ('capacity', 'amenities')
        }),
        ('Pricing', {
            'fields': ('base_hourly_rate',)
        }),
        ('Operating Hours', {
            'fields': ('opening_time', 'closing_time')
        }),
        ('Status & Verification', {
            'fields': ('is_active', 'is_verified')
        }),
        ('Contact', {
            'fields': ('phone_number', 'email')
        }),
        ('Ratings', {
            'fields': ('average_rating', 'total_reviews'),
            'classes': ('collapse',)
        }),
        ('Staff Management', {
            'fields': ('managers',),
            'description': 'User Story 12: Add/Remove court managers'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    filter_horizontal = ('managers',)
    inlines = [CourtImageInline, DynamicPricingInline]

    def rating_display(self, obj):
        rating = float(obj.average_rating or 0)
        stars = '⭐' * int(rating)

        # make stars safe separately
        safe_stars = format_html("{}", stars)

        # now combine safely without float formatting bugs
        return format_html(
            "{} <span style='color: gray;'>({})</span>",
            safe_stars,
            f"{rating:.2f}"
        )

    def booking_count(self, obj):
        """Display booking count"""
        count = obj.bookings.filter(status='CONFIRMED').count()
        return format_html(
            '<span style="font-weight: bold; color: green;">{}</span>',
            count
        )
    booking_count.short_description = 'Bookings'

    actions = [
        'activate_courts', 'deactivate_courts',
        'verify_courts', 'export_court_list'
    ]

    def activate_courts(self, request, queryset):
        """Activate selected courts"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} court(s) activated.')
    activate_courts.short_description = 'Activate selected courts'

    def deactivate_courts(self, request, queryset):
        """Deactivate selected courts"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} court(s) deactivated.')
    deactivate_courts.short_description = 'Deactivate selected courts'

    def verify_courts(self, request, queryset):
        """Verify selected courts"""
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} court(s) verified.')
    verify_courts.short_description = 'Verify selected courts'

    def export_court_list(self, request, queryset):
        """User Story 6: Export court data"""
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="courts.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Name', 'Owner', 'Type', 'City', 'Rating',
            'Hourly Rate', 'Active', 'Verified'
        ])

        for court in queryset:
            writer.writerow([
                court.name,
                court.owner.full_name,
                court.court_type,
                court.city,
                court.average_rating,
                court.base_hourly_rate,
                court.is_active,
                court.is_verified
            ])

        return response
    export_court_list.short_description = 'Export selected courts to CSV'


@admin.register(DynamicPricing)
class DynamicPricingAdmin(admin.ModelAdmin):
    """
    Admin interface for Dynamic Pricing
    Addresses User Story: 14
    """
    list_display = (
        'court', 'description', 'time_range',
        'days_display', 'hourly_rate', 'is_active'
    )
    list_filter = ('is_active', 'court__city')
    search_fields = ('court__name', 'description')

    fieldsets = (
        ('Court', {
            'fields': ('court',)
        }),
        ('Time Configuration', {
            'fields': ('start_time', 'end_time', 'days_of_week')
        }),
        ('Pricing', {
            'fields': ('hourly_rate', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    def time_range(self, obj):
        """Display time range"""
        return f"{obj.start_time} - {obj.end_time}"
    time_range.short_description = 'Time'

    def days_display(self, obj):
        """Display days of week safely"""
        return obj.days_of_week

    days_display.short_description = 'Days'


@admin.register(CourtBlockedSlot)
class CourtBlockedSlotAdmin(admin.ModelAdmin):
    """
    Admin interface for Blocked Time Slots
    Addresses User Story: 18
    """
    list_display = (
        'court', 'blocked_date', 'time_range',
        'reason', 'blocked_by'
    )
    list_filter = ('blocked_date', 'court__city')
    search_fields = ('court__name', 'reason')
    date_hierarchy = 'blocked_date'
    readonly_fields = ('created_at', 'blocked_by')

    fieldsets = (
        ('Court & Date', {
            'fields': ('court', 'blocked_date')
        }),
        ('Time Range', {
            'fields': ('start_time', 'end_time')
        }),
        ('Details', {
            'fields': ('reason', 'notes', 'blocked_by')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def time_range(self, obj):
        """Display time range"""
        return f"{obj.start_time} - {obj.end_time}"
    time_range.short_description = 'Time'

    def save_model(self, request, obj, form, change):
        """Auto-set blocked_by to current user"""
        if not obj.pk:
            obj.blocked_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(CourtReview)
class CourtReviewAdmin(admin.ModelAdmin):
    """
    Admin interface for Court Reviews
    Addresses User Story: 19, 39
    """
    list_display = (
        'court', 'player', 'rating_stars', 'review_preview',
        'is_visible', 'is_flagged', 'created_at'
    )
    list_filter = (
        'rating', 'is_visible', 'is_flagged',
        'created_at', 'court__city'
    )
    search_fields = (
        'court__name', 'player__full_name',
        'review_text', 'owner_response'
    )
    readonly_fields = ('created_at', 'updated_at', 'responded_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Review Information', {
            'fields': ('court', 'player', 'rating', 'review_text')
        }),
        ('Owner Response', {
            'fields': ('owner_response', 'responded_at')
        }),
        ('Moderation', {
            'fields': ('is_visible', 'is_flagged', 'flag_reason')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def rating_stars(self, obj):
        """Display rating as stars"""
        return '⭐' * obj.rating
    rating_stars.short_description = 'Rating'

    def review_preview(self, obj):
        """Show first 50 characters of review"""
        return (obj.review_text[:50] + '...') if len(obj.review_text) > 50 else obj.review_text
    review_preview.short_description = 'Review'

    actions = ['approve_reviews', 'flag_reviews', 'hide_reviews']

    def approve_reviews(self, request, queryset):
        """Approve and make reviews visible"""
        updated = queryset.update(is_visible=True, is_flagged=False)
        self.message_user(request, f'{updated} review(s) approved.')
    approve_reviews.short_description = 'Approve selected reviews'

    def flag_reviews(self, request, queryset):
        """Flag reviews for moderation"""
        updated = queryset.update(is_flagged=True)
        self.message_user(request, f'{updated} review(s) flagged.')
    flag_reviews.short_description = 'Flag selected reviews'

    def hide_reviews(self, request, queryset):
        """Hide abusive reviews"""
        updated = queryset.update(is_visible=False)
        self.message_user(request, f'{updated} review(s) hidden.')
    hide_reviews.short_description = 'Hide selected reviews'


@admin.register(EquipmentItem)
class EquipmentItemAdmin(admin.ModelAdmin):
    """
    Admin interface for Equipment Items
    Addresses User Story: 29
    """
    list_display = (
        'name', 'court', 'availability_display',
        'rental_rate', 'damage_penalty', 'is_active'
    )
    list_filter = ('is_active', 'court__city')
    search_fields = ('name', 'court__name', 'description')

    fieldsets = (
        ('Basic Information', {
            'fields': ('court', 'name', 'description', 'is_active')
        }),
        ('Quantity', {
            'fields': ('quantity_total', 'quantity_available')
        }),
        ('Pricing', {
            'fields': ('rental_rate', 'damage_penalty')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    def availability_display(self, obj):
        """Display availability status"""
        if obj.quantity_available == 0:
            color = 'red'
            status = 'Unavailable'
        elif obj.quantity_available < obj.quantity_total / 2:
            color = 'orange'
            status = f'{obj.quantity_available}/{obj.quantity_total}'
        else:
            color = 'green'
            status = f'{obj.quantity_available}/{obj.quantity_total}'

        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, status
        )
    availability_display.short_description = 'Availability'
