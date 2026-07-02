from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from courses.models import Course
from departments.models import Department
from registrations.models import CourseRegistration
from students.models import Student


def get_student(request):
    return Student.objects.filter(user=request.user).first()


@login_required
def dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin_dashboard')
    return redirect('student_dashboard')


@login_required
def student_dashboard(request):
    student = get_student(request)
    registrations = CourseRegistration.objects.filter(student=student).select_related('course') if student else []
    courses = Course.objects.filter(is_active=True)
    pending = registrations.filter(status='pending').count() if student else 0
    context = {
        'student': student,
        'registrations': registrations,
        'courses': courses,
        'pending_count': pending,
    }
    return render(request, "dashboard/student_dashboard.html", context)


@login_required
def student_profile(request):
    student = get_student(request)
    return render(request, "dashboard/student_profile.html", {'student': student})


@login_required
def available_courses(request):
    student = get_student(request)
    registrations = CourseRegistration.objects.filter(student=student)
    registered_course_ids = registrations.values_list('course_id', flat=True)
    courses = Course.objects.filter(is_active=True).order_by('code')
    return render(request, "dashboard/available_courses.html", {
        'student': student,
        'courses': courses,
        'registered_course_ids': registered_course_ids,
    })


@login_required
def register_courses(request):
    student = get_student(request)
    if not student:
        messages.error(request, "No student profile was found for your account.")
        return redirect('student_dashboard')

    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Course, pk=course_id, is_active=True)
        registration, created = CourseRegistration.objects.get_or_create(student=student, course=course)
        if created:
            messages.success(request, f"{course.title} has been added to your registrations.")
        else:
            messages.info(request, f"You are already registered for {course.title}.")
        return redirect('register_courses')

    registrations = CourseRegistration.objects.filter(student=student)
    registered_course_ids = registrations.values_list('course_id', flat=True)
    courses = Course.objects.filter(is_active=True).order_by('code')
    return render(request, "dashboard/register_courses.html", {
        'student': student,
        'courses': courses,
        'registered_course_ids': registered_course_ids,
    })


@login_required
def student_registrations(request):
    student = get_student(request)
    registrations = CourseRegistration.objects.filter(student=student).select_related('course')
    return render(request, "dashboard/my_registrations.html", {
        'student': student,
        'registrations': registrations,
    })


@login_required
def student_notifications(request):
    notifications = [
        {"title": "Registration Window Open", "message": "You can now register courses for the upcoming semester."},
        {"title": "Status Update", "message": "One or more of your course registrations has been approved."},
    ]
    return render(request, "dashboard/notifications.html", {
        'notifications': notifications,
    })


@login_required
def registration_slip(request):
    student = get_student(request)
    registrations = CourseRegistration.objects.filter(student=student).select_related('course')
    total_units = sum(reg.course.credit_hours for reg in registrations)
    return render(request, "dashboard/registration_slip.html", {
        'student': student,
        'registrations': registrations,
        'total_units': total_units,
    })


@login_required
def student_settings(request):
    student = get_student(request)
    return render(request, "dashboard/settings.html", {'student': student})


@login_required
def admin_dashboard(request):
    total_students = Student.objects.count()
    total_courses = Course.objects.count()
    total_departments = Department.objects.count()
    registrations = CourseRegistration.objects.select_related('student', 'course').order_by('-registered_at')[:10]
    pending_registrations = CourseRegistration.objects.filter(status='pending').count()

    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_departments': total_departments,
        'registrations': registrations,
        'pending_registrations': pending_registrations,
    }
    return render(request, "dashboard/admin_dashboard.html", context)