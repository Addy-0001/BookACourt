from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, EmailVerificationToken, PhoneVerificationToken, PasswordResetToken

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    # Fields to display in list view
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_email_verified', 'is_phone_verified', 'is_active', 'is_staff', 'created_at')
    list_filter = ('role', 'is_email_verified', 'is_phone_verified', 'is_active', 'is_staff', 'created_at')
    search_fields = ('email', 'phone_number', 'first_name', 'last_name')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    # Specify email as the username field
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    # Fieldsets for detail view
    fieldsets = (
        ('Account Info', {'fields': ('id', 'email', 'phone_number', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Verification', {'fields': ('is_email_verified', 'is_phone_verified')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

    # Fields for creating a new user in admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )

# The token admin classes don’t need changes
@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'expires_at', 'is_used')
    list_filter = ('is_used', 'created_at', 'expires_at')
    search_fields = ('user__email',)
    readonly_fields = ('id', 'token', 'created_at')


@admin.register(PhoneVerificationToken)
class PhoneVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'expires_at', 'is_used', 'attempts')
    list_filter = ('is_used', 'created_at', 'expires_at')
    search_fields = ('user__phone_number',)
    readonly_fields = ('id', 'created_at')


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'expires_at', 'is_used')
    list_filter = ('is_used', 'created_at', 'expires_at')
    search_fields = ('user__email',)
    readonly_fields = ('id', 'token', 'created_at')
