from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthFlowTests(TestCase):
    def test_registration_redirects_to_login_and_login_redirects_to_dashboard(self):
        register_url = reverse('register')
        response = self.client.post(register_url, {
            'username': 'newstudent',
            'email': 'newstudent@example.com',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        user = get_user_model().objects.get(username='newstudent')
        self.assertTrue(user is not None)

        login_url = reverse('login')
        response = self.client.post(login_url, {
            'username': 'newstudent',
            'password': 'StrongPass123',
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))
