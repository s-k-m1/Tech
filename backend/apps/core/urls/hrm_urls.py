from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.core.views.hrm_views import EmployeeViewSet, AttendanceViewSet, LeaveViewSet, PayrollViewSet

router = DefaultRouter()
router.register(r"employees", EmployeeViewSet)
router.register(r"attendance", AttendanceViewSet)
router.register(r"leaves", LeaveViewSet)
router.register(r"payroll", PayrollViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
