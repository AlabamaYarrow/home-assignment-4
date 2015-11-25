from page_objects.base import *
from page_objects.auth_page import AuthPage
from page_objects.inbox_page import InboxPage
from page_objects.sent_page import SentPage
from page_objects.letter_page import LetterPage


class MovingCommon(object):
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


class MoveToTrashTest(unittest.TestCase, MovingCommon):

    def setUp(self):
        self.driver = MovingCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        MovingCommon.fill_sent_box(self.driver)

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_recieved_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.delete()

        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_spam_inbox()
        self.assertEquals(inbox_page.have_letter('1'), True)

    def tearDown(self):
        MovingCommon.clear_sent_box(self.driver)
        self.driver.quit()