from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import CourseRegistration
from .serializers import CourseRegistrationSerializer
from students.models import Student


class CourseRegistrationViewSet(viewsets.ModelViewSet):
    """
    Staff: full access to every registration.
    Regular students: can only see and create their OWN registrations.
    A student can never view or modify another student's registration,
    even by guessing an id in the URL — enforced via get_queryset().
    """
    serializer_class = CourseRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = CourseRegistration.objects.select_related('student', 'course')
        if user.is_staff:
            return qs.order_by('-registered_at')
        return qs.filter(student__user=user).order_by('-registered_at')

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_staff:
            serializer.save()
            return

        student = Student.objects.filter(user=user).first()
        if not student:
            raise PermissionDenied("No student profile is linked to your account.")
        serializer.save(student=student)