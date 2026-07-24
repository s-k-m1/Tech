from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from apps.core.models import User
from apps.core.serializers.email_serializers import EmailVerificationSerializer, ResendVerificationSerializer
from apps.core.tasks.notification_tasks import send_verification_email


class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["token"]

        try:
            uidb64 = request.query_params.get("uid")
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, User.DoesNotExist):
            return Response({"error": "Invalid verification link"}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_verified = True
            user.save(update_fields=["is_verified"])
            return Response({"message": "Email verified successfully"})

        return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResendVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
            if user.is_verified:
                return Response({"message": "Email already verified"})
            send_verification_email.delay(user.email, user.id)
        except User.DoesNotExist:
            pass

        return Response({"message": "Verification email sent if account exists"})
