import os, re, shutil, datetime, hashlib, time
from itertools import islice
from common.utils.FilePathUtil import FilePathUtil


LOG_ROOT = "monkey/logs"
HISTORY_ROOT = "monkey/history_logs"


class ProjectLog:
    def __init__(self):
        self.log_root = LOG_ROOT
        self.log_path = "{}/{}".format(LOG_ROOT, "log.txt")
        self.history_root = HISTORY_ROOT

    def tear_down(self):
        # 创建历史结果目录
        if not os.path.exists(self.history_root):
            os.makedirs(self.history_root)
        # 将本次结果目录复制到历史结果目录
        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        dest_dir = "{}/{}".format(self.history_root, now)
        shutil.copytree(self.log_root, dest_dir)


class DeviceLog:
    def __init__(self, sn, path):
        self.sn = sn
        self.path = path + self.sn + os.sep
        self.anr_dir = self.path + "anr" + os.sep
        self.crash_dir = self.path + "crash" + os.sep
        self.dump_dir = self.path + "dumpsys" + os.sep
        self.log_path = self.path + "monkey.log"

    # def __repr__(self):
    #     return repr(self.__dict__)

    @staticmethod
    def __remove_excess_traces(anr_info):
        # 获取PID
        pid = 0
        for line in anr_info:
            if line.startswith(r"PID: "):
                pid = re.findall(r"PID: (\d+)", line)[0]
                break
        # 获取anr traces起始、末尾行，对应pid的起始、末尾行:
        trace_start = 0
        trace_end = 0
        trace_pid_start = 0
        trace_pid_end = 0
        for i in range(len(anr_info)):
            line = anr_info[i]
            if "----- pid " in line and trace_start == 0:
                trace_start = i
            if "----- end " in line:
                trace_end = i
            if "----- pid %s " % pid in line and trace_pid_start == 0:
                trace_pid_start = i
            if "----- end %s " % pid in line and trace_pid_end == 0:
                trace_pid_end = i
        # 如果起始、末尾行有问题，则不处理
        if not (0 < trace_start <= trace_pid_start < trace_pid_end <= trace_end or
                (trace_pid_start == trace_pid_end == 0 < trace_start < trace_end)):
            return anr_info
        # 处理保留信息
        anr_store = []
        for i in range(len(anr_info)):
            line = anr_info[i]
            if i < trace_start or i > trace_end or trace_pid_start <= i <= trace_pid_end:
                anr_store.append(line)
        return anr_store

    def check(self, packageName):
        with open(self.log_path, "r") as fp:
            # 判断文件行是否为anr或crash，如果是则做相关处理
            is_anr = 0
            is_crash = False
            # anr和crash计数
            anr_cnt = 0
            crash_cnt = 0
            # anr和crash信息
            anr_info = []
            crash_info = []

            # 逐行读取日志信息
            for line in fp:
                # ANR处理
                if line.startswith("// NOT RESPONDING: {} ".format(packageName)):
                    if is_anr == 0:
                        anr_cnt += 1
                    is_anr += 1
                if is_anr != 0:
                    anr_info.append(line)
                if is_anr != 0 and line.strip() == "// meminfo status was 0":
                    is_anr -= 1
                    if is_anr == 0:
                        # 去掉多余的traces
                        anr_info = self.__remove_excess_traces(anr_info)
                        # 存成文件
                        with open("{}/anr_{}_{}.txt".format(self.anr_dir, packageName, anr_cnt), "w") as anr_fp:
                            for anr_line in anr_info:
                                anr_fp.write(anr_line)
                        # 清空
                        anr_info = []
                # CRASH处理
                if line.startswith("// CRASH: {} ".format(packageName)) or line.startswith("// CRASH: {}:".format(packageName)):
                    is_crash = True
                    crash_cnt += 1

                if is_crash:
                    crash_info.append(line)

                if is_crash and line.strip() == "//":
                    # 存成文件
                    with open("{}/crash_{}_{}.txt".format(self.crash_dir, packageName, crash_cnt), "w") as crash_fp:
                        for crash_line in crash_info:
                            crash_fp.write(crash_line)
                    # 清空
                    crash_info = []
                    is_crash = False

    @staticmethod
    def __numerical_sort(value):
        numbers = re.compile(r"(\d+)")
        parts = numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
        return parts

    def get(self):
        # 获取anr、crash、dumpsys
        anr_fn_list = os.listdir(self.anr_dir)
        anr_fn_list = sorted(anr_fn_list, key=self.__numerical_sort, reverse=False)
        anr_cnt = len(anr_fn_list)
        crash_fn_list = os.listdir(self.crash_dir)
        crash_fn_list = sorted(crash_fn_list, key=self.__numerical_sort, reverse=False)
        crash_cnt = len(crash_fn_list)
        dumpsys_fn_list = os.listdir(self.dump_dir)
        # 将anr、crash、dumpsys写入附件list
        att_list = []
        for fn in anr_fn_list:
            att_list.append("{}/{}".format(self.anr_dir, fn))
        for fn in crash_fn_list:
            att_list.append("{}/{}".format(self.crash_dir, fn))
        for fn in dumpsys_fn_list:
            att_list.append("{}/{}".format(self.dump_dir, fn))
        report_path = os.getcwd().split('appium_autotest')[0] + 'appium_autotest' + os.sep + 'performence' + os.sep + 'report' + os.sep + 'report.html'
        att_list.append(report_path)

        # 获取crash和anr文件对象和次数
        crash_file_dict = self.crashFileDict()
        anr_file_dict = self.anrFileDict()
        # 返回anr_cnt、crash_cnt和att_list
        return anr_cnt, crash_cnt, att_list, crash_file_dict, anr_file_dict


    def getCrashHash(self, f):
        hash = hashlib.md5()
        # Crash log首行pid不同，去掉首行进行比对
        for line in islice(f , 10 , None):
        # next(f)
        # for line in f.readlines():
            hash.update(line)

        return hash.hexdigest()

    def getAnrHash(self, f):
        hash = hashlib.md5()
        reason = f.readlines()[3]
        print(reason)
        hash.update(reason)
        return hash.hexdigest()

    def isCrashHashEqual(self, f1, f2):
        str1 = self.getCrashHash(f1)
        str2 = self.getCrashHash(f2)
        return str1 == str2

    def isAnrEqual(self, f1, f2):
        if f1.readlines[3] == f2.readlines[3]:
            return True
        else:
            return False

    def fileList(self):
        '''
        获取crash文件的file列表
        '''
        file_list = []
        list = os.listdir(self.crash_dir)  # 列出文件夹下所有的目录与文件
        for i in range(0, len(list)):
            path = os.path.basename(list[i])
            f = open(self.crash_dir + path, "rb")
            file_list.append(f)

        return file_list

    def crashHashDict(self):
        file_hash_list = []
        file_hash_dict = {}
        list = os.listdir(self.crash_dir)
        for i in range(0, len(list)):
            path = os.path.basename(list[i])
            crash_log = self.crash_dir + path
            f = open(crash_log, "rb")
            file_hash_list.append(self.getCrashHash(f))

        for hash in file_hash_list:
            file_hash_dict.update({hash : file_hash_list.count(hash)})

        return file_hash_dict

    def crashFileDict(self):
        file_list = []
        # file_list = {}
        list = os.listdir(self.crash_dir)  # 列出文件夹下所有的目录与文件
        for i in range(0, len(list)):
            path = os.path.basename(list[i])
            f = open(self.crash_dir + path, "rb")
            file_list.append(f)

        file_hash_list = []
        file_hash_dict = {}
        file_dict = {}
        list = os.listdir(self.crash_dir)
        for i in range(0, len(list)):
            path = os.path.basename(list[i])
            crash_log = self.crash_dir + path
            f = open(crash_log, "rb")
            file_hash_list.append(self.getCrashHash(f))

        for hash in file_hash_list:
            file_hash_dict.update({hash: file_hash_list.count(hash)})

        for k,v in file_hash_dict.items():
            for file in file_list:
                # file.seek(0)
                if self.getCrashHash(file) == k:
                    file.seek(0)
                    # file_dict.update({file.read().decode('utf-8') : v})
                    file_dict.update({self.convertReportFile(file) : v})
                    break

        return file_dict

    def anrFileDict(self):
        file_list = []
        list = os.listdir(self.anr_dir)  # 列出文件夹下所有的目录与文件
        for i in range(0, len(list)):
            path = os.path.basename(list[i])
            f = open(self.anr_dir + path, "rb")
            file_list.append(f)

        file_hash_list = []
        file_hash_dict = {}
        file_dict = {}
        list = os.listdir(self.anr_dir)
        for i in range(0, len(list)):
            path = os.path.basename(list[i])
            anr_log = self.anr_dir + path
            f = open(anr_log, "rb")
            file_hash_list.append(self.getAnrHash(f))

        for hash in file_hash_list:
            file_hash_dict.update({hash: file_hash_list.count(hash)})

        for k, v in file_hash_dict.items():
            for file in file_list:
                if self.getAnrHash(file) == k:
                    file.seek(0)
                    # file_dict.update({file.read().decode('utf-8'): v})
                    file_dict.update({self.convertReportFile(file): v})
                    break

        for k, v in file_dict.items():
            print(k)
            print(v)
            print('=================================================================')
        return file_dict

    def convertReportFile(self, f):
        lines = f.readlines()
        str = ''
        for line in lines:
            line_new = line.decode('utf-8') + r'<br>'
            str += line_new
        return str

if __name__ == '__main__':
    sn = '111111'
    path = '/Users/xuanlonghua/Documents/ZD/Projects/appium_autotest/monkey/logs/'
    dl = DeviceLog(sn, path)
    dl.anrFileDict()






































