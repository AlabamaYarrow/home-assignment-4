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


class LetterHead(Component, WaitForPageLoad):
    SUBJECT = '//div[@class="b-letter__head__subj__text"]'
    FROMEMAIL = '//div[@data-mnemo="from"]'
    TOEMAIL = "//span[@class='b-letter__head__addrs__value']"
    DATE = "//div[@class='b-letter__head__date']"
    BODY = "//div[@class='js-body b-letter__body__wrap']"
    FLAG = "//div[contains(@class,'b-letter__controls__flag')]/div"
    READSTATUS = "//div[contains(@class,'letter__controls__status')]/div"
    flag_set_class = "b-flag_yes"
    unread_class = "b-letterstatus_unread"

    def get_subject(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.SUBJECT)
        )
        return self.driver.find_element_by_xpath(self.SUBJECT).text

    def get_email_from(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.FROMEMAIL)
        )
        data = self.driver.find_element_by_xpath(self.FROMEMAIL).text
        return data[data.index('<')+1:-1]

    def get_email_to(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.TOEMAIL)
        )
        return self.driver.find_element_by_xpath(self.TOEMAIL).text

    def get_date(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.DATE)
        )
        return self.driver.find_element_by_xpath(self.DATE).text

    def get_body(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.BODY)
        )
        return self.driver.find_element_by_xpath(self.BODY).text

    def change_flag(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.FLAG)
        )
        self.driver.find_element_by_xpath(self.FLAG).click()

    def is_flag_set(self):          
        return self.flag_set_class in self.driver.find_element_by_xpath(self.FLAG).get_attribute("class")

    def change_read_status(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.READSTATUS)
        )
        self.driver.find_element_by_xpath(self.READSTATUS).click()

    def is_read_status(self):          
        return self.unread_class not in self.driver.find_element_by_xpath(self.READSTATUS).get_attribute("class")


class LetterToolbar(Component, WaitForPageLoad):
    TOOLBAR = '//div[contains(@id,"b-toolbar__right")]\
        /div[not(contains(@style,"display: none"))]'
    NEXT = '//div[@data-name="letter_next"]'
    PREV = '//div[@data-name="letter_prev"]'
    REPLY = '//span[text() = "Ответить"]'
    REPLYALL = '//span[text() = "Ответить всем"]'
    FORWARD = '//span[text() = "Переслать"]'
    CONFIRMSPAM = '//div[@class = "is-confirmSpam_in"]'
    ATTRLETTER = 'aria-disabled'
    DELETE = '//div[@data-name="remove"]'
    ARCHIVEDROP = '//div[contains(@data-shortcut,"archive")]'
    ARCHIVE = '//div[contains(@class,"b-dropdown__list")]/a'
    SPAM = '//div[@data-name="spam"]'
    SPAMPOOPUP = '//div[@class="is-confirmSpam_in"]//button[contains(@class,"confirm-cancel")]'
    MORE = '//div[@class="b-sticky" and not (contains(@style,"visibility: hidden;"))]\
        //div[@data-group="letter-more"]/div'
    MOREREAD = '//a[@data-name="read"]'
    MOREUNREAD = '//a[@data-name="unread"]'
    FLAGYES = '//a[@data-name="flag_yes"]'
    FLAGNO = '//a[@data-name="flag_no"]'

    def prev_letter_is_disabled(self):
        toolbar = self.driver.find_element_by_xpath(self.TOOLBAR)
        is_disabled = toolbar.find_element_by_xpath(self.PREV).get_attribute(self.ATTRLETTER)
        return is_disabled == u'disabled'

    def next_letter_is_disabled(self):
        toolbar = self.driver.find_element_by_xpath(self.TOOLBAR)
        is_disabled = toolbar.find_element_by_xpath(self.NEXT).get_attribute(self.ATTRLETTER)
        return is_disabled == u'disabled'

    def get_prev_letter(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.TOOLBAR)
        )
        with WaitForPageLoad(self.driver):
            self.driver.find_element_by_xpath(self.TOOLBAR + self.PREV).click()

    def get_next_letter(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.TOOLBAR)
        )
        with WaitForPageLoad(self.driver):
            self.driver.find_element_by_xpath(self.TOOLBAR + self.NEXT).click()

    def reply(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.TOOLBAR)
        )
        with WaitForPageLoad(self.driver):
            self.driver.find_element_by_xpath(self.TOOLBAR + self.REPLY).click()

    def reply_all(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.TOOLBAR)
        )
        with WaitForPageLoad(self.driver):
            self.driver.find_element_by_xpath(self.TOOLBAR + self.REPLYALL).click()

    def forward(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.TOOLBAR)
        )
        with WaitForPageLoad(self.driver):
            self.driver.find_element_by_xpath(self.TOOLBAR + self.FORWARD).click()

    def delete(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.TOOLBAR)
        )
        with WaitForPageLoad(self.driver):
            self.driver.find_element_by_xpath(self.TOOLBAR + self.DELETE).click()

    def archive(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.TOOLBAR + self.ARCHIVEDROP)
        )

        self.driver.find_element_by_xpath(self.TOOLBAR + self.ARCHIVEDROP).click()

        with WaitForPageLoad(self.driver):
            self.driver.find_element_by_xpath(self.TOOLBAR + self.ARCHIVE).click()

    def spam(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.TOOLBAR)
        )
        self.driver.find_element_by_xpath(self.TOOLBAR + self.SPAM).click()

        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.SPAMPOOPUP)
        )

        with WaitForPageLoad(self.driver):
            self.driver.find_element_by_xpath(self.SPAMPOOPUP).click()

    def more_unread(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.MORE)
        )
        self.driver.find_element_by_xpath(self.MORE).click()

        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.MOREUNREAD)
        )
        self.driver.find_element_by_xpath(self.MOREUNREAD).click()

    def more_read(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.MORE)
        )
        self.driver.find_element_by_xpath(self.MORE).click()

        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.MOREREAD)
        )
        self.driver.find_element_by_xpath(self.MOREREAD).click()

    def more_flag_yes(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.MORE)
        )
        self.driver.find_element_by_xpath(self.MORE).click()

        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.FLAGYES)
        )
        self.driver.find_element_by_xpath(self.FLAGYES).click()

    def more_flag_no(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.MORE)
        )
        self.driver.find_element_by_xpath(self.MORE).click()

        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.FLAGNO)
        )
        self.driver.find_element_by_xpath(self.FLAGNO).click()