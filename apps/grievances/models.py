import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Department(models.Model):
    """
    Department model matching CPGRAMS ministry/department structure.
    """
    org_code = models.CharField(max_length=20, unique=True)
    org_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    default_sla_days = models.IntegerField(default=30)
    daily_capacity = models.IntegerField(default=10, help_text="Officer processing capacity per day")

    def __str__(self):
        return f"{self.org_name} ({self.org_code})"


class OfficerProfile(models.Model):
    """
    Extends standard Django User for Government Officers.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='officer_profile')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='officers')
    designation = models.CharField(max_length=100, default="Nodal Grievance Officer")
    contact_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.department.org_code}"


class CitizenProfile(models.Model):
    """
    Extends standard Django User for Citizens.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='citizen_profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.state or 'N/A'})"


class Grievance(models.Model):
    """
    Core Grievance lifecycle model integrating Full-Stack, ML, Fuzzy Logic, and GA outputs.
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('REJECTED', 'Rejected'),
    ]

    tracking_id = models.CharField(max_length=36, unique=True, default=uuid.uuid4, editable=False)
    citizen = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grievances')
    subject = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)
    submission_date = models.DateTimeField(default=timezone.now)

    predicted_category = models.CharField(max_length=100, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='grievances')
    is_duplicate = models.BooleanField(default=False)
    similar_grievance_id = models.CharField(max_length=36, blank=True, null=True)
    similarity_score = models.FloatField(default=0.0)

    severity_level = models.IntegerField(default=5, help_text="Scale 1-10")
    public_impact = models.IntegerField(default=5, help_text="Scale 1-10")
    fuzzy_priority_score = models.FloatField(default=0.0, help_text="Computed by scikit-fuzzy FIS (0-100)")
    sla_deadline = models.DateTimeField(null=True, blank=True)
    optimized_position = models.IntegerField(default=0, help_text="GA-computed processing queue sequence")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    assigned_officer = models.ForeignKey(OfficerProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_grievances')
    resolution_date = models.DateTimeField(null=True, blank=True)
    resolution_remarks = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.sla_deadline and self.submission_date:
            days = self.department.default_sla_days if self.department else 30
            self.sla_deadline = self.submission_date + timezone.timedelta(days=days)
        super().save(*args, **kwargs)

    @property
    def waiting_time_days(self):
        end_time = self.resolution_date or timezone.now()
        return (end_time - self.submission_date).days

    def __str__(self):
        return f"[{self.tracking_id[:8]}] {self.subject} ({self.status})"


class ActionHistory(models.Model):
    """
    Audit log maintaining officer remarks and status transitions.
    """
    grievance = models.ForeignKey(Grievance, on_delete=models.CASCADE, related_name='action_history')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    previous_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    remarks = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Action on {self.grievance.tracking_id[:8]} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"