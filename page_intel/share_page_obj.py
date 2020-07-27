from page_intel.share import share
from page.aqy import aqy

class share_page_obj:
    def __init__(self, driver):
        self.driver = driver

    def re_share(self):
        return share(self.driver)

