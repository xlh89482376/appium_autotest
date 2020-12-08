import os, platform, time, random, subprocess, shutil
from common.utils.ConfigUtil import ConfigController
from common.utils.FilePathUtil import FilePathUtil
from common.base.Command import Cmd
from common.utils.AnalyzeLogUtil import ProjectLog
from common.utils.AnalyzeLogUtil import DeviceLog
from common.utils.SendEmailUtil import SendMail
from common.utils import timeout_command

Project_Path = os.getcwd().split('appium_autotest')[0] + 'appium_autotest' + os.sep + 'monkey' + os.sep
Monkey_Config_Path = FilePathUtil().get_monkey_config_path()


class MonkeyCmd(object):

    def __init__(self, serialno):
        self.section = 'monkey'
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
        self.package_list = ConfigController(Monkey_Config_Path).get(self.section, "packageName").split(',')
        self.nopackage_list = ConfigController(Monkey_Config_Path).get(self.section, "noPackageName").split(',')
        self.excute_package_list = []

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
        print(rm_result)
        if rm_result is None:
            return True
        else:
            return False

    def rm_whitelist(self):
        rm_result = self.shell("rm sdcard/whitelist.txt").stdout.read().decode('utf-8')
        print(rm_result)
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

        throttle = ConfigController(Monkey_Config_Path).get(self.section, "throttle")
        count = ConfigController(Monkey_Config_Path).get(self.section, "count")
        section1 = "gmail"
        rcpt_list = ConfigController(Monkey_Config_Path).get(section1, "receiver").split(',')

        with open(self.whitelist, 'a') as f:
            f.truncate(0)
            for list in self.package_list:
                f.write(list + '\n')

        with open(self.blacklist, 'a') as f:
            f.truncate(0)
            for list in self.nopackage_list:
                f.write(list + '\n')

        return serialno_list, throttle, count, rcpt_list

    def dumpsys_activity(self):
        dumpsys_name = "dumpsys_{}.txt".format(self.serialno)
        # adb shell dumpsys activity
        cmd = "adb -s {} shell dumpsys activity > {}/{}".format(self.serialno, self.dump_path, dumpsys_name)
        timeout_command.run(cmd)

    def run_monkey(self, serialno, path, throttle=700, cnt=5000):
        # 生成随机数
        rand = random.randint(0, 65535)
        print(self.package_list)
        print(self.nopackage_list)

        if len(self.package_list):
            self.push_whitelist()
            for list in self.package_list:
                self.excute_package_list.append(list)
                cmd = "adb -s {} shell am force-stop {}".format(serialno, list)
                os.popen(cmd)
                time.sleep(3)
            cmd = "adb -s {} shell monkey --pkg-whitelist-file /sdcard/whitelist.txt -s {} --ignore-crashes --ignore-timeouts --throttle {} -v -v -v {} > {}".\
                format(serialno, rand, throttle, cnt, path)
            print(cmd)
            os.popen(cmd).read()
            time.sleep(5)
        elif len(self.nopackage_list):
            self.push_blacklist()
            for list in self.nopackage_list:
                self.excute_package_list.append(list)
                cmd = "adb -s {} shell am force-stop {}".format(serialno, list)
                print(cmd)
                os.popen(cmd)
                time.sleep(3)
            # 执行monkey命令
            cmd = "adb -s {} shell monkey --pkg-blacklist-file /sdcard/blacklist.txt -s {} --ignore-crashes --ignore-timeouts --throttle {} -v -v -v {} > {}".\
                format(serialno, rand, throttle, cnt, path)
            print(cmd)
            os.popen(cmd).read()
            time.sleep(5)
        else:
            print("请确保参数正确")

    def monkey_test(self):

        serialno_list, throttle, count, rcpt_list = self.init()

        device_log = DeviceLog(self.serialno, self.logs)

        self.run_monkey(self.serialno, self.monkey_log, throttle, count)
        self.dumpsys_activity()

        for package in self.excute_package_list:
            device_log.check(package)

        anr_cnt, crash_cnt, att_list = device_log.get()
        print(rcpt_list)
        # 发送邮件
        self.send_log(rcpt_list, anr_cnt, crash_cnt, att_list)

    def send_log(self, rcpt_list, anr_cnt, crash_cnt, att_list):
        # 如果没有anr和crash，则不发邮件
        # prj_name = prj_info["name"]

        # if anr_cnt == 0 and crash_cnt == 0:
        #     subject = u"Monkey测试通过"
        # else:
        #     subject = u"Monkey测试异常提醒"

        subject = u"Monkey测试通过"

        content = "<table border='1' cellspacing='0' cellpadding='0'>" \
                  + "</table>" \
                  + "<br/><p>具体日志见附件</p>"

        status, reason = SendMail().send_mail(rcpt_list, subject, content, att_list=att_list)
        if status:
            # logging.info("Succeed in sending mails")
            print("send email successed")
        else:
            # logging.error("Failed to send mails, reason: %s" % reason)
            print("send email failed")




if __name__ == '__main__':
    cmd = Cmd()
    sn = cmd.get_device_sno()
    mk = MonkeyCmd(sn)
    # mk.init()
    mk.monkey_test()
    # print(mk.whitelist)
    # print(mk.blacklist)