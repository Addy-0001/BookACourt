from django.conf import settings
from twilio.rest import Client


def send_otp_sms(phone_number, otp_code):
    """
    Send OTP code via SMS using Twilio

    Args:
        phone_number: Phone number in international format
        otp_code: 6-digit OTP code
    """
    if not all([
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN,
        settings.TWILIO_PHONE_NUMBER
    ]):
        # If Twilio is not configured, just log the OTP
        print(f"OTP for {phone_number}: {otp_code}")
        return True

    try:
        client = Client(settings.TWILIO_ACCOUNT_SID,
                        settings.TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=f"Your BookACourt verification code is: {otp_code}. Valid for 5 minutes.",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=str(phone_number)
        )

        return message.sid
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")
        return False


def send_welcome_sms(phone_number, full_name):
    """
    Send welcome SMS to new user

    Args:
        phone_number: Phone number in international format
        full_name: User's full name
    """
    if not all([
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN,
        settings.TWILIO_PHONE_NUMBER
    ]):
        print(f"Welcome message for {phone_number}")
        return True

    try:
        client = Client(settings.TWILIO_ACCOUNT_SID,
                        settings.TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=f"Welcome to BookACourt, {full_name}! Start booking your favorite courts now.",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=str(phone_number)
        )

        return message.sid
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")
        return False
