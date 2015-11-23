from base import *


class NavigationCommon(object):
    @staticmethod
    def fill_sent_box(driver):
        inbox_page = InboxPage(driver)
        inbox_page.send_letter('1')
        inbox_page.send_letter('2')
        inbox_page.send_letter('3')

    @staticmethod
    def clear_sent_box(driver):
        sent_page = SentPage(driver)
        sent_page.open()
        sent_page.clear_box()

    @staticmethod
    def get_driver():
        return Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, BROWSER).copy()
        )


class NavigatePreviousTest(unittest.TestCase, NavigationCommon):

    def setUp(self):
        self.driver = NavigationCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        NavigationCommon.fill_sent_box(self.driver)

    def test(self):
        sent_page = SentPage(self.driver)
        sent_page.open()
        sent_page.wait_for_letter('2')
        sent_page.open_letter('2')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.get_prev_letter()
        subject = letter_page.letter_head.get_subject()
        self.assertEquals('1', subject)

    def tearDown(self):
        NavigationCommon.clear_sent_box(self.driver)
        self.driver.quit()


class NavigateMultiplePreviousTest(unittest.TestCase, NavigationCommon):

    def setUp(self):
        self.driver = NavigationCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        NavigationCommon.fill_sent_box(self.driver)

    def test(self):
        sent_page = SentPage(self.driver)
        sent_page.open()
        sent_page.wait_for_letter('3')
        sent_page.open_letter('3')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.get_prev_letter()
        letter_page.letter_toolbar.get_prev_letter()
        subject = letter_page.letter_head.get_subject()
        self.assertEquals('1', subject)

    def tearDown(self):
        NavigationCommon.clear_sent_box(self.driver)
        self.driver.quit()


class NavigateReturnTest(unittest.TestCase, NavigationCommon):

    def setUp(self):
        self.driver = NavigationCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        NavigationCommon.fill_sent_box(self.driver)

    def test(self):
        sent_page = SentPage(self.driver)
        sent_page.open()
        sent_page.wait_for_letter('3')
        sent_page.open_letter('3')

        letter_page = LetterPage(self.driver)
        letter_page.letter_toolbar.get_prev_letter()
        letter_page.letter_toolbar.get_next_letter()
        subject = letter_page.letter_head.get_subject()
        self.assertEquals('3', subject)

    def tearDown(self):
        NavigationCommon.clear_sent_box(self.driver)
        self.driver.quit()


class NavigateNoForwardTest(unittest.TestCase, NavigationCommon):

    def setUp(self):
        self.driver = NavigationCommon.get_driver()
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()
        NavigationCommon.fill_sent_box(self.driver)

    def test(self):
        sent_page = SentPage(self.driver)
        sent_page.open()
        sent_page.wait_for_letter('3')
        sent_page.open_letter('3')

        letter_page = LetterPage(self.driver)
        is_disabled = letter_page.letter_toolbar.prev_letter_is_disabled()
        self.assertEquals(True, is_disabled)

    def tearDown(self):
        NavigationCommon.clear_sent_box(self.driver)
        self.driver.quit()



