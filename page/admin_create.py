from common.base import base
import page, time

class admin_create(base):
    def __init__(self, driver):
        base.__init__(self, driver)

    def click_admin_btn(self):
        self.click_element(page.admin_btn)

    def click_user1_btn(self):
        self.click_element(page.user1_btn)

    def click_create_btn(self):
        self.click_element(page.create_btn)

    def click_start_recognition_btn(self):
        self.click_element(page.start_recognition_btn)

    def click_cancel_btn(self):
        self.click_element(page.cancel_btn)

    def input_nike_name(self):
        self.input_text(page.nike_name_txt, "1111")

    def input_password(self):
        self.input_text(page.password_txt, "111111")

    def input_password_confirm(self):
        self.input_text(page.password_confirm_txt, "111111")

    def input_safety_answer(self):
        self.input_text(page.safety_answer_txt, "1111")

    def click_next(self):
        self.click_element(page.next_btn)

    def click_complete(self):
        self.click_element(page.complete_btn)