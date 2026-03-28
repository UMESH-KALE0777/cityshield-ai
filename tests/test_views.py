from django.test import TestCase, Client
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_login_page_loads(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_success_redirects_to_dashboard(self):
        response = self.client.post('/accounts/login/', {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertRedirects(response, '/dashboard/')

    def test_dashboard_requires_login(self):
        response = self.client.get('/dashboard/')
        self.assertRedirects(response, '/accounts/login/?next=/dashboard/')

    def test_hotspot_requires_login(self):
        response = self.client.get('/hotspots/')
        self.assertEqual(response.status_code, 302)
