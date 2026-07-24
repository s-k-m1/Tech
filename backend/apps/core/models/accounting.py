from django.db import models
from django.utils.translation import gettext_lazy as _
from .account import BaseModel, Tenant, User, Branch


class AccountType(BaseModel):
    ACCOUNT_CATEGORY = (
        ("asset", "Asset"),
        ("liability", "Liability"),
        ("equity", "Equity"),
        ("income", "Income"),
        ("expense", "Expense"),
    )

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="account_types")
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=ACCOUNT_CATEGORY)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ["tenant", "name"]
        verbose_name = _("Account Type")
        verbose_name_plural = _("Account Types")

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Account(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="accounts")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True, related_name="accounts")
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE, related_name="accounts")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    opening_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    current_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

    class Meta:
        unique_together = ["tenant", "code"]
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")

    def __str__(self):
        return f"{self.code} - {self.name}"


class JournalEntry(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="journal_entries")
    entry_number = models.CharField(max_length=100, unique=True)
    entry_date = models.DateField()
    description = models.TextField()
    reference_type = models.CharField(max_length=50, blank=True)
    reference_id = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="journal_entries")
    is_posted = models.BooleanField(default=False)
    posted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Journal Entry")
        verbose_name_plural = _("Journal Entries")
        ordering = ["-entry_date", "-created_at"]

    def __str__(self):
        return self.entry_number


class JournalLineItem(BaseModel):
    journal_entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name="line_items")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="line_items")
    description = models.CharField(max_length=255, blank=True)
    debit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    class Meta:
        verbose_name = _("Journal Line Item")
        verbose_name_plural = _("Journal Line Items")


class Transaction(BaseModel):
    TRANSACTION_TYPE = (
        ("payment", "Payment"),
        ("receipt", "Receipt"),
        ("transfer", "Transfer"),
        ("adjustment", "Adjustment"),
    )

    TRANSACTION_STATUS = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    )

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="transactions")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True, related_name="transactions")
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
    transaction_number = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS, default="pending")
    transaction_date = models.DateTimeField(auto_now_add=True)
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="outgoing_transactions", null=True, blank=True)
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="incoming_transactions", null=True, blank=True)
    reference_number = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")
        ordering = ["-transaction_date"]

    def __str__(self):
        return self.transaction_number


class Budget(BaseModel):
    BUDGET_STATUS = (
        ("draft", "Draft"),
        ("approved", "Approved"),
        ("active", "Active"),
        ("closed", "Closed"),
    )

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="budgets")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True, related_name="budgets")
    name = models.CharField(max_length=255)
    fiscal_year = models.IntegerField()
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=BUDGET_STATUS, default="draft")
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")

    class Meta:
        verbose_name = _("Budget")
        verbose_name_plural = _("Budgets")

    def __str__(self):
        return f"{self.name} - FY{self.fiscal_year}"


class BudgetLineItem(BaseModel):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name="line_items")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="budget_items")
    allocated_amount = models.DecimalField(max_digits=15, decimal_places=2)
    spent_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    class Meta:
        verbose_name = _("Budget Line Item")
        verbose_name_plural = _("Budget Line Items")
        unique_together = ["budget", "account"]

    @property
    def remaining(self):
        return self.allocated_amount - self.spent_amount
