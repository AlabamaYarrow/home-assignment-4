# -*- coding: utf-8 -*-

from base import *


class InboxPage(Page, ClearBoxMixin):
    PATH = '/messages'

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

        wait_until(self.driver, BUTTONSENDFROM).click()
        wait_until(self.driver, EMAILFIELDTO)

        self.driver.find_element_by_xpath(EMAILFIELDTO).send_keys(email_to)
        if email_copy != "":
            self.driver.find_element_by_xpath(EMAILFIELDCOPY).send_keys(email_copy)
        self.driver.find_element_by_xpath(SUBJECTFIELD).send_keys(nameLetter)

        self.driver.switch_to.frame(self.driver.find_element_by_xpath(BODYFRAME))
        self.driver.find_element_by_xpath(BODELETTER).send_keys(nameLetter)
        self.driver.switch_to_default_content()

        wait_until(self.driver, BUTTONSEND).click()

    def have_letter(self, subject):
        letter = '//a[@data-subject="'+subject+'"]'
        try:
            self.driver.find_element_by_xpath(letter)
            return True
        except NoSuchElementException:   
            return False

    def open_letter(self, subject):
        letter = '//a[@data-subject="'+subject+'"]'
        try:
            self.driver.find_element_by_xpath(letter).click()
        except NoSuchElementException:
            self.driver.get(self.driver.current_url)
            self.driver.find_element_by_xpath(letter).click()


class Folders(Component):
    SENTFOLDER = '/sent'
    RECIEVEDFOLDER = '/inbox'
    SPAMFOLDER = '/spam'
    TRASHFOLDER = '/trash'

    def get_sent_inbox(self):
        self.driver.get(Page.BASE_URL + InboxPage.PATH + self.SENTFOLDER)

    def get_recieved_inbox(self):
        self.driver.get(Page.BASE_URL + InboxPage.PATH + self.RECIEVEDFOLDER)

    def get_spam_inbox(self):
        self.driver.get(Page.BASE_URL + InboxPage.PATH + self.SPAMFOLDER)

    def get_trash_inbox(self):
        self.driver.get(Page.BASE_URL + InboxPage.PATH + self.TRASHFOLDER)
