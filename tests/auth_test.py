from base import *


class AuthTest(unittest.TestCase):

    def setUp(self):
        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, BROWSER).copy()
        )
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authenticate()

    def test(self):
        inbox_page = InboxPage(self.driver)
        email = inbox_page.top_status.get_email()
        self.assertEquals(email, USER_EMAIL)

    def tearDown(self):
        self.driver.quit()
