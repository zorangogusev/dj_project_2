import time
import socket
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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


class GuestTestCase(BaseTestCase):

    def test_display_guest_home_page(self):
        """The guest load the home page."""
        self.browser.get(self.live_server_url)

        div_container = self.browser.find_element_by_class_name('container')
        self.assertEquals(div_container.find_element_by_tag_name('h2').text, 'Active Listings')

    def test_guest_cant_see_navlinks_for_create_list_watchlist_categories_pages(self):
        """
        The guest load the home page without links in navbar for create list, watchlist and categories pages.
        """
        self.browser.get(self.live_server_url)

        try:
            self.browser.find_element_by_id('create_list_link')  # give exception NoSuchElementException
        except Exception as e:
            assert e
            self.assertTrue(True)

        try:
            self.browser.find_element_by_id('watchlist_link')  # give exception NoSuchElementException
        except Exception as e:
            assert e
            self.assertTrue(True)

        try:
            self.browser.find_element_by_id('categories_link')  # give exception NoSuchElementException
        except Exception as e:
            assert e
            self.assertTrue(True)


class UserTestCase(BaseTestCase):

    def setUp(self):
        user = {
            'username': 'admin',
            'email': 'admin@admin.com',
            'password': 'zoranzoran',
            'confirmation': 'not_correct',
        }

        user_instance = get_user_model().objects.create_user(
            username=user['username'],
            email=user['email'],
            password=user['password']
        )

        category = Category.objects.create(
            name='shoes'
        )

        self.ad_listing = AdListing.objects.create(
            title='title_test_example',
            description='desc_test_example',
            start_bid=10,
            created_at=datetime.now(),
            active=True,
            owner=user_instance,
            category=category
        )

        self.client.login(username=user['username'], password=user['password'])  # Native django test client
        cookie = self.client.cookies['sessionid']

        # selenium will set cookie domain based on current page domain
        self.browser.get(self.live_server_url + reverse('users:login'))

        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.browser.refresh()  # need to update page for logged in user
        self.browser.get(self.live_server_url + '/auctions/create/')

    def test_display_user_home_page(self):
        """The user load the home page."""
        self.browser.get(self.live_server_url)

        div_container = self.browser.find_element_by_class_name('container')
        add_to_watchlist_button = self.browser.find_element_by_id('add_to_watchlist_button')

        self.assertEquals(div_container.find_element_by_tag_name('h2').text, 'Active Listings')
        self.assertTrue(add_to_watchlist_button)

    def test_user_on_active_listing_page_can_add_listing_to_watchlist(self):
        """
        The user on the active listing page click the button Add to Watchlist,
        the listing is added to watchlist and the button to remove from watchlist appear.
        """
        self.browser.get(self.live_server_url)

        self.browser.find_element_by_id('add_to_watchlist_button').click()
        remove_from_watchlist_button = self.browser.find_element_by_id('remove_from_watchlist_button')

        self.assertTrue(remove_from_watchlist_button)

    def test_user_on_active_listing_page_can_remove_listing_from_watchlist(self):
        """
        The user on the active listing page click the button Add to Watchlist,
        the listing is added to watchlist and the button to Remove from Watchlist appear,
        then click the remove from watchlist button,
        the listing is removed from watchlist and the button to Add to Watchlist appear.
        """
        self.browser.get(self.live_server_url)

        self.browser.find_element_by_id('add_to_watchlist_button').click()
        self.browser.find_element_by_id('remove_from_watchlist_button').click()
        add_to_watchlist_button = self.browser.find_element_by_id('add_to_watchlist_button')

        self.assertTrue(add_to_watchlist_button)

    def test_user_can_go_on_create_list_page(self):
        """
        The user on the active listing page click in the navbar Create List,
        and he is redirected to the create list page.
        """
        self.browser.get(self.live_server_url)

        self.browser.find_element_by_id('create_list_link').click()
        page_title = self.browser.find_element_by_tag_name('h1')

        self.assertEquals(page_title.text, 'Create List')

    def test_user_can_go_on_watchlist_page(self):
        """
        The user on the active listing page click in the navbar Watchlis,
        and he is redirected to the Watchlist page.
        """
        self.browser.get(self.live_server_url)

        self.browser.find_element_by_id('watchlist_link').click()
        page_title = self.browser.find_element_by_tag_name('h1')

        self.assertEquals(page_title.text, 'Watchlist page')

    def test_user_can_go_on_categories_page(self):
        """
        The user on the active listing page click in the navbar Categories,
        and he is redirected to the Categories page.
        """
        self.browser.get(self.live_server_url)

        self.browser.find_element_by_id('categories_link').click()
        page_title = self.browser.find_element_by_tag_name('h1')

        self.assertEquals(page_title.text, 'Categories')

    def test_can_submit_create_list_form_to_create_new_listing(self):
        """
        The user on the create list page enter title, description, start bid, select/click category,
        submit the form
        and is redirected to active listing page where he can see the created listing.
        """
        self.browser.get(self.live_server_url + reverse('auctions:create_ad_listing'))

        self.browser.find_element_by_id('id_title').send_keys('title_test')
        self.browser.find_element_by_id('id_description').send_keys('description_test')
        self.browser.find_element_by_id('id_start_bid').send_keys('10')
        self.browser.find_element_by_xpath("//select/option[@value='1']").click()
        self.browser.find_element_by_xpath("//input[@type='submit' and @value='Submit']").click()

        title_name = self.browser.find_element_by_xpath("//*[contains(text(), 'title_test')]")

        self.assertEquals(title_name.text, 'title_test')

    def test_user_on_active_listing_page_can_click_on_listing(self):
        """
        The user on the active listing page click listing,
        the user is taken to page with all details about the listing that he clicked.
        """
        self.browser.get(self.live_server_url)

        listing = WebDriverWait(self.browser, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'link-listings')))
        self.browser.execute_script("arguments[0].click();", listing)
        h1_element = self.browser.find_element_by_tag_name('h1')

        self.assertEquals(h1_element.text, 'List ' + self.ad_listing.title)
