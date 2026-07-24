from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.microsoft.views import MicrosoftOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialAccount
from allauth.account.utils import complete_social_login
from allauth.socialaccount.helpers import SocialLogin
from django.contrib.auth import get_user_model
from apps.core.tasks.notification_tasks import send_social_login_welcome

User = get_user_model()


class SocialLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, provider):
        code = request.data.get("code")
        redirect_uri = request.data.get("redirect_uri")

        if not code or not redirect_uri:
            return Response({"error": "code and redirect_uri required"}, status=status.HTTP_400_BAD_REQUEST)

        providers = {
            "google": (GoogleOAuth2Adapter, "google"),
            "github": (GitHubOAuth2Adapter, "github"),
            "microsoft": (MicrosoftOAuth2Adapter, "microsoft"),
        }

        if provider not in providers:
            return Response({"error": f"Unsupported provider: {provider}"}, status=status.HTTP_400_BAD_REQUEST)

        adapter_cls, provider_id = providers[provider]
        adapter = adapter_cls(request)
        client = OAuth2Client(
            request, adapter.client_id, adapter.secret,
            adapter.access_token_url, adapter.authorize_url, redirect_uri,
        )

        try:
            access_token = client.get_access_token(code)
            login = adapter.complete_login(request, access_token.token)
            login.state = SocialLogin.state_from_request(request)

            complete_social_login(request, login)

            user = login.user
            user.is_verified = True
            user.save(update_fields=["is_verified"])

            refresh = RefreshToken.for_user(user)
            send_social_login_welcome.delay(user.email, provider)

            return Response({
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "username": user.username,
                    "user_type": user.user_type,
                },
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GoogleLoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
        adapter = GoogleOAuth2Adapter(request)
        return Response({
            "authorize_url": adapter.authorize_url,
            "client_id": adapter.client_id,
        })


class GitHubLoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
        adapter = GitHubOAuth2Adapter(request)
        return Response({
            "authorize_url": adapter.authorize_url,
            "client_id": adapter.client_id,
        })


class MicrosoftLoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        from allauth.socialaccount.providers.microsoft.views import MicrosoftOAuth2Adapter
        adapter = MicrosoftOAuth2Adapter(request)
        return Response({
            "authorize_url": adapter.authorize_url,
            "client_id": adapter.client_id,
        })
