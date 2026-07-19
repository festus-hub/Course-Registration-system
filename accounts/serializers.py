from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from students.models import Student

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    """
    Public signup. Always creates a STUDENT account — is_staff is never
    settable here. Mirrors the template-based register_view exactly:
    student_id is auto-generated (STU-0001 pattern), and department is
    left unset at signup — an admin assigns it later via
    /students/manage/<pk>/edit/.
    """
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("That username is already taken.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_staff=False,  
        )
        student = Student.objects.create(
            user=user,
            student_id=f'STU-{user.id:04d}',   
        )
        return student


class RegisterResponseSerializer(serializers.Serializer):
    """Just for documenting the response shape in Swagger."""
    id = serializers.IntegerField()
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    student_id = serializers.CharField()