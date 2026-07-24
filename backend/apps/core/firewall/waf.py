import re
from apps.core.firewall.request_validator import RequestValidator


class WAFEngine:
    def __init__(self):
        self.validator = RequestValidator()
        self.blocked_patterns = [
            (r"(\b(union|select|insert|drop|delete|update|alter|exec|eval)\b.*\b(from|into|set|where)\b)", "SQL Injection"),
            (r"<script.*?>.*?</script>", "XSS"),
            (r"on\w+\s*=", "XSS Event Handler"),
            (r"javascript:", "XSS Protocol"),
            (r"\.\./", "Directory Traversal"),
            (r"\.\.\\", "Directory Traversal (Windows)"),
            (r"/etc/passwd", "File Inclusion"),
            (r"php://", "PHP Wrapper"),
        ]

    def validate_request(self, request):
        if not self.validator.validate_method(request.method):
            return {"allowed": False, "reason": "HTTP method not allowed", "attack_type": "invalid_method"}

        for pattern, attack_type in self.blocked_patterns:
            if request.body:
                if re.search(pattern, request.body.decode("utf-8", errors="ignore"), re.IGNORECASE):
                    return {"allowed": False, "reason": f"Blocked: {attack_type} detected in body", "attack_type": attack_type}

            for key, value in request.GET.items():
                if re.search(pattern, str(value), re.IGNORECASE):
                    return {"allowed": False, "reason": f"Blocked: {attack_type} detected in query param {key}", "attack_type": attack_type}

            for key, value in request.POST.items():
                if re.search(pattern, str(value), re.IGNORECASE):
                    return {"allowed": False, "reason": f"Blocked: {attack_type} detected in form data {key}", "attack_type": attack_type}

            for key, value in request.headers.items():
                if re.search(pattern, str(value), re.IGNORECASE):
                    return {"allowed": False, "reason": f"Blocked: {attack_type} detected in header {key}", "attack_type": attack_type}

        if not self.validator.validate_content_type(request):
            return {"allowed": False, "reason": "Content-Type not allowed", "attack_type": "invalid_content_type"}

        if not self.validator.validate_file_upload(request):
            return {"allowed": False, "reason": "File upload validation failed", "attack_type": "malicious_upload"}

        return {"allowed": True, "attack_type": None}
