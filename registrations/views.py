from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

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

def delete_registration(request, pk):
    registration = get_object_or_404(CourseRegistration, pk=pk)
    if request.method == 'POST':
        registration.delete()
        return redirect('registration_list')
    return render(request, 'registrations/confirm_delete.html', {'registration': registration})

def view_registration(request, pk):
    registration = get_object_or_404(CourseRegistration, pk=pk)
    return render(request, 'registrations/view.html', {'registration': registration})   

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
    p.drawString(50, y, f"student: {registration.student.user}")
    y -= 20
    p.drawString(50, y, f"Email: {registration.student.user.email}")
    y -= 20
    p.drawString(50, y, f"Course: {registration.course.title} ({registration.course.code})")
    y -= 20
    p.drawString(50, y, f"Section: {registration}")
    y -= 20
    p.drawString(50, y, f"Enrolled on: {registration.registered_at}")

    p.showPage()
    p.save()

    return response

def registration_edit(request, pk):
    registration = get_object_or_404(CourseRegistration, pk=pk)
    if request.method == 'POST':
        
        return redirect('registration_list')
    return render(request, 'registrations/edit.html', {'registration': registration})


