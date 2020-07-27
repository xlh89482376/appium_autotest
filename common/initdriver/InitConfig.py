from common.utils.ConfigUtil import ConfigController
from common.utils.FilePathUtil import FilePathUtil
from common.dev.DeviceInfo import DeviceInfo
from common.utils.LoggingUtil import LoggingController
from common.base.Command import Cmd


class InitConfiger(object):

    def __init__(self):
        self.cmd = Cmd()
        self.path = FilePathUtil().get_config_run_path()
        self.config = ConfigController(self.path)
        self.log4py = LoggingController()
        self.dev_info = DeviceInfo().get_infos_as_dict()

    def get_desired_caps_dict(self):
        section = "desired_caps"
        desired_caps_dict = {}
        sno_list = self.cmd.get_device_list()
        if not len(sno_list):
            return None
        for sno in sno_list:
            self.cmd.set_serialno(sno)
            if int(float(self.dev_info[sno]["os_version"][0])) < 5:
                desired_caps_dict[sno] = {"platformName":"Android",
                                          "platformVersion":self.dev_info[sno]["os_version"],
                                          "deviceName":sno,
                                          "appPackage":self.config.get(section, "appPackage"),
                                          "appActivity":self.config.get(section, "appActivity"),
                                          "unicodeKeyboard":True,
                                          "resetKeyboard":True,
                                          "noReset":True,
                                          "automationName":"Uiautomator1"
                                          }
            else:
                desired_caps_dict[sno] = {"platformName": "Android",
                                          "platformVersion": self.dev_info[sno]["os_version"],
                                          "deviceName": sno,
                                          "appPackage": self.config.get(section, "appPackage"),
                                          "appActivity": self.config.get(section, "appActivity"),
                                          "unicodeKeyboard": True,
                                          "resetKeyboard": True,
                                          "noReset": True,
                                          "automationName": "Uiautomator2"
                                          }

        return desired_caps_dict

    def get_host_port(self):
        host_port_list = ['127.0.0.1:4723', '127.0.0.1:4724']
        return host_port_list


if __name__ == '__main__':
    pass

    # i = InitConfiger()
    # # print(i.dev_info['fe80849']['os_version'])
    # res = i.get_desired_caps_dict()


