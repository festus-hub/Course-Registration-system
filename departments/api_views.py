from rest_framework import viewsets
from .models import Department
from .serializers import DepartmentSerializer
from core.permissions import IsStaffOrReadOnly   


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all().order_by('name')
    serializer_class = DepartmentSerializer
    permission_classes = [IsStaffOrReadOnly]