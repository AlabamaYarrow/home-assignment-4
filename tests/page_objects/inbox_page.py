# -*- coding: utf-8 -*-

from base import *


class InboxPage(Page, ClearBoxMixin, WaitForPageLoad):
    PATH = ''

    @property
    def top_status(self):
        return TopStatus(self.driver)

    @property
    def folders(self):
        return Folders(self.driver)

    def send_letter(self, nameLetter, email_to="nikuda@mail.ru", email_copy=""):
        SENTFORM = '//div[@id="b-compose"]'
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
            lambda d: d.find_element_by_xpath(SENTFORM)
                and d.find_element_by_xpath(SENTFORM).get_attribute("style") != "display: none;"
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

    def have_letter(self, subject):
        LETTER = '//a[@data-subject="'+subject+'"]'  
        try:
            self.driver.find_element_by_xpath(LETTER)
            return True
        except NoSuchElementException:   
            return False



class Folders(Component, WaitForPageLoad):
    SENTFOLDER = '//i[contains(@class, "ico_folder_send")]'
    INBOXFOLDER = '//i[contains(@class, "ico_folder_inbox")]'
    SPAMFOLDER = '//i[contains(@class, "ico_folder_spam")]'
    ARCHIVEFOLDER = '//i[contains(@class, "ico_folder_archive")]'
    TRASHFOLDER = '//i[contains(@class, "ico_folder_trash")]'

    def get_sent_inbox(self):
        WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: self.driver.find_element_by_xpath(self.SENTFOLDER)
        )
        with WaitForPageLoad(self.driver):
            self.driver.find_element_by_xpath(self.SENTFOLDER).click()

    def get_recieved_inbox(self):
        with WaitForPageLoad(self.driver):
            self.driver.find_element_by_xpath(self.INBOXFOLDER).click()

    def get_spam_inbox(self):
        with WaitForPageLoad(self.driver):
            self.driver.find_element_by_xpath(self.SPAMFOLDER).click()

    def get_archive_inbox(self):
        with WaitForPageLoad(self.driver):
            self.driver.find_element_by_xpath(self.ARCHIVEFOLDER).click()

    def get_trash_inbox(self):
        with WaitForPageLoad(self.driver):
            self.driver.find_element_by_xpath(self.BINFOLDER).click()