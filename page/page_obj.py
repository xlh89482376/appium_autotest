from page.admin_create import admin_create

class page_obj:
    def __init__(self, driver):
        self.driver = driver

    def re_admin_create(self):
        return admin_create(self.driver)