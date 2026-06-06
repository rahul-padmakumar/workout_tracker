from celery import shared_task
from django.core.mail import send_mail
import os


@shared_task(priority=0)
def send_otp(otp_value, recipient_email):
    """Send an email using Django's send_mail helper."""
    print("Sending email...")
    # Implement your email sending logic here. Example using send_mail:
    send_mail(
        "Your OTP Code",
        f"Your OTP code is: {otp_value}",
        from_email=os.environ.get("EMAIL_HOST_USER"),
        recipient_list=[recipient_email],
    )


@shared_task(priority=1)
def send_password_reset_email(reset_link, recipient_email):
    """Send a password reset email."""
    # Implement your password reset email sending logic here.
    print(f"Sending password reset email to {recipient_email}...")
    # Example: send_mail(subject, message, from_email, recipient_list)
    send_mail(
        "Password Reset Request",
        (f"Click the link to reset your password: {reset_link}"),
        from_email=os.environ.get("EMAIL_HOST_USER"),
        recipient_list=[recipient_email],
    )
