# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@author  :  Xuanlh
@since   :  2021/3/3 4:09 PM
@desc    :  所有控制功能都在这里
"""

import time, threading
from common.utils.PerformenceUtils.Monitor import Monitor

class PerformenceManager():

    def __init__(self, packageName, serialno):
        self.monitor = Monitor(packageName, serialno)
        self.t1 = threading.Thread(target=self.write_pickle)
        self.flag = False
        self.__serialno = serialno

    def write_pickle(self):
        while True:
            self.monitor.write_cpu_rate()
            self.monitor.write_mem()
            self.monitor.write_fps()
            # 采集频率
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

