import subprocess
import re, os, platform
from common.utils.FilePathUtil import FilePathUtil
from common.utils.DateTimeUtil import DateTimeManager
from common.utils.LoggingUtil import LoggingController
from common.utils.ParamCheckUtil import ParamCheckUtil


class Cmd(object):

    def __init__(self):
        self.system = platform.system()
        self.find_type = None
        if self.system is "Windows":
            self.find_type = "findstr"
        else:
            self.find_type = "grep"
        self.command = "adb"
        self.__serialno = ""
        self.crash_log_path = FilePathUtil().get_crash_log_path()
        self.screenshot_path = FilePathUtil().get_screenshot_path()
        self.dt = DateTimeManager().getCurrentDateTime()
        self.log4py = LoggingController()
        self.xml_path = FilePathUtil().get_xml_path()
        self.parm = ParamCheckUtil()
        self.yml_path = FilePathUtil().get_yml_path()
        self.anr_path = FilePathUtil().get_anr_path()

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

    def get_device_state(self):
        """
        获取设备状态
        """
        return self.adb("get-state").stdout.read().decode('utf-8').strip()

    def get_device_sno(self):
        """
        获取设备id
        """
        return self.adb("get-serialno").stdout.read().decode('utf-8').strip()

    @property
    def get_device_list(self):
        """
        获取设备列表
        """
        devices = []
        result = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
        result.reverse()
        for line in result[1:]:
            if "attached" not in line.decode('utf-8').strip() and "daemon" not in line.decode('utf-8').strip():
                devices.append(line.decode('utf-8').split()[0].split(':')[0])
            else:
                break
        return devices

    def get_device_num(self):
        return len(self.get_device_list)

    def get_device_SN(self):
        """
        车机SN
        @return:
        """
        return self.shell("getprop gsm.serial").stdout.read().decode('utf-8').strip()

    def get_android_os_version(self):
        """
        获取设备中的Android版本号
        """
        return self.shell("getprop ro.build.version.release").stdout.read().decode('utf-8').strip()

    def get_sdk_version(self):
        """
        获取设备SDK版本号
        """
        return self.shell("getprop ro.build.version.sdk").stdout.read().decode('utf-8').strip()

    def get_device_model(self):
        """
        获取设备型号
        """
        return self.shell("getprop ro.product.model").stdout.read().decode('utf-8').strip()

    def get_device_brand(self):
        """
        获取设备品牌
        """
        return self.shell("getprop ro.product.brand").stdout.read().decode('utf-8').strip()

    def get_device_name(self):
        """
        获取设备名称
        """
        return self.shell("getprop ro.product.name").stdout.read().decode('utf-8').strip()

    def get_device_board(self):
        """
        获取设备处理器型号
        """
        return self.shell("getprop ro.product.board").stdout.read().decode('utf-8').strip()

    def get_screen_size(self):
        """
        获取屏幕分辨率
        """
        return self.shell("wm size").stdout.read().decode('utf-8').split(": ")[1].strip()

    def get_device_dpi(self):
        """
        获取屏幕dpi
        """
        return self.shell("wm density").stdout.read().decode('utf-8').split(": ")[1].strip()

    def get_device_ip(self):
        """
        获取ip
        """
        ip = self.shell("ifconfig wlan0").stdout.readlines()[1].decode('utf-8').split()[1].split(":")[1]
        return ip

    def get_device_mac(self):
        """
        获取MAC地址
        """
        return self.shell("cat /sys/class/net/wlan0/address").stdout.read().decode('utf-8').strip()

    def get_device_cpu(self):
        """
        获取CPU信息
        """
        return self.shell("cat /proc/cpuinfo").stdout.read().decode('utf-8').strip()

    def get_device_memory(self):
        """
        获取系统内存信息
        """
        return self.shell("cat /proc/meminfo").stdout.read().decode('utf-8').strip()

    def get_device_ram(self):
        """
        获取ram信息
        """
        ram_k = int(self.shell("cat /proc/meminfo").stdout.readlines()[0].decode('utf-8').\
            split()[1])
        ram_g = ram_k // 1000000
        if ram_k % 10000000 >= 500000:
            ram_g += 1
        return ram_g

    def get_app_memory(self, packageName):
        """
        获取应用内存信息
        """
        return self.shell("cat dumpsys meminfo %s | %s TOTAL" % (packageName, self.find_type))\
            .stdout.read().decode('utf-8').strip()

    def get_cpu_time(self):
        """
        获取总的cpu使用时间
        """
        return self.shell("cat /proc/stat").stdout.read().decode('utf-8').strip()

    def get_pid_cpu_jiff(self, pid):
        """
        获取进程cpu时间片
        """
        return self.shell("cat /proc/%s/stat" % pid).stdout.read().decode('utf-8').strip()

    def get_pid_fps(self, packageName):
        """
        获取进程fps
        """
        return self.shell("dumpsys gfxinfo %s" % packageName).stdout.read().decode('utf-8').strip()

    def get_pid_flow(self):
        pass

    def get_uid(self):
        pass

    def get_app_version(self, packageName):

        return self.shell("dumpsys package %s | %s versionName" % (packageName, self.find_type)).stdout.read().decode('utf-8').split('=')[1]

    def get_app_pid(self, packageName):
        """
        获取进程pid
        """
        if self.system is "Windows":
            pidinfo = self.shell("ps | findstr %s$" % packageName).stdout.read()
        else:
            pidinfo = self.shell("ps | grep -w %s" % packageName).stdout.read()

        if pidinfo == '':
            return "the process doesn't exist."

        pattern = re.compile(r"\d+")
        result = pidinfo.decode('utf-8').split(" ")
        result.remove(result[0])

        return  pattern.findall(" ".join(result))[0]

    def get_focused_package_and_activity(self):
        """
        获取当前应用包名和Activity
        :return:
        """
        return self.shell("dumpsys window | %s mCurrentFocus" % self.find_type).stdout.\
                   read().decode('utf-8').split()[-1][:-1]

    def get_current_package_name(self):
        """
        获取当前应用包名
        """
        return self.get_focused_package_and_activity().split('/')[0]

    def get_current_activity(self):
        """
        获取当前应用Activity
        """
        return self.get_focused_package_and_activity().split('/')[1]

    @property
    def get_system_app_list(self):
        """
        获取设备中安装的系统应用包名列表
        """
        sysApp = []
        for packages in self.shell("pm list packages -s").stdout.readlines():
            sysApp.append(packages.split(str.encode(":"))[-1].decode('utf-8').splitlines()[0])

        return sysApp

    def get_all_app_list(self):
        """
        获取设备中安装的所有应用列表
        @return: 返回安装的所有应用列表
        """
        allApp = []
        for packages in self.shell("pm list packages").stdout.readlines():
            allApp.append(packages.split(str.encode(":"))[-1].decode('utf-8').splitlines()[0])

        return allApp

    def get_third_app_list(self):
        """
        获取设备中安装的第三方应用包名列表
        """
        thirdApp = []
        for packages in self.shell("pm list packages -3").stdout.readlines():
            thirdApp.append(packages.split(str.encode(":"))[-1].decode('utf-8').splitlines()[0])
        return thirdApp

    def get_matching_app_list(self, keyword):
        """
        模糊查询与keyword匹配的应用包名列表
        """
        matApp = []
        for packages in self.shell("pm list packages %s" % keyword).stdout.readlines():
            matApp.append(packages.split(str.encode(":"))[-1].decode('utf-8').splitlines()[0])
        return matApp

    def get_app_start_total_time(self, component):
        """
        获取启动应用所花时间
        """

        time = self.shell("am start -W %s | %s TotalTime" % (component, self.find_type)) \
            .stdout.read().split(str.encode(": "))[-1]

        return int(time)

    def do_install_app(self, appFile, packageName):
        """
        安装app，app名字不能含中文字符
        args:- appFile -: app路径
        usage: install("d:\\apps\\Weico.apk")
        """
        self.adb("install %s" % appFile)
        if not self.is_install_app(packageName):
            return True
        else:
            return False

    def do_uninstall_app(self, packageName):
        """
        卸载应用
        """
        self.adb(" uninstall %s" % packageName)
        if not self.is_install_app(packageName):
            return True
        else:
            return False

    def is_install_app(self, packageName):
        """
        判断应用是否安装，已安装返回True，否则返回False
        """
        flag = False
        result = self.get_third_app_list()
        if result is None or len(result) < 0:
            return None
        for i in result:
            if re.search(packageName, i.strip()):
                flag = True
        return flag

    def do_pull_file(self, remote, local):
        """
        pull文件
        """
        self.adb(" pull %s %s" % (remote, local))

    def do_push_file(self, local, remote):
        """
        push文件
        """
        self.adb(" push %s %s" % (local, remote))

    def do_clear_app_data(self, packageName):
        """
        清除应用用户数据
        """
        if "Success" in self.shell("pm clear %s" % packageName).stdout.read().decode('utf-8').splitlines():
            return "clear user data success "
        else:
            return "make sure package exist"

    def do_start_activity(self, component):
        """
        启动一个Activity
        """
        self.shell("am start -n %s" % component)

    def do_reset_current_app(self):
        """
        重置当前应用
        """
        packageName = self.get_current_package_name()
        component = self.get_focused_package_and_activity()
        self.do_clear_app_data(packageName)
        self.do_start_activity(component)

    def do_reboot(self):
        """
        重启设备
        """
        self.adb("reboot")

    def do_kill_process(self, pid):
        """
        杀死应用进程
        """
        if self.shell("kill %s" % str(pid)).stdout.read().decode().split(": ")[-1] == "":
            return "kill success"

        else:
            return self.shell("kill %s" % str(pid)).stdout.read().decode().split(": ")[-1]

    def do_quit_app(self, packageName):
        """
        退出app，类似于kill掉进程
        """
        self.shell("am force-stop %s" % packageName)

    @staticmethod
    def get_adb_process_pid():
        """
        获取adb进程pid
        """
        pid = os.popen("lsof -i tcp:5037").readlines()[1].split()[1]
        return pid

    @staticmethod
    def port_is_used(port):
        flag = False
        port_res = subprocess.Popen('lsof -i tcp:%s' % port, shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE).stdout.readlines()
        print(port_res)
        if len(port_res):
            return True

        return flag

    @staticmethod
    def do_stop_and_restart_5037():
        """
        杀掉并重启adb进程，目前只适配了mac
        """
        pid = os.popen("lsof -i tcp:5037").readlines()[1].split()[1]
        os.system("kill 9 %s" % pid)
        os.system("adb start-server")

    def get_crash_log(self):

        self.adb(r" pull /sdcard/crash/ %s" % self.crash_log_path)
        self.log4py.debug("pull crash to result/logs/crash")

    def clear_crash_log(self):
        self.shell(r" rm -rf sdcard/crash/")
        self.log4py.debug("clear device crash")

    def get_anr(self):
        self.adb(r" pull /data/anr/ %s" % self.anr_path)
        self.log4py.debug("pull anr to result/logs/anr")

    def clear_anr(self):
        self.shell(r" rm -rf /data/anr/")
        self.log4py.debug("clear device anr")

    def close_logcat(self):
        self.shell("killall -2 logcat")
        # os.system("adb shell killall -2 logcat")

    @staticmethod
    def clear_logcat():
        os.popen('adb logcat -b all -c')

    # 封装截图方法
    def get_screenshot(self):
        path = self.screenshot_path + self.dt + r".png"
        self.adb("exec-out screencap -p > %s" % path)
        return path

    def get_uidump_xml(self, yml_name):

        if float(self.get_sdk_version()) >= 19:
            self.shell("uiautomator dump --compressed /data/local/tmp/uidump.xml").wait()
        else:
            self.shell("uiautomator dump /data/local/tmp/uidump.xml").wait()

        self.adb("pull /data/local/tmp/uidump.xml %s" % (self.xml_path + str(self.get_current_package_name()) + ".xml")).wait()
        self.shell("rm /data/local/tmp/uidump.xml").wait()

        xml_file_name = str(self.get_current_package_name()) + ".xml"
        # print(xml_file_name)

        pk_dict = {}

        dict1 = self.parm.load_xml_data(xml_file_name)

        pk_dict[self.get_current_package_name()] = dict1

        self.parm.write_yaml_data(yml_name, dict)


if __name__ == '__main__':
    adb = Cmd()
    packageName = 'com.android.settings'
    adb.get_pid(packageName)


