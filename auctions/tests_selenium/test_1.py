from selenium import webdriver
from auctions.models import Category, AdListing, Comment, Bid
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time


class TestAuctions(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_browser(self):
        # self.assertEquals(1, 1)
        self.browser.get(self.live_server_url)
        time.sleep(2)
