from page_objects.base import *
from page_objects.auth_page import AuthPage
from page_objects.inbox_page import InboxPage
from page_objects.sent_page import SentPage
from page_objects.letter_page import LetterPage


class NavigationCommon(object):

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


class ReviewTest(unittest.TestCase, NavigationCommon):

    def setUp(self):
        self.driver = NavigationCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()

    def test(self):

        inbox_page = InboxPage(self.driver)
        # inbox_page.send_letter("Message1", "nikuda@mail.ru")
        inbox_page.folders.get_sent_inbox()

        sentPage = SentPage(self.driver)
        sentPage.open_letter("Message1")

        letterPage = LetterPage(self.driver)

        print letterPage.letter_head.is_read_status()
        letterPage.letter_head.change_read_status()
        print letterPage.letter_head.is_read_status()
        letterPage.letter_head.change_read_status()
        print letterPage.letter_head.is_read_status()
        letterPage.letter_head.change_read_status()
        print letterPage.letter_head.is_read_status()

        ###### reply/reply_all
        # inbox_page.folders.get_recieved_inbox()
        # time.sleep(3)

        # letterPage.letter_toolbar.reply()
        # letterPage.letter_toolbar.reply_all()
        # letterPage.letter_toolbar.forward()

        # sent_letter_page = SentLetterPage(self.driver)

        # print "email_to: " + sent_letter_page.data.get_email_to()
        # print "email_copy: " + sent_letter_page.data.get_email_copy()
        # print "subject: " + sent_letter_page.data.get_subject()
        # print "body: " + sent_letter_page.data.get_body()
        pass

    def tearDown(self):
        # NavigationCommon.clear_sent_box(self.driver)
        self.driver.quit()