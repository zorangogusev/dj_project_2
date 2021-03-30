import time
import socket

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from auctions.models import Category, AdListing, Comment, Bid


@tag('selenium')
@override_settings(ALLOWED_HOSTS=['*'])
class BaseTestCase(StaticLiveServerTestCase):
    """
    Provides base test class which connects to the Docker
    container running selenium.
    """
    host = '0.0.0.0'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.host = socket.gethostbyname(socket.gethostname())

        # for testing in docker
        cls.browser = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.FIREFOX,
        )

        # for testing in venv
        # cls.browser = webdriver.Firefox()

        cls.browser.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()


class FunctionalTestCase(BaseTestCase):

    def test_display_home_page(self):
        self.browser.get(self.live_server_url)

        div_container = self.browser.find_element_by_class_name('container')
        self.assertEquals(div_container.find_element_by_tag_name('h2').text, 'Active Listings')
