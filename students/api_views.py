from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializer
from core.permissions import IsStaffOnly


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('user', 'department').order_by('student_id')
    serializer_class = StudentSerializer
    permission_classes = [IsStaffOnly]