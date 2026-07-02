from django.contrib import admin

from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'department', 'credit_hours', 'semester', 'is_active')
    search_fields = ('code', 'title', 'department__name')
    list_filter = ('department', 'is_active', 'semester')
    fields = ('department', 'code', 'title', 'description', 'credit_hours', 'semester', 'is_active')
    ordering = ('department', 'code')
