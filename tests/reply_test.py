# -*- coding: utf-8 -*-
from page_objects.base import *
from page_objects.auth_page import AuthPage
from page_objects.inbox_page import InboxPage
from page_objects.sent_page import SentPage
from page_objects.letter_page import LetterPage
from page_objects.sent_letter_page import SentLetterPage


class ReplyCommon(object):
    @staticmethod
    def fill_inbox(driver):
        inbox_page = InboxPage(driver)
        inbox_page.send_letter('1')

    @staticmethod
    def clear_inbox(driver):
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


class ReplyEmailToTest(unittest.TestCase, ReplyCommon):

    def setUp(self):
        self.driver = ReplyCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        ReplyCommon.fill_inbox(self.driver)

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')
        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.reply()
        sent_letter_page = SentLetterPage(self.driver)
        self.assertEqual(sent_letter_page.data.get_email_to(), 'nikuda@mail.ru')

    def tearDown(self):
        ReplyCommon.clear_inbox(self.driver)
        self.driver.quit()


class ReplySubjectTest(unittest.TestCase, ReplyCommon):

    def setUp(self):
        self.driver = ReplyCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        ReplyCommon.fill_inbox(self.driver)

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.reply()
        sent_letter_page = SentLetterPage(self.driver)
        self.assertEqual(sent_letter_page.data.get_subject(), 'Re: 1')

    def tearDown(self):
        ReplyCommon.clear_inbox(self.driver)
        self.driver.quit()


class ReplyMailTextTest(unittest.TestCase, ReplyCommon):

    def setUp(self):
        self.driver = ReplyCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        inbox_page = InboxPage(self.driver)
        inbox_page.send_letter('abrakadabra')

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('abrakadabra')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.reply()
        sent_letter_page = SentLetterPage(self.driver)
        body_text = sent_letter_page.data.get_body()
        self.assertTrue('abrakadabra' in body_text)

    def tearDown(self):
        ReplyCommon.clear_inbox(self.driver)
        self.driver.quit()


class ReplyAllEmailToTest(unittest.TestCase, ReplyCommon):

    def setUp(self):
        self.driver = ReplyCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        ReplyCommon.fill_inbox(self.driver)

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')
        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.reply_all()
        sent_letter_page = SentLetterPage(self.driver)
        self.assertEqual(sent_letter_page.data.get_email_to(), 'nikuda@mail.ru')

    def tearDown(self):
        ReplyCommon.clear_inbox(self.driver)
        self.driver.quit()


class ReplyAllSubjectTest(unittest.TestCase, ReplyCommon):

    def setUp(self):
        self.driver = ReplyCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        ReplyCommon.fill_inbox(self.driver)

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.reply_all()
        sent_letter_page = SentLetterPage(self.driver)
        self.assertEqual(sent_letter_page.data.get_subject(), 'Re: 1')

    def tearDown(self):
        ReplyCommon.clear_inbox(self.driver)
        self.driver.quit()


class ReplyAllMailTextTest(unittest.TestCase, ReplyCommon):

    def setUp(self):
        self.driver = ReplyCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        inbox_page = InboxPage(self.driver)
        inbox_page.send_letter('abrakadabra')

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('abrakadabra')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.reply_all()
        sent_letter_page = SentLetterPage(self.driver)
        body_text = sent_letter_page.data.get_body()
        self.assertTrue('abrakadabra' in body_text)

    def tearDown(self):
        ReplyCommon.clear_inbox(self.driver)
        self.driver.quit()


class ForwardNoEmailToTest(unittest.TestCase, ReplyCommon):

    def setUp(self):
        self.driver = ReplyCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        ReplyCommon.fill_inbox(self.driver)

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')
        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.forward()
        sent_letter_page = SentLetterPage(self.driver)
        self.assertEqual(sent_letter_page.data.get_email_to(), '')

    def tearDown(self):
        ReplyCommon.clear_inbox(self.driver)
        self.driver.quit()


class ForwardSubjectTest(unittest.TestCase, ReplyCommon):

    def setUp(self):
        self.driver = ReplyCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        ReplyCommon.fill_inbox(self.driver)

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.forward()
        sent_letter_page = SentLetterPage(self.driver)
        self.assertEqual(sent_letter_page.data.get_subject(), 'Fwd: 1')

    def tearDown(self):
        ReplyCommon.clear_inbox(self.driver)
        self.driver.quit()


class ForwardMailTextTest(unittest.TestCase, ReplyCommon):

    def setUp(self):
        self.driver = ReplyCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        inbox_page = InboxPage(self.driver)
        inbox_page.send_letter('abrakadabra')

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('abrakadabra')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.forward()
        sent_letter_page = SentLetterPage(self.driver)
        body_text = sent_letter_page.data.get_body()
        self.assertTrue('abrakadabra' in body_text)

    def tearDown(self):
        ReplyCommon.clear_inbox(self.driver)
        self.driver.quit()