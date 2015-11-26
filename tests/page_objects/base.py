# -*- coding: utf-8 -*-

import os
import urlparse
import unittest
import time

from selenium.webdriver import DesiredCapabilities, Remote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


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


class ToolbarJS(object):
    ## TODO: перенести переменную scriptFindToolbar в описание класса, а в методах вызывать её

    @staticmethod
    def get_check_all_script():
        scriptFindToolbar = '\
            topTollbar = $(".b-sticky").filter(function () { return $(this).css("z-index") == 100 });\
            rightToolbar = topTollbar.find("#b-toolbar__right").children();\
            visibleToolbar = $(rightToolbar).filter(function () { return $(this).css("display") != "none" });'

        return scriptFindToolbar + '\
        checkbox = visibleToolbar.find(".b-checkbox__checkmark");\
        checkbox.click();'

    @staticmethod
    def get_delete_script():
        scriptFindToolbar = '\
            topTollbar = $(".b-sticky").filter(function () { return $(this).css("z-index") == 100 });\
            rightToolbar = topTollbar.find("#b-toolbar__right").children();\
            visibleToolbar = $(rightToolbar).filter(function () { return $(this).css("display") != "none" });'

        return scriptFindToolbar + '\
        btn = visibleToolbar.find("span").filter(function () { return $(this).text() == "Удалить" });\
        btn.click();'

    @staticmethod
    def get_archive_script():
        scriptFindToolbar = '\
            topTollbar = $(".b-sticky").filter(function () { return $(this).css("z-index") == 100 });\
            rightToolbar = topTollbar.find("#b-toolbar__right").children();\
            visibleToolbar = $(rightToolbar).filter(function () { return $(this).css("display") != "none" });'

        return scriptFindToolbar + '\
        btn = visibleToolbar.find("span").filter(function () { return $(this).text() == "В архив" });\
        btn.click();'

    @staticmethod
    def get_spam_script():
        scriptFindToolbar = '\
            topTollbar = $(".b-sticky").filter(function () { return $(this).css("z-index") == 100 });\
            rightToolbar = topTollbar.find("#b-toolbar__right").children();\
            visibleToolbar = $(rightToolbar).filter(function () { return $(this).css("display") != "none" });'

        return scriptFindToolbar + '\
        btn = visibleToolbar.find("span").filter(function () { return $(this).text() == "Спам" });\
        btn.click();'

    @staticmethod
    def get_spam_confirm_script():
        return '$(".confirm-cancel").filter(function () { return $(this).text() == "Да" }).click();'


class TopStatus(Component):
    EMAIL = '//i[@id="PH_user-email"]'

    def get_email(self):
        return self.driver.find_element_by_xpath(self.EMAIL).text


class ClearBoxMixin(WaitForPageLoad, ToolbarJS):
    EMPTYFOLDER = '//span[@class="b-datalist__empty__text"]/../../../..'

    def clear_box(self, driver):
        empty_msg = self.driver.find_elements_by_xpath(self.EMPTYFOLDER)
        flagEmpty = True

        for item in empty_msg:
            if "display: none" in item.get_attribute("style"):
                flagEmpty = False

        if not (empty_msg and flagEmpty):
            scriptCheckAll = ToolbarJS.get_check_all_script()
            scriptDelete = ToolbarJS.get_delete_script()

            driver.execute_script(scriptCheckAll)
            with WaitForPageLoad(self.driver):
                driver.execute_script(scriptDelete)