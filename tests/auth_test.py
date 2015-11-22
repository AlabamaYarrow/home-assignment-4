import os

import unittest
import urlparse

from selenium.webdriver import DesiredCapabilities, Remote
from selenium.webdriver.support.ui import WebDriverWait

from base import Page, Component


class AuthPage(Page):
    PATH = ''

    @property
    def form(self):
        return AuthForm(self.driver)


class AuthForm(Component):
    LOGIN = '//input[@name="Login"]'
    PASSWORD = '//input[@name="Password"]'
    SUBMIT = '//button[contains(concat(" ", @class, " "), " js-login-page__external__submit ")]'

    def set_login(self, login):
        self.driver.find_element_by_xpath(self.LOGIN).send_keys(login)

    def set_password(self, pwd):
        self.driver.find_element_by_xpath(self.PASSWORD).send_keys(pwd)

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT).click()


class AuthTest(unittest.TestCase):
    USERNAME = u'testuser'
    USER_EMAIL = os.environ['TTHA4USER']
    PASSWORD = os.environ['TTHA4PASSWORD']

    def setUp(self):
        browser = os.environ.get('TTHA4BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

    def tearDown(self):
        self.driver.quit()

    def test(self):
        auth_page = AuthPage(self.driver)
        auth_page.open()

        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_form = auth_page.form
        auth_form.set_login(self.USER_EMAIL)
        auth_form.set_password(self.PASSWORD)
        auth_form.submit()

