from rest_framework import viewsets
from apps.core.models.accounting import (
    AccountType, Account, JournalEntry, Transaction, Budget,
)
from apps.core.serializers.accounting_serializers import (
    AccountTypeSerializer, AccountSerializer, JournalEntrySerializer,
    TransactionSerializer, BudgetSerializer,
)
from apps.core.permissions import DynamicRBACPermission


class AccountTypeViewSet(viewsets.ModelViewSet):
    serializer_class = AccountTypeSerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return AccountType.objects.filter(tenant=self.request.user.tenant)


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return Account.objects.filter(tenant=self.request.user.tenant)


class JournalEntryViewSet(viewsets.ModelViewSet):
    serializer_class = JournalEntrySerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return JournalEntry.objects.filter(tenant=self.request.user.tenant)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return Transaction.objects.filter(tenant=self.request.user.tenant)


class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return Budget.objects.filter(tenant=self.request.user.tenant)
