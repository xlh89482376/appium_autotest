import hashlib, os
from itertools import islice
from common.utils.DateTimeUtil import DateTimeManager

class FileUtil():

    def __init__(self):
        # self.time = DateTimeManager().getCurrentDate()
        pass

    @staticmethod
    def getCrashHash(f):
        hash = hashlib.md5()
        # Crash log首行pid不同，去掉首行进行比对
        for line in islice(f , 1 , None):
            hash.update(line)

        return hash.hexdigest()

    def isCrashHashEqual(self, f1, f2):
        str1 = self.getCrashHash(f1)
        str2 = self.getCrashHash(f2)
        return str1 == str2

    def fileList(self):
        '''
        获取crash文件的file列表
        '''
        file_list = []
        rootdir = r'/Users/xuanlonghua/Documents/ZD/Projects/appium_autotest/monkey/logs/emulator-5554/crash/'
        list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
        for i in range(0, len(list)):
            path = os.path.basename(list[i])
            crash_log = rootdir + path
            f = open(crash_log, "rb")
            file_list.append(f)

        return file_list

    def fileHashList(self):
        '''
        获取所有crash文件的hash列表
        '''
        file_hash_list = []
        rootdir = r'/Users/xuanlonghua/Documents/ZD/Projects/appium_autotest/monkey/logs/emulator-5554/crash/'
        list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
        for i in range(0, len(list)):
            path = os.path.basename(list[i])
            crash_log = rootdir + path
            f = open(crash_log, "rb")
            file_hash_list.append(self.getCrashHash(f))

        return file_hash_list

    def fileCnt(self, file_list):
        '''
        获取所有crash文件去重后的hash列表
        '''
        file_cnt = []
        for file in file_list:
            # print(self.getCrashHash(file))
            if file not in file_cnt:
                # file_cnt.append(file)
                file_cnt.append(file)

        return file_cnt

    def hashCnt(self, hash_list):
        '''
        获取hash对应的文件和数量
        '''
        hash_dict = {}
        for hash in hash_list:
            # print(hash_list.count(hash))
            hash_dict.update({hash : hash_list.count(hash)})

        print(hash_dict)


if __name__ == '__main__':
    fu = FileUtil()
    f1 = open("/Users/xuanlonghua/Documents/ZD/Projects/appium_autotest/monkey/logs/emulator-5554/crash/crash_com.zhidao.testapplication_1.txt", "rb")
    f2 = open("/Users/xuanlonghua/Documents/ZD/Projects/appium_autotest/monkey/logs/emulator-5554/crash/crash_com.zhidao.testapplication_2.txt", "rb")
    print(fu.isCrashHashEqual(f1, f2))

    fl = fu.fileList()
    print(fl)

    file_list = fu.fileHashList()
    print(file_list)

    file_cnt = fu.fileCnt(file_list)
    print(file_cnt)

    fu.hashCnt(file_list)