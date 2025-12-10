from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_order_email(subject, message, recipient_list):
    """
    Send email asynchronously via Celery.
    """
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False
    )
