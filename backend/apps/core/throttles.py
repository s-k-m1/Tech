from rest_framework.throttling import SimpleRateThrottle


class LoginRateThrottle(SimpleRateThrottle):
    scope = "login"

    def get_cache_key(self, request, view):
        email = request.data.get("email")
        if not email:
            return None
        return self.cache_format % {"scope": self.scope, "ident": email}


class RegisterRateThrottle(SimpleRateThrottle):
    scope = "register"

    def get_cache_key(self, request, view):
        return self.cache_format % {
            "scope": self.scope,
            "ident": request.META.get("REMOTE_ADDR", ""),
        }


class OTPRateThrottle(SimpleRateThrottle):
    scope = "otp_verify"

    def get_cache_key(self, request, view):
        return self.cache_format % {
            "scope": self.scope,
            "ident": request.META.get("REMOTE_ADDR", ""),
        }


class PasswordResetThrottle(SimpleRateThrottle):
    scope = "password_reset"

    def get_cache_key(self, request, view):
        email = request.data.get("email")
        if not email:
            return None
        return self.cache_format % {"scope": self.scope, "ident": email}
