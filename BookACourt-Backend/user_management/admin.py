from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.db.models import Count, Q
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    User, UserRole, PasswordResetToken, UserPreference,
    PlayerStats, Friendship
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin interface for User model
    Addresses User Stories: 2, 30, 31, 47
    """
    list_display = (
        'phone_number', 'full_name', 'email', 'role',
        'is_active', 'is_phone_verified', 'loyalty_points_display',
        'created_at'
    )
    list_filter = (
        'role', 'is_active', 'is_phone_verified',
        'is_staff', 'is_superuser', 'created_at'
    )
    search_fields = ('phone_number', 'full_name', 'email', 'city')
    ordering = ('-created_at',)

    fieldsets = (
        ('Authentication', {
            'fields': ('phone_number', 'password', 'is_phone_verified')
        }),
        ('Personal Info', {
            'fields': ('full_name', 'email', 'profile_picture', 'date_of_birth', 'address', 'city')
        }),
        ('Role & Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Loyalty Program', {
            'fields': ('loyalty_points',),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('last_login', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at', 'last_login')

    add_fieldsets = (
        ('Create New User', {
            'classes': ('wide',),
            'fields': (
                'phone_number', 'full_name', 'email', 'password1',
                'password2', 'role', 'is_active', 'is_phone_verified'
            ),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions')

    actions = [
        'activate_users', 'deactivate_users', 'verify_phone_numbers',
        'make_court_owner', 'make_court_manager', 'make_player'
    ]

    def loyalty_points_display(self, obj):
        """Display loyalty points with color coding"""
        if obj.role == UserRole.PLAYER:
            color = 'green' if obj.loyalty_points > 100 else 'orange'
            return format_html(
                '<span style="color: {}; font-weight: bold;">{} pts</span>',
                color, obj.loyalty_points
            )
        return '-'
    loyalty_points_display.short_description = 'Loyalty Points'

    def activate_users(self, request, queryset):
        """User Story 2: Suspend/Activate accounts"""
        updated = queryset.update(is_active=True)
        self.message_user(
            request, f'{updated} user(s) activated successfully.')
    activate_users.short_description = 'Activate selected users'

    def deactivate_users(self, request, queryset):
        """User Story 2: Suspend/Activate accounts"""
        updated = queryset.update(is_active=False)
        self.message_user(
            request, f'{updated} user(s) deactivated successfully.')
    deactivate_users.short_description = 'Deactivate selected users'

    def verify_phone_numbers(self, request, queryset):
        """Verify phone numbers for selected users"""
        updated = queryset.update(is_phone_verified=True)
        self.message_user(request, f'{updated} phone number(s) verified.')
    verify_phone_numbers.short_description = 'Verify phone numbers'

    def make_court_owner(self, request, queryset):
        """Change role to Court Owner"""
        updated = queryset.update(role=UserRole.COURT_OWNER)
        self.message_user(
            request, f'{updated} user(s) changed to Court Owner.')
    make_court_owner.short_description = 'Change to Court Owner'

    def make_court_manager(self, request, queryset):
        """Change role to Court Manager"""
        updated = queryset.update(role=UserRole.COURT_MANAGER)
        self.message_user(
            request, f'{updated} user(s) changed to Court Manager.')
    make_court_manager.short_description = 'Change to Court Manager'

    def make_player(self, request, queryset):
        """Change role to Player"""
        updated = queryset.update(role=UserRole.PLAYER)
        self.message_user(request, f'{updated} user(s) changed to Player.')
    make_player.short_description = 'Change to Player'

    def get_queryset(self, request):
        """User Story 2: View list of all users"""
        qs = super().get_queryset(request)
        return qs.select_related().prefetch_related('groups', 'user_permissions')


@admin.register(PlayerStats)
class PlayerStatsAdmin(admin.ModelAdmin):
    """
    Admin interface for Player Statistics
    Addresses User Story: 44
    """
    list_display = (
        'player', 'total_bookings', 'total_matches_played',
        'matches_won', 'matches_lost', 'win_loss_ratio',
        'sportsmanship_rating', 'no_show_count'
    )
    list_filter = ('player__city', 'no_show_count')
    search_fields = ('player__full_name', 'player__phone_number')
    readonly_fields = (
        'created_at', 'updated_at', 'win_loss_ratio',
        'total_bookings', 'total_matches_played',
        'matches_won', 'matches_lost'
    )

    fieldsets = (
        ('Player Information', {
            'fields': ('player',)
        }),
        ('Booking Statistics', {
            'fields': ('total_bookings', 'no_show_count')
        }),
        ('Match Statistics', {
            'fields': (
                'total_matches_played', 'matches_won',
                'matches_lost', 'win_loss_ratio'
            )
        }),
        ('Ratings', {
            'fields': ('sportsmanship_rating', 'total_ratings_received')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        """Stats are auto-created with player"""
        return False


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    """
    Admin interface for User Preferences
    Addresses User Story: 31
    """
    list_display = (
        'user', 'email_notifications', 'sms_notifications',
        'push_notifications', 'preferred_sports'
    )
    list_filter = (
        'email_notifications', 'sms_notifications',
        'push_notifications'
    )
    search_fields = ('user__full_name', 'user__phone_number',
                     'preferred_sports')

    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Notification Preferences', {
            'fields': (
                'email_notifications', 'sms_notifications',
                'push_notifications'
            )
        }),
        ('Game Preferences', {
            'fields': ('preferred_sports', 'preferred_time_slots')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    """
    Admin interface for Friendships
    Addresses User Story: 42
    """
    list_display = (
        'from_user', 'to_user', 'status_badge',
        'created_at', 'updated_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = (
        'from_user__full_name', 'to_user__full_name',
        'from_user__phone_number', 'to_user__phone_number'
    )
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Friendship Details', {
            'fields': ('from_user', 'to_user', 'status')
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
            'ACCEPTED': 'green',
            'REJECTED': 'red',
        }
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    actions = ['accept_requests', 'reject_requests']

    def accept_requests(self, request, queryset):
        """Accept pending friend requests"""
        updated = queryset.filter(status='PENDING').update(status='ACCEPTED')
        self.message_user(request, f'{updated} friend request(s) accepted.')
    accept_requests.short_description = 'Accept selected requests'

    def reject_requests(self, request, queryset):
        """Reject pending friend requests"""
        updated = queryset.filter(status='PENDING').update(status='REJECTED')
        self.message_user(request, f'{updated} friend request(s) rejected.')
    reject_requests.short_description = 'Reject selected requests'


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """
    Admin interface for Password Reset Tokens
    Addresses User Story: 47
    """
    list_display = (
        'user', 'token_preview', 'is_valid_badge',
        'is_used', 'created_at', 'expires_at'
    )
    list_filter = ('is_used', 'created_at', 'expires_at')
    search_fields = ('user__full_name', 'user__phone_number', 'token')
    readonly_fields = ('token', 'created_at', 'expires_at', 'is_valid')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Token Information', {
            'fields': ('user', 'token', 'is_used')
        }),
        ('Validity', {
            'fields': ('created_at', 'expires_at', 'is_valid')
        }),
    )

    def token_preview(self, obj):
        """Show first 10 characters of token"""
        return f"{obj.token[:10]}..."
    token_preview.short_description = 'Token'

    def is_valid_badge(self, obj):
        """Display validity status with badge"""
        is_valid = obj.is_valid()
        color = 'green' if is_valid else 'red'
        text = 'Valid' if is_valid else 'Invalid'
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 10px; border-radius: 3px;">{}</span>',
            color, text
        )
    is_valid_badge.short_description = 'Valid'

    def has_add_permission(self, request):
        """Tokens are created programmatically"""
        return False

    actions = ['invalidate_tokens']

    def invalidate_tokens(self, request, queryset):
        """Mark tokens as used"""
        updated = queryset.update(is_used=True)
        self.message_user(request, f'{updated} token(s) invalidated.')
    invalidate_tokens.short_description = 'Invalidate selected tokens'


# Customize admin site headers
admin.site.site_header = "BookACourt Main Admin Panel"
admin.site.site_title = 'BookACourt Admin'
admin.site.index_title = 'Welcome to BookACourt Admin Panel'
