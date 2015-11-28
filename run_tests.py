# -*- coding: utf-8 -*-

import sys
import unittest

from tests import navigation_test, reply_test, letter_data_test, flags_test, moving_test, moar_test


if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(navigation_test.NavigateTest),
        unittest.makeSuite(reply_test.ReplyTest),
        unittest.makeSuite(letter_data_test.LetterDataTest),
        unittest.makeSuite(flags_test.FlagsTest),
        unittest.makeSuite(moving_test.MoveTest),
        unittest.makeSuite(moar_test.MoarTest),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
