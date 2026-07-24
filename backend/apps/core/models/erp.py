from django.db import models
from django.utils.translation import gettext_lazy as _
from .account import BaseModel, Tenant, User, Branch


class Supplier(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="suppliers")
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    tax_id = models.CharField(max_length=100, blank=True)
    payment_terms = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")

    def __str__(self):
        return self.name


class Warehouse(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="warehouses")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="warehouses")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ["tenant", "code"]
        verbose_name = _("Warehouse")
        verbose_name_plural = _("Warehouses")

    def __str__(self):
        return f"{self.name} ({self.code})"


class Category(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ["tenant", "name"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Product(BaseModel):
    PRODUCT_TYPE = (
        ("raw_material", "Raw Material"),
        ("finished_good", "Finished Good"),
        ("service", "Service"),
    )

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE, default="finished_good")
    unit = models.CharField(max_length=50, default="pcs")
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    min_stock_level = models.IntegerField(default=0)
    max_stock_level = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to="products/", blank=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return f"{self.name} ({self.sku})"


class Inventory(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="inventory")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="inventory")
    quantity = models.IntegerField(default=0)
    reserved_quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ["product", "warehouse"]
        verbose_name = _("Inventory")
        verbose_name_plural = _("Inventories")

    @property
    def available_quantity(self):
        return self.quantity - self.reserved_quantity


class PurchaseOrder(BaseModel):
    PURCHASE_STATUS = (
        ("draft", "Draft"),
        ("pending", "Pending Approval"),
        ("approved", "Approved"),
        ("shipped", "Shipped"),
        ("received", "Received"),
        ("cancelled", "Cancelled"),
    )

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="purchase_orders")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="purchase_orders")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="purchase_orders")
    order_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=PURCHASE_STATUS, default="draft")
    order_date = models.DateField(auto_now_add=True)
    expected_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    tax_total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchase_orders")

    class Meta:
        verbose_name = _("Purchase Order")
        verbose_name_plural = _("Purchase Orders")

    def __str__(self):
        return self.order_number


class PurchaseOrderItem(BaseModel):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = _("Purchase Order Item")
        verbose_name_plural = _("Purchase Order Items")


class Invoice(BaseModel):
    INVOICE_TYPE = (
        ("sale", "Sale"),
        ("purchase", "Purchase"),
        ("credit_note", "Credit Note"),
        ("debit_note", "Debit Note"),
    )

    INVOICE_STATUS = (
        ("draft", "Draft"),
        ("sent", "Sent"),
        ("paid", "Paid"),
        ("overdue", "Overdue"),
        ("cancelled", "Cancelled"),
    )

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="invoices")
    invoice_number = models.CharField(max_length=100, unique=True)
    invoice_type = models.CharField(max_length=20, choices=INVOICE_TYPE, default="sale")
    status = models.CharField(max_length=20, choices=INVOICE_STATUS, default="draft")
    issue_date = models.DateField()
    due_date = models.DateField()
    client_name = models.CharField(max_length=255, blank=True)
    client_email = models.EmailField(blank=True)
    client_address = models.TextField(blank=True)
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    tax_total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invoices")

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")

    def __str__(self):
        return self.invoice_number

    @property
    def balance_due(self):
        return self.grand_total - self.paid_amount


class InvoiceItem(BaseModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = _("Invoice Item")
        verbose_name_plural = _("Invoice Items")
