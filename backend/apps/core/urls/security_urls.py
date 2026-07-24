from django.urls import path
from apps.core.views.security_views import SecurityDashboardView, SecurityReportView

urlpatterns = [
    path("dashboard/", SecurityDashboardView.as_view(), name="security-dashboard"),
    path("report/", SecurityReportView.as_view(), name="security-report"),
]
