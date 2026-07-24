from rest_framework import viewsets
from apps.core.models.ticket import Ticket, TicketComment
from apps.core.serializers.ticket_serializers import TicketSerializer, TicketCommentSerializer
from apps.core.permissions import DynamicRBACPermission


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return Ticket.objects.filter(tenant=self.request.user.tenant)


class TicketCommentViewSet(viewsets.ModelViewSet):
    serializer_class = TicketCommentSerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return TicketComment.objects.filter(ticket__tenant=self.request.user.tenant)
