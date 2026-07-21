from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import Department
from .forms import DepartmentForm


@staff_member_required
def department_list(request):
    departments = Department.objects.all().order_by('name')
    return render(request, 'departments/list.html', {'departments': departments})


@staff_member_required
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully.')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'departments/form.html', {'form': form, 'is_edit': False})


@staff_member_required
def department_edit(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully.')
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'departments/form.html', {'form': form, 'is_edit': True, 'department': department})


@staff_member_required
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Department removed successfully.')
        return redirect('department_list')
    return render(request, 'departments/confirm_delete.html', {'department': department})