from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'department', 'department_name', 'code', 'title',
            'description', 'credit_hours', 'semester', 'is_active',
        ]
        read_only_fields = ['id']