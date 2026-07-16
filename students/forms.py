from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user', 'student_id', 'department', 'admission_year', 'is_active']