import time
import socket

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse
from django.contrib.auth import get_user_model
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
        # cls.browser = webdriver.Remote(
        #     command_executor='http://selenium:4444/wd/hub',
        #     desired_capabilities=DesiredCapabilities.FIREFOX,
        # )

        # for testing in venv
        cls.browser = webdriver.Firefox()

        cls.browser.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()


class LoginSeleniumTest(BaseTestCase):

    def test_login_user_with_correct_data(self):
        """
        The user on the login page enter correct username and password,
        click the login button,
        and after login the user is redirected to active listings page.
        """
        self.browser.get(self.live_server_url + reverse('users:login'))
        get_user_model().objects.create_user(username='testuser', email='test@test.com', password='12345')

        self.browser.find_element_by_id('username').send_keys('testuser')
        self.browser.find_element_by_id('password').send_keys('12345')

        self.browser.find_element_by_class_name('login_btn').click()

        div_container = self.browser.find_element_by_class_name('container')
        self.assertEquals(div_container.find_element_by_tag_name('h2').text, 'Active Listings')

    def test_dont_login_user_with_uncorrect_data(self):
        """
        The user on the login page enter not correct username and password,
        click the login button,
        and after login the user is return to the login page with error message.
        """
        self.browser.get(self.live_server_url + reverse('users:login'))
        get_user_model().objects.create_user(username='testuser', email='test@test.com', password='12345')

        self.browser.find_element_by_id('username').send_keys('not_correct_username')
        self.browser.find_element_by_id('password').send_keys('12345')

        self.browser.find_element_by_class_name('login_btn').click()

        check_element = self.browser.find_element_by_class_name('login_btn')
        check_element_2 = self.browser.find_element_by_class_name('login-register-message')

        self.assertEquals(check_element.get_attribute('value'), 'Login')
        self.assertEquals(check_element_2.text, 'Invalid username and/or password.')


class RegisterSeleniumTest(BaseTestCase):

    def test_register_user_with_correct_data(self):
        """
        The user on the register page enter username, email, password and confirmation password,
        click the register button,
        and after registration the user is automatically logged in and redirected to active listings page.
        """
        self.browser.get(self.live_server_url + reverse('users:register'))

        user = {
            'username': 'admin',
            'email': 'admin@admin.com',
            'password': 'zoranzoran',
            'confirmation': 'zoranzoran',
        }

        self.browser.find_element_by_id('username').send_keys(user['username'])
        self.browser.find_element_by_id('email').send_keys(user['email'])
        self.browser.find_element_by_id('password').send_keys(user['password'])
        self.browser.find_element_by_id('confirmation').send_keys(user['confirmation'])

        self.browser.find_element_by_id('register-button').click()

        div_container = self.browser.find_element_by_class_name('container')
        self.assertEquals(div_container.find_element_by_tag_name('h2').text, 'Active Listings')

    def test_cant_register_user_with_unmatching_password(self):
        """
        The user on the register page enter username, email, password and not correct confirmation password,
        click the register button,
        and the user is returned to registration page with message.
        """
        self.browser.get(self.live_server_url + reverse('users:register'))

        user = {
            'username': 'admin',
            'email': 'admin@admin.com',
            'password': 'zoranzoran',
            'confirmation': 'not_correct',
        }

        self.browser.find_element_by_id('username').send_keys(user['username'])
        self.browser.find_element_by_id('email').send_keys(user['email'])
        self.browser.find_element_by_id('password').send_keys(user['password'])
        self.browser.find_element_by_id('confirmation').send_keys(user['confirmation'])

        self.browser.find_element_by_id('register-button').click()

        check_element = self.browser.find_element_by_class_name('login-register-message')
        self.assertEquals(check_element.text, 'Passwords must match.')


class LogoutSeleniumTest(BaseTestCase):

    def setUp(self):
        user = {
            'username': 'admin',
            'email': 'admin@admin.com',
            'password': 'zoranzoran',
            'confirmation': 'not_correct',
        }

        get_user_model().objects.create_user(
            username=user['username'],
            email=user['email'],
            password=user['password']
        )

        self.client.login(username=user['username'], password=user['password'])  # Native django test client
        cookie = self.client.cookies['sessionid']
        self.browser.get(self.live_server_url + reverse('users:login'))  # selenium will set cookie domain based on current page domain
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.browser.refresh()  # need to update page for logged in user
        self.browser.get(self.live_server_url + '/auctions/create/')

    def test_logged_in_user_can_logout(self):
        """
        The loggedIn user can click the logout button,
        the user is logged out and returned to active listing page as unregistered guest.
        """
        self.browser.find_element_by_id('logout_user').click()
        register_user = self.browser.find_element_by_id('register_user')
        login_user = self.browser.find_element_by_id('login_user')

        div_container = self.browser.find_element_by_class_name('container')
        self.assertEquals(div_container.find_element_by_tag_name('h2').text, 'Active Listings')
        self.assertEquals(register_user.text, 'Register')
        self.assertEquals(login_user.text, 'Log In')
