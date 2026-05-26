from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email(subject, message, sender_email, recipient_email):
    # Implement your email sending logic here
    # For example, you can use Django's send_mail function
    send_mail(subject, message, from_email=sender_email, recipient_list=[recipient_email])