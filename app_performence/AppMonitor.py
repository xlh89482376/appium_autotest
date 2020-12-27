import os, re, time
import AppAdbCom
from AppOperatePick import OperatePick
from PerConfig import AppPerCon

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(os.path.realpath('__file__')), p))
dev_list = []
ad = AppAdbCom.AdbDebug()
pick = OperatePick()
Config = AppPerCon()

class AppMoni(object):


    def IsIp(self, dev):
        if dev == '':
            return False
        index = dev.find(':')
        if index != -1:
            ip = dev[:index]
            addr = ip.split('.')
            if len(addr) != 4:
                return False
            for i in addr:
                if int(i) < 255 and int(i) >= 0:
                    return True
                else:
                    return False

    def get_device(self):
        rt = os.popen('adb devices').readlines()
        n = len(rt) - 2
        print('当前已连接待测试手机数为：' + str(n))
        for i in range(n):
            nPos = rt[i + 1].index('\t')
            dev = rt[i+1][:nPos]
            dev_list.append(dev)
        return dev_list

    def get_pid(self, target, pack):
        pid = ad.adbGetPid(target, pack)
        return pid

    def get_devSystemison(self, target):
        return ad.adbGetAndroidVersion(target)

    def get_battery(self, target):
        battery = 0
        list = ad.adbGetBattery(target).split()
        for k,v in enumerate(list):
            if str(v) == 'level:':
                battery = int(list[k+1])
        print('--------battery--------')
        if self.IsIp(target) == True:
            target = target.split(':')[0].replace('.', '')
            print(type(battery))
            pick.writeInfo(battery, PATH(Config.info_path + target + '_battery.pickle'))
        else:
            pick.writeInfo(battery, PATH(Config.info_path + target + '_battery.pickle'))
        return battery

    def totalCpuTime(self, dev):
        user = nice = system = idle = iowait = irq = softirq = 0

        res = ad.adbGetCpuTime(dev).split()
        try:
            for info in res:
                if info == 'cpu':
                    user = res[1]
                    nice = res[2]
                    system = res[3]
                    idle = res[4]
                    iowait = res[5]
                    irq = res[6]
                    softirq = res[7]
                    result = int(user) + int(nice) + int(system) + int(idle) + int(iowait) + int(irq) + int(softirq)
                    return result
        except:
            print("cpu time 异常")
            return 0

    def pidCpuJiff(self, target, pid):
        utime = stime = cutime = cstime = 0
        try:
            res = ad.adbGetPidJiff(target, pid).split()
            utime = res[13]
            stime = res[14]
            cutime = res[15]
            cstime = res[16]
            result = int(utime) + int(stime) + int(cutime) + int(cstime)
        except:
            print("cpu jiff 异常")
            result = 0
        return result

    def cpu_jiffrate(self, dev, packname):

        pid = self.get_pid(dev, packname)

        processCpuTime1 = self.pidCpuJiff(dev, pid)
        totalCpuTime1 = self.totalCpuTime(dev)

        time.sleep(1)

        processCpuTime2 = self.pidCpuJiff(dev, pid)
        totalCpuTime2 = self.totalCpuTime(dev)

        processCpuTime3 = processCpuTime2 - processCpuTime1
        totalCpuTime3 = (totalCpuTime2 - totalCpuTime1)

        cpu = 100 * (processCpuTime3) / (totalCpuTime3)

        return cpu

    def pid_cpuRate(self, dev, packname, flag):

        pid = self.get_pid(dev, packname)

        print(pid)


        if int(self.get_devSystemison(dev).split('.')[0]) < 8:
            print("release < 8")
            reslist = ad.call_adb('-s %s shell top -s cpu -n 1 | grep %s' % (dev, pid)).split()
            ratelist = list(reslist[4])
            strRate = ''
            for i in range(len(ratelist) - 1):
                strRate += ratelist[i]
            rate = int(strRate)
        else:
            print("计算rate")
            rate = self.cpu_jiffrate(dev, packname)
        print('----------设备：%s cpurate-----------' % dev)
        if rate >= 0 and flag == 0:
            if self.IsIp(dev):
                devIp = dev.split(':')[0].replace('.', '')
                pick.writeInfo(rate, PATH(Config.info_path + devIp + '_' + Config.package_name + '_' + 'Free_cpu.pickle'))
                pick.writeInfo(time.strftime('%H:%M:%S', time.localtime(time.time())),
                                             PATH(Config.info_path + devIp + '_' +Config.package_name + '_' + 'Free_cpu.pickle'))
            else:
                pick.writeInfo(rate, PATH(Config.info_path + dev + '_' +Config.package_name + '_' + 'Free_cpu.pickle'))
                pick.writeInfo(time.strftime('%H:%M:%S', time.localtime(time.time())),
                               PATH(Config.info_path + dev + '_' + Config.package_name + '_' + 'Free_cpu.pickle'))
        elif rate >= 0 and flag == 1:
            if self.IsIp(dev):
                devIP = dev.split(':')[0].replace(".", "")
                pick.writeInfo(rate, PATH(Config.info_path + devIP + "_"+ Config.package_name + "_" + "Medium_cpu.pickle"))
                pick.writeInfo(time.strftime("%H:%M:%S", time.localtime(time.time())),
                               PATH(Config.info_path + devIP + "_" + Config.package_name + "_" + "Medium_cpu.pickle"))
            else:
                pick.writeInfo(rate, PATH(Config.info_path + dev + "_"+ Config.package_name + "_" + "Medium_cpu.pickle"))
                pick.writeInfo(time.strftime("%H:%M:%S", time.localtime(time.time())),
                               PATH(Config.info_path + dev + "_" + Config.package_name + "_" + "Medium_cpu.pickle"))
        elif rate >= 0 and flag == 2:
            if self.IsIp(dev):
                devIP = dev.split(':')[0].replace(".", "")
                pick.writeInfo(rate, PATH(Config.info_path + devIP + "_"+ Config.package_name + "_" + "Full_cpu.pickle"))
                pick.writeInfo(time.strftime("%H:%M:%S", time.localtime(time.time())),
                               PATH(Config.info_path + devIP + "_" + Config.package_name + "_" + "Full_cpu.pickle"))
            else:
                pick.writeInfo(rate, PATH(Config.info_path + dev + "_"+ Config.package_name + "_" + "Full_cpu.pickle"))
                pick.writeInfo(time.strftime("%H:%M:%S", time.localtime(time.time())),
                               PATH(Config.info_path + dev + "_" + Config.package_name + "_" + "Full_cpu.pickle"))
        elif rate >= 0 and flag == 3:
            if self.IsIp(dev):
                devIP = dev.split(':')[0].replace(".", "")
                pick.writeInfo(rate, PATH(Config.info_path + devIP + "_"+ Config.package_name + "_" + "Manual_cpu.pickle"))
                pick.writeInfo(time.strftime("%H:%M:%S", time.localtime(time.time())),
                               PATH(Config.info_path + devIP + "_" + Config.package_name + "_" + "Manual_cpu.pickle"))
            else:
                pick.writeInfo(rate, PATH(Config.info_path + dev + "_"+ Config.package_name + "_" + "Manual_cpu.pickle"))
                pick.writeInfo(time.strftime("%H:%M:%S", time.localtime(time.time())),
                               PATH(Config.info_path + dev + "_" + Config.package_name + "_" + "Manual_cpu.pickle"))
        return rate

    def pid_Jiff(self, dev, pid):
        processCpuTime1 = self.pidCpuJiff(dev, pid)
        time.sleep(1)
        processCpuTime2 = self.pidCpuJiff(dev, pid)
        processCpuTime3 = processCpuTime2 - processCpuTime1
        jiff = processCpuTime3
        print('----------jiff---------')
        if jiff >= 0:
            if self.IsIp(dev):
                devIP = dev.split(':')[0].replace('.', '')
                pick.writeInfo(jiff, PATH(Config.info_path + devIP + '_' + Config.package_name + '_' + '_jiff.pickle'))
            else:
                pick.writeInfo(jiff, PATH(Config.info_path + dev + '_' + Config.package_name + '_' + '_jiff.pickle'))
        return jiff

    def pid_mem(self, dev, pkg_name, flag):
        # lis = ad.adbGetDevPidMem(dev, pkg_name).split()
        # data = 100
        # print(lis)

        data = 0
        str1 = ad.adbGetDevPidMem(dev, pkg_name)
        print(str1)
        # time.sleep(5)
        lis = str1.split()
        print(lis)

        for i in range(len(lis)):
            if lis[i] == 'TOTAL':
                data = lis[i+1]
                print(data)
                break
        mem1 = int(data) / 1024
        mem = round(mem1, 2)
        print(mem)
        print('--------设备：%s mem--------' % dev)
        print(type(dev))
        if mem >= 0 and flag == 0:
            if self.IsIp(dev):
                devIP = dev.split(':')[0].replace('.', '')
                pick.writeInfo(mem, PATH(Config.info_path + devIP + '_' + Config.package_name + '_' + 'Free_mem.pickle'))
                pick.writeInfo(time.strftime('%H:%M:%S', time.localtime(time.time())),
                               PATH(Config.info_path + devIP + '_' + Config.package_name + '_' + 'Free_mem.pickle'))
        elif mem >= 0 and flag == 1:
            print("1111122222")
            if self.IsIp(dev):
                devIP = dev.split(':')[0].replace(".", "")
                pick.writeInfo(mem, PATH(Config.info_path + devIP + "_"+ Config.package_name + "_" + "Medium_mem.pickle"))
                pick.writeInfo(time.strftime("%H:%M:%S", time.localtime(time.time())),
                               PATH(Config.info_path + devIP + "_" + Config.package_name + "_" + "Medium_mem.pickle"))
            else:
                pick.writeInfo(mem, PATH(Config.info_path + dev + "_"+ Config.package_name + "_" + "Medium_mem.pickle"))
                pick.writeInfo(time.strftime("%H:%M:%S", time.localtime(time.time())),
                               PATH(Config.info_path + dev + "_" + Config.package_name + "_" + "Medium_mem.pickle"))
        elif mem >= 0 and flag == 2:
            if self.IsIp(dev):
                devIP = dev.split(':')[0].replace(".", "")
                pick.writeInfo(mem, PATH(Config.info_path + devIP + "_"+ Config.package_name + "_" + "Full_mem.pickle"))
                pick.writeInfo(time.strftime("%H:%M:%S", time.localtime(time.time())),
                               PATH(Config.info_path + devIP + "_" + Config.package_name + "_" + "Full_mem.pickle"))
            else:
                pick.writeInfo(mem, PATH(Config.info_path + dev + "_"+ Config.package_name + "_" + "Full_mem.pickle"))
                pick.writeInfo(time.strftime("%H:%M:%S", time.localtime(time.time())),
                               PATH(Config.info_path + dev + "_" + Config.package_name + "_" + "Full_mem.pickle"))
        elif mem >= 0 and flag == 3:
            if self.IsIp(dev):
                devIP = dev.split(':')[0].replace(".", "")
                pick.writeInfo(mem, PATH(Config.info_path + devIP + "_"+ Config.package_name + "_" + "Manual_mem.pickle"))
                pick.writeInfo(time.strftime("%H:%M:%S", time.localtime(time.time())),
                               PATH(Config.info_path + devIP + "_" + Config.package_name + "_" + "Manual_mem.pickle"))
            else:
                pick.writeInfo(mem, PATH(Config.info_path + dev + "_"+ Config.package_name + "_" + "Manual_mem.pickle"))
                pick.writeInfo(time.strftime("%H:%M:%S", time.localtime(time.time())),
                               PATH(Config.info_path + dev + "_" + Config.package_name + "_" + "Manual_mem.pickle"))
        return mem

    def pid_fps(self, dev, pkg_name, flag):
        indexStart = 0
        indexEnd = 0
        results = ad.adbGetPidfps(dev, pkg_name)
        frames = [x for x in results.split('\n')]
        jank_count = 0
        vsync_overtime = 0
        render_time = 0
        try:
            for k,v in enumerate(frames):
                if v == '\tDraw\tPrepare\tProcess\tExecute' or v == '\tDraw\tProcess\tExecute\r':
                    indexStart = k + 1
                elif v == 'View hierarchy:' or v == 'View hierarchy:\r':
                    indexEnd = k - 1
            fra = frames[indexStart:indexEnd]
            frame_count = len(fra)
            for frame in fra:
                time_block = re.split(r'\s+', frame.strip())
                for k, v in enumerate(frames):
                    if v == '\tDraw\tProcess\tExecute\r':
                        render_time = float(time_block[0]) + float(time_block[1]) + float(time_block[2])
                    elif v == '\tDraw\tPrepare\tProcess\tExecute':
                        render_time = float(time_block[0]) + float(time_block[1]) + float(time_block[2]) + float(time_block[3])

                if render_time > 16.67:
                    jank_count += 1
                    if render_time % 16.67 == 0:
                        vsync_overtime += int(render_time / 16.67) - 1
                    else:
                        vsync_overtime += int(render_time / 16.67)

            print('-------fps--------')
            if frame_count == 0:
                _fps = 60
            else:
                _fps = int(frame_count * 60) / (frame_count + vsync_overtime)
            if flag == 1:
                if self.IsIp(dev):
                    devIP = dev.split(':')[0].replace(".", "")
                    pick.writeInfo(_fps, PATH(Config.info_path + devIP + "_"+ Config.package_name + "_" + "Medium_fps.pickle"))
                    pick.writeInfo(time.strftime("%H:%M:%S", time.localtime(time.time())),
                                   PATH(Config.info_path + devIP + "_" + Config.package_name + "_" + "Medium_fps.pickle"))
                else:
                    pick.writeInfo(_fps, PATH(Config.info_path + dev + "_"+ Config.package_name + "_" + "Medium_fps.pickle"))
                    pick.writeInfo(time.strftime("%H:%M:%S", time.localtime(time.time())),
                                   PATH(Config.info_path + dev + "_" + Config.package_name + "_" + "Medium_fps.pickle"))

            elif flag == 2:
                if self.IsIp(dev):
                    devIP = dev.split(':')[0].replace(".", "")
                    pick.writeInfo(_fps, PATH(Config.info_path + devIP + "_"+ Config.package_name + "_" + "Full_fps.pickle"))
                    pick.writeInfo(time.strftime("%H:%M:%S", time.localtime(time.time())),
                                   PATH(Config.info_path + devIP + "_" + Config.package_name + "_" + "Full_fps.pickle"))
                else:
                    pick.writeInfo(_fps, PATH(Config.info_path + dev + "_"+ Config.package_name + "_" + "Full_fps.pickle"))
                    pick.writeInfo(time.strftime("%H:%M:%S", time.localtime(time.time())),
                                   PATH(Config.info_path + dev + "_" + Config.package_name + "_" + "Full_fps.pickle"))
            elif flag == 3:
                if self.IsIp(dev):
                    devIP = dev.split(':')[0].replace(".", "")
                    pick.writeInfo(_fps, PATH(Config.info_path + devIP + "_"+ Config.package_name + "_" + "Manual_fps.pickle"))
                    pick.writeInfo(time.strftime("%H:%M:%S", time.localtime(time.time())),
                                   PATH(Config.info_path + devIP + "_" + Config.package_name + "_" + "Manual_fps.pickle"))
                else:
                    pick.writeInfo(_fps, PATH(Config.info_path + dev + "_"+ Config.package_name + "_" + "Manual_fps.pickle"))
                    pick.writeInfo(time.strftime("%H:%M:%S", time.localtime(time.time())),
                                   PATH(Config.info_path + dev + "_" + Config.package_name + "_" + "Manual_fps.pickle"))
            return _fps
        except Exception as e:
            print("请打开开发者模式中的GPU显示")


    def flow(self, dev, packname, activity):
        ad.adbStopActivity(dev, packname)
        flow1 = self.pid_flowSingle(dev, packname, 0)
        time.sleep(1)
        ad.adbStartActivity(dev, activity)
        time.sleep(15)
        flow2 = self.pid_flowSingle(dev, packname, 1)
        flow = (flow2 - flow1) / 1024
        if self.IsIp(dev) == True:
            devIp = dev.split(':')[0].replace('.', '')
            pick.writeInfo(flow, PATH(Config.info_path + devIp + '_' + Config.package_name + '_' + 'first_flow.pickle'))
        else:
            pick.writeInfo(flow, PATH(Config.info_path + dev + '_' + Config.package_name + '_' + 'first_flow.pickle'))
        return flow

    def pid_flowSingle(self, dev, packname, flag):
        flow = ad.adbGetPidflow(dev, packname, flag)
        return flow

    def pid_startTime(self, dev, packname):
        time = ad.adbGetPidflow(dev, packname)
        return int(time)

if __name__ == '__main__':
    pass































