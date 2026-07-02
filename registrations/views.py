from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import CourseRegistration


@login_required
def registration_list(request):
    registrations = CourseRegistration.objects.select_related('student', 'course').order_by('-registered_at')
    return render(request, 'registrations/list.html', {'registrations': registrations})


@login_required
def update_registration_status(request, pk):
    registration = get_object_or_404(CourseRegistration, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in {'pending', 'approved', 'rejected'}:
            registration.status = status
            registration.save()
        return redirect('registration_list')
    return render(request, 'registrations/update_status.html', {'registration': registration})
