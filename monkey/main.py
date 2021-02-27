import threading
from common.base.Command import Cmd
from common.base.MonkeyCommand import MonkeyCmd

# com.android.settings 配置文件
SETTINGS_CONFIG_PATH = "/Users/xuanlonghua/Documents/ZD/Projects/appium_autotest/monkey/config/launcher.ini"

cmd = Cmd()
serialno_list = cmd.get_device_list()

def main():
    # 多线程测试
    thread_list = []
    for serialno in serialno_list:
        monkey_cmd = MonkeyCmd(serialno, SETTINGS_CONFIG_PATH)
        print(serialno)
        thread = threading.Thread(
            target=monkey_cmd.monkey_test
        )
        thread_list.append(thread)
    # 启动所有线程
    for thread in thread_list:
        thread.start()
    # 主线程等待所有子线程退出
    for thread in thread_list:
        thread.join()


if __name__ == "__main__":
    # 初始化日志
    # project_log = ProjectLog()
    # project_log.set_up()
    # 主程序
    main()
    # 将本次结果复制到历史日志目录
    # project_log.tear_down()




