import subprocess
import platform
import yaml
from common.utils.FilePathUtil import FilePathUtil


class BroadcastCommand(object):

    def __init__(self):
        self.system = platform.system()
        self.find_type = None
        if self.system is "Windows":
            self.find_type = "findstr"
        else:
            self.find_type = "grep"
        self.command = "adb shell am broadcast -a"
        self.__serialno = ""
        self.yaml_path = FilePathUtil().get_broadcast_path

    @property
    def serialno(self):
        return self.__serialno

    @serialno.setter
    def serialno(self, sno):
        self.__serialno = sno

    def broadcast(self, action, **kwargs):
        params = ""
        for key, value in kwargs.items():
            params = params + " --es " + key + " \"%s\"" % value
        if self.__serialno == "" or self.__serialno is None:
            cmd = "%s %s%s" % (self.command, str(action), str(params))
        else:
            cmd = "%s -s %s %s %s" % (self.command,
                                      self.__serialno,
                                      str(action),
                                      str(params))

        s = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        r = s.stdout.read().decode('utf-8').splitlines()[1][-1]
        if int(r) == 0:
            return True
        else:
            return False

    def load_yaml(self):
        with open(self.yaml_path, "r") as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    def get_action(self, bc_name):
        return self.load_yaml()[bc_name]["action"]

    def get_params(self, bc_name):
        try:
            return self.load_yaml()[bc_name]["params"]
        except Exception as e:
            print(e)
            return None

    def send_broadcast(self, bc_name):
        action = self.get_action(bc_name)
        params = self.get_params(bc_name)
        if params is not None:
            return self.broadcast(action, **params)
        else:
            return self.broadcast(action)


if __name__ == '__main__':
    bc = BroadcastCommand()
    # action = "com.example.LatLng"
    # dic = {"startLatLng":"116.411209,39.96712", "endLatLng":"116.411214,39.965065"}
    # r = bc.broadcast(action, **dic)
    # print(r)
    # print(bc.load_yaml())
    # print(bc.get_action("sendlocation"))
    # print(bc.get_params("sendclear"))
    bc.send_broadcast("sendlocation")
    # bc.send_broadcast("sendlatlon")
    # bc.send_broadcast("sendmockgps")
    # aa = bc.send_broadcast("sendclear")
    # print(aa)
