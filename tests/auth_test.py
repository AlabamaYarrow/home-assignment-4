import os
import unittest
from base import *

class AuthTest(unittest.TestCase):
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
        self.driver.quit()

    def testAuth(self):
        inbox_page = InboxPage(self.driver)
        email = inbox_page.top_status.get_email()

        self.assertEquals(email, self.USER_EMAIL)
        


        

