# -*- coding: utf-8 -*-

import sys
import unittest

from tests.review_test import ReviewTest
from tests import auth_test, navigation_test, reply_test


if __name__ == '__main__':
    suite = unittest.TestSuite((
        # unittest.makeSuite(auth_test.AuthTest),
        # unittest.makeSuite(ReviewTest),

        unittest.makeSuite(navigation_test.NavigatePreviousTest),
        # unittest.makeSuite(navigation_test.NavigateMultiplePreviousTest),
        # unittest.makeSuite(navigation_test.NavigateReturnTest),
        # unittest.makeSuite(navigation_test.NavigateNoPrevTest),
        #
        # unittest.makeSuite(navigation_test.NavigateNextTest),
        # unittest.makeSuite(navigation_test.NavigateMultipleNextTest),
        # unittest.makeSuite(navigation_test.NavigateReturnNextTest),
        # unittest.makeSuite(navigation_test.NavigateNoNextTest),

        # unittest.makeSuite(reply_test.ReplyTest),

    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
