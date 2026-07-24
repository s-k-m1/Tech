from rest_framework import viewsets, mixins
from apps.core.models.notification import Notification
from apps.core.serializers.notification_serializers import NotificationSerializer
from apps.core.permissions import DynamicRBACPermission


class NotificationViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    def perform_update(self, serializer):
        serializer.save(is_read=True, read_at=timezone.now())
