from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from functional_tests.base import FunctionalTest

class LayOutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        #edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        #She notices the input is nicely centered
        inputbox = self.get_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 
            512, 
            delta=10
        )
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        self.wait_for(self.get_input_box)
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 
            512, 
            delta=10
        )
