from base import *
import time

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
        inbox_page.send_letter("Message1", "nikuda@mail.ru", "mihail777str@yandex.ru")
        inbox_page.folders.get_sent_inbox()

        sentPage = SentPage(self.driver)
        sentPage.open_letter("Message1")

        letterPage = LetterPage(self.driver)
        # letterPage.letter_toolbar.delete()

        ###### reply/reply_all
        # letterPage.letter_toolbar.reply()
        letterPage.letter_toolbar.reply_all()

        sent_letter_page = SentLetterPage(self.driver)

        print "email_to: " + sent_letter_page.data.get_email_to()
        print "email_copy: " + sent_letter_page.data.get_email_copy()
        print "subject: " + sent_letter_page.data.get_subject()
        print "body: " + sent_letter_page.data.get_body()

    def tearDown(self):
        NavigationCommon.clear_sent_box(self.driver)
        self.driver.quit()