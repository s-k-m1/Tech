from rest_framework import viewsets
from apps.core.models.erp import (
    Supplier, Warehouse, Category, Product, Inventory,
    PurchaseOrder, Invoice,
)
from apps.core.serializers.erp_serializers import (
    SupplierSerializer, WarehouseSerializer, CategorySerializer,
    ProductSerializer, InventorySerializer, PurchaseOrderSerializer,
    InvoiceSerializer,
)
from apps.core.permissions import DynamicRBACPermission


class SupplierViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierSerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return Supplier.objects.filter(tenant=self.request.user.tenant)


class WarehouseViewSet(viewsets.ModelViewSet):
    serializer_class = WarehouseSerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return Warehouse.objects.filter(tenant=self.request.user.tenant)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return Category.objects.filter(tenant=self.request.user.tenant)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return Product.objects.filter(tenant=self.request.user.tenant)


class InventoryViewSet(viewsets.ModelViewSet):
    serializer_class = InventorySerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return Inventory.objects.filter(product__tenant=self.request.user.tenant)


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseOrderSerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return PurchaseOrder.objects.filter(tenant=self.request.user.tenant)


class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return Invoice.objects.filter(tenant=self.request.user.tenant)
