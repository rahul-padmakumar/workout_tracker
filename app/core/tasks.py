from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email(subject, message, sender_email, recipient_email):
    """Send an email using Django's send_mail helper."""
    print("Sending email...")
    # Implement your email sending logic here. Example using send_mail:
    send_mail(
        subject,
        message,
        from_email=sender_email,
        recipient_list=[recipient_email],
    )
