from django.test import TestCase
from apps.core.models import Tenant, User, Branch, Department, Role


class AccountModelTests(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(
            name="Test Corp", slug="test-corp", contact_email="test@test.com"
        )

    def test_tenant_creation(self):
        self.assertEqual(str(self.tenant), "Test Corp")
        self.assertEqual(self.tenant.slug, "test-corp")

    def test_user_creation(self):
        user = User.objects.create_user(
            email="user@test.com",
            username="testuser",
            password="Test@123",
            tenant=self.tenant,
            user_type="employee",
        )
        self.assertEqual(user.email, "user@test.com")
        self.assertTrue(user.check_password("Test@123"))

    def test_branch_creation(self):
        branch = Branch.objects.create(
            tenant=self.tenant, name="HQ", code="HQ001"
        )
        self.assertEqual(str(branch), "Test Corp - HQ")

    def test_department_creation(self):
        branch = Branch.objects.create(tenant=self.tenant, name="HQ", code="HQ001")
        dept = Department.objects.create(
            tenant=self.tenant, branch=branch, name="Engineering", code="ENG"
        )
        self.assertEqual(str(dept), "HQ - Engineering")

    def test_role_creation(self):
        role = Role.objects.create(
            tenant=self.tenant,
            name="Admin",
            slug="admin",
            permissions={"allowed": ["*"], "denied": []},
        )
        self.assertEqual(str(role), "Admin")
