# -*- coding: utf-8 -*-

from base import *


class LetterPage(Page):
    PATH = ''

    def open(self):
        self.letter_head.get_subject()

    @property
    def letter_head(self):
        return LetterHead(self.driver)

    @property
    def letter_toolbar(self):
        return LetterToolbar(self.driver)


class LetterHead(Component, WaitForPageLoad):
    SUBJECT = '//div[@class="b-letter__head__subj__text"]'
    FROMMAIL = '//div[@data-mnemo="from"]'
    TOEMAIL = "//span[@class='b-letter__head__addrs__value']"
    DATE = "//div[@class='b-letter__head__date']"
    BODY = "//div[@class='js-body b-letter__body__wrap']"
    FLAG = "//div[contains(@class,'b-letter__controls__flag')]/div"
    READSTATUS = "//div[contains(@class,'letter__controls__status')]/div"
    flag_set_class = "b-flag_yes"
    unread_class = "b-letterstatus_unread"

    def get_subject(self):
        return wait_until(self.driver, self.SUBJECT).text

    def get_email_from(self):
        data = wait_until(self.driver, self.FROMMAIL).text
        return data[data.index('<')+1:-1]

    def get_email_to(self):
        return wait_until(self.driver, self.FROMMAIL).text

    def get_date(self):
        return wait_until(self.driver, self.DATE).text

    def get_body(self):
        return wait_until(self.driver, self.BODY).text

    def change_flag(self):
        wait_until(self.driver, self.FLAG).click()

    def is_flag_set(self):          
        return self.flag_set_class in self.driver.find_element_by_xpath(self.FLAG).get_attribute("class")

    def change_read_status(self):
        wait_until(self.driver, self.READSTATUS).click()

    def is_read_status(self):          
        return self.unread_class not in self.driver.find_element_by_xpath(self.READSTATUS).get_attribute("class")


class LetterToolbar(Component, ToolbarJS):
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

    def __init__(self, driver):
        super(LetterToolbar, self).__init__(driver)
        self.toolbar = wait_until(self.driver, self.TOOLBAR)

    def prev_letter_is_disabled(self):
        is_disabled = self.toolbar.find_element_by_xpath(self.PREV).get_attribute(self.ATTRLETTER)
        return is_disabled == u'disabled'

    def next_letter_is_disabled(self):
        is_disabled = self.toolbar.find_element_by_xpath(self.NEXT).get_attribute(self.ATTRLETTER)
        return is_disabled == u'disabled'

    def get_prev_letter(self):
        subject = self.driver.find_element_by_xpath(LetterHead.SUBJECT)
        current_subject_text = subject.text
        self.toolbar.find_element_by_xpath(self.PREV).click()
        WebDriverWait(self.driver, 10, 0.1).until(
            lambda d:
                (d.find_element_by_xpath(LetterHead.SUBJECT).text != current_subject_text)
        )

    def get_next_letter(self):
        subject = self.driver.find_element_by_xpath(LetterHead.SUBJECT)
        current_subject_text = subject.text
        self.toolbar.find_element_by_xpath(self.NEXT).click()
        WebDriverWait(self.driver, 10, 0.1).until(
            lambda d:
                d.find_element_by_xpath(LetterHead.SUBJECT).text != current_subject_text
        )

    def reply(self):
        wait_until(self.toolbar, self.REPLY).click()

    def reply_all(self):
        wait_until(self.toolbar, self.REPLYALL).click()

    def forward(self):
        wait_until(self.toolbar, self.FORWARD).click()

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
        scriptAfterPopup = ToolbarJS.get_spam_confirm_script()

        self.driver.execute_script(scriptBeforePopup)

        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.CONFIRMSPAM)
        )

        self.driver.execute_script(scriptAfterPopup)
