# -*- coding: utf-8 -*-

import os
import urlparse
import unittest
import time

from selenium.webdriver import DesiredCapabilities, Remote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


USER_EMAIL = os.environ['TTHA4USER']
PASSWORD = os.environ['TTHA4PASSWORD']
BROWSER = os.environ.get('TTHA4BROWSER', 'CHROME')


class Page(object):
    BASE_URL = 'https://e.mail.ru/'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
        self.driver.maximize_window()


class Component(object):
    def __init__(self, driver):
        self.driver = driver

def wait_for(condition_function):
    start_time = time.time()
    while time.time() < start_time + 10:
        if condition_function():
            return True
        else:
            time.sleep(0.1)
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )

class WaitForPageLoad(object):
    CHANGEBLOCK = '//div[@class="b-layout  b-layout_flex"]'

    def __init__(self, driver):
        self.driver = driver

    def __enter__(self):
        self.old_page = self.driver.find_element_by_xpath(self.CHANGEBLOCK).text

    def page_has_loaded(self):
        new_page = self.driver.find_element_by_xpath(self.CHANGEBLOCK).text
        return new_page != self.old_page

    def __exit__(self, *_):
        wait_for(self.page_has_loaded)

class ToolbarJS(object):
    ## TODO: перенести переменную scriptFindToolbar в описание класса, а в методах вызывать её

    @staticmethod
    def get_check_all_script():
        scriptFindToolbar = '\
            topTollbar = $(".b-sticky").filter(function () { return $(this).css("z-index") == 100 });\
            rightToolbar = topTollbar.find("#b-toolbar__right").children();\
            visibleToolbar = $(rightToolbar).filter(function () { return $(this).css("display") != "none" });'

        return scriptFindToolbar + '\
        checkbox = visibleToolbar.find(".b-checkbox__checkmark");\
        checkbox.click();'

    @staticmethod
    def get_delete_script():
        scriptFindToolbar = '\
            topTollbar = $(".b-sticky").filter(function () { return $(this).css("z-index") == 100 });\
            rightToolbar = topTollbar.find("#b-toolbar__right").children();\
            visibleToolbar = $(rightToolbar).filter(function () { return $(this).css("display") != "none" });'

        return scriptFindToolbar + '\
        deleteBtn = visibleToolbar.find("span").filter(function () { return $(this).text() == "Удалить" });\
        deleteBtn.click();'


class AuthPage(Page):
    PATH = ''

    @property
    def form(self):
        return AuthForm(self.driver)

    def authenticate(self):
        self.form.set_login(USER_EMAIL)
        self.form.set_password(PASSWORD)
        self.form.submit()


class ClearBoxMixin(WaitForPageLoad, ToolbarJS):
    EMPTYFOLDER = '//span[contains(text(), "У вас нет отправленных писем")]'

    def clear_box(self, driver):
        try:
            self.driver.find_element_by_xpath(self.EMPTYFOLDER)
        except NoSuchElementException:
            scriptCheckAll = ToolbarJS.get_check_all_script()
            scriptDelete = ToolbarJS.get_delete_script()

            driver.execute_script(scriptCheckAll)
            with WaitForPageLoad(self.driver):
                driver.execute_script(scriptDelete)


class InboxPage(Page, ClearBoxMixin, WaitForPageLoad):
    PATH = ''

    @property
    def top_status(self):
        return TopStatus(self.driver)

    @property
    def folders(self):
        return Folders(self.driver)

    def send_letter(self, nameLetter, email_to="nikuda@mail.ru", email_copy=""):
        BUTTONSENDFROM = '//span[contains(text(), "Написать письмо")]'
        BUTTONSEND = '//span[contains(text(), "Отправить")]'
        EMAILFIELDTO = '//textarea[@data-original-name="To"]'
        EMAILFIELDCOPY = '//textarea[@data-original-name="CC"]'
        SUBJECTFIELD = '//input[@name="Subject"]'
        BODYFRAME = '//iframe[starts-with(@id,"compose_")]'
        BODELETTER = '//body'
        SENTSTATUS = '//div[@class="message-sent__title"]'

        with WaitForPageLoad(self.driver):
            self.driver.find_element_by_xpath(BUTTONSENDFROM).click()

        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(EMAILFIELDTO)
        )

        self.driver.find_element_by_xpath(EMAILFIELDTO).send_keys(email_to)
        if email_copy != "":
            self.driver.find_element_by_xpath(EMAILFIELDCOPY).send_keys(email_copy)
        self.driver.find_element_by_xpath(SUBJECTFIELD).send_keys(nameLetter)

        self.driver.switch_to.frame(self.driver.find_element_by_xpath(BODYFRAME))
        self.driver.find_element_by_xpath(BODELETTER).send_keys(nameLetter)
        self.driver.switch_to_default_content()

        with WaitForPageLoad(self.driver):
            self.driver.find_element_by_xpath(BUTTONSEND).click()


class SentLetterPage(Page):
    PATH = ''

    @property
    def data(self):
        return SentLetterData(self.driver)


class SentPage(Page, ClearBoxMixin, WaitForPageLoad):
    PATH = '/messages/sent/'


    def wait_for_letter(self, subject):
        letter = '//a[@data-subject="'+subject+'"]'
        while True:
            try:
                self.driver.find_element_by_xpath(letter)
                break
            except NoSuchElementException:
                self.open()

    def open_letter(self, subject):
        LETTER = '//a[@data-subject="'+subject+'"]'
        with WaitForPageLoad(self.driver):
            self.driver.find_element_by_xpath(LETTER).click()



class LetterPage(Page):
    PATH = ''

    @property
    def letter_head(self):
        return LetterHead(self.driver)

    @property
    def letter_toolbar(self):
        return LetterToolbar(self.driver)       


class AuthForm(Component):
    LOGIN = '//input[@name="Login"]'
    PASSWORD = '//input[@name="Password"]'
    SUBMIT = '//button[contains(concat(" ", @class, " "), " js-login-page__external__submit ")]'

    def set_login(self, login):
        self.driver.find_element_by_xpath(self.LOGIN).send_keys(login)

    def set_password(self, pwd):
        self.driver.find_element_by_xpath(self.PASSWORD).send_keys(pwd)

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT).click()


class TopStatus(Component):
    EMAIL = '//i[@id="PH_user-email"]'

    def get_email(self):
        return self.driver.find_element_by_xpath(self.EMAIL).text


class Folders(Component, WaitForPageLoad):
    SENTFOLDER = '//i[contains(@class, "ico_folder_send")]'
    
    def get_sent_inbox(self):
        ICO = self.driver.find_element_by_xpath(self.SENTFOLDER)
        classes = ICO.find_element_by_xpath("../../..").get_attribute("class")
        if "b-nav__item_active" not in classes:
            with WaitForPageLoad(self.driver):
                self.driver.find_element_by_xpath(self.SENTFOLDER).click()


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
    ARCHIVE = '//span[text() = "В архив"]'
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
        scriptDelete = ToolbarJS.get_delete_script()
        with WaitForPageLoad(self.driver):
            self.driver.execute_script(scriptDelete)

    # def archive(self):
    #     toolbar = self.driver.find_element_by_xpath(self.TOOLBAR)
    #     toolbar.find_element_by_xpath(self.ARCHIVE).click()

class SentLetterData(Component):
    EMAILBLOCKTO = '//div[contains(@class,"js-row-To")]'
    EMAILBLOCKCOPY = '//div[contains(@class,"js-row-CC")]'
    EMAILFIELD = 'compose__header__field__box'
    SUBJECTFIELD = '//input[@name="Subject"]'
    BODYFRAME = '//iframe[starts-with(@id,"compose_")]'
    BODELETTER = '//body'

    def get_email_to(self):
        emailToBlock = self.driver.find_element_by_xpath(self.EMAILBLOCKTO)
        return emailToBlock.find_element_by_class_name(self.EMAILFIELD).text

    def get_email_copy(self):
        emailCopyBlock = self.driver.find_element_by_xpath(self.EMAILBLOCKCOPY)
        return emailCopyBlock.find_element_by_class_name(self.EMAILFIELD).text

    def get_subject(self):
        return self.driver.find_element_by_xpath(self.SUBJECTFIELD).get_attribute("value")

    def get_body(self):
        self.driver.switch_to.frame(self.driver.find_element_by_xpath(self.BODYFRAME))
        body = self.driver.find_element_by_xpath(self.BODELETTER).text
        self.driver.switch_to_default_content()
        return body
