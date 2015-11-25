# -*- coding: utf-8 -*-

from base import *


class SentLetterPage(Page):
    PATH = ''

    @property
    def data(self):
        return SentLetterData(self.driver)


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
