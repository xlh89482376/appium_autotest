# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@author  :  Xuanlh
@since   :  2021/2/28 8:10 PM
@desc    :  初始化持久性文件 写入 报告
"""

import os, shutil, time
from common.base.PerformenceCommand import PerformenceCmd
from common.utils.PerformenceUtils.OperatePick import OperatePick
from common.utils.PerformenceUtils.OperateFileUtil import OperateFileUtil
from pyecharts import Bar, Line, Page, Overlap

PROJECT_PATH = os.getcwd().split('appium_autotest')[0] + 'appium_autotest' + os.sep + 'performence' + os.sep
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(os.path.realpath('__file__')), p))
pick = OperatePick()

class Monitor(object):

    def __init__(self, package_name, serialno, config_path=None):
        self.pid = PerformenceCmd().get_pid(package_name)
        self.battery = PerformenceCmd().get_battery
        self.__serialno = serialno
        self.config_path = config_path
        self.package_name = package_name
        self.info_path = PROJECT_PATH + os.sep + 'result' +  os.sep + 'info' + os.sep + self.__serialno + os.sep
        self.battery_path = PATH(self.info_path + 'battery.pickle')
        self.mem_path = PATH(self.info_path + 'memory.pickle')
        self.usable_mem_path = PATH(self.info_path + 'usable.pickle')
        self.cpu_path = PATH(self.info_path + 'cpu.pickle')
        self.jiff_path = PATH(self.info_path + 'jiff.pickle')
        self.fps_path = PATH(self.info_path + 'fps.pickle')
        self.gpu_usage_path = PATH(self.info_path + 'gpu.pickle')
        self.report_path = PROJECT_PATH + 'report' + os.sep

    def init(self):
        """
        初始化
        """
        # 在info目录创建对应的sn目录
        if os.path.exists(self.info_path):
            shutil.rmtree(self.info_path)
        os.makedirs(self.info_path)
        # 电量 内存 cpu jiff fps... 的 pickle文件创建
        OperateFileUtil(self.battery_path).touch_file()
        OperateFileUtil(self.mem_path).touch_file()
        OperateFileUtil(self.usable_mem_path).touch_file()
        OperateFileUtil(self.cpu_path).touch_file()
        OperateFileUtil(self.jiff_path).touch_file()
        OperateFileUtil(self.fps_path).touch_file()
        OperateFileUtil(self.gpu_usage_path).touch_file()

    def write_battery(self):
        """
        电量 写入 pickle
        """
        print(type(self.battery))
        pick.writeInfo(self.battery, PATH(self.battery_path))

    def write_cpu_rate(self):
        """
        cpu 占用写入 pickle
        """
        cpu_rate = PerformenceCmd().get_cpu_jiff_rate(self.package_name)
        if cpu_rate >= 0:
            pick.writeInfo(cpu_rate, PATH(self.cpu_path))
            pick.writeInfo(time.strftime('%H:%M:%S', time.localtime(time.time())), PATH(self.cpu_path))
        else:
            print("unkown error: write cpu rate")

    def write_mem(self):
        """
        mem 写入 pickle
        """
        mem = PerformenceCmd().get_mem(self.package_name)
        if mem >= 0:
            pick.writeInfo(mem, PATH(self.mem_path))
            pick.writeInfo(time.strftime('%H:%M:%S', time.localtime(time.time())), PATH(self.mem_path))
        else:
            print("unkown error: write usable_mem")

    def write_usable_mem(self):
        """
        usable_mem 写入 pickle
        """
        usable_mem = PerformenceCmd().get_usable_mem()
        if usable_mem >= 0:
            pick.writeInfo(usable_mem, PATH(self.usable_mem_path))
            pick.writeInfo(time.strftime('%H:%M:%S', time.localtime(time.time())), PATH(self.usable_mem_path))
        else:
            print("unkown error: write mem")

    def write_fps(self):
        """
        fps 写入 pickle
        """
        fps, total_frames, jumping_frames = PerformenceCmd().get_fps(self.package_name)
        print(type(fps))
        if fps >= 0:
            pick.writeInfo(fps, PATH(self.fps_path))
            pick.writeInfo(time.strftime('%H:%M:%S', time.localtime(time.time())), PATH(self.fps_path))
        else:
            print("unkown error: write pickle")

    def write_gpu_usage_rate(self):
        """
        gpu 写入 pickle
        @return:
        """
        gpu_usage_rate = PerformenceCmd().get_gpu_usage_rate()
        if gpu_usage_rate >= 0:
            pick.writeInfo(gpu_usage_rate, PATH(self.gpu_usage_path))
            pick.writeInfo(time.strftime('%H:%M:%S', time.localtime(time.time())), PATH(self.gpu_usage_path))
        else:
            print("unkown error: write gpu")

    def report(self):
        """
        发送报告功能文件路径和初始化都抽离到这里，所有报告功能在此处实现
        Todo:监控数据需要分离 方便后面单独抓取某个数据
        """
        cpu_rate_list = pick.readInfo(self.cpu_path)
        mem_list = pick.readInfo(self.mem_path)
        fps_list = pick.readInfo(self.fps_path)
        usable_mem_list = pick.readInfo(self.usable_mem_path)
        gpu_usage_rate_list = pick.readInfo(self.gpu_usage_path)

        cpu1 = [i for i in cpu_rate_list if type(i) == str]
        cpu2 = [i for i in cpu_rate_list if type(i) != str]
        mem1 = [i for i in mem_list if type(i) == str]
        mem2 = [i for i in mem_list if type(i) != str]
        fps1 = [i for i in fps_list if type(i) == str]
        fps2 = [i for i in fps_list if type(i) != str]
        usable_mem1 = [i for i in usable_mem_list if type(i) == str]
        usable_mem2 = [i for i in usable_mem_list if type(i) != str]
        gpu_usage_rate1 = [i for i in gpu_usage_rate_list if type(i) == str]
        gpu_usage_rate2 = [i for i in gpu_usage_rate_list if type(i) != str]


        page = Page("性能测试报告")

        # cpu 数据绘制
        cpu_bar = Bar()
        cpu_bar.add('ROKI_bar', cpu1, cpu2)
        cpu_line = Line("性能测试报告" + '-' + 'CPU占用', "设备信息", width=1200, height=400)
        cpu_line.add('ROKI_line', cpu1, cpu2, is_stack=True, is_label_show=True, is_smooth=False, is_more_utils=True,
                     is_datazoom_show=False, yaxis_formatter='%', mark_point=['max', 'min'], mark_line=['average'])
        cpu_overlap = Overlap("性能测试报告" + '-' + 'CPU占用', width=1200, height=400)
        cpu_overlap.add(cpu_line)
        cpu_overlap.add(cpu_bar)
        page.add(cpu_overlap)

        # mem 数据绘制
        mem_bar = Bar()
        mem_bar.add('ROKI_bar', mem1, mem2)
        mem_line = Line("性能测试报告" + '-' + 'MEM消耗', width=1200, height=400)
        mem_line.add('ROKI_line', mem1, mem2, is_stack=True, is_label_show=True, is_smooth=False, is_more_utils=True,
                     is_datazoom_show=False, yaxis_formatter='%', mark_point=['max', 'min'], mark_line=['average'])
        mem_overlap = Overlap(width=1200, height=400)
        mem_overlap.add(mem_line)
        mem_overlap.add(mem_bar)
        page.add(mem_overlap)

        # fps 数据绘制
        fps_bar = Bar()
        fps_bar.add('ROKI_bar', fps1, fps2)
        fps_line = Line("性能测试报告" + '-' + 'FPS', width=1200, height=400)
        fps_line.add('ROKI_line', fps1, fps2, is_stack=True, is_label_show=True, is_smooth=False, is_more_utils=True,
                     is_datazoom_show=False, yaxis_formatter='%', mark_point=['max', 'min'], mark_line=['average'])
        fps_overlap = Overlap(width=1200, height=400)
        fps_overlap.add(fps_line)
        fps_overlap.add(fps_bar)
        page.add(fps_overlap)

        # usable_mem 数据绘制
        usable_mem_bar = Bar()
        usable_mem_bar.add('ROKI_bar', usable_mem1, usable_mem2)
        usable_mem_line = Line("性能测试报告" + '-' + '可用MEM', width=1200, height=400)
        usable_mem_line.add('ROKI_line', usable_mem1, usable_mem2, is_stack=True, is_label_show=True, is_smooth=False, is_more_utils=True,
                     is_datazoom_show=False, yaxis_formatter='%', mark_point=['max', 'min'], mark_line=['average'])
        usable_mem_overlap = Overlap(width=1200, height=400)
        usable_mem_overlap.add(usable_mem_line)
        usable_mem_overlap.add(usable_mem_bar)
        page.add(usable_mem_overlap)

        # gpu_usage_rate 数据绘制
        gpu_usage_bar = Bar()
        gpu_usage_bar.add('ROKI_bar', gpu_usage_rate1, gpu_usage_rate2)
        gpu_usage_line = Line("性能测试报告" + '-' + 'GPU使用率', width=1200, height=400)
        gpu_usage_line.add('ROKI_line', gpu_usage_rate1, gpu_usage_rate2, is_stack=True, is_label_show=True, is_smooth=False,
                            is_more_utils=True,
                            is_datazoom_show=False, yaxis_formatter='%', mark_point=['max', 'min'],
                            mark_line=['average'])
        gpu_usage_overlap = Overlap(width=1200, height=400)
        gpu_usage_overlap.add(gpu_usage_line)
        gpu_usage_overlap.add(gpu_usage_bar)
        page.add(gpu_usage_overlap)

        # render
        page.render(self.report_path + 'report.html')


if __name__ == '__main__':
    print(PATH)
    packageName = "com.android.settings"
    serialno = "ZD8012348473834"
    config_path = 123
    m = Monitor(packageName, serialno, config_path)
    m.init()
    # m.write_battery()
    m.write_cpu_rate()