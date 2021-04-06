# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@author  :  Xuanlh  
@since   :  2021/4/6 6:46 PM
@desc    :  所有自动驾驶都在这里 感知&决策&控制做单独封装 上层做逻辑控制 和 最终数据展现
"""

import os
import pandas as pd

# 日志文件存放路径
FOLDER_PATH = "/Users/xuanlonghua/Desktop/未命名文件夹"

def walk_folder(folder_path):
    """
    遍历文件夹内所有文件
    @param folder_path: 文件夹路径
    @return: 文件列表
    """
    for root, dirs, files in os.walk(folder_path):
        file_list = []
        for f in files:
            if str(f).endswith(".txt"):
                file_list.append(os.path.join(root, f))
        return file_list


class AutoDrive(object):

    def __init__(self,folder_path):
        self._folder_name = folder_path

    def image_data_analysis(self):
        """
        图像识别日志解析
        @return: fps
        """
        file_list = walk_folder(self._folder_name)
        result_dict = {}
        for f in file_list:
            fps,ms_sum = Perception(f).get_fps()
            result_dict.update({f:{"fps":fps,"ms_sum":ms_sum}})
        return result_dict

class Perception(object):

    def __init__(self, file_path):
        self._file_path = file_path

    def get_fps(self):
        """
        获取fps
        @return: int fps & list ms值
        """
        df = pd.read_table(self._file_path,header=None)
        df_list = df.values.tolist()
        i = 0
        time_list = []
        while i < len(df_list):
            if str(df_list[i][0]).startswith("Run"):
                time_list.append(int(str(df_list[i][0].split(": ")[1].split("m")[0])))
            i += 1
        j = 0
        ms_sum = 0
        while j < len(time_list):
            ms_sum += time_list[j]
            j += 1
        ms_avg = ms_sum/len(time_list)
        fps = int(1000/ms_avg)
        return fps, time_list


if __name__ == '__main__':
    auto = AutoDrive(FOLDER_PATH)
    result = auto.image_data_analysis()
    print(result)
