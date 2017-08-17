from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import skip
from functional_tests.base import FunctionalTest

class ItemValidationTest(FunctionalTest):
    #@skip
    def test_cannot_add_empty_list_items(self):
        #Edith goes to the home and accidentally tries to submit
        #an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        input_box = self.get_item_input_box()
        input_box.send_keys(Keys.ENTER)

        #The home page refreshes, and there is an error message saying
        #that list items cannot be blank
        self.wait_for(lambda:self.browser.find_element_by_css_selector('#id_text:invalid'))
        #She tries, again with some text for the item, which now works
        input_box.send_keys('Buy milk')
        input_box.send_keys(Keys.ENTER)
        self.wait_for(lambda:self.browser.find_element_by_css_selector('#id_text:invalid'))

        #Perversely, she now decides to submit a secon blank list item
        input_box = self.get_item_input_box()
        input_box.send_keys(Keys.ENTER)
        #She receives a similar warning on the list page
        self.wait_for(lambda:self.browser.find_element_by_css_selector('#id_text:invalid'))
        #And she can correct it by filling some text in
        input_box = self.get_item_input_box()
        input_box.send_keys('Make Tea')
        input_box.send_keys(Keys.ENTER)
        input_box = self.get_item_input_box()
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make Tea')

    def test_cannot_add_duplicate_items(self):
        #Edith goes to the home page and starts a new list
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy wellies')

        #She accidentally tries to enter a duplicate item
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)

        #She sees a helpful error message
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You've already got this in your list"
            ))