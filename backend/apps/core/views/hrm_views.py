from rest_framework import viewsets
from apps.core.models.hrm import Employee, Attendance, Leave, Payroll
from apps.core.serializers.hrm_serializers import (
    EmployeeSerializer, AttendanceSerializer, LeaveSerializer, PayrollSerializer
)
from apps.core.permissions import DynamicRBACPermission


class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return Employee.objects.filter(tenant=self.request.user.tenant)


class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return Attendance.objects.filter(employee__tenant=self.request.user.tenant)


class LeaveViewSet(viewsets.ModelViewSet):
    serializer_class = LeaveSerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return Leave.objects.filter(employee__tenant=self.request.user.tenant)


class PayrollViewSet(viewsets.ModelViewSet):
    serializer_class = PayrollSerializer
    permission_classes = [DynamicRBACPermission]

    def get_queryset(self):
        return Payroll.objects.filter(employee__tenant=self.request.user.tenant)
