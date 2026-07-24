from rest_framework import viewsets
from apps.core.models.project import Project, Milestone, Sprint, Task, TaskComment
from apps.core.serializers.project_serializers import (
    ProjectSerializer, MilestoneSerializer, SprintSerializer,
    TaskSerializer, TaskCommentSerializer,
)
from apps.core.permissions import DynamicRBACPermission


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return Project.objects.filter(tenant=self.request.user.tenant)


class MilestoneViewSet(viewsets.ModelViewSet):
    serializer_class = MilestoneSerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return Milestone.objects.filter(project__tenant=self.request.user.tenant)


class SprintViewSet(viewsets.ModelViewSet):
    serializer_class = SprintSerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return Sprint.objects.filter(project__tenant=self.request.user.tenant)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return Task.objects.filter(project__tenant=self.request.user.tenant)


class TaskCommentViewSet(viewsets.ModelViewSet):
    serializer_class = TaskCommentSerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return TaskComment.objects.filter(task__project__tenant=self.request.user.tenant)
