from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.core.views.crm_views import LeadViewSet, ClientViewSet, ContractViewSet, MeetingViewSet

router = DefaultRouter()
router.register(r"leads", LeadViewSet)
router.register(r"clients", ClientViewSet)
router.register(r"contracts", ContractViewSet)
router.register(r"meetings", MeetingViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
