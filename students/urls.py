from django.urls import path

from .views import (
    register_course_view,
    student_courses_view,
    student_profile_view,
    student_registrations_view,
    students_dashboard,
)

urlpatterns = [
    path('', students_dashboard, name='students_dashboard'),
    path('profile/', student_profile_view, name='student_profile_view'),
    path('courses/', student_courses_view, name='student_courses'),
    path('register/', register_course_view, name='register_course'),
    path('registrations/', student_registrations_view, name='student_registrations_view'),
]
