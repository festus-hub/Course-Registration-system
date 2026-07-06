from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from students.models import Student


class RegisterCoursesViewTests(TestCase):
    def test_student_register_courses_page_renders(self):
        User = get_user_model()
        user = User.objects.create_user(username='student1', password='testpass123')
        Student.objects.create(user=user, student_id='STU001')

        self.client.force_login(user)
        response = self.client.get(reverse('register_courses'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register Courses')
