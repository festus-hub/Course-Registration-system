from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Course
from .forms import CourseForm


#STUDENTS 

@login_required
def course_list(request):
    courses = Course.objects.filter(is_active=True).order_by('code')
    return render(request, 'courses/course_list.html', {'courses': courses})


@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course})


#ADMIN/STAFF

@staff_member_required
def course_manage_list(request):
    courses = Course.objects.select_related('department').order_by('department__name', 'code')

    department_id = request.GET.get('department')
    if department_id:
        courses = courses.filter(department_id=department_id)

    from departments.models import Department
    departments = Department.objects.all().order_by('name')

    return render(request, 'courses/manage/list.html', {
        'courses': courses,
        'departments': departments,
        'selected_department': department_id,
    })


@staff_member_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course created successfully.')
            return redirect('course_manage_list')
    else:
        form = CourseForm()
    return render(request, 'courses/manage/form.html', {'form': form, 'is_edit': False})


@staff_member_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully.')
            return redirect('course_manage_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/manage/form.html', {'form': form, 'is_edit': True, 'course': course})


@staff_member_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course removed successfully.')
        return redirect('course_manage_list')
    return render(request, 'courses/manage/confirm_delete.html', {'course': course})