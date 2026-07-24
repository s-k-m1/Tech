from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from apps.core.models import User, Device
from apps.core.serializers.auth_serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer, DeviceSerializer
)
from apps.core.services.auth_service import AuthService
from apps.core.utils.rate_limit import rate_limit


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"message": "User registered successfully", "user": UserSerializer(user).data},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @rate_limit(key="login", limit=5, period=60)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(request=request, email=email, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        device_data = {
            "device_name": request.data.get("device_name", "Unknown"),
            "device_type": request.data.get("device_type", "web"),
            "ip_address": request.META.get("REMOTE_ADDR", ""),
            "user_agent": request.META.get("HTTP_USER_AGENT", ""),
        }

        auth_service = AuthService()
        result = auth_service.login(user, request, device_data)

        if result.get("requires_2fa"):
            return Response({"requires_2fa": True, "token": result["token"]})

        return Response(result, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        auth_service = AuthService()
        result = auth_service.verify_otp(
            token=request.data.get("token"),
            otp=request.data.get("otp"),
            request=request,
        )
        return Response(result, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        auth_service = AuthService()
        auth_service.logout(request.user, request)
        return Response({"message": "Logged out successfully"})


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class DeviceListView(generics.ListAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return Device.objects.filter(user=self.request.user)


class DeviceDeleteView(generics.DestroyAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return Device.objects.filter(user=self.request.user)
