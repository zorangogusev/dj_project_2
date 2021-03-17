from django.test import TestCase
from django.urls import reverse, resolve


class TestViews(TestCase):

    def setUp(self):
        self.login_url = reverse('users:login')
        self.register_url = reverse('users:register')
        self.user = {
            'username': 'admin',
            'email': 'admin@admin.com',
            'password': 'zoranzoran',
            'confirmation': 'zoranzoran',
        }

    def test_user_can_see_index_page(self):
        url = reverse('auctions:index')
        response = self.client.get(url)

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'auctions/index.html')

    def test_logged_in_user_can_see_create_list_page(self):
        url = reverse('auctions:create_list')

        # register user and immediately the user is logged in
        self.client.post(self.register_url, self.user, format='text/html')

        response = self.client.get(url, format='text/html')

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'auctions/create_list.html')

    def test_not_logged_in_user_can_not_see_create_list_page(self):
        url = reverse('auctions:create_list')

        response = self.client.get(url, format='text/html')
        self.assertTrue(response.status_code, 302)
