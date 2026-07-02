from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from courses.models import Course
from departments.models import Department
from registrations.models import CourseRegistration
from students.models import Student


class StudentPortalViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='student1',
            email='student1@example.com',
            password='secret1234',
            role='student',
        )
        self.department = Department.objects.create(name='Computer Science')
        self.student = Student.objects.create(
            user=self.user,
            student_id='STU-001',
            department=self.department,
        )
        self.course = Course.objects.create(
            department=self.department,
            code='CSC101',
            title='Introduction to Computing',
            credit_hours=3,
        )
        CourseRegistration.objects.create(student=self.student, course=self.course, status='pending')

    def test_student_dashboard_requires_login(self):
        response = self.client.get(reverse('students_dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_student_dashboard_renders_for_student(self):
        self.client.login(username='student1', password='secret1234')
        response = self.client.get(reverse('students_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome Back')
        self.assertContains(response, 'Introduction to Computing')
