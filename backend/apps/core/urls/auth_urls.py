from django.urls import path
from apps.core.views.auth_views import (
    RegisterView, LoginView, VerifyOTPView, LogoutView,
    ProfileView, DeviceListView, DeviceDeleteView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("verify-otp/", VerifyOTPView.as_view(), name="auth-verify-otp"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
    path("profile/", ProfileView.as_view(), name="auth-profile"),
    path("devices/", DeviceListView.as_view(), name="auth-devices"),
    path("devices/<uuid:pk>/", DeviceDeleteView.as_view(), name="auth-device-delete"),
]
