# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@author  :  Xuanlh  
@file    :  Monitor.py
@since   :  2021/2/28 7:22 PM
@desc    :  pickle文件初始化 写入
"""

import os, shutil, time
from common.base.Command import Cmd
from common.base.PerformenceCommand import PerformenceCmd
from common.utils.PerformenceUtils.OperatePick import OperatePick
from common.utils.PerformenceUtils.OperateFileUtil import OperateFileUtil

PROJECT_PATH = os.getcwd().split('appium_autotest')[0] + 'appium_autotest' + os.sep + 'performence' + os.sep
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(os.path.realpath('__file__')), p))
dev_list = Cmd.get_device_list
pick = OperatePick()

class Monitor(object):

    def __init__(self, packageName, serialno, config_path=None):
        self.pid = PerformenceCmd().get_pid(packageName)
        self.battery = PerformenceCmd().get_battery
        self.__serialno = serialno
        self.config_path = config_path
        self.packageName = packageName
        self.info_path = PROJECT_PATH + os.sep + 'result' + os.sep + self.__serialno + os.sep + 'info' + os.sep
        self.battery_path = PATH(self.info_path + 'battery.pickle')
        self.mem_path = PATH(self.info_path + 'memory.pickle')
        self.cpu_path = PATH(self.info_path + 'cpu.pickle')
        self.jiff_path = PATH(self.info_path + 'jiff.pickle')
        self.fps_path = PATH(self.info_path + 'fps.pickle')

    def init(self):
        """
        初始化
        """
        # 创建对应sn的info目录
        if os.path.exists(self.info_path):
            shutil.rmtree(self.info_path)
        os.makedirs(self.info_path)
        # 电量 内存 cpu jiff fps 的 pickle文件创建
        OperateFileUtil(self.battery_path).touch_file()
        OperateFileUtil(self.mem_path).touch_file()
        OperateFileUtil(self.cpu_path).touch_file()
        OperateFileUtil(self.jiff_path).touch_file()
        OperateFileUtil(self.fps_path).touch_file()

    def write_battery(self):
        """
        电量写入pickle
        """
        print(type(self.battery))
        pick.writeInfo(self.battery, PATH(self.battery_path))

    def write_cpu_rate(self):
        """
        cpu占用写入pickle
        """
        cpu_rate = PerformenceCmd().get_cpu_jiff_rate(self.packageName)
        if cpu_rate >= 0:
            pick.writeInfo(cpu_rate, PATH(self.cpu_path))
            pick.writeInfo(time.strftime('%H:%M:%S', time.localtime(time.time())), PATH(self.cpu_path))
        else:
            print("unkown error: write cpu rate")

    def write_mem(self):
        """
        mem写入pickle
        """
        mem = PerformenceCmd().get_mem(self.packageName)
        if mem >= 0:
            pick.writeInfo(mem, PATH(self.mem_path))
            pick.writeInfo(time.strftime('%H:%M:%S', time.localtime(time.time())), PATH(self.mem_path))
        else:
            print("unkown error: write mem")

    def write_fps(self):
        """
        fps写入pickle
        """
        fps, total_frames, jumping_frames = PerformenceCmd().get_fps(self.packageName)
        print(type(fps))
        if fps >= 0:
            pick.writeInfo(fps, PATH(self.fps_path))
            pick.writeInfo(time.strftime('%H:%M:%S', time.localtime(time.time())), PATH(self.mem_path))
        else:
            print("unkown error: write pickle")



if __name__ == '__main__':
    print(PATH)
    packageName = "com.android.settings"
    serialno = "ZD8012348473834"
    config_path = 123
    m = Monitor(packageName, serialno, config_path)
    m.init()
    # m.write_battery()
    m.write_cpu_rate()