from django import forms
from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['department', 'code', 'title', 'description', 'credit_hours', 'semester', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }