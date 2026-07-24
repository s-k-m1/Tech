from rest_framework import viewsets
from apps.core.models.crm import Lead, Client, Contract, Meeting
from apps.core.serializers.crm_serializers import (
    LeadSerializer, ClientSerializer, ContractSerializer, MeetingSerializer
)
from apps.core.permissions import DynamicRBACPermission


class LeadViewSet(viewsets.ModelViewSet):
    serializer_class = LeadSerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return Lead.objects.filter(tenant=self.request.user.tenant)


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return Client.objects.filter(tenant=self.request.user.tenant)


class ContractViewSet(viewsets.ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return Contract.objects.filter(tenant=self.request.user.tenant)


class MeetingViewSet(viewsets.ModelViewSet):
    serializer_class = MeetingSerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return Meeting.objects.filter(tenant=self.request.user.tenant)
