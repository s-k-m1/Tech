from django.test import TestCase
from apps.core.firewall.waf import WAFEngine
from apps.core.firewall.rate_limiter import RateLimiter
from apps.core.firewall.request_validator import RequestValidator


class WAFEngineTests(TestCase):
    def setUp(self):
        self.waf = WAFEngine()

    def test_sql_injection_detection(self):
        request = self._mock_request(body=b"SELECT * FROM users WHERE id=1")
        result = self.waf.validate_request(request)
        self.assertFalse(result["allowed"])
        self.assertIn("SQL Injection", result["reason"])

    def test_xss_detection(self):
        request = self._mock_request(body=b"<script>alert('xss')</script>")
        result = self.waf.validate_request(request)
        self.assertFalse(result["allowed"])
        self.assertIn("XSS", result["reason"])

    def test_directory_traversal_detection(self):
        request = self._mock_request(body=b"../../../etc/passwd")
        result = self.waf.validate_request(request)
        self.assertFalse(result["allowed"])

    def test_clean_request_passes(self):
        request = self._mock_request(body=b'{"name": "John", "email": "john@test.com"}')
        result = self.waf.validate_request(request)
        self.assertTrue(result["allowed"])

    def _mock_request(self, body=b""):
        class MockRequest:
            method = "POST"
            GET = {}
            POST = {}
            headers = {}
            body = body
        return MockRequest()


class RateLimiterTests(TestCase):
    def setUp(self):
        self.limiter = RateLimiter()

    def test_within_limit(self):
        result = self.limiter.is_rate_limited("test-ip", "test-action", limit=5, period=60)
        self.assertFalse(result)

    def test_remaining_count(self):
        for _ in range(3):
            self.limiter.is_rate_limited("test-ip", "test-action2", limit=5, period=60)
        remaining = self.limiter.get_remaining("test-ip", "test-action2", limit=5, period=60)
        self.assertEqual(remaining, 2)


class RequestValidatorTests(TestCase):
    def setUp(self):
        self.validator = RequestValidator()

    def test_valid_method(self):
        self.assertTrue(self.validator.validate_method("GET"))
        self.assertTrue(self.validator.validate_method("POST"))
        self.assertFalse(self.validator.validate_method("INVALID"))
