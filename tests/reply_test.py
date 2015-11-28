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


class ReplyTest(unittest.TestCase, ReplyCommon):

    def setUp(self):
        self.driver = ReplyCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        ReplyCommon.fill_inbox(self.driver)

    def test_reply_email_to(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')
        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.reply()
        sent_letter_page = SentLetterPage(self.driver)
        email_to = sent_letter_page.data.get_email_to()
        ReplyCommon.clear_inbox(self.driver)
        self.assertEqual(email_to, 'nikuda@mail.ru')

    def test_reply_subject(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.reply()
        sent_letter_page = SentLetterPage(self.driver)
        subject = sent_letter_page.data.get_subject()
        ReplyCommon.clear_inbox(self.driver)
        self.assertEqual(subject, 'Re: 1')

    def test_reply_mail_text(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('abrakadabra')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.reply()
        sent_letter_page = SentLetterPage(self.driver)
        body_text = sent_letter_page.data.get_body()
        ReplyCommon.clear_inbox(self.driver)
        self.assertTrue('abrakadabra' in body_text)

    def test_reply_all_email_to(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')
        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.reply_all()
        sent_letter_page = SentLetterPage(self.driver)
        email_to = sent_letter_page.data.get_email_to()
        ReplyCommon.clear_inbox(self.driver)
        self.assertEqual(email_to, 'nikuda@mail.ru')

    def test_reply_all_subject(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.reply_all()
        sent_letter_page = SentLetterPage(self.driver)
        subject = sent_letter_page.data.get_subject()
        ReplyCommon.clear_inbox(self.driver)
        self.assertEqual(subject, 'Re: 1')

    def test_reply_all_mail_text(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('abrakadabra')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.reply_all()
        sent_letter_page = SentLetterPage(self.driver)
        body_text = sent_letter_page.data.get_body()
        ReplyCommon.clear_inbox(self.driver)
        self.assertTrue('abrakadabra' in body_text)

    def test_forward_no_email_to_test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')
        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.forward()
        sent_letter_page = SentLetterPage(self.driver)
        email_to = sent_letter_page.data.get_email_to()
        ReplyCommon.clear_inbox(self.driver)
        self.assertEqual(email_to, '')

    def test_forward_subject(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.forward()
        sent_letter_page = SentLetterPage(self.driver)
        subject = sent_letter_page.data.get_subject()
        ReplyCommon.clear_inbox(self.driver)
        self.assertEqual(subject, 'Fwd: 1')

    def test_forward_email_text(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('abrakadabra')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.forward()
        sent_letter_page = SentLetterPage(self.driver)
        body_text = sent_letter_page.data.get_body()
        ReplyCommon.clear_inbox(self.driver)
        self.assertTrue('abrakadabra' in body_text)

    def tearDown(self):
        self.driver.quit()
