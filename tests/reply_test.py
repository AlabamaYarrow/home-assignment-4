# -*- coding: utf-8 -*-
from base import *


class ReplyCommon(object):
    @staticmethod
    def fill_inbox(driver):
        inbox_page = InboxPage(driver)
        inbox_page.send_letter('1', email=USER_EMAIL)

    @staticmethod
    def clear_inbox(driver):
        inbox_page = InboxPage(driver)
        inbox_page.open()
        inbox_page.clear_box(driver)

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

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.open()
        # inbox_page.open_letter('1')
        # letter_page = LetterPage(self.driver)
        # letter_page.letter_toolbar.reply()

    def tearDown(self):
        ReplyCommon.clear_inbox(self.driver)
        self.driver.quit()
