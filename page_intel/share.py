from common.baseapi.BaseAppiumApi import BaseAppiumApi
import page_intel

class share(BaseAppiumApi):
    def __init__(self, driver):
        BaseAppiumApi.__init__(self, driver)

    def click_start_btn(self):
        self.click_element(page_intel.start_btn)

    def click_share_btn(self):
        self.click_element(page_intel.share_btn)

    def click_shigu_btn(self):
        self.click_element(page_intel.shigu_btn)

    def click_lukuang_btn(self):
        self.click_element(page_intel.lukuang_btn)

    def find_toast(self):
        return self.get_toast(page_intel.share_successd_toast)