from django.urls import path
from apps.core.views.social_auth_views import (
    GoogleLoginAPIView, GitHubLoginAPIView, MicrosoftLoginAPIView,
    SocialLoginView,
)

urlpatterns = [
    path("google/", GoogleLoginAPIView.as_view(), name="google-auth"),
    path("github/", GitHubLoginAPIView.as_view(), name="github-auth"),
    path("microsoft/", MicrosoftLoginAPIView.as_view(), name="microsoft-auth"),
    path("callback/<str:provider>/", SocialLoginView.as_view(), name="social-auth-callback"),
]
