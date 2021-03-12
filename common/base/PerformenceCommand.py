# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@author  :  Xuanlh
@since   :  2021/2/28 8:10 PM
@desc    :  抓取所有性能参数
"""

import time
from common.base.Command import Cmd

class PerformenceCmd(Cmd):

    def __init__(self):
        Cmd.__init__(self)

    def get_pid(self, package_name):
        """
        通过包名获取进程id
        @param package_name: 包名
        @return 进程id
        """
        try:
            pid = self.shell("ps | %s %s" % (self.find_type, package_name)).stdout.readlines()[0].decode('utf-8').split()[1]

            return pid

        except Exception as e:
            print("Error: %s" % e)
            return None

    @property
    def get_battery(self):
        """
        获取电量百分比

        Current Battery Service state:
        AC powered: false           //false表示没使用AC电源
        USB powered: true           //true表示使用USB电源
        Wireless powered: false     //false表示没使用无线电源
        status: 2                   //2表示电池正在充电，1表示没充电
        health: 2                   //2表示电池状态优秀
        present: true               //true表示已安装电池
        level: 63                   //电池百分比
        scale: 100                  //满电量时电池百分比为100%（不确定是否正确）
        voltage: 3781               //电池电压3.781V
        temperature: 250            //电池温度为25摄氏度
        technology: Li-ion          //电池类型为锂电池

        @return: 电池百分比
        """
        try:
            battery = self.shell("dumpsys battery").stdout.readlines()[10].decode('utf-8').split()[1]
            return int(battery.rstrip())
        except Exception as e:
            print("Error: %s" % e)

    @property
    def get_cpu_time(self):
        """
        CPU指标：user，nice, system, idle, iowait, irq, softirq

        cpu指标含义
        user 用户态时间
        nice 用户态时间(低优先级，nice>0)
        system 内核态时间
        idle 空闲时间
        iowait I/O等待时间
        irq 硬中断
        softirq 软中断

         ~/Documents/ZD/Projects/appium_autotest   2.0 ●✚  adb shell cat /proc/stat
        cpu  5832 2599 8716 5526504 1034 1 114 0 0 0
        cpu0 435 242 2482 1379618 417 1 84 0 0 0
        cpu1 673 490 1151 1387896 227 0 8 0 0 0
        cpu2 928 727 1574 1386311 185 0 10 0 0 0
        cpu3 3796 1140 3509 1372679 205 0 12 0 0 0
        intr 2223301 19 0 0 0 6 0 0 0 1 0 26873 8736 0 0 0 0 0 21 247839 1 0 3889 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        ctxt 4943107
        btime 1614513412
        processes 6882
        procs_running 1
        procs_blocked 0
        softirq 1385003 143748 270835 9607 6892 0 0 418091 256736 1566 277528

        @return: cpu使用时长
        """
        try:
            result = self.shell("cat /proc/stat").stdout.readlines()[0].decode('utf-8').split()
            if result[0] == 'cpu':
                user = result[1]
                nice = result[2]
                system = result[3]
                idle = result[4]
                iowait = result[5]
                irq = result[6]
                softirq = result[7]
                cpu_time = int(user) + int(nice) + int(system) + int(idle) + int(iowait) + int(irq) + int(softirq)
            else:
                print('unknown error')
                cpu_time = 0
        except Exception as e:
            print("Error: %s" % e)
            cpu_time = 0
        return cpu_time

    def get_pid_cpu_jiff(self, pid):
        """
        用于获取某一个进程的统计信息

        pid： 进程ID.
        comm: task_struct结构体的进程名
        state: 进程状态, 此处为S
        ppid: 父进程ID （父进程是指通过fork方式，通过clone并非父进程）
        pgrp：进程组ID
        session：进程会话组ID
        tty_nr：当前进程的tty终点设备号
        tpgid：控制进程终端的前台进程号
        flags：进程标识位，定义在include/linux/sched.h中的PF_*, 此处等于1077952832
        minflt： 次要缺页中断的次数，即无需从磁盘加载内存页. 比如COW和匿名页
        cminflt：当前进程等待子进程的minflt
        majflt：主要缺页中断的次数，需要从磁盘加载内存页. 比如map文件
        majflt：当前进程等待子进程的majflt
        utime: 该进程处于用户态的时间，单位jiffies，此处等于166114
        stime: 该进程处于内核态的时间，单位jiffies，此处等于129684
        cutime：当前进程等待子进程的utime
        cstime: 当前进程等待子进程的utime
        priority: 进程优先级, 此次等于10.
        nice: nice值，取值范围[19, -20]，此处等于-10
        num_threads: 线程个数, 此处等于221
        itrealvalue: 该字段已废弃，恒等于0
        starttime：自系统启动后的进程创建时间，单位jiffies，此处等于2284
        vsize：进程的虚拟内存大小，单位为bytes
        rss: 进程独占内存+共享库，单位pages，此处等于93087
        rsslim: rss大小上限
        说明：

        第10~17行主要是随着时间而改变的量；
        内核时间单位，sysconf(_SC_CLK_TCK)一般地定义为jiffies(一般地等于10ms)
        starttime: 此值单位为jiffies, 结合/proc/stat的btime，可知道每一个线程启动的时间点
        1500827856 + 2284/100 = 1500827856, 转换成北京时间为2017/7/24 0:37:58
        第四行数据很少使用,只说一下该行第7至9个数的含义:

        signal：即将要处理的信号，十进制，此处等于6660
        blocked：阻塞的信号，十进制
        sigignore：被忽略的信号，十进制，此处等于36088

         ~/Documents/ZD/Projects/appium_autotest   2.0 ●✚  adb shell cat /proc/3963/stat
        3963 (ndroid.settings) S 1510 1510 0 0 -1 1077961024 // 1-9
        10338 0 90 0 23 43 0 0                               // 10-17
        10 -10 17 0 41692 1521840128 30160 4294967295        // 18-25
        2853281792 2853297780 3214346128 3214338080 2852080324 0 4612 0 1073775864 4294967295 0 0 17 3 0 0 5 0 0 2853305660 2853306368 2878910464 3214347212 3214347288 3214347288 3214348260 0

        @return: cpu_jiff
        """
        try:
            result = self.shell("cat /proc/%s/stat" % pid).stdout.read().decode('utf-8').split()
            utime = result[13]
            stime = result[14]
            cutime = result[15]
            cstime = result[16]
            pid_cpu_jiff = int(utime) + int(stime) + int(cutime) + int(cstime)
        except Exception as e:
            print("Error: %s" % e)
            pid_cpu_jiff = 0
        return pid_cpu_jiff

    def get_cpu_jiff_rate(self, package_name):
        """
        cpu占用
        @param package_name: 包名
        @return: 瞬时cpu占用
        """
        pid = self.get_pid(package_name)
        print("pid: " + str(pid))
        if int(Cmd().get_android_os_version().split('.')[0]) < 8:
            print(11111)
            cpu_jiff_rate = self.shell("top -s cpu -n 1 | %s %s" % (self.find_type, pid)).stdout.read().decode('utf-8').split()[4][:-1]
            return int(cpu_jiff_rate)
        else:
            process_cpu_time = self.get_pid_cpu_jiff(pid)
            cpu_time = self.get_cpu_time

            time.sleep(1)

            process_cpu_time_1 = self.get_pid_cpu_jiff(pid)
            cpu_time_1 = self.get_cpu_time

            result_process_cpu_time = process_cpu_time_1 - process_cpu_time
            result_cpu_time = cpu_time_1 - cpu_time

            cpu_jiff_rate = 100 * result_process_cpu_time / result_cpu_time

            return int(cpu_jiff_rate)

    def get_mem(self, package_name):
        """
        获取单应用 mem 占用
        @param package_name: 应用包名
        @return: mem
        """
        mem_KB = self.shell("dumpsys meminfo %s | %s TOTAL" % (package_name, self.find_type)).stdout.readlines()[0].split()[1].decode('utf-8')
        mem_MB = round(int(mem_KB) / 1024)

        return mem_MB

    def get_usable_mem(self):
        """
        获取系统可用 mem
        @return: mem
        """
        mem_KB = self.shell("cat /proc/meminfo").stdout.readlines()[2].split()[1].decode('utf-8')
        mem_MB = round(int(mem_KB) / 1024)

        return mem_MB

    def get_fps(self, package_name):
        """
        获取fps

        前提：开发者选项-GPU呈现模式分析 选择adb shell dumpsys gfxinfo中

         ~/Documents/ZD/Projects/appium_autotest   2.0 ●✚  adb shell  dumpsys gfxinfo com.android.settings
        Draw    Prepare Process Execute
        8.08    0.24    1.86    1.10
        4.08    0.18    1.89    1.14
        4.04    0.20    1.83    1.17
        4.08    0.18    1.49    1.28
        4.04    0.17    1.57    0.99
        4.07    0.22    1.64    1.26
        Draw:     表示在Java中创建显示列表部分中，OnDraw()方法占用的时间
        Prepare:  准备时间
        Process:  表示渲染引擎执行显示列表所花的时间，view越多，时间就越长
        Execute:  表示把一帧数据发送到屏幕上排版显示实际花费的时间，其实是实际显示帧数据的后台缓存区与前台缓冲区交换后并将前台缓冲区的内容显示到屏幕上的时间
        将上面的四个时间加起来就是绘制一帧所需要的时间，如果超过了16.67就表示掉帧了

        PS:
        Android定义了流畅度的数据标准,以60FPS为标准(FPS为每秒绘制的帧数),帧数过小就会出现卡顿感
        每一帧在安卓系统中分4个阶段,4个阶段的总和超过16.67(1秒60帧,算下来平均1帧的间隔就约是16.67ms)就认为丢帧
        这个定义在Android6.0以前是一定的,但是现在已经没有固定的标准了,因为目前安卓系统有3层缓存机制,加上硬件上的进步,即使超过16.67,也不一定会出现卡顿感。所以这个数据在测试时作为一种对比和相对衡量标准，也可根据需求自定义标准

        计算结果:
        通过以上数据，就可以获取到每一帧的时间、总帧数；从而就可以计算出jank数、vsync数，进而就可以得到最终的FPS和丢帧率数据

        @param package_name: 包名
        @return: fps total_frames jumping_frames 输出总帧数和丢帧数 用于后续统计丢帧率
        """
        result = self.shell("dumpsys gfxinfo %s" % package_name).stdout.readlines()

        # _fps = 0
        # jank数
        jumping_frames = 0
        # 总帧数
        total_frames = 0
        # 丢帧率(暂时不需要)
        # lose_frame_rate = 0
        # 单帧时长 Draw + Prepare + Process + Execute 通过 / 16.67 计算fps
        # render_time = 0
        # 额外花费垂直同步脉冲的数量
        vsync_time = 0
        flag = False

        for line in result:
            # print(line.decode('utf-8'))
            if "Execute" in line.decode('utf-8'):
                flag = True
                continue

            if "View hierarchy" in line.decode('utf-8'):
                break

            if flag:
                line_list = line.decode('utf-8').split()
                if line_list is not []:
                    total_frames += 1
                    # print(line_list)
                    render_time = float(line_list[0]) + float(line_list[1]) + float(line_list[2]) + float(line_list[3])
                    if render_time > 16.67:
                        jumping_frames +=1
                        if render_time % 16.67 == 0:
                            vsync_time += int(render_time / 16.67) - 1
                        else:
                            vsync_time += int(render_time / 16.67)

        if jumping_frames == 0:
            _fps = 60
        else:
            _fps = int(total_frames / (total_frames + vsync_time) * 60)

        return _fps, total_frames, jumping_frames

    def get_gpu_usage_rate(self):
        """
        获取 gpu 使用率
        目前只支持高通芯片获取 后续补充 目前控制先放到上层
        @return: gpu使用率
        """
        gpu_usage_rate = self.shell("cat /sys/class/kgsl/kgsl-3d0/gpu_busy_percentage").stdout.readlines()[0].split()[0].decode('utf-8')

        return int(gpu_usage_rate)


if __name__ == '__main__':
    # packageName = "com.android.settings"
    packageName = "com.mogo.launcher.f"
    # pc = PerformenceCmd().get_cpu_time
    # PerformenceCmd().get_cpu_jiff_rate(packageName)
    # PerformenceCmd().get_fps(packageName)
    # PerformenceCmd().get_usable_mem()
    # PerformenceCmd().get_gpu_usage_rate()

    while True:
        PerformenceCmd().get_cpu_jiff_rate(packageName)
        time.sleep(3)

