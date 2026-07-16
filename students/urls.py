from django.urls import path

from .views import (
    register_course_view,
    student_courses_view,
    student_create,
    student_delete,
    student_detail,
    student_edit,
    student_list,
    student_profile_view,
    student_registrations_view,
    students_dashboard,
)

urlpatterns = [
    # --- Student self-service (unchanged from your original) ---
    path('', students_dashboard, name='students_dashboard'),
    path('profile/', student_profile_view, name='student_profile_view'),
    path('courses/', student_courses_view, name='student_courses'),
    path('register/', register_course_view, name='register_course'),
    path('registrations/', student_registrations_view, name='student_registrations_view'),

    # --- Admin student management (new, staff-only) ---
    path('manage/', student_list, name='student_list'),
    path('manage/create/', student_create, name='student_create'),
    path('manage/<int:pk>/', student_detail, name='student_detail'),
    path('manage/<int:pk>/edit/', student_edit, name='student_edit'),
    path('manage/<int:pk>/delete/', student_delete, name='student_delete'),
]