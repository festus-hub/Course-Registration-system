from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("student/", views.student_dashboard, name="student_dashboard"),
    path("student/profile/", views.student_profile, name="student_profile"),
    path("student/available-courses/", views.available_courses, name="available_courses"),
    path("student/register-courses/", views.register_courses, name="register_courses"),
    path("student/my-registrations/", views.student_registrations, name="student_registrations"),
    path("student/notifications/", views.student_notifications, name="student_notifications"),
    path("student/registration-slip/", views.registration_slip, name="registration_slip"),
    path("student/settings/", views.student_settings, name="student_settings"),
    path("admin/", views.admin_dashboard, name="admin_dashboard"),
]