from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.core.views.project_views import (
    ProjectViewSet, MilestoneViewSet, SprintViewSet,
    TaskViewSet, TaskCommentViewSet,
)

router = DefaultRouter()
router.register(r"projects", ProjectViewSet)
router.register(r"milestones", MilestoneViewSet)
router.register(r"sprints", SprintViewSet)
router.register(r"tasks", TaskViewSet)
router.register(r"task-comments", TaskCommentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
