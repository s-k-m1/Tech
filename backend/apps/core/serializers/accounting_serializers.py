from rest_framework import serializers
from apps.core.models.accounting import (
    AccountType, Account, JournalEntry, JournalLineItem,
    Transaction, Budget, BudgetLineItem,
)


class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = "__all__"
        read_only_fields = ["tenant"]


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"
        read_only_fields = ["tenant", "current_balance"]


class JournalLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalLineItem
        fields = "__all__"


class JournalEntrySerializer(serializers.ModelSerializer):
    line_items = JournalLineItemSerializer(many=True, read_only=True)

    class Meta:
        model = JournalEntry
        fields = "__all__"
        read_only_fields = ["tenant"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = ["tenant"]


class BudgetLineItemSerializer(serializers.ModelSerializer):
    remaining = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = BudgetLineItem
        fields = "__all__"


class BudgetSerializer(serializers.ModelSerializer):
    line_items = BudgetLineItemSerializer(many=True, read_only=True)

    class Meta:
        model = Budget
        fields = "__all__"
        read_only_fields = ["tenant"]
