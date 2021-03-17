from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class RegisterTest(TestCase):
    def setUp(self):
        self.register_url = reverse('users:register')
        self.user = {
            'username': 'admin',
            'email': 'admin@admin.com',
            'password': 'zoranzoran',
            'confirmation': 'zoranzoran',
        }
        self.user_unmatching_password = {
            'username': 'admin',
            'email': 'admin@admin.com',
            'password': 'zoranzoran',
            'confirmation': 'zoranzoran4',
        }

    def test_can_view_register_page_correctly(self):
        response = self.client.get(self.register_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_can_register_user(self):
        response = self.client.post(self.register_url, self.user, format='text/html')

        self.assertEqual(response.status_code, 302)

    def test_cant_register_user_with_unmatching_passwords(self):
        response = self.client.post(self.register_url, self.user_unmatching_password, format='text/html')
        message = response.context['message']

        self.assertEqual(len(message[0]), 1)
        self.assertEqual(str(message), 'Passwords must match.')


class LoginTest(TestCase):
    def setUp(self):
        self.login_url = reverse('users:login')
        self.register_url = reverse('users:register')
        self.user = {
            'username': 'admin',
            'email': 'admin@admin.com',
            'password': 'zoranzoran',
            'confirmation': 'zoranzoran',
        }

    def test_can_access_login_page(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_user_can_login_successfully(self):
        # create user
        self.client.post(self.register_url, self.user, format='text/html')
        User = get_user_model()
        user = User.objects.filter(username=self.user['username']).first()
        user.is_active = True
        user.save()

        response = self.client.post(self.login_url, self.user, format='text/html')

        self.assertEqual(response.status_code, 302)

    def test_guest_can_not_login(self):
        User = get_user_model()
        user = User.objects.filter(username=self.user['username']).first()
        response = self.client.post(self.login_url, self.user, format='text/html')
        message = response.context['message']

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertEqual(len(message[0]), 1)
        self.assertEqual(str(message), 'Invalid username and/or password.')


class LogoutTest(TestCase):

    def setUp(self):
        self.login_url = reverse('users:login')
        self.register_url = reverse('users:register')
        self.logout_url = reverse('users:logout')
        self.user = {
            'username': 'admin',
            'email': 'admin@admin.com',
            'password': 'zoranzoran',
            'confirmation': 'zoranzoran',
        }

    def test_logged_in_user_can_logout(self):
        self.client.post(self.register_url, self.user, format='text/html')
        User = get_user_model()
        user = User.objects.filter(username=self.user['username']).first()
        user.is_active = True
        user.save()
        self.client.post(self.login_url, self.user, format='text/html')

        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)