# -*- coding: utf-8 -*-
import os
import urlparse
import unittest
import time

from selenium.webdriver import DesiredCapabilities, Remote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


USER_EMAIL = os.environ['TTHA4USER']
PASSWORD = os.environ['TTHA4PASSWORD']
BROWSER = os.environ.get('TTHA4BROWSER', 'CHROME')


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


def wait_for(condition_function):
    start_time = time.time()
    while time.time() < start_time + 10:
        if condition_function():
            return True
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )

class WaitForPageLoad(object):
    CHANGEBLOCK = '//div[@class="b-layout  b-layout_flex"]'

    def __init__(self, driver):
        self.driver = driver

    def __enter__(self):
        self.old_page = self.driver.find_element_by_xpath(self.CHANGEBLOCK).text

    def page_has_loaded(self):
        new_page = self.driver.find_element_by_xpath(self.CHANGEBLOCK).text
        return new_page != self.old_page

    def __exit__(self, *_):
        wait_for(self.page_has_loaded)

class TopStatus(Component):
    EMAIL = '//i[@id="PH_user-email"]'

    def get_email(self):
        return self.driver.find_element_by_xpath(self.EMAIL).text


class ClearBoxMixin(WaitForPageLoad):
    TOOLBAR = '//div[@class="b-sticky" and not (contains(@style,"visibility: hidden;"))]\
        //div[contains(@data-cache-key, "undefined") and not(contains(@style,"display: none"))]'
    CHECKBOXALL = '//div[@class="b-checkbox__checkmark"]'
    DELETEBTN = '//div[@data-name="remove"]'
    EMPTYBOX = '//div[@class="b-layout  b-layout_flex"]\
        //div[contains(@data-cache-key, "undefined") and not(contains(@style,"display: none"))]\
        //div[contains(@ class, "b-datalist__empty")]'

    def clear_box(self, driver):
        empty_box = self.driver.find_elements_by_xpath(self.EMPTYBOX)
        if not len(empty_box):
            WebDriverWait(self.driver, 30, 0.1).until(
                lambda d: d.find_element_by_xpath(self.TOOLBAR)
            )
            self.driver.find_element_by_xpath(self.TOOLBAR + self.CHECKBOXALL).click()
            with WaitForPageLoad(self.driver):
                self.driver.find_element_by_xpath(self.TOOLBAR + self.DELETEBTN).click()