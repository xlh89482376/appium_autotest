import configparser
from common.utils.LoggingUtil import LoggingController


class ConfigController(object):

    def __init__(self, path):
        self.path = path
        self.config = configparser.ConfigParser()
        self.config.read(self.path, encoding="utf-8")
        self.log4py = LoggingController()
        
    def get(self, section, key):
        """
        读取配置文件
        """
        result = self.config.get(section, key)

        return result

    def set(self, section, key, value):
        """
        写入配置文件
        """
        try:
            self.config.set(section, key, value)
            self.config.write(open(self.path, 'w'))
        except Exception as e:
            return False
        return True


