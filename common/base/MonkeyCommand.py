import os, platform, time, random, subprocess, shutil
from common.utils.ConfigUtil import ConfigController
from common.utils.FilePathUtil import FilePathUtil
from common.base.Command import Cmd
from common.utils.AnalyzeLogUtil import ProjectLog
from common.utils.AnalyzeLogUtil import DeviceLog
from common.utils.SendEmailUtil import SendMail
from common.utils import timeout_command
from jinja2 import Environment, PackageLoader
from common.utils.DateTimeUtil import DateTimeManager

Project_Path = os.getcwd().split('appium_autotest')[0] + 'appium_autotest' + os.sep + 'monkey' + os.sep
# Monkey_Config_Path = FilePathUtil().get_monkey_config_path()


class MonkeyCmd(object):

    def __init__(self, serialno, config_path):
        self.config_path = config_path
        self.section = 'monkey'
        self.section1 = 'gmail'
        self.system = platform.system()
        self.find_type = None
        if self.system is "Windows":
            self.find_type = "findstr"
        else:
            self.find_type = "grep"
        self.command = "adb"
        self.__serialno = serialno
        self.project_path = Project_Path
        self.data = self.project_path + "data" + os.sep
        self.whitelist = self.data + "whitelist.txt"
        self.blacklist = self.data + 'blacklist.txt'
        self.logs = self.project_path + 'logs' + os.sep
        self.deviceroot = self.project_path + "logs" + os.sep + self.__serialno + os.sep
        self.anr_path = self.deviceroot + "anr"
        self.crash_path = self.deviceroot + "crash"
        self.dump_path = self.deviceroot + "dumpsys"
        self.monkey_log = self.deviceroot + "monkey.log"
        self.package_list = ConfigController(self.config_path).get(self.section, "packageName").split(',')
        self.nopackage_list = ConfigController(self.config_path).get(self.section, "noPackageName").split(',')
        self.excute_package_list = []
        self.app_name = ConfigController(self.config_path).get(self.section, "appName")
        self.tester = ConfigController(self.config_path).get(self.section, "tester")
        self.time = DateTimeManager().getCurrentDate()
        self.result = None
        self.color = ''

    # def __repr__(self):
    #     return repr(self.__dict__)

    @property
    def serialno(self):
        return self.__serialno

    @serialno.setter
    def serialno(self, sno):
        self.__serialno = sno

    def adb(self, args):
        if self.__serialno == "" or self.__serialno is None:
            cmd = "%s %s" % (self.command, str(args))
        else:
            cmd = "%s -s %s %s" % (self.command, self.__serialno, str(args))
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def shell(self, args):
        if self.__serialno == "" or self.__serialno is None:
            cmd = "%s shell %s" % (self.command, str(args))
        else:
            cmd = "%s -s %s shell %s" % (self.command, self.__serialno, str(args))
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def rm_blacklist(self):
        rm_result = self.shell("rm sdcard/blacklist.txt").stdout.read().decode('utf-8')
        if rm_result is None:
            return True
        else:
            return False

    def rm_whitelist(self):
        rm_result = self.shell("rm sdcard/whitelist.txt").stdout.read().decode('utf-8')
        if rm_result is None:
            return True
        else:
            return False

    def push_blacklist(self):
        self.adb("push %s /sdcard/" % self.blacklist)

    def push_whitelist(self):
        self.adb("push %s /sdcard/" % self.whitelist)

    def init(self):
        """
        初始化功能
        :return:设备列表、monkey参数、收件人列表
        """
        serialno_list = Cmd().get_device_list()

        if os.path.exists(self.logs):
            shutil.rmtree(self.logs)
        os.makedirs(self.logs)

        if os.path.exists(self.data):
            shutil.rmtree(self.data)
        os.makedirs(self.data)

        if os.path.exists(self.deviceroot):
            shutil.rmtree(self.deviceroot)
        # 创建device所需的日志目录
        os.makedirs(self.deviceroot)
        os.makedirs(self.anr_path)
        os.makedirs(self.crash_path)
        os.makedirs(self.dump_path)

        throttle = ConfigController(self.config_path).get(self.section, "throttle")
        count = ConfigController(self.config_path).get(self.section, "count")
        # section1 = "gmail"
        rcpt_list = ConfigController(self.config_path).get(self.section1, "receiver").split(',')
        print(rcpt_list)

        with open(self.whitelist, 'a') as f:
            f.truncate(0)
            for list in self.package_list:
                f.write(list + '\n')

        with open(self.blacklist, 'a') as f:
            f.truncate(0)
            for list in self.nopackage_list:
                f.write(list + '\n')

        # app_name = ConfigController(Monkey_Config_Path).get(self.section, "appName")
        app_names = self.app_name.split(',')
        pack_names = ConfigController(self.config_path).get(self.section, "packageName").split(',')
        versions = ConfigController(self.config_path).get(self.section, "version").split(',')

        app_list = []
        apps_list = []

        for i in range(len(app_names)):
            app_list.append(app_names[i])
            app_list.append(pack_names[i])
            app_list.append(versions[i])
            apps_list.append(app_list)

            app_list = []

        cmd = Cmd()

        sn = cmd.get_device_SN()

        return serialno_list, throttle, count, rcpt_list, apps_list, sn, self.tester, self.time, self.app_name

    def dumpsys_activity(self):
        dumpsys_name = "dumpsys_{}.txt".format(self.serialno)
        # adb shell dumpsys activity
        cmd = "adb -s {} shell dumpsys activity > {}/{}".format(self.serialno, self.dump_path, dumpsys_name)
        timeout_command.run(cmd)

    def run_monkey(self, serialno, path, throttle=700, cnt=5000):
        # 生成随机数
        rand = random.randint(0, 65535)

        if len(self.package_list):
            self.push_whitelist()
            for list in self.package_list:
                self.excute_package_list.append(list)
                cmd = "adb -s {} shell am force-stop {}".format(serialno, list)
                os.popen(cmd)
                time.sleep(3)
            cmd = "adb -s {} shell monkey --pkg-whitelist-file /sdcard/whitelist.txt -s {} --ignore-crashes --ignore-timeouts --throttle {} -v -v -v {} > {} 2>&1".\
                format(serialno, rand, throttle, cnt, path)
            os.popen(cmd).read()
            time.sleep(5)
        elif len(self.nopackage_list):
            self.push_blacklist()
            for list in self.nopackage_list:
                self.excute_package_list.append(list)
                cmd = "adb -s {} shell am force-stop {}".format(serialno, list)
                os.popen(cmd)
                time.sleep(3)
            # 执行monkey命令
            cmd = "adb -s {} shell monkey --pkg-blacklist-file /sdcard/blacklist.txt -s {} --ignore-crashes --ignore-timeouts --throttle {} -v -v -v {} > {} 2>&1 &".\
                format(serialno, rand, throttle, cnt, path)
            os.popen(cmd).read()
            time.sleep(5)
        else:
            print("请确保参数正确")

    def monkey_test(self):

        serialno_list, throttle, count, rcpt_list, apps_list, sn, tester, time, app_name = self.init()
        start_time = DateTimeManager().getDateTime()
        device_log = DeviceLog(self.serialno, self.logs)

        self.run_monkey(self.serialno, self.monkey_log, throttle, count)
        self.dumpsys_activity()

        for package in self.excute_package_list:
            device_log.check(package)

        anr_cnt, crash_cnt, att_list, crash_file_dict, anr_file_dict = device_log.get()

        end_time = DateTimeManager().getDateTime()

        total_time = format((end_time-start_time).seconds/3600, '.1f')

        # 发送邮件
        self.send_log(rcpt_list, anr_cnt, crash_cnt, att_list, apps_list, tester, time, app_name, sn, total_time, crash_file_dict, anr_file_dict)

        # Todo: 测试报告需要的数据。crash、anr总次数；crash、anr分类数量；crash、anr各个分类数量；crash、anr文件

    def monkey_stop(self):
        monkey_name = 'com.android.commands.monkey'
        pid = subprocess.Popen('adb -s ' + self.__serialno + ' shell ps | grep ' + monkey_name, shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE).stdout.readlines()
        if pid == '':
            print('No monkey running in %s' % self.__serialno)
        else:
            for item in pid:
                if item.split()[8].decode() == monkey_name:
                    monkey_pid = item.split()[1].decode()
                    cmd_monkey = 'adb -s ' + self.__serialno + ' shell kill %s' % (monkey_pid)
                    os.popen(cmd_monkey)
                    print('Monkey in %s was killed' % self.__serialno)
                    time.sleep(2)

    def send_log(self, rcpt_list, anr_cnt, crash_cnt, att_list, apps_list, tester, time, app_name, sn, total_time, crash_file_dict, anr_file_dict):

        subject = u"【质量中心】【稳定性测试报告】「%s」-%s-%s" % (self.app_name, self.tester, self.time)

        if anr_cnt == 0 and crash_cnt == 0:
            self.result = "PASS"
            self.color = "green"
        else:
            self.result = "FAIL"
            self.color = "red"


        env = Environment(loader=PackageLoader('templates', 'temp'))

        template = env.get_template("report.html")

        content = template.render(apps_list=apps_list, crash_cnt=crash_cnt, anr_cnt=anr_cnt, result=self.result, tester=tester, time=time, app_name=app_name, device_name=self.__serialno, sn=sn, total_time=total_time, crash_file_dict=crash_file_dict, anr_file_dict=anr_file_dict, color=self.color)

        status, reason = SendMail(self.config_path).send_mail(rcpt_list, subject, content, att_list=att_list)
        if status:
            print("send email successed")
        else:
            print("send email failed")

if __name__ == '__main__':
    cmd = Cmd()
    sn = cmd.get_device_sno()
    mk = MonkeyCmd(sn)
    # mk.init()
    mk.monkey_test()
    # mk.monkey_stop()

    # mk.init()
