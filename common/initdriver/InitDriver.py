import subprocess, re, multiprocessing, os, time, pytest
from appium import webdriver
from common.initdriver.InitConfig import InitConfiger
from common.base.Command import Cmd
from common.utils.LoggingUtil import LoggingController
from common.utils.FilePathUtil import FilePathUtil
from common.utils.ConfigUtil import ConfigController


class InitDriver(object):
    def __init__(self):
        self.log4py = LoggingController()
        self.run_config = InitConfiger()
        self.cmd = Cmd()
        self.service_path = FilePathUtil().get_service_path()
        self.config = ConfigController(self.service_path)

    def init_driver(self):

        desired_caps_dict = self.run_config.get_desired_caps_dict()
        sno_list = self.cmd.get_device_list()
        port = 4723
        print(sno_list)

        if not len(sno_list):
            return None
        for sno in sno_list:
            # self.cmd.set_serialno(sno)
            os.system('appium -p %d' % port)
            self.cmd.serialno = sno
            desired_caps = desired_caps_dict[sno]

            url = 'http://127.0.0.1:%d/wd/hub' % port

            num = 0
            while num <= 5:
                try:
                    driver = webdriver.Remote(url, desired_caps)
                except Exception as e:
                    self.log4py.error("连接appium服务，实例化driver时出错，尝试重连...({})".format(num))
                    num = num + 1
                    continue
                self.log4py.info("webdriver连接信息：{}：{}".format(url, str(desired_caps)))

                while True:
                    if self.cmd.port_is_used(port):
                        port = port+1
                    else:
                        break
                print(port)

                return driver




if __name__ == '__main__':
    i = InitDriver()
    i.init_driver()










