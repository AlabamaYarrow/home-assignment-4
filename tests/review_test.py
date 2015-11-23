import os
import unittest
from base import *

class ReviewTest(unittest.TestCase):
    USER_EMAIL = os.environ['TTHA4USER']
    PASSWORD = os.environ['TTHA4PASSWORD']

    def setUp(self):
        browser = os.environ.get('TTHA4BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_form = auth_page.form
        auth_form.set_login(self.USER_EMAIL)
        auth_form.set_password(self.PASSWORD)
        auth_form.submit()


    def tearDown(self):
        # inbox_page = InboxPage(self.driver)
        # inbox_page.folders.get_sent_inbox()

        # sentPage = SentPage(self.driver)
        # sentPage.clear_box()
        self.driver.quit()

    def test(self):
        inbox_page = InboxPage(self.driver)

        # inbox_page.send_letter("Message1")
        # inbox_page.send_letter("Message2")
        # inbox_page.send_letter("Message3")

        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()

        sentPage = SentPage(self.driver)
        sentPage.open_letter("Message2")

        letterPage = LetterPage(self.driver)
        print letterPage.letter_head.get_subject()

        letterPage.letter_toolbar.get_prev_letter()
        print letterPage.letter_head.get_subject()


        

