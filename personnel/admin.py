from django.contrib import admin
from .models import Employee, EmployeeWorkInfo


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'remaining_leave_days', 'is_active')
    list_filter = ['is_active']
    search_fields = ('user', 'email')


@admin.register(EmployeeWorkInfo)
class EmployeeWorkAdmin(admin.ModelAdmin):
    list_display = ('employee', 'is_active')
    list_filter = ['is_active']
