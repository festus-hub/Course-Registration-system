from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Student


@admin.register(Student)
class StudentAdmin(ModelAdmin):
    list_display = ('student_id', 'user', 'department', 'is_active')
    search_fields = ('student_id', 'user__username', 'department__name')
    list_filter = ('department', 'is_active', 'admission_year')