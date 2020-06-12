import sys, os
sys.path.append(os.getcwd())

from page.page_obj import page_obj
from common.init_driver import init_driver
import pytest, time
from common.tools import tools
import allure
import subprocess
import logging
import functools
from _pytest.runner import runtestprotocol
from _pytest.runner import pytest_runtest_makereport

class Test_admin_create():
    def setup_class(self):
        self.driver = init_driver()
        self.admin_create_obj = page_obj(self.driver).re_admin_create()

    def teardown_class(self):
        self.driver.quit()

    # @getImage
    def test_click_user1(self):
        self.admin_create_obj.click_user1_btn()
        time.sleep(10)

    def take_screenShot(self, name="takeShot"):
        '''
        method explain:获取当前屏幕的截图
        parameter explain：【name】 截图的名称
        Usage:
            device.take_screenShot(u"个人主页")   #实际截图保存的结果为：2018-01-13_17_10_58_个人主页.png
        '''
        day = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        fq = "./screenShots/" + day
        # fq =os.getcwd()[:-4] +'screenShots\\'+day    根据获取的路径，然后截取路径保存到自己想存放的目录下
        tm = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime(time.time()))
        type = '.png'
        filename = ""
        if os.path.exists(fq):
            filename = fq + "/" + tm + "_" + name + type
        else:
            os.makedirs(fq)
            filename = fq + "/" + tm + "_" + name + type
        # c = os.getcwd()
        # r"\\".join(c.split("\\"))     #此2行注销实现的功能为将路径中的\替换为\\
        self.driver.get_screenshot_as_file(filename)


    # def test_click_create(self):
    #     self.admin_create_obj.click_create_btn()
    #     time.sleep(1)
    #     self.take_screenShot("创建")

    # @getImage
    def test_click_start_recogniton(self):
        # self.admin_create_obj.click_start_recognition_btn()
        # time.sleep(6)
        assert False


    #
    # def test_click_cancel(self):
    #     self.admin_create_obj.click_cancel_btn()
    #     time.sleep(1)
    #
    # def test_input_nike_name(self):
    #     self.admin_create_obj.input_nike_name()
    #     time.sleep(1)
    #
    # def test_input_password(self):
    #     self.admin_create_obj.input_password()
    #     time.sleep(1)
    #
    # def test_input_password_confirm(self):
    #     self.admin_create_obj.input_password_confirm()
    #     time.sleep(1)
    #
    # def test_input_safety_answer(self):
    #     self.admin_create_obj.input_safety_answer()
    #     time.sleep(1)
    #
    # def test_next(self):
    #     self.admin_create_obj.click_next()
    #
    # def test_click_complete(self):
    #     self.admin_create_obj.click_complete()
    #     # self.driver.get_screenshot_as_file("111.png")
    #     tools.take_screenShot(self.driver)
