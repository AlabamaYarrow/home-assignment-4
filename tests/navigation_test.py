from page_objects.base import *
from page_objects.auth_page import AuthPage
from page_objects.inbox_page import InboxPage
from page_objects.sent_page import SentPage
from page_objects.letter_page import LetterPage


class NavigationCommon(object):
    @staticmethod
    def fill_sent_box(driver):
        inbox_page = InboxPage(driver)
        inbox_page.send_letter('1')
        inbox_page.send_letter('2')
        inbox_page.send_letter('3')

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


class NavigateTest(unittest.TestCase, NavigationCommon):
    def setUp(self):
        self.driver = NavigationCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        NavigationCommon.fill_sent_box(self.driver)

    def test_previous(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('2')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.get_prev_letter()
        subject = letter_page.letter_head.get_subject()
        NavigationCommon.clear_sent_box(self.driver)
        self.assertEquals(subject, '3')

    def test_multiple_previous(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.get_prev_letter()
        letter_page.letter_toolbar.get_prev_letter()
        subject = letter_page.letter_head.get_subject()
        NavigationCommon.clear_sent_box(self.driver)
        self.assertEquals(subject, '3')

    def test_previous_return(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('3')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.get_next_letter()
        letter_page.letter_toolbar.get_prev_letter()

        subject = letter_page.letter_head.get_subject()
        NavigationCommon.clear_sent_box(self.driver)
        self.assertEquals('3', subject)

    def test_no_previous(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('3')

        letter_page = LetterPage(self.driver)
        is_disabled = letter_page.letter_toolbar.prev_letter_is_disabled()
        NavigationCommon.clear_sent_box(self.driver)
        self.assertEquals(True, is_disabled)

    def test_next(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('2')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.get_next_letter()
        subject = letter_page.letter_head.get_subject()
        NavigationCommon.clear_sent_box(self.driver)
        self.assertEquals('1', subject)

    def test_multiple_next(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('3')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.get_next_letter()
        letter_page.letter_toolbar.get_next_letter()
        subject = letter_page.letter_head.get_subject()
        NavigationCommon.clear_sent_box(self.driver)
        self.assertEquals('1', subject)

    def test_return_next(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.get_prev_letter()
        letter_page.letter_toolbar.get_next_letter()
        subject = letter_page.letter_head.get_subject()
        NavigationCommon.clear_sent_box(self.driver)
        self.assertEquals('1', subject)

    def test_no_next(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        is_disabled = letter_page.letter_toolbar.next_letter_is_disabled()
        NavigationCommon.clear_sent_box(self.driver)
        self.assertEquals(True, is_disabled)

    def tearDown(self):
        self.driver.quit()
