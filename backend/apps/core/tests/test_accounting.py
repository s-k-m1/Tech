from django.test import TestCase
from apps.core.models import Tenant
from apps.core.models.accounting import AccountType, Account


class AccountingModelTests(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(
            name="Acct Corp", slug="acct-corp", contact_email="acct@test.com"
        )

    def test_account_type_creation(self):
        acc_type = AccountType.objects.create(
            tenant=self.tenant, name="Cash", category="asset"
        )
        self.assertIn("Cash", str(acc_type))

    def test_account_creation(self):
        acc_type = AccountType.objects.create(
            tenant=self.tenant, name="Cash", category="asset"
        )
        account = Account.objects.create(
            tenant=self.tenant,
            account_type=acc_type,
            name="Petty Cash",
            code="1001",
            opening_balance=5000,
            current_balance=5000,
        )
        self.assertEqual(str(account), "1001 - Petty Cash")
