from page_ddox.set_ll import set_ll

class set_ll_page_obj():
    def __init__(self, driver):
        self.driver = driver

    def re_set_ll(self):
        return set_ll(self.driver)