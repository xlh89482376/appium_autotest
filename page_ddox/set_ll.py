from common.baseapi.BaseAppiumApi import BaseAppiumApi
import page_ddox

class set_ll(BaseAppiumApi):
    def __init__(self, driver):
        BaseAppiumApi.__init__(self, driver)

    def click_input_btn(self):
        self.click_element(page_ddox.input_btn)

    def click_start_btn(self):
        self.click_element(page_ddox.start_btn)

    def click_clear_btn(self):
        self.click_element(page_ddox.clear_btn)

    def click_stop_btn(self):
        self.click_element(page_ddox.stop_btn)

    def input_start_ll(self, ll):
        self.input_text(page_ddox.start_ll, ll)

    def input_end_ll(self, ll):
        self.input_text(page_ddox.end_ll, ll)

    def click_commit_btn(self):
        self.click_element(page_ddox.commit_btn)

    def home(self):
        self.do_keyevent(3)
