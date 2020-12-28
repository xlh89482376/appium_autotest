import os
from common.utils.LoggingUtil import LoggingController


class FilePathUtil():


    def __init__(self):
        self.log4py = LoggingController()
        # self.project_path = os.getcwd().split("common")[0]
        # self.monkey_config = self.project_path + "config" + os.sep + "launcher.ini"
        # self.monkey_log = self.project_path + "monkey" + os.sep + "logs"

    def get_project_path(self):
        abspath = os.getcwd()
        project_path = abspath.split("appium_autotest")[0] + "appium_autotest" + os.sep
        return project_path

    def get_monkey_config_path(self):
        monkey_config_path = self.get_project_path() + "config" + os.sep + "launcher.ini"
        return monkey_config_path

    def get_broadcast_path(self):
        # broadcast_path = self.get_project_path() + os.sep + "testdata" + os.sep + "yaml" + os.sep + "broadcast.yml"
        broadcast_path = self.get_project_path() + "testdata" + os.sep + "yaml" + os.sep + "broadcast.yml"
        return broadcast_path

    def get_config_run_path(self):
        config_run_path = self.get_project_path() + os.sep + "config" + os.sep + "run.ini"
        return config_run_path

    def get_scripts_log_path(self):
        scripts_log_path = self.get_project_path() + os.sep + "result" + os.sep + "logs" + os.sep + "logs4script" + os.sep + "script.log"
        self.log4py.info(scripts_log_path)
        return scripts_log_path

    def get_report_path(self):
        report_path = self.get_project_path() + os.sep + "result" + os.sep + "reports"
        return report_path

    def get_yaml_path(self):
        yaml_path = self.get_project_path() + os.sep + "testdata" + os.sep + "yaml" + os.sep
        return yaml_path

    def get_service_path(self):
        service_path = self.get_project_path() + os.sep + "config" + os.sep + "Service.ini"
        return service_path

    def get_logcat_path(self):
        logcat_path = self.get_project_path() + os.sep + "result" + os.sep + "logs" + os.sep + "logcat" + os.sep
        return logcat_path

    def get_crash_log_path(self):
        crash_log_path = self.get_project_path() + os.sep + "result" + os.sep + "logs" + os.sep + "crashlog"
        return crash_log_path

    def get_screenshot_path(self):
        screenshot_path = self.get_project_path() + os.sep + "result" + os.sep + "screenshot" + os.sep
        return screenshot_path

    def get_xml_path(self):
        xml_path = self.get_project_path() + "analysis_UIdump" + os.sep + "xml_file" + os.sep
        return xml_path

    def get_yml_path(self):
        yaml_path = self.get_project_path() + "analysis_UIdump" + os.sep + "yml_file" + os.sep
        return yaml_path

    def get_anr_path(self):
        anr_path = self.get_project_path() + os.sep + "result" + os.sep + "logs" + os.sep + "anr" + os.sep
        return anr_path

if __name__ == '__main__':
    f = FilePathUtil()
    # print(f.get_project_path())
    # print(f.get_config_run_path())
    # print(f.get_xml_path())
    print(os.getcwd().split("common")[0])
    print(os.getcwd().split("appium_autotest")[0])