from django.contrib.auth import get_user_model
from django.test import TestCase
from datetime import datetime
from auctions.models import Category, List
from auctions.util import check_bid


class TestUtil(TestCase):
    def setUp(self):
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

    def test_check_bid_return_true(self):
        check = check_bid(11, self.list)

        self.assertTrue(check)

    def test_check_bid_return_false(self):
        check = check_bid(9, self.list)

        self.assertFalse(check)
