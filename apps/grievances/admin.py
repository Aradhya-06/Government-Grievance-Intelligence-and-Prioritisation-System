from django.contrib import admin
from .models import Department, OfficerProfile, CitizenProfile, Grievance, ActionHistory


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('org_code', 'org_name', 'default_sla_days', 'daily_capacity')
    search_fields = ('org_code', 'org_name')


@admin.register(OfficerProfile)
class OfficerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'designation', 'contact_number')
    list_filter = ('department',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')


@admin.register(CitizenProfile)
class CitizenProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'state', 'district', 'phone_number')
    search_fields = ('user__username', 'state', 'district')


class ActionHistoryInline(admin.TabularInline):
    model = ActionHistory
    extra = 0
    readonly_fields = ('updated_by', 'previous_status', 'new_status', 'remarks', 'timestamp')


@admin.register(Grievance)
class GrievanceAdmin(admin.ModelAdmin):
    list_display = ('tracking_id', 'subject', 'department', 'status', 'fuzzy_priority_score', 'optimized_position', 'submission_date')
    list_filter = ('status', 'department', 'predicted_category', 'is_duplicate')
    search_fields = ('tracking_id', 'subject', 'description')
    readonly_fields = ('tracking_id', 'submission_date', 'waiting_time_days')
    inlines = [ActionHistoryInline]