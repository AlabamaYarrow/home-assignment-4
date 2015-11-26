# -*- coding: utf-8 -*-

from page_objects.base import *
from page_objects.auth_page import AuthPage
from page_objects.inbox_page import InboxPage
from page_objects.sent_page import SentPage
from page_objects.letter_page import LetterPage
from page_objects.sent_letter_page import SentLetterPage


class FlagsCommon(object):
    @staticmethod
    def fill_sent_box(driver):
        inbox_page = InboxPage(driver)
        inbox_page.send_letter('1', email_to=USER_EMAIL)

    @staticmethod
    def clear_sent_box(driver):
        inbox_page = InboxPage(driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(driver)
        sent_page.clear_box(driver)

        inbox_page.folders.get_recieved_inbox()
        sent_page = SentPage(driver)
        sent_page.clear_box(driver)

    @staticmethod
    def get_driver():
        return Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, BROWSER).copy()
        )


class SetFlagTest(unittest.TestCase, FlagsCommon):

    def setUp(self):
        self.driver = FlagsCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        FlagsCommon.fill_sent_box(self.driver)

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_recieved_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        letter_page.letter_head.change_flag()
        flag_set = letter_page.letter_head.is_flag_set()
        FlagsCommon.clear_sent_box(self.driver)
        self.assertEquals(flag_set, True)

    def tearDown(self):
        self.driver.quit()


class UnsetFlagTest(unittest.TestCase, FlagsCommon):

    def setUp(self):
        self.driver = FlagsCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        FlagsCommon.fill_sent_box(self.driver)

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_recieved_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        letter_page.letter_head.change_flag()
        letter_page.letter_head.change_flag()
        flag_set = letter_page.letter_head.is_flag_set()
        FlagsCommon.clear_sent_box(self.driver)
        self.assertEquals(flag_set, False)

    def tearDown(self):
        self.driver.quit()


class SetReadTest(unittest.TestCase, FlagsCommon):

    def setUp(self):
        self.driver = FlagsCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        FlagsCommon.fill_sent_box(self.driver)

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_recieved_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        letter_page.letter_head.change_read_status()
        is_read = letter_page.letter_head.is_read_status()
        FlagsCommon.clear_sent_box(self.driver)
        self.assertEquals(is_read, False)

    def tearDown(self):
        self.driver.quit()


class UnsetReadTest(unittest.TestCase, FlagsCommon):

    def setUp(self):
        self.driver = FlagsCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        FlagsCommon.fill_sent_box(self.driver)

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_recieved_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        letter_page.letter_head.change_read_status()
        letter_page.letter_head.change_read_status()
        is_read = letter_page.letter_head.is_read_status()
        FlagsCommon.clear_sent_box(self.driver)
        self.assertEquals(is_read, True)

    def tearDown(self):
        self.driver.quit()
