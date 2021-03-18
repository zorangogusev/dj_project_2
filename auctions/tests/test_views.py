from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve
from auctions.models import List, Category, User
from datetime import datetime


class TestViews(TestCase):

    def setUp(self):
        self.login_url = reverse('users:login')
        self.register_url = reverse('users:register')
        self.user_data = {
            'username': 'admin',
            'email': 'admin@admin.com',
            'password': 'zoranzoran',
            'confirmation': 'zoranzoran',
        }

        # Create category, user, list for testing
        self.UserInstance = get_user_model()
        self.UserInstance = self.UserInstance.objects.create(
            username='test',
            email='test@test.com',
            password='testpassword'
        )

        self.category = Category.objects.create(
            name='shoes'
        )

        self.list = List.objects.create(
            title='title_test_example',
            description='desc_test_example',
            start_bid=10,
            created_at=datetime.now(),
            active=True,
            owner=self.UserInstance,
            category=self.category
        )

        self.list_data = {
            'title': 'title',
            'description': 'desc_test_example',
            'start_bid': 10,
            'category': self.category.id
        }

    def test_user_can_see_index_page(self):
        url = reverse('auctions:index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auctions/index.html')

    def test_logged_in_user_can_see_list_page(self):
        url = reverse('auctions:view_list', args=[self.list.id])

        # register user and immediately the user is logged in
        self.client.post(self.register_url, self.user_data, format='text/html')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auctions/view_list.html')

    def test_not_logged_in_user_can_not_see_list_page(self):
        url = reverse('auctions:view_list', args=[self.list.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_see_create_list_page(self):
        url = reverse('auctions:create_list')

        # register user and immediately the user is logged in
        self.client.post(self.register_url, self.user_data, format='text/html')

        response = self.client.get(url, format='text/html')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auctions/create_list.html')

    def test_not_logged_in_user_can_not_see_create_list_page(self):
        url = reverse('auctions:create_list')

        response = self.client.get(url, format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_create_new_list(self):
        url = reverse('auctions:create_list')

        # register user and immediately the user is logged in
        self.client.post(self.register_url, self.user_data, format='text/html')

        response = self.client.post(url, self.list_data, format='text/html')

        print('response is: ', response)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(List.objects.filter(title='title').first().title, 'title')

    def test_not_logged_in_user_can_not_create_new_list(self):
        url = reverse('auctions:create_list')

        response = self.client.post(url, self.list_data, format='text/html')

        print('response is: ', response)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(List.objects.all().count(), 1)
