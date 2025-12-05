from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Sum
from django.utils import timezone
from .models import (
    Booking, CancellationPolicy, BookingNotification, EquipmentRental,
    MatchEvent, MatchParticipant, PlayerRating, BookingShare
)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Admin interface for Bookings
    Addresses User Stories: 13, 20, 22, 34, 35, 38
    """
    list_display = (
        'booking_reference', 'court', 'player', 'booking_date',
        'time_range', 'status_badge', 'payment_status_badge',
        'total_amount', 'is_walk_in'
    )
    list_filter = (
        'status', 'payment_status', 'payment_method',
        'booking_date', 'is_walk_in', 'court__city'
    )
    search_fields = (
        'booking_reference', 'court__name', 'player__full_name',
        'player__phone_number', 'walk_in_guest_name'
    )
    date_hierarchy = 'booking_date'
    readonly_fields = (
        'booking_reference', 'created_at', 'updated_at',
        'cancelled_at', 'refund_amount'
    )

    fieldsets = (
        ('Booking Details', {
            'fields': (
                'booking_reference', 'court', 'player',
                'booking_date', 'start_time', 'end_time'
            )
        }),
        ('Status', {
            'fields': ('status', 'payment_status', 'payment_method')
        }),
        ('Pricing', {
            'fields': (
                'base_amount', 'discount_amount',
                'loyalty_points_used', 'total_amount'
            )
        }),
        ('Walk-in Booking', {
            'fields': ('is_walk_in', 'walk_in_guest_name'),
            'classes': ('collapse',),
            'description': 'User Story 22: Handle walk-in bookings'
        }),
        ('Additional Information', {
            'fields': ('notes', 'special_requests'),
            'classes': ('collapse',)
        }),
        ('Cancellation', {
            'fields': (
                'cancelled_at', 'cancellation_reason', 'refund_amount'
            ),
            'classes': ('collapse',),
            'description': 'User Story 35: Manage cancellations'
        }),
        ('Tracking', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def time_range(self, obj):
        """Display time range"""
        return f"{obj.start_time} - {obj.end_time}"
    time_range.short_description = 'Time'

    def status_badge(self, obj):
        """Display status with color badge"""
        colors = {
            'PENDING': 'orange',
            'CONFIRMED': 'green',
            'CANCELLED': 'red',
            'COMPLETED': 'blue',
            'NO_SHOW': 'darkred',
        }
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def payment_status_badge(self, obj):
        """Display payment status with color badge"""
        colors = {
            'PENDING': 'orange',
            'COMPLETED': 'green',
            'REFUNDED': 'blue',
            'FAILED': 'red',
        }
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 8px; border-radius: 3px;">{}</span>',
            colors.get(obj.payment_status, 'gray'),
            obj.get_payment_status_display()
        )
    payment_status_badge.short_description = 'Payment'

    actions = [
        'confirm_bookings', 'cancel_bookings', 'mark_completed',
        'mark_no_show', 'export_bookings'
    ]

    def confirm_bookings(self, request, queryset):
        """Confirm pending bookings"""
        updated = queryset.filter(status='PENDING').update(status='CONFIRMED')
        self.message_user(request, f'{updated} booking(s) confirmed.')
    confirm_bookings.short_description = 'Confirm selected bookings'

    def cancel_bookings(self, request, queryset):
        """Cancel bookings"""
        for booking in queryset.exclude(status='CANCELLED'):
            booking.status = 'CANCELLED'
            booking.cancelled_at = timezone.now()
            booking.save()

        count = queryset.filter(status='CANCELLED').count()
        self.message_user(request, f'{count} booking(s) cancelled.')
    cancel_bookings.short_description = 'Cancel selected bookings'

    def mark_completed(self, request, queryset):
        """Mark bookings as completed"""
        updated = queryset.update(status='COMPLETED')
        self.message_user(
            request, f'{updated} booking(s) marked as completed.')
    mark_completed.short_description = 'Mark as completed'

    def mark_no_show(self, request, queryset):
        """User Story 24: Mark no-shows"""
        updated = queryset.update(status='NO_SHOW')

        # Update player stats
        for booking in queryset:
            if hasattr(booking.player, 'stats'):
                booking.player.stats.no_show_count += 1
                booking.player.stats.save()

        self.message_user(request, f'{updated} booking(s) marked as no-show.')
    mark_no_show.short_description = 'Mark as no-show'

    def export_bookings(self, request, queryset):
        """User Story 6, 13: Export booking data"""
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="bookings.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Reference', 'Court', 'Player', 'Date', 'Time',
            'Status', 'Payment Status', 'Amount'
        ])

        for booking in queryset:
            writer.writerow([
                booking.booking_reference,
                booking.court.name,
                booking.player.full_name,
                booking.booking_date,
                f"{booking.start_time}-{booking.end_time}",
                booking.get_status_display(),
                booking.get_payment_status_display(),
                booking.total_amount
            ])

        return response
    export_bookings.short_description = 'Export to CSV'

    def get_queryset(self, request):
        """User Story 13: View bookings"""
        qs = super().get_queryset(request)
        return qs.select_related('court', 'player', 'created_by')


@admin.register(CancellationPolicy)
class CancellationPolicyAdmin(admin.ModelAdmin):
    """
    Admin interface for Cancellation Policies
    Addresses User Story: 15
    """
    list_display = (
        'court', 'cancellation_deadline_hours',
        'full_refund_hours', 'partial_refund_percentage',
        'no_show_penalty_percentage'
    )
    list_filter = ('court__city',)
    search_fields = ('court__name', 'policy_text')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Court', {
            'fields': ('court',)
        }),
        ('Cancellation Deadlines', {
            'fields': (
                'cancellation_deadline_hours',
                'full_refund_hours',
                'partial_refund_hours'
            )
        }),
        ('Refund Configuration', {
            'fields': (
                'partial_refund_percentage',
                'no_show_penalty_percentage'
            )
        }),
        ('Policy Text', {
            'fields': ('policy_text',),
            'description': 'Full policy description shown to players'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BookingNotification)
class BookingNotificationAdmin(admin.ModelAdmin):
    """
    Admin interface for Booking Notifications
    Addresses User Story: 41
    """
    list_display = (
        'notification_type', 'booking', 'user',
        'delivery_status', 'is_read', 'sent_at'
    )
    list_filter = (
        'notification_type', 'is_read', 'sent_via_email',
        'sent_via_sms', 'sent_via_push', 'sent_at'
    )
    search_fields = (
        'booking__booking_reference', 'user__full_name',
        'message'
    )
    date_hierarchy = 'sent_at'
    readonly_fields = ('sent_at',)

    fieldsets = (
        ('Notification Details', {
            'fields': (
                'notification_type', 'booking',
                'user', 'message'
            )
        }),
        ('Delivery Status', {
            'fields': (
                'is_read', 'sent_via_email',
                'sent_via_sms', 'sent_via_push'
            )
        }),
        ('Timestamp', {
            'fields': ('sent_at',)
        }),
    )

    def delivery_status(self, obj):
        """Show delivery channels"""
        channels = []
        if obj.sent_via_email:
            channels.append('📧 Email')
        if obj.sent_via_sms:
            channels.append('📱 SMS')
        if obj.sent_via_push:
            channels.append('🔔 Push')
        return ' | '.join(channels) if channels else 'Not sent'
    delivery_status.short_description = 'Delivered Via'

    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        """Mark notifications as read"""
        updated = queryset.update(is_read=True)
        self.message_user(
            request, f'{updated} notification(s) marked as read.')
    mark_as_read.short_description = 'Mark as read'


@admin.register(EquipmentRental)
class EquipmentRentalAdmin(admin.ModelAdmin):
    """
    Admin interface for Equipment Rentals
    Addresses User Story: 29
    """
    list_display = (
        'equipment', 'booking', 'quantity',
        'rental_cost', 'status_badge',
        'damage_charge', 'returned_by'
    )
    list_filter = ('status', 'equipment__court__city')
    search_fields = (
        'equipment__name', 'booking__booking_reference',
        'damage_notes'
    )
    readonly_fields = ('created_at', 'updated_at', 'returned_at')

    fieldsets = (
        ('Rental Information', {
            'fields': (
                'booking', 'equipment',
                'quantity', 'rental_cost'
            )
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Return Information', {
            'fields': (
                'returned_at', 'returned_by',
                'damage_notes', 'damage_charge'
            ),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        """Display status with color badge"""
        colors = {
            'ACTIVE': 'green',
            'RETURNED': 'blue',
            'DAMAGED': 'red',
        }
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 8px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    actions = ['mark_returned', 'mark_damaged']

    def mark_returned(self, request, queryset):
        """Mark equipment as returned"""
        for rental in queryset:
            rental.status = 'RETURNED'
            rental.returned_at = timezone.now()
            rental.returned_by = request.user
            rental.save()

        count = queryset.count()
        self.message_user(request, f'{count} rental(s) marked as returned.')
    mark_returned.short_description = 'Mark as returned'

    def mark_damaged(self, request, queryset):
        """Mark equipment as damaged"""
        updated = queryset.update(status='DAMAGED')
        self.message_user(request, f'{updated} rental(s) marked as damaged.')
    mark_damaged.short_description = 'Mark as damaged'


class MatchParticipantInline(admin.TabularInline):
    """Inline for match participants"""
    model = MatchParticipant
    extra = 0
    fields = ('player', 'is_confirmed', 'attended', 'joined_at')
    readonly_fields = ('joined_at',)


@admin.register(MatchEvent)
class MatchEventAdmin(admin.ModelAdmin):
    """
    Admin interface for Match Events
    Addresses User Stories: 27, 28, 36, 37
    """
    list_display = (
        'title', 'court', 'created_by', 'match_date',
        'match_time', 'participants_display', 'status_badge',
        'skill_level'
    )
    list_filter = ('status', 'skill_level', 'sport_type', 'match_date')
    search_fields = (
        'title', 'court__name', 'created_by__full_name',
        'description'
    )
    date_hierarchy = 'match_date'
    readonly_fields = ('created_at', 'updated_at', 'current_players')
    inlines = [MatchParticipantInline]

    fieldsets = (
        ('Event Details', {
            'fields': (
                'title', 'description', 'sport_type',
                'court', 'booking'
            )
        }),
        ('Creator', {
            'fields': ('created_by',)
        }),
        ('Capacity', {
            'fields': ('max_players', 'current_players')
        }),
        ('Date & Time', {
            'fields': ('match_date', 'match_time', 'duration_hours')
        }),
        ('Requirements', {
            'fields': ('skill_level',)
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def participants_display(self, obj):
        """Display participant count"""
        if obj.is_full():
            color = 'red'
        elif obj.current_players > obj.max_players / 2:
            color = 'green'
        else:
            color = 'orange'

        return format_html(
            '<span style="color: {}; font-weight: bold;">{}/{}</span>',
            color, obj.current_players, obj.max_players
        )
    participants_display.short_description = 'Participants'

    def status_badge(self, obj):
        """Display status with color badge"""
        colors = {
            'OPEN': 'green',
            'FULL': 'orange',
            'IN_PROGRESS': 'blue',
            'COMPLETED': 'gray',
            'CANCELLED': 'red',
        }
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 8px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    actions = ['cancel_matches', 'mark_in_progress', 'mark_completed']

    def cancel_matches(self, request, queryset):
        """User Story 27: Update status if canceled"""
        updated = queryset.update(status='CANCELLED')
        self.message_user(request, f'{updated} match(es) cancelled.')
    cancel_matches.short_description = 'Cancel selected matches'

    def mark_in_progress(self, request, queryset):
        """Mark matches as in progress"""
        updated = queryset.update(status='IN_PROGRESS')
        self.message_user(
            request, f'{updated} match(es) marked as in progress.')
    mark_in_progress.short_description = 'Mark as in progress'

    def mark_completed(self, request, queryset):
        """Mark matches as completed"""
        updated = queryset.update(status='COMPLETED')
        self.message_user(request, f'{updated} match(es) marked as completed.')
    mark_completed.short_description = 'Mark as completed'


@admin.register(PlayerRating)
class PlayerRatingAdmin(admin.ModelAdmin):
    """
    Admin interface for Player Ratings
    Addresses User Story: 40
    """
    list_display = (
        'rated_player', 'rated_by', 'match_event',
        'rating_stars', 'misconduct_reported', 'created_at'
    )
    list_filter = ('rating', 'misconduct_reported', 'created_at')
    search_fields = (
        'rated_player__full_name', 'rated_by__full_name',
        'feedback', 'misconduct_details'
    )
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Rating Information', {
            'fields': (
                'match_event', 'rated_by',
                'rated_player', 'rating', 'feedback'
            )
        }),
        ('Misconduct', {
            'fields': ('misconduct_reported', 'misconduct_details'),
            'classes': ('collapse',)
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )

    def rating_stars(self, obj):
        """Display rating as stars"""
        return '⭐' * obj.rating
    rating_stars.short_description = 'Rating'

    actions = ['review_misconduct']

    def review_misconduct(self, request, queryset):
        """Review misconduct reports"""
        count = queryset.filter(misconduct_reported=True).count()
        self.message_user(
            request,
            f'{count} rating(s) with misconduct reports selected for review.'
        )
    review_misconduct.short_description = 'Review misconduct reports'


@admin.register(BookingShare)
class BookingShareAdmin(admin.ModelAdmin):
    """
    Admin interface for Booking Shares
    Addresses User Story: 46
    """
    list_display = (
        'booking', 'shared_by', 'share_token_preview',
        'joined_count', 'max_joins', 'validity_badge',
        'expires_at'
    )
    list_filter = ('created_at', 'expires_at')
    search_fields = (
        'booking__booking_reference', 'shared_by__full_name',
        'share_token'
    )
    readonly_fields = ('share_token', 'created_at')

    fieldsets = (
        ('Share Information', {
            'fields': (
                'booking', 'shared_by',
                'share_token', 'max_joins'
            )
        }),
        ('Joined Users', {
            'fields': ('joined_users',)
        }),
        ('Validity', {
            'fields': ('expires_at', 'created_at')
        }),
    )

    filter_horizontal = ('joined_users',)

    def share_token_preview(self, obj):
        """Show first 10 characters of token"""
        return f"{obj.share_token[:10]}..."
    share_token_preview.short_description = 'Token'

    def joined_count(self, obj):
        """Display joined user count"""
        count = obj.joined_users.count()
        color = 'red' if count >= obj.max_joins else 'green'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, count
        )
    joined_count.short_description = 'Joined'

    def validity_badge(self, obj):
        """Display validity status"""
        is_valid = obj.is_valid()
        color = 'green' if is_valid else 'red'
        text = 'Valid' if is_valid else 'Expired'
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 8px; border-radius: 3px;">{}</span>',
            color, text
        )
    validity_badge.short_description = 'Valid'
