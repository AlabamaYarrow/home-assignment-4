# -*- coding: utf-8 -*-

from base import *


class LetterPage(Page):
    PATH = ''

    @property
    def letter_head(self):
        return LetterHead(self.driver)

    @property
    def letter_toolbar(self):
        return LetterToolbar(self.driver)


class LetterHead(Component):
    SUBJECT = '//div[@class="b-letter__head__subj__text"]'

    def get_subject(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.SUBJECT)
        )
        return self.driver.find_element_by_xpath(self.SUBJECT).text


class LetterToolbar(Component, WaitForPageLoad, ToolbarJS):
    TOOLBAR = '//div[@data-mnemo="toolbar-letter"]'
    NEXT = '//div[@data-name="letter_next"]'
    PREV = '//div[@data-name="letter_prev"]'
    REPLY = '//span[text() = "Ответить"]'
    REPLYALL = '//span[text() = "Ответить всем"]'
    FORWARD = '//span[text() = "Переслать"]'
    DELETE = '//span[text() = "Удалить"]'
    ARCHIVEDROP = '//div[@data-shortcut="e: \'archive\' "]'
    ARCHIVE = '//span[text() = "В архив"]'
    CONFIRMSPAM = '//div[@class = "is-confirmSpam_in"]'
    ATTRLETTER = 'aria-disabled'

    def prev_letter_is_disabled(self):
        toolbar = self.driver.find_element_by_xpath(self.TOOLBAR)
        is_disabled = toolbar.find_element_by_xpath(self.PREV).get_attribute(self.ATTRLETTER)
        return is_disabled == u'disabled'

    def next_letter_is_disabled(self):
        toolbar = self.driver.find_element_by_xpath(self.TOOLBAR)
        is_disabled = toolbar.find_element_by_xpath(self.NEXT).get_attribute(self.ATTRLETTER)
        return is_disabled == u'disabled'

    def get_prev_letter(self):
        toolbar = self.driver.find_element_by_xpath(self.TOOLBAR)
        subject = self.driver.find_element_by_xpath(LetterHead.SUBJECT)
        current_subject_text = subject.text
        toolbar.find_element_by_xpath(self.PREV).click()
        WebDriverWait(self.driver, 10, 0.1).until(
            lambda d:
                (d.find_element_by_xpath(LetterHead.SUBJECT).text != current_subject_text)
        )

    def get_next_letter(self):
        toolbar = self.driver.find_element_by_xpath(self.TOOLBAR)
        subject = self.driver.find_element_by_xpath(LetterHead.SUBJECT)
        current_subject_text = subject.text
        toolbar.find_element_by_xpath(self.NEXT).click()
        WebDriverWait(self.driver, 10, 0.1).until(
            lambda d:
                d.find_element_by_xpath(LetterHead.SUBJECT).text != current_subject_text
        )

    def reply(self):
        toolbar = self.driver.find_element_by_xpath(self.TOOLBAR)
        with WaitForPageLoad(self.driver):
            toolbar.find_element_by_xpath(self.REPLY).click()

    def reply_all(self):
        toolbar = self.driver.find_element_by_xpath(self.TOOLBAR)
        with WaitForPageLoad(self.driver):
            toolbar.find_element_by_xpath(self.REPLYALL).click()

    def forward(self):
        toolbar = self.driver.find_element_by_xpath(self.TOOLBAR)
        with WaitForPageLoad(self.driver):
            toolbar.find_element_by_xpath(self.FORWARD).click()

    def delete(self):
        script = ToolbarJS.get_delete_script()
        with WaitForPageLoad(self.driver):
            self.driver.execute_script(script)

    def archive(self):
        script = ToolbarJS.get_archive_script()
        with WaitForPageLoad(self.driver):
            self.driver.execute_script(script)

    def spam(self):
        scriptBeforePopup = ToolbarJS.get_spam_script()
        scriptAfterPopup  = ToolbarJS.get_spam_confirm_script()

        self.driver.execute_script(scriptBeforePopup)

        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.CONFIRMSPAM)
        )

        self.driver.execute_script(scriptAfterPopup)

