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
def send_bulk_email(emails):
    for recipient, subj, msg in emails:
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


@shared_task
def send_verification_email(recipient, user_id):
    from django.utils.http import urlsafe_base64_encode
    from django.utils.encoding import force_bytes
    from django.contrib.auth.tokens import default_token_generator

    uid = urlsafe_base64_encode(force_bytes(user_id))
    token = default_token_generator.make_token(user_id)
    verification_url = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}/"

    send_mail(
        "Verify Your Email",
        f"Click the link to verify your email: {verification_url}",
        settings.DEFAULT_FROM_EMAIL,
        [recipient],
        fail_silently=False,
    )


@shared_task
def send_social_login_welcome(recipient, provider):
    send_mail(
        "Welcome - Social Login",
        f"You have successfully signed in with {provider}.",
        settings.DEFAULT_FROM_EMAIL,
        [recipient],
        fail_silently=False,
    )
