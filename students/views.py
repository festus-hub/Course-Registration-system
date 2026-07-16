from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from courses.models import Course
from registrations.models import CourseRegistration
from students.models import Student
from .forms import StudentForm


@login_required
def students_dashboard(request):
    student = Student.objects.filter(user=request.user).first()
    registrations = CourseRegistration.objects.filter(student=student).select_related('course') if student else []
    pending_count = registrations.filter(status='pending').count() if student else 0

    context = {
        'student': student,
        'registrations': registrations,
        'pending_count': pending_count,
    }
    return render(request, 'students/dashboard.html', context)


@login_required
def student_profile_view(request):
    student = Student.objects.filter(user=request.user).first()
    return render(request, 'students/profile.html', {'student': student})


@login_required
def student_courses_view(request):
    student = Student.objects.filter(user=request.user).first()
    registrations = CourseRegistration.objects.filter(student=student).values_list('course_id', flat=True)
    courses = Course.objects.filter(is_active=True).order_by('code')
    return render(request, 'students/courses.html', {
        'student': student,
        'courses': courses,
        'registered_course_ids': list(registrations),
    })


@login_required
def register_course_view(request):
    student = Student.objects.filter(user=request.user).first()
    if not student:
        messages.error(request, 'No student profile was found for your account.')
        return redirect('students_dashboard')

    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Course, pk=course_id, is_active=True)
        registration, created = CourseRegistration.objects.get_or_create(student=student, course=course)
        if created:
            messages.success(request, f'{course.title} was added to your registrations.')
        else:
            messages.info(request, f'You are already registered for {course.title}.')
        return redirect('register_course')

    return redirect('student_courses')


@login_required
def student_registrations_view(request):
    student = Student.objects.filter(user=request.user).first()
    registrations = CourseRegistration.objects.filter(student=student).select_related('course') if student else []
    return render(request, 'students/registrations.html', {
        'student': student,
        'registrations': registrations,
    })


@staff_member_required
def student_list(request):
    students = Student.objects.select_related('user', 'department').order_by('student_id')

    department_id = request.GET.get('department')
    if department_id:
        students = students.filter(department_id=department_id)

    from departments.models import Department
    departments = Department.objects.all().order_by('name')

    return render(request, 'students/manage/list.html', {
        'students': students,
        'departments': departments,
        'selected_department': department_id,
    })


@staff_member_required
def student_detail(request, pk):
    student = get_object_or_404(Student.objects.select_related('user', 'department'), pk=pk)
    registrations = student.registrations.select_related('course').order_by('-registered_at')
    return render(request, 'students/manage/detail.html', {
        'student': student,
        'registrations': registrations,
    })


@staff_member_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student created successfully.')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/manage/form.html', {'form': form, 'is_edit': False})


@staff_member_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/manage/form.html', {'form': form, 'is_edit': True, 'student': student})


@staff_member_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student removed successfully.')
        return redirect('student_list')
    return render(request, 'students/manage/confirm_delete.html', {'student': student})