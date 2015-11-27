from page_objects.base import *
from page_objects.auth_page import AuthPage
from page_objects.inbox_page import InboxPage
from page_objects.sent_page import SentPage
from page_objects.letter_page import LetterPage


class MovingCommon(object):
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


class MoveToTrashTest(unittest.TestCase, MovingCommon):

    def setUp(self):
        self.driver = MovingCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        MovingCommon.fill_inbox(self.driver)

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.delete()
        inbox_page.folders.get_trash_inbox()
        is_letter_present = inbox_page.have_letter('1')
        MovingCommon.clear_inbox(self.driver)
        self.assertEquals(is_letter_present, True)

    def tearDown(self):
        self.driver.quit()


class MoveToArchiveTest(unittest.TestCase, MovingCommon):

    def setUp(self):
        self.driver = MovingCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        MovingCommon.fill_inbox(self.driver)

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.archive()
        inbox_page.folders.get_archive_inbox()
        is_letter_present = inbox_page.have_letter('1')
        MovingCommon.clear_inbox(self.driver)
        self.assertEquals(is_letter_present, True)

    def tearDown(self):
        self.driver.quit()


class MoveToSpamTest(unittest.TestCase, MovingCommon):

    def setUp(self):
        self.driver = MovingCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        MovingCommon.fill_inbox(self.driver)

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.spam()
        inbox_page.folders.get_spam_inbox()
        is_letter_present = inbox_page.have_letter('1')
        MovingCommon.clear_inbox(self.driver)
        self.assertEquals(is_letter_present, True)

    def tearDown(self):
        self.driver.quit()


class MoveToTest(unittest.TestCase, MovingCommon):

    def setUp(self):
        self.driver = MovingCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        MovingCommon.fill_inbox(self.driver)

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.archive()
        inbox_page.folders.get_archive_inbox()
        is_letter_present = inbox_page.have_letter('1')
        MovingCommon.clear_inbox(self.driver)
        self.assertEquals(is_letter_present, True)

    def tearDown(self):
        self.driver.quit()
