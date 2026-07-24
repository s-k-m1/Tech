from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.core.views.ticket_views import TicketViewSet, TicketCommentViewSet

router = DefaultRouter()
router.register(r"tickets", TicketViewSet)
router.register(r"comments", TicketCommentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
