# -*- coding: utf-8 -*-

from base import *


class SentPage(Page, ClearBoxMixin, WaitForPageLoad):
    def wait_for_letter(self, subject):
        letter = '//a[@data-subject="'+subject+'"]'
        while True:
            try:
                self.driver.find_element_by_xpath(letter)
                break
            except NoSuchElementException:
                self.open()

    def open_letter(self, subject):
        LETTER = '//div[@class="b-layout  b-layout_flex"]\
        //div[contains(@data-cache-key, "undefined") and not(contains(@style,"display: none"))]\
        //a[@data-subject="'+subject+'"]'

        with WaitForPageLoad(self.driver):
            self.driver.find_element_by_xpath(LETTER).click()