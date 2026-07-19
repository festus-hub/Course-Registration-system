from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Student
        fields = [
            'id', 'user', 'username', 'email', 'student_id',
            'department', 'department_name', 'admission_year', 'is_active',
        ]
        read_only_fields = ['id']