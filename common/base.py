from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

class base:
    def __init__(self, driver):
        self.driver = driver

    def find_element_I(self,loc,timeout=10,poll=0.5):
        return WebDriverWait(self.driver,timeout,poll).until(lambda x:x.find_element(*loc))

    def find_elements_I(self,loc,timeout=10,poll=0.5):
        return WebDriverWait(self.driver,timeout,poll).until(lambda x:x.find_elements(*loc))

    def click_element(self,loc):
        self.find_element_I(loc).click()

    def click_elements(self,loc,num):
        self.find_elements_I(loc)[num].click()

    def input_text(self,loc,text):
        input = self.find_element_I(loc)
        input.clear()
        input.send_keys(text)

    def swipe(self,start_x, start_y, end_x, end_y, duration):
        return self.driver.swipe(start_x, start_y, end_x, end_y, duration)

