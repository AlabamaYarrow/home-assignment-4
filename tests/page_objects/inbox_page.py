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
            lambda d: d.find_element_by_xpath(EMAILFIELDTO) and
            self.driver.find_element_by_xpath(BUTTONSEND)
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


class Folders(Component, WaitForPageLoad):
    SENTFOLDER = '//i[contains(@class, "ico_folder_send")]'

    def get_sent_inbox(self):
        # ICO = self.driver.find_element_by_xpath(self.SENTFOLDER)
        # classes = ICO.find_element_by_xpath("../../..").get_attribute("class")
        # if "b-nav__item_active" not in classes:
        with WaitForPageLoad(self.driver):
            self.driver.find_element_by_xpath(self.SENTFOLDER).click()