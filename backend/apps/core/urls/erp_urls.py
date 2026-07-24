from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.core.views.erp_views import (
    SupplierViewSet, WarehouseViewSet, CategoryViewSet,
    ProductViewSet, InventoryViewSet, PurchaseOrderViewSet,
    InvoiceViewSet,
)

router = DefaultRouter()
router.register(r"suppliers", SupplierViewSet)
router.register(r"warehouses", WarehouseViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"products", ProductViewSet)
router.register(r"inventory", InventoryViewSet)
router.register(r"purchase-orders", PurchaseOrderViewSet)
router.register(r"invoices", InvoiceViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
