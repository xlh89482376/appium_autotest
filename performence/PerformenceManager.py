# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@author  :  Xuanlh  
@file    :  PerformenceManager.py
@since   :  2021/3/3 4:09 PM
@desc    :  控制
"""

import time, threading, os
from common.utils.PerformenceUtils.Monitor import Monitor
from common.utils.PerformenceUtils.OperatePick import OperatePick
from pyecharts import Bar, Line, Page, Overlap

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
        self.monitor.init()
        self.t1.start()

    def stop(self):
        self.flag = True

    def create_report(self):
        cpu_rate_list = pick.readInfo(self.cpu_path)
        # mem_list = pick.readInfo(self.mem_path)
        # fps_list = pick.readInfo(self.fps_path)

        v1 = [i for i in cpu_rate_list if type(i) == str]
        v2 = [i for i in cpu_rate_list if type(i) != str]

        page = Page("性能测试报告")

        attr = v1
        bar = Bar()
        bar.add('ROKI_bar', attr, v2)
        line = Line("性能测试报告" + '-' + 'CPU占用', "设备信息", width=1200, height=400)

        line.add('ROKI_line', attr, v2, is_stack=True, is_label_show=True, is_smooth=False, is_more_utils=True,
                 is_datazoom_show=False, yaxis_formatter='%', mark_point=['max', 'min'], mark_line=['average'])

        overlap = Overlap("性能测试报告" + '-' + 'CPU占用', width=1200, height=400)
        overlap.add(line)
        overlap.add(bar)
        page.add(overlap)

        page.render(self.report_path + 'report.html')

if __name__ == '__main__':
    packageName = "com.mogo.launcher.f"
    serialno = "ZD80123823728"
    pm = PerformenceManager(packageName, serialno)
    # pm.run()
    # time.sleep(200)
    # pm.stop()
    pm.create_report()

