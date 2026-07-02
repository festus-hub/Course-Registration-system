from django.db import models

from departments.models import Department


class Course(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name='Department/School',
        help_text='Select the department or school offering this course.',
    )
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    credit_hours = models.PositiveIntegerField(
        default=3,
        verbose_name='Units',
        help_text='Number of credit units for this course.',
    )
    semester = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Courses'

    def __str__(self):
        return f"{self.code} - {self.title}"
