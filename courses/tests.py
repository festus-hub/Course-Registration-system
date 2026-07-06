from django.test import TestCase
from django.urls import reverse

from courses.models import Course
from departments.models import Department


class CourseAccessTests(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name='Computer Science', code='CS', description='Tech')
        self.course = Course.objects.create(
            department=self.department,
            code='CS101',
            title='Introduction to Computing',
            description='A beginner-friendly introduction to computing.',
            credit_hours=3,
            semester='First',
            is_active=True,
        )

    def test_course_list_page_displays_courses(self):
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.course.title)
        self.assertContains(response, self.course.code)

    def test_course_detail_page_displays_course_information(self):
        response = self.client.get(reverse('course_detail', args=[self.course.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.course.title)
        self.assertContains(response, self.course.description)
