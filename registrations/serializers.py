from rest_framework import serializers
from .models import CourseRegistration


class CourseRegistrationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.username', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = CourseRegistration
        fields = [
            'id', 'student', 'student_name', 'course', 'course_title',
            'course_code', 'status', 'status_display', 'registered_at',
        ]
        read_only_fields = ['id', 'registered_at']