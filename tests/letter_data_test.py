# -*- coding: utf-8 -*-

from page_objects.base import *
from page_objects.auth_page import AuthPage
from page_objects.inbox_page import InboxPage
from page_objects.sent_page import SentPage
from page_objects.letter_page import LetterPage
from page_objects.sent_letter_page import SentLetterPage


class LetterDataCommon(object):
    @staticmethod
    def fill_sent_box(driver):
        inbox_page = InboxPage(driver)
        inbox_page.send_letter('1')

    @staticmethod
    def clear_sent_box(driver):
        inbox_page = InboxPage(driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(driver)
        sent_page.clear_box(driver)

    @staticmethod
    def get_driver():
        return Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, BROWSER).copy()
        )


class LetterSubjectTest(unittest.TestCase, LetterDataCommon):

    def setUp(self):
        self.driver = LetterDataCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        LetterDataCommon.fill_sent_box(self.driver)

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        subject = letter_page.letter_head.get_subject()
        self.assertEquals(subject, '1')

    def tearDown(self):
        LetterDataCommon.clear_sent_box(self.driver)
        self.driver.quit()


class LetterEmailFromTest(unittest.TestCase, LetterDataCommon):

    def setUp(self):
        self.driver = LetterDataCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        LetterDataCommon.fill_sent_box(self.driver)

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        email_from = letter_page.letter_head.get_email_from()
        self.assertEquals(email_from, USER_EMAIL)

    def tearDown(self):
        LetterDataCommon.clear_sent_box(self.driver)
        self.driver.quit()


class LetterEmailToTest(unittest.TestCase, LetterDataCommon):

    def setUp(self):
        self.driver = LetterDataCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        LetterDataCommon.fill_sent_box(self.driver)

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        email_to = letter_page.letter_head.get_email_to()
        self.assertEquals(email_to, 'nikuda@mail.ru')

    def tearDown(self):
        LetterDataCommon.clear_sent_box(self.driver)
        self.driver.quit()


class LetterDatetimeExistsTest(unittest.TestCase, LetterDataCommon):

    def setUp(self):
        self.driver = LetterDataCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        LetterDataCommon.fill_sent_box(self.driver)

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        letter_date = letter_page.letter_head.get_date()
        self.assertNotEquals(letter_date, '')

    def tearDown(self):
        LetterDataCommon.clear_sent_box(self.driver)
        self.driver.quit()


class LetterBodyExistsTest(unittest.TestCase, LetterDataCommon):

    def setUp(self):
        self.driver = LetterDataCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        LetterDataCommon.fill_sent_box(self.driver)

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        letter_body = letter_page.letter_head.get_body()
        self.assertNotEquals(letter_body, '')

    def tearDown(self):
        LetterDataCommon.clear_sent_box(self.driver)
        self.driver.quit()