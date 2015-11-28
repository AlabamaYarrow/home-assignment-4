# -*- coding: utf-8 -*-

import sys
import unittest

from tests import navigation_test, reply_test, letter_data_test, flags_test, moving_test, moar_test


if __name__ == '__main__':
    suite = unittest.TestSuite((

        unittest.makeSuite(navigation_test.NavigatePreviousTest),
        unittest.makeSuite(navigation_test.NavigateMultiplePreviousTest),
        unittest.makeSuite(navigation_test.NavigateReturnTest),
        unittest.makeSuite(navigation_test.NavigateNoPrevTest),

        unittest.makeSuite(navigation_test.NavigateNextTest),
        unittest.makeSuite(navigation_test.NavigateMultipleNextTest),
        unittest.makeSuite(navigation_test.NavigateReturnNextTest),
        unittest.makeSuite(navigation_test.NavigateNoNextTest),

        unittest.makeSuite(reply_test.ReplyEmailToTest),
        unittest.makeSuite(reply_test.ReplySubjectTest),
        unittest.makeSuite(reply_test.ReplyMailTextTest),

        unittest.makeSuite(reply_test.ReplyAllEmailToTest),
        unittest.makeSuite(reply_test.ReplyAllSubjectTest),
        unittest.makeSuite(reply_test.ReplyAllMailTextTest),

        unittest.makeSuite(reply_test.ForwardNoEmailToTest),
        unittest.makeSuite(reply_test.ForwardSubjectTest),
        unittest.makeSuite(reply_test.ForwardMailTextTest),

        unittest.makeSuite(letter_data_test.LetterSubjectTest),
        unittest.makeSuite(letter_data_test.LetterEmailFromTest),
        unittest.makeSuite(letter_data_test.LetterEmailToTest),
        unittest.makeSuite(letter_data_test.LetterDatetimeExistsTest),
        unittest.makeSuite(letter_data_test.LetterBodyExistsTest),

        unittest.makeSuite(flags_test.SetFlagTest),
        unittest.makeSuite(flags_test.UnsetFlagTest),
        unittest.makeSuite(flags_test.SetReadTest),
        unittest.makeSuite(flags_test.UnsetReadTest),

        unittest.makeSuite(moving_test.MoveToTrashTest),
        unittest.makeSuite(moving_test.MoveToSpamTest),
        unittest.makeSuite(moving_test.MoveToArchiveTest),
        unittest.makeSuite(moving_test.MoveToTest),

        unittest.makeSuite(moar_test.MoarMarkUnreadTest),
        unittest.makeSuite(moar_test.MoarMarkReadTest),
        unittest.makeSuite(moar_test.MoarUnsetFlagTest),
        unittest.makeSuite(moar_test.MoarSetFlagTest),


    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
