from common.baseapi.BaseAppiumApi import BaseAppiumApi
import page

class aqy(BaseAppiumApi):
    def __init__(self, driver):
        BaseAppiumApi.__init__(self, driver)

    # 点击确定按钮
    def click_confirm(self):
        self.click_element(page.confirm_button)

    # 点击我的按钮
    def click_my(self):
        self.click_element(page.my_btn)

    # 点击未登录
    def click_no_login(self):
        self.click_element(page.no_login_btn)

    # 点击其他方式登录
    def click_other_login(self):
        self.click_element(page.other_login_btn)

    # 点击密码登录
    def click_password_login(self):
        self.click_element(page.password_login_btn)

    # 点击输入手机号输入框
    def click_phone_edit(self):
        self.click_element(page.phone_edit_text)

    # 输入phone
    def input_phone(self):
        self.input_text(page.phone_edit_text, '13581683031')

    # 点击password
    def click_password_edit(self):
        self.click_element(page.password_login_btn)

    # 输入password
    def input_password(self):
        self.input_text(page.password_login_btn, 'xlh89482376')

    # 点击login
    def click_login(self):
        self.click_element(page.login_btn)

    # 点击搜索
    def click_search(self):
        self.click_element(page.search_btn)

    # 点击搜索框
    def click_search_edit_text(self):
        self.click_element(page.search_edit_text)

    # 输入搜索内容
    def input_search(self):
        self.input_text(page.search_edit_text, "新世界")

    # 点击搜索
    def enter_search(self):
        self.click_elements(page.search_result, 0)

    # 点击继续播放
    def continue_play(self):
        self.click_element(page.continue_play_btn)




