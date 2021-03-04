# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@author  :  Xuanlh  
@file    :  PerformenceManager.py
@since   :  2021/3/3 4:09 PM
@desc    :  所有控制功能都在这里
"""

import time, threading, os
from common.utils.PerformenceUtils.Monitor import Monitor
from common.utils.PerformenceUtils.OperatePick import OperatePick

PROJECT_PATH = os.getcwd().split('appium_autotest')[0] + 'appium_autotest' + os.sep + 'performence' + os.sep
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(os.path.realpath('__file__')), p))
pick= OperatePick()

class PerformenceManager():

    def __init__(self, packageName, serialno):
        self.monitor = Monitor(packageName, serialno)
        self.t1 = threading.Thread(target=self.write_pickle)
        self.flag = False
        self.__serialno = serialno
        self.info_path = PROJECT_PATH + os.sep + 'result' + os.sep + self.__serialno + os.sep + 'info' + os.sep
        self.battery_path = PATH(self.info_path + 'battery.pickle')
        self.mem_path = PATH(self.info_path + 'memory.pickle')
        self.cpu_path = PATH(self.info_path + 'cpu.pickle')
        self.jiff_path = PATH(self.info_path + 'jiff.pickle')
        self.fps_path = PATH(self.info_path + 'fps.pickle')
        self.report_path = PROJECT_PATH + 'report' + os.sep

    def write_pickle(self):
        while True:
            self.monitor.write_cpu_rate()
            self.monitor.write_mem()
            self.monitor.write_fps()
            time.sleep(5)
            if self.flag:
                break

    def run(self):
        """
        性能监控的 启动 方法
        @return:
        """
        self.monitor.init()
        self.t1.start()

    def stop(self):
        """
        性能监控的 停止 方法
        @return:
        """
        self.flag = True

    def create_report(self):
        """
        性能监控的 创建报告 方法
        @return:
        """
        self.monitor.report()


if __name__ == '__main__':
    packageName = "com.mogo.launcher.f"
    serialno = "ZD80123823728"
    pm = PerformenceManager(packageName, serialno)
    pm.run()
    time.sleep(100)
    pm.stop()
    pm.create_report()

