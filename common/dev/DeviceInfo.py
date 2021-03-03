from common.base.Command import Cmd
from common.utils.LoggingUtil import LoggingController


class DeviceInfo(object):
    def __init__(self):
        self.cmd = Cmd()
        self.log4py = LoggingController()

    def get_infos_as_dict(self):

        try:
            info = {}
            lists = self.cmd.get_device_list
            if not len(lists):
                self.log4py.info("无任何设备处于连接状态")
                return None
            self.log4py.info("开始获取设备信息.....")
            i = 1
            for sno in lists:
                # self.cmd.set_serialno(sno)
                self.cmd.serialno = sno
                brand, model, os_version, dpi, screen_size, name = \
                    self.get_device_info()
                info[sno] = {"brand":brand, "model":model, "os_version":os_version, "dpi":dpi,
                             "screen_size":screen_size, "name":name}

                self.log4py.info("%d.设备连接信息：%s-%s" % (i, sno, info[sno]))
                i += 1
            self.log4py.info("设备信息获取完毕，设备总数量：%s" % len(lists))

            return info
        except Exception as e:
            print(e)
            self.log4py.error("获取设备信息时发生错误")
            return None

    def get_device_info(self):
        """
        获取设备信息
        """
        try:
            name = self.cmd.get_device_sno()
            brand = self.cmd.get_device_brand()
            model = self.cmd.get_device_model()
            os_version = self.cmd.get_android_os_version()
            ram = self.cmd.get_device_ram()
            dpi = self.cmd.get_device_dpi()
            # ip = self.cmd.get_device_ip()
            screen_size = self.cmd.get_screen_size()

            return brand, model, os_version, dpi, screen_size, name

        except Exception as e:
            self.log4py.error("Get device info happen ERROR :" + str(e))
            return None

if __name__ == '__main__':
    pass
    dev = DeviceInfo()
    res = {}
    dev = dev.get_infos_as_dict()
    print(dev)