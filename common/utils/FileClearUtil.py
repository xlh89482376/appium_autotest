from common.utils.FilePathUtil import FilePathUtil
from common.utils.LoggingUtil import LoggingController
import shutil, os, stat

class FileClearUtil():
    def __init__(self):
        self.log4py = LoggingController()
        self.clear = shutil
        self.report_path = FilePathUtil().get_report_path()
        self.script_log = FilePathUtil().get_scripts_log_path()
        self.logcat_path = FilePathUtil().get_logcat_path()
        self.crash_log_path = FilePathUtil().get_crash_log_path()
        self.screeshot_path = FilePathUtil().get_screenshot_path()
        self.anr_path = FilePathUtil().get_anr_path()

    def do_clear_screenshot(self):
        shutil.rmtree(self.screeshot_path)
        self.log4py.debug("clear history screenshot")
        os.mkdir(self.screeshot_path)

    def do_clear_logcat(self):
        shutil.rmtree(self.logcat_path)
        self.log4py.debug("clear history logcat")
        os.mkdir(self.logcat_path)

    def do_clear_crash_log(self):
        shutil.rmtree(self.crash_log_path)
        self.log4py.debug("clear history crash")
        os.mkdir(self.crash_log_path)

    def do_clear_report(self):
        if self.is_file_by_suffix_json(self.report_path):
            shutil.rmtree(self.report_path)
            self.log4py.debug("clear history report")
            os.mkdir(self.report_path)
        else:
            self.log4py.debug("history report not exist")

    def do_clear_script_log(self):

        self.clear_file_input(self.script_log)
        self.log4py.debug("clear script.log")

    def is_file_by_suffix_json(self, path):
        Files = os.listdir(path)
        if Files != []:
            for k in range(len(Files)):
                # 提取文件夹内所有文件的后缀
                Files[k] = os.path.splitext(Files[k])[1]

        Str = '.json'
        if Str in Files:
            return True
        else:
            return False

    def is_file_by_suffix_log(cls, path):
        Files = os.listdir(path)
        if Files != []:
            for k in range(len(Files)):
                # 提取文件夹内所有文件的后缀
                Files[k] = os.path.splitext(Files[k])[1]

        Str = '.log'
        if Str in Files:
            return True
        else:
            return False

    def clear_file_input(self, path):
        with open(path, "r+") as f:
            f.seek(0)
            f.truncate()

    def do_clear_anr(self):
        shutil.rmtree(self.anr_path)
        self.log4py.debug("clear history anr")
        os.mkdir(self.anr_path)

if __name__ == '__main__':
    f = FileClearUtil()
    f.do_clear_screenshot()



