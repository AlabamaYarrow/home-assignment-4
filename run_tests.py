# -*- coding: utf-8 -*-


import sys
import unittest
from tests.auth_test import AuthTest
from tests.review_test import ReviewTest


if __name__ == '__main__':
    suite = unittest.TestSuite((
        # unittest.makeSuite(AuthTest),
        unittest.makeSuite(ReviewTest),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())