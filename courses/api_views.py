from rest_framework import viewsets
from .models import Course
from .serializers import CourseSerializer
from core.permissions import IsStaffOrReadOnly


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related('department').order_by('code')
    serializer_class = CourseSerializer
    permission_classes = [IsStaffOrReadOnly]