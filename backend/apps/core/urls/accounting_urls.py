from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.core.views.accounting_views import (
    AccountTypeViewSet, AccountViewSet, JournalEntryViewSet,
    TransactionViewSet, BudgetViewSet,
)

router = DefaultRouter()
router.register(r"account-types", AccountTypeViewSet)
router.register(r"accounts", AccountViewSet)
router.register(r"journal-entries", JournalEntryViewSet)
router.register(r"transactions", TransactionViewSet)
router.register(r"budgets", BudgetViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
