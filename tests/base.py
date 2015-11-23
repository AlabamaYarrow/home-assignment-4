# -*- coding: utf-8 -*-

import os

import urlparse

import unittest

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


class AuthPage(Page):
    PATH = ''

    @property
    def form(self):
        return AuthForm(self.driver)

    def authenticate(self):
        self.form.set_login(USER_EMAIL)
        self.form.set_password(PASSWORD)
        self.form.submit()


class InboxPage(Page):
    PATH = ''

    @property
    def top_status(self):
        return TopStatus(self.driver)

    @property
    def folders(self):
        return Folders(self.driver)

    def send_letter(self, nameLetter):
        BUTTONSENDFROM = '//span[contains(text(), "Написать письмо")]'
        BUTTONSEND = '//span[contains(text(), "Отправить")]'
        EMAILFIELD = '//textarea[@data-original-name="To"]'
        SUBJECTFIELD = '//input[@name="Subject"]'
        BODYFRAME = '//iframe[starts-with(@id,"compose_")]'
        BODELETTER = '//body'
        EMAIL = "nikuda@mail.ru"
        SENTSTATUS = '//div[@class="message-sent__title"]'

        self.driver.find_element_by_xpath(BUTTONSENDFROM).click()

        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(EMAILFIELD)
        )

        self.driver.find_element_by_xpath(EMAILFIELD).send_keys(EMAIL)
        self.driver.find_element_by_xpath(SUBJECTFIELD).send_keys(nameLetter)

        self.driver.switch_to.frame(self.driver.find_element_by_xpath(BODYFRAME))
        self.driver.find_element_by_xpath(BODELETTER).send_keys(nameLetter)
        self.driver.switch_to_default_content()

        self.driver.find_element_by_xpath(BUTTONSEND).click()

        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(SENTSTATUS)
        )


class SentLetterPage(Page):
    PATH = ''

    @property
    def data(self):
        return SentLetterData(self.driver)


class SentPage(Page):
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
        letter = '//a[@data-subject="'+subject+'"]'
        url = self.driver.find_element_by_xpath(letter).get_attribute('href')
        self.driver.get(url)

    def clear_box(self):
        CHECKBOX = '//div[@class="b-checkbox__checkmark"]'
        DELETEBTN = '//span[contains(text(), "Удалить")]'

        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(CHECKBOX)
        )

        self.driver.find_element_by_xpath(CHECKBOX).click()
        self.driver.find_element_by_xpath(DELETEBTN).click()


class LetterPage(Page):
    PATH = ''

    @property
    def letter_head(self):
        return LetterHead(self.driver)

    @property
    def letter_toolbar(self):
        return LetterToolbar(self.driver)       

    def clear_box(self):
        CHECKBOX = '//div[@class="b-checkbox__checkmark"]'
        DELETEBTN = '//span[contains(text(), "Удалить")]'

        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(CHECKBOX)
        )

        self.driver.find_element_by_xpath(CHECKBOX).click()
        self.driver.find_element_by_xpath(DELETEBTN).click()


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


class Folders(Component):
    SENTFOLDER = '//i[contains(@class, "ico_folder_send")]'
    
    def get_sent_inbox(self):
        self.driver.find_element_by_xpath(self.SENTFOLDER).click()


class LetterHead(Component):
    SUBJECT = '//div[@class="b-letter__head__subj__text"]'
    
    def get_subject(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.SUBJECT)
        )
        return self.driver.find_element_by_xpath(self.SUBJECT).text


class LetterToolbar(Component):
    NEXT = '//div[@data-name="letter_next"]'
    PREV = '//div[@data-name="letter_prev"]'
    REPLY = '//span[text() = "Ответить"]'
    REPLY = '//span[text() = "Ответить всем"]'
    ATTRLETTER = 'aria-disabled'

    def prev_letter_is_disabled(self):
        is_disabled = self.driver.find_element_by_xpath(self.PREV).get_attribute(ATTRLETTER)
        return is_disabled == u'disabled'

    def next_letter_is_disabled(self):
        is_disabled = self.driver.find_element_by_xpath(self.NEXT).get_attribute(ATTRLETTER)
        return is_disabled == u'disabled'

    def get_prev_letter(self):
        return self.driver.find_element_by_xpath(self.PREV).click()

    def get_next_letter(self):
        return self.driver.find_element_by_xpath(self.NEXT).click()

    def reply(self):
        return self.driver.find_element_by_xpath(self.REPLY).click()

    def reply_all(self):
        return self.driver.find_element_by_xpath(self.REPLY).click()


class SentLetterData(Component):
    EMAILBLOCK = '//div[contains(@class,"js-row-To")]'
    EMAILFIELD = '//div[contains(@class,"compose__header__field__box")]'
    SUBJECTFIELD = '//input[@name="Subject"]'
    BODYFRAME = '//iframe[starts-with(@id,"compose_")]'
    BODELETTER = '//body'

    def get_email(self):
        emailBlock = self.driver.find_element_by_xpath(self.EMAILBLOCK)
        return emailBlock.find_element_by_xpath(self.EMAILFIELD).text

    def get_subject(self):
        return self.driver.find_element_by_xpath(self.SUBJECTFIELD).get_attribute("value")

    def get_body(self):
        self.driver.switch_to.frame(self.driver.find_element_by_xpath(self.BODYFRAME))
        return self.driver.find_element_by_xpath(self.BODELETTER).text