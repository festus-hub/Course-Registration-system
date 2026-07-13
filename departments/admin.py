from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Department


@admin.register(Department)
class DepartmentAdmin(ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')
    list_filter = ('created_at',)