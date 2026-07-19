from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from .models import CourseRegistration
from .forms import CourseRegistrationForm


@staff_member_required
def registration_list(request):
    registrations = CourseRegistration.objects.select_related('student', 'course').order_by('-registered_at')
    return render(request, 'registrations/list.html', {'registrations': registrations})


@staff_member_required
def update_registration_status(request, pk):
    registration = get_object_or_404(CourseRegistration, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in {'pending', 'approved', 'rejected'}:
            registration.status = status
            registration.save()
        return redirect('registration_list')
    return render(request, 'registrations/update_status.html', {'registration': registration})


@staff_member_required
def delete_registration(request, pk):
    registration = get_object_or_404(CourseRegistration, pk=pk)
    if request.method == 'POST':
        registration.delete()
        return redirect('registration_list')
    return render(request, 'registrations/confirm_delete.html', {'registration': registration})


@staff_member_required
def view_registration(request, pk):
    registration = get_object_or_404(CourseRegistration, pk=pk)
    return render(request, 'registrations/view.html', {'registration': registration})


@staff_member_required
def download_registration_pdf(request, pk):
    registration = get_object_or_404(CourseRegistration, pk=pk)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="registration_{registration.pk}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    y = height - 80
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "Course registration")
    y -= 40

    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"Student: {registration.student.user}")
    y -= 20
    p.drawString(50, y, f"Email: {registration.student.user.email}")
    y -= 20
    p.drawString(50, y, f"Course: {registration.course.title} ({registration.course.code})")
    y -= 20
    p.drawString(50, y, f"Status: {registration.get_status_display()}")
    y -= 20
    p.drawString(50, y, f"Enrolled on: {registration.registered_at.strftime('%B %d, %Y')}")

    p.showPage()
    p.save()

    return response


@staff_member_required
def registration_edit(request, pk):
    registration = get_object_or_404(CourseRegistration, pk=pk)

    if request.method == 'POST':
        form = CourseRegistrationForm(request.POST, instance=registration)
        if form.is_valid():
            form.save()
            return redirect('registration_list')
    else:
        form = CourseRegistrationForm(instance=registration)

    return render(request, 'registrations/edit.html', {'form': form, 'registration': registration})