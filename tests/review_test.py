from base import *
import time


class ReviewTest(unittest.TestCase):

    def setUp(self):
        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, BROWSER).copy()
        )

        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()


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

        inbox_page.folders.get_sent_inbox()
        time.sleep(1)

        sentPage = SentPage(self.driver)
        sentPage.open_letter("Message1")

        time.sleep(1)
        letterPage = LetterPage(self.driver)

        # letterPage.letter_toolbar.delete()

        # reply/reply_all

        letterPage.letter_toolbar.reply()
        # letterPage.letter_toolbar.reply_all()
        # letterPage.letter_toolbar.delete()
        time.sleep(3)

        sent_letter_page = SentLetterPage(self.driver)

        print sent_letter_page.data.get_email_to()
        print sent_letter_page.data.get_email_copy()
        print sent_letter_page.data.get_subject()
        print sent_letter_page.data.get_body()

        # jump to prev/next leter

        # print letterPage.letter_head.get_subject()
        # letterPage.letter_toolbar.get_prev_letter()
        # print letterPage.letter_head.get_subject()
        # letterPage.letter_toolbar.get_next_letter()
        # print letterPage.letter_head.get_subject()