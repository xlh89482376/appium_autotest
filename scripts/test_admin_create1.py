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
        # re_obj.click_user1_btn()
        assert True
        time.sleep(30)
        # assert False
        # assert self.apm.is_element_exist("开始创建")




