from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_email(recipient, subject, message):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient],
        fail_silently=False,
    )


@shared_task
def send_bulk_email(recipient_list, subject, message):
    for recipient, subj, msg in recipient_list:
        send_mail(subj, msg, settings.DEFAULT_FROM_EMAIL, [recipient], fail_silently=False)


@shared_task
def send_otp_email(recipient, otp):
    send_mail(
        "Your OTP Code",
        f"Your OTP code is: {otp}. It expires in 5 minutes.",
        settings.DEFAULT_FROM_EMAIL,
        [recipient],
        fail_silently=False,
    )
