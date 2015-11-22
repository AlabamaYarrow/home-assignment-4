# -*- coding: utf-8 -*-

import os

import unittest
import urlparse

from selenium.webdriver import DesiredCapabilities, Remote
from selenium.webdriver.support.ui import WebDriverWait

class Page(object):
    BASE_URL = 'https://e.mail.ru/'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
        self.driver.maximize_window()

class Component(object):
    def __init__(self, driver):
        self.driver = driver

class AuthPage(Page):
    PATH = ''

    @property
    def form(self):
        return AuthForm(self.driver)

class InboxPage(Page):
    PATH = ''

    @property
    def top_status(self):
        return TopStatus(self.driver)

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

class TopStatus(Component):
    EMAIL = '//i[@id="PH_user-email"]'

    def get_email(self):
        return self.driver.find_element_by_xpath(self.EMAIL).text