from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import ChoicesDropdownFilter
from .models import CourseRegistration


@admin.register(CourseRegistration)
class CourseRegistrationAdmin(ModelAdmin):
    list_display = ['student', 'course', 'status', 'registered_at']
    list_filter = [('status', ChoicesDropdownFilter)]
    search_fields = ['student__user__username', 'course__title', 'course__code']
    ordering = ['-registered_at']
    autocomplete_fields = ['student', 'course']