from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .models import CustomUser


@shared_task
def send_verification_email(user_id, token):
    """Send email verification link to user."""
    try:
        user = CustomUser.objects.get(id=user_id)
        
        # Construct verification URL - adjust this based on your frontend
        verification_url = f"{settings.FRONTEND_URL}/verify-email/{token}"
        
        subject = "Email Verification - Book A Court"
        message = f"""
        Hello {user.first_name or user.email},
        
        Thank you for registering with Book A Court. Please verify your email address by clicking the link below:
        
        {verification_url}
        
        This link will expire in 24 hours.
        
        If you didn't register this account, please ignore this email.
        
        Best regards,
        Book A Court Team
        """
        
        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <div style="max-width: 600px; margin: 0 auto;">
                    <h2>Email Verification - Book A Court</h2>
                    <p>Hello {user.first_name or user.email},</p>
                    <p>Thank you for registering with Book A Court. Please verify your email address by clicking the button below:</p>
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{verification_url}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                            Verify Email
                        </a>
                    </div>
                    <p>Or copy this link: <a href="{verification_url}">{verification_url}</a></p>
                    <p><strong>This link will expire in 24 hours.</strong></p>
                    <p>If you didn't register this account, please ignore this email.</p>
                    <hr style="margin: 30px 0;">
                    <p style="color: #666; font-size: 12px;">Best regards,<br/>Book A Court Team</p>
                </div>
            </body>
        </html>
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return f"Verification email sent to {user.email}"
    
    except CustomUser.DoesNotExist:
        return f"User with id {user_id} not found"
    except Exception as e:
        return f"Error sending verification email: {str(e)}"


@shared_task
def send_password_reset_email(user_id, token):
    """Send password reset link to user."""
    try:
        user = CustomUser.objects.get(id=user_id)
        
        # Construct password reset URL - adjust this based on your frontend
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{token}"
        
        subject = "Password Reset - Book A Court"
        message = f"""
        Hello {user.first_name or user.email},
        
        We received a request to reset your password. Click the link below to set a new password:
        
        {reset_url}
        
        This link will expire in 1 hour.
        
        If you didn't request a password reset, please ignore this email.
        
        Best regards,
        Book A Court Team
        """
        
        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <div style="max-width: 600px; margin: 0 auto;">
                    <h2>Password Reset - Book A Court</h2>
                    <p>Hello {user.first_name or user.email},</p>
                    <p>We received a request to reset your password. Click the button below to set a new password:</p>
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{reset_url}" style="background-color: #008CBA; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                            Reset Password
                        </a>
                    </div>
                    <p>Or copy this link: <a href="{reset_url}">{reset_url}</a></p>
                    <p><strong>This link will expire in 1 hour.</strong></p>
                    <p>If you didn't request a password reset, please ignore this email.</p>
                    <hr style="margin: 30px 0;">
                    <p style="color: #666; font-size: 12px;">Best regards,<br/>Book A Court Team</p>
                </div>
            </body>
        </html>
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return f"Password reset email sent to {user.email}"
    
    except CustomUser.DoesNotExist:
        return f"User with id {user_id} not found"
    except Exception as e:
        return f"Error sending password reset email: {str(e)}"