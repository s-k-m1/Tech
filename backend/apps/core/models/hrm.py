from django.db import models
from django.utils.translation import gettext_lazy as _
from .account import BaseModel, Tenant, User, Branch, Department


class Employee(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee_profile")
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="employees")
    employee_id = models.CharField(max_length=50)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.CharField(max_length=255)
    joining_date = models.DateField()
    salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)
    documents = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ["tenant", "employee_id"]
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")


class Attendance(BaseModel):
    ATTENDANCE_STATUS = (
        ("present", "Present"),
        ("absent", "Absent"),
        ("late", "Late"),
        ("half_day", "Half Day"),
        ("leave", "On Leave"),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendance")
    date = models.DateField()
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS, default="present")
    notes = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        unique_together = ["employee", "date"]
        verbose_name = _("Attendance")
        verbose_name_plural = _("Attendances")


class Leave(BaseModel):
    LEAVE_TYPE = (
        ("annual", "Annual"),
        ("sick", "Sick"),
        ("personal", "Personal"),
        ("maternity", "Maternity"),
        ("paternity", "Paternity"),
        ("unpaid", "Unpaid"),
    )

    LEAVE_STATUS = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("cancelled", "Cancelled"),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="leaves")
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=LEAVE_STATUS, default="pending")
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Leave")
        verbose_name_plural = _("Leaves")


class Payroll(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="payrolls")
    month = models.IntegerField()
    year = models.IntegerField()
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2)
    allowances = models.JSONField(default=dict, blank=True)
    deductions = models.JSONField(default=dict, blank=True)
    net_salary = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ["employee", "month", "year"]
        verbose_name = _("Payroll")
        verbose_name_plural = _("Payrolls")
