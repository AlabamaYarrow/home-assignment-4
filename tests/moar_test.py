from page_objects.base import *
from page_objects.auth_page import AuthPage
from page_objects.inbox_page import InboxPage
from page_objects.sent_page import SentPage
from page_objects.letter_page import LetterPage


class MoarCommon(object):
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

        inbox_page.folders.get_recieved_inbox()
        sent_page = SentPage(driver)
        sent_page.clear_box(driver)

    @staticmethod
    def get_driver():
        return Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, BROWSER).copy()
        )


class MoarMarkUnreadTest(unittest.TestCase, MoarCommon):

    def setUp(self):
        self.driver = MoarCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        MoarCommon.fill_inbox(self.driver)

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.more_unread()
        read_status = letter_page.letter_head.is_read_status()
        MoarCommon.clear_inbox(self.driver)
        self.assertEquals(read_status, False)

    def tearDown(self):
        self.driver.quit()


class MoarMarkReadTest(unittest.TestCase, MoarCommon):

    def setUp(self):
        self.driver = MoarCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        MoarCommon.fill_inbox(self.driver)

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.more_unread()
        letter_page.letter_toolbar.more_read()
        read_status = letter_page.letter_head.is_read_status()
        MoarCommon.clear_inbox(self.driver)
        self.assertEquals(read_status, True)

    def tearDown(self):
        self.driver.quit()


class MoarSetFlagTest(unittest.TestCase, MoarCommon):

    def setUp(self):
        self.driver = MoarCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        MoarCommon.fill_inbox(self.driver)

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.more_flag_yes()
        is_flag_set = letter_page.letter_head.is_flag_set()
        MoarCommon.clear_inbox(self.driver)
        self.assertEquals(is_flag_set, True)

    def tearDown(self):
        self.driver.quit()


class MoarUnsetFlagTest(unittest.TestCase, MoarCommon):

    def setUp(self):
        self.driver = MoarCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        MoarCommon.fill_inbox(self.driver)

    def test(self):
        inbox_page = InboxPage(self.driver)
        inbox_page.folders.get_sent_inbox()
        sent_page = SentPage(self.driver)
        sent_page.open_letter('1')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.more_flag_yes()
        letter_page.letter_toolbar.more_flag_no()
        read_status = letter_page.letter_head.is_flag_set()
        MoarCommon.clear_inbox(self.driver)
        self.assertEquals(read_status, False)

    def tearDown(self):
        self.driver.quit()


