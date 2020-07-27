import sys, os, allure, time, pytest
sys.path.append(os.getcwd())

from page.page_obj import page_obj
from common.initdriver.InitDriver import InitDriver
from common.base.Command import Cmd
from common.baseapi.BaseAppiumApi import BaseAppiumApi
from common.utils.FileClearUtil import FileClearUtil
from scripts import conftest as ct
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from airtest.core.api import *


class Test_admin_create():

    # def setup_class(self):
        # fc = FileClearUtil()
        # fc.do_clear_report()
        # fc.do_clear_script_log()
        # self.adb = Cmd()
        # self.driver = InitDriver().init_driver()
        # self.apm = BaseAppiumApi(self.driver)
        # self.admin_create_obj = page_obj(self.driver).re_admin_create()

    # def teardown_class(self):
    #     self.driver.quit()

    # def test_option(self, pytestconfig):
    #     print("'foo' set to:", pytestconfig.getoption('foo'))
    #     print("'myopt' set to:", pytestconfig.getoption('myopt'))

    def test_click_user1(self, re_obj):
        re_obj.click_user1_btn()
        time.sleep(3)
        # assert False
        # assert self.apm.is_element_exist("开始创建")

    @allure.step("点击创建按钮")
    def test_click_create(self, re_obj):
        re_obj.click_create_btn()
        time.sleep(3)
        # driver.quit()

    # def test_click_create(self):
    #     auto_setup(__file__)
    #     connect_device('Android:///')
    #     start_app("com.zhidaoauto.personcenter")
    #     poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
    #     poco(text="开始创建").click()
    #     time.sleep(5)


    def test_meituan(self, apm, re_obj):
        apm.do_start_activity("com.zhidao.com.zhidaoauto.pre.amaplocation", "com.zhidaoauto.pre.amaplocation.MainActivity")
        re_obj.click_meituan_confirm_btn()
        time.sleep(3)
        # assert False

    # @allure.step("点击开始识别按钮")
    # def test_click_start_recogniton(self, re_obj):
    #     re_obj.click_start_recognition_btn()
    #     time.sleep(3)

    #
    # @allure.step("点击取消按钮")
    # def test_click_cancel(self):
    #     self.admin_create_obj.click_cancel_btn()
    #     time.sleep(3)
    #
    # @allure.step("输入昵称")
    # def test_input_nike_name(self):
    #     self.admin_create_obj.input_nike_name()
    #     time.sleep(3)
    #
    # def test_input_password(self):
    #     self.admin_create_obj.input_password()
    #     time.sleep(3)
    #
    # def test_input_password_confirm(self):
    #     self.admin_create_obj.input_password_confirm()
    #     time.sleep(3)
    #
    # def test_input_safety_answer(self):
    #     self.admin_create_obj.input_safety_answer()
    #     time.sleep(3)
    #
    # def test_next(self):
    #     self.admin_create_obj.click_next()
    #     time.sleep(3)
    #
    # def test_click_complete(self):
    #     self.admin_create_obj.click_complete()
    #     time.sleep(10)
    #     assert False


