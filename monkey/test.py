# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@author  :  Xuanlh  
@file    :  test.py
@since   :  2021/3/4 6:27 PM
@desc    :  
"""

import os

report_path = os.getcwd().split('appium_autotest')[0] + 'appium_autotest' + os.sep + 'performence' + os.sep + 'report' + os.sep + 'report.html'

performence_report = ""
flag = False
with open(report_path, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        if r"<title>性能测试报告</title>" in line:
            flag = True
            continue
        if r"</html>" in line:
            break
        if flag:
            performence_report += line

print(performence_report)