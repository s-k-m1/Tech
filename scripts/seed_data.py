import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
django.setup()

from apps.core.models import Tenant, User, Role, Branch, Department


def seed():
    tenant = Tenant.objects.create(
        name="Demo Corp",
        slug="demo",
        contact_email="admin@demo.com",
        subscription_plan="enterprise",
    )

    branch = Branch.objects.create(
        tenant=tenant,
        name="Head Office",
        code="HQ",
        is_head_office=True,
    )

    dept = Department.objects.create(
        tenant=tenant,
        branch=branch,
        name="Engineering",
        code="ENG",
    )

    admin = User.objects.create_superuser(
        email="admin@sktech.io",
        username="admin",
        password="Admin@123",
        tenant=tenant,
        user_type="superadmin",
        is_verified=True,
    )
    admin.branches.add(branch)
    admin.departments.add(dept)

    role = Role.objects.create(
        tenant=tenant,
        name="Admin",
        slug="admin",
        permissions={
            "allowed": ["*"],
            "denied": [],
        },
        is_system=True,
    )

    print("Seed data created successfully!")


if __name__ == "__main__":
    seed()
