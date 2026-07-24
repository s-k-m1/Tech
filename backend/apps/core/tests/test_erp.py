from django.test import TestCase
from apps.core.models import Tenant
from apps.core.models.erp import Supplier, Warehouse, Category, Product


class ERPModelTests(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(
            name="ERP Corp", slug="erp-corp", contact_email="erp@test.com"
        )

    def test_supplier_creation(self):
        supplier = Supplier.objects.create(
            tenant=self.tenant, name="ACME Supplies", email="acme@test.com"
        )
        self.assertEqual(str(supplier), "ACME Supplies")

    def test_warehouse_creation(self):
        from apps.core.models import Branch
        branch = Branch.objects.create(tenant=self.tenant, name="HQ", code="HQ")
        warehouse = Warehouse.objects.create(
            tenant=self.tenant, branch=branch, name="Main Warehouse", code="MW01"
        )
        self.assertEqual(str(warehouse), "Main Warehouse (MW01)")

    def test_category_creation(self):
        category = Category.objects.create(
            tenant=self.tenant, name="Electronics"
        )
        self.assertEqual(str(category), "Electronics")

    def test_product_creation(self):
        product = Product.objects.create(
            tenant=self.tenant,
            name="Laptop",
            sku="LAP-001",
            purchase_price=800,
            selling_price=1200,
        )
        self.assertEqual(str(product), "Laptop (LAP-001)")
