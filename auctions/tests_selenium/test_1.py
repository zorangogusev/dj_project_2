import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from auctions.models import Category, AdListing, Comment, Bid


class FunctionalTestCase(StaticLiveServerTestCase):
    # for testing in docker uncomment, for testing in venv comment it
    host = 'web'

    def setUp(self):
        # for testing in venv
        # self.browser = webdriver.Firefox()

        # for testing in docker
        self.browser = webdriver.Remote(
            command_executor="http://selenium:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.FIREFOX
        )

    def tearDown(self):
        self.browser.close()

    def test_display_home_page(self):
        self.browser.get(self.live_server_url)

        div_container = self.browser.find_element_by_class_name('container')
        self.assertEquals(div_container.find_element_by_tag_name('h2').text, 'Active Listings')
