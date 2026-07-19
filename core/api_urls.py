from rest_framework.routers import DefaultRouter
from django.urls import path, include

from departments.api_views import DepartmentViewSet
from courses.api_views import CourseViewSet
from students.api_views import StudentViewSet
from registrations.api_views import CourseRegistrationViewSet

router = DefaultRouter()
router.register('departments', DepartmentViewSet, basename='api-department')
router.register('courses', CourseViewSet, basename='api-course')
router.register('students', StudentViewSet, basename='api-student')
router.register('registrations', CourseRegistrationViewSet, basename='api-registration')

urlpatterns = [
    path('', include(router.urls)),
]