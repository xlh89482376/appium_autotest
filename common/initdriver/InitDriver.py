import subprocess, re, multiprocessing, os, time, pytest
from time import ctime
from appium import webdriver
from common.initdriver.InitConfig import InitConfiger
from common.base.Command import Cmd
from common.utils.LoggingUtil import LoggingController
from common.utils.FilePathUtil import FilePathUtil
from common.utils.ConfigUtil import ConfigController
from concurrent.futures import ProcessPoolExecutor


class InitDriver(object):
    def __init__(self):
        self.log4py = LoggingController()
        self.run_config = InitConfiger()
        self.cmd = Cmd()
        self.service_path = FilePathUtil().get_service_path()
        self.config = ConfigController(self.service_path)

    def get_port(self, sno):
        try:
            port = self.config.get(sno, sno)
            if port:
                self.log4py.info("设备：{} 服务端口：{}".format(sno, port))
            return port
        except Exception as e:
            self.log4py.debug("设备：{} 服务端口：未启动".format(sno))
            return None

    def is_port_used(self, port_num):
        flag = False
        try:
            port_res = subprocess.Popen('netstat -ano | findstr %s | findstr LISTENING' % port_num, shell=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE).stdout.readlines()
            reg = re.compile(str(port_num))
            for i in range(len(port_res)):
                ip_port = port_res[i].strip().split("   ")
                if re.search(reg, ip_port[1]):
                    flag = True
                    self.log4py.info(str(port_num) + " 端口的服务已经启动." )
            if not flag:
                self.log4py.info(str(port_num) + " 端口的服务未启动.")
        except Exception as e:
            self.log4py.error(str(port_num) + " port get occupied status failure: " + str(e))
        return flag

    def init_driver(self):

        desired_caps_dict = self.run_config.get_desired_caps_dict()
        sno_list = self.cmd.get_device_list

        if not len(sno_list):
            return None
        for sno in sno_list:
            # self.cmd.set_serialno(sno)
            self.cmd.serialno = sno
            desired_caps = desired_caps_dict[sno]

            url = 'http://127.0.0.1:4723/wd/hub'

            num = 0
            while num <= 5:
                try:
                    driver = webdriver.Remote(url, desired_caps)
                except Exception as e:
                    self.log4py.error("连接appium服务，实例化driver时出错，尝试重连...({})".format(num))
                    num = num + 1
                    continue
                self.log4py.info("webdriver连接信息：{}：{}".format(url, str(desired_caps)))
                return driver


if __name__ == '__main__':
    pass










