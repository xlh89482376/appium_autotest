import os
import datetime
import logging
import inspect
from colorama import Fore

logfilepath = os.getcwd().split("common")[0] + "/result/logs/logs4script/"
if not os.path.exists(logfilepath):
    os.makedirs(logfilepath,  mode=0o777)

# 将对应文件实例化成一个FileHandler对象，让不同级别的日志共用该Filehandler，这样做到日志打印到一个文件中
# ToDo:log输入空行，以及其他非格式内容

hd = logging.FileHandler(os.path.abspath(os.path.join(logfilepath, "script.log")))
handlers = {logging.DEBUG: hd,logging.INFO: hd,logging.WARNING: hd, logging.ERROR: hd}


class LoggingController(object):

    def __init__(self, level=logging.NOTSET):
        self.__loggers = {}
        log_levels = handlers.keys()
        for level in log_levels:
            logger = logging.getLogger(str(level))
            logger.addHandler(handlers[level])
            logger.setLevel(level)
            self.__loggers.update({level: logger})

    @staticmethod
    def time_now_formate():
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')

    def get_log_message(self, level, message):
        frame, filename, lineNo, functionName, code, unknowField = inspect.stack()[2]
        '''日志格式：[时间] [类型] [记录代码] 信息'''
        relative_path = filename.split("appium_autotest")[1]
        relative_path = relative_path.replace("/", ".")
        relative_path = relative_path.replace("\\", ".")
        relative_path = relative_path.replace(".", "", 1)

        return "%s %s %s %s - %s" % (self.time_now_formate(), level, relative_path, lineNo, message)

        # return "%s - %s" % (self.time_now_formate(), message)

    def info(self, message):
        message = self.get_log_message("INFO", message)
        self.__loggers[logging.INFO].info(message)

    def error(self, message):
        message = self.get_log_message("ERROR", message)
        self.__loggers[logging.ERROR].error(message)

    def warning(self, message):
        message = self.get_log_message("WARNING", message)
        self.__loggers[logging.WARNING].warning(message)

    def debug(self, message):
        message = self.get_log_message("DEBUG", message)
        self.__loggers[logging.DEBUG].debug(message)

    def critical(self, message):
        message = self.get_log_message("CRITICAL", message)
        self.__loggers[logging.CRITICAL].critical(message)

if __name__ == '__main__':
    log4py = LoggingController()
    log4py.info("xxxxxx")

