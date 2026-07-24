from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.core.services.security_ai_service import SecurityAIService
from apps.core.permissions import DynamicRBACPermission


class SecurityDashboardView(APIView):
    permission_classes = [DynamicRBACPermission]

    def get(self, request):
        service = SecurityAIService()
        dashboard_data = service.get_dashboard_data(request.user.tenant)
        return Response(dashboard_data)


class SecurityReportView(APIView):
    permission_classes = [DynamicRBACPermission]

    def get(self, request):
        service = SecurityAIService()
        report = service.generate_report(request.user.tenant)
        return Response(report)
