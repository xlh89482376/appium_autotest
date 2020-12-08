import sys
import json
import logging
import traceback
from common.base.Command import Cmd
from common.utils.SendEmailUtil import SendMail
from common.utils.AnalyzeLogUtil import DeviceLog
from common.utils.FilePathUtil import FilePathUtil
from common.utils.ConfigUtil import ConfigController

section = "monkey"
section1 = "gmail"
packageName = ConfigController(FilePathUtil().get_monkey_config_path()).get(section, "packageName")
appName = ConfigController(FilePathUtil().get_monkey_config_path()).get(section, "appName")
rcpt_list = ConfigController(FilePathUtil().get_monkey_config_path()).get(section1, "receiver")

def monkey_test(serialno, packageName, throttle, count):

    cmd = Cmd()
    device_log = DeviceLog(serialno)

    device_log.init()

    cmd.run_monkey(serialno, packageName, FilePathUtil().get_monkey_log_path(), throttle, count)
    # logging.info(">>> Done")
    # 生成dumpsys信息
    # logging.info(">>> Dumpsys activities")
    # cmd.dumpsys_activity(device_log.dump_dir)
    # logging.info(">>> Done")


    device_log.check(packageName)

    anr_cnt, crash_cnt, att_list = device_log.get()
    # 发送邮件
    send_log(rcpt_list, anr_cnt, crash_cnt, att_list)


def send_log(rcpt_list, anr_cnt, crash_cnt, att_list):
    # 如果没有anr和crash，则不发邮件
    # prj_name = prj_info["name"]

    if anr_cnt == 0 and crash_cnt == 0:
        subject = u"%s Monkey测试通过" % appName
    else:
        subject = u"%s Monkey测试异常提醒" % appName
    content = "<table border='1' cellspacing='0' cellpadding='0'>" \
              + "<tr align='center'><th style='width:600px' colspan='2'>{} Monkey测试结果</th></tr>".format(appName) \
              + "<tr><td width='30%%'><b>SN</b></td><td width='70%%'>{}</a></td></tr>".format(Cmd().get_device_SN()) \
              + "<tr><td width='30%%'><b>安装包文件名</b></td><td width='70%%'>{}</a></td></tr>".format(appName) \
              + "<tr><td width='30%%'><b>安装包包名</b></td><td width='70%%'>{}</td>".format(packageName) \
              + "<tr><td width='30%%'><b>发现ANR次数</b></td><td width='70%%'>{}</td>".format(anr_cnt) \
              + "<tr><td width='30%%'><b>发现CRASH次数</b></td><td width='70%%'>{}</td>".format(crash_cnt) \
              + "</table>" \
              + "<br/><p>具体日志见附件</p>"

    status, reason = SendMail().send_mail(rcpt_list, subject, content, att_list=att_list)
    if status:
        # logging.info("Succeed in sending mails")
        print("send email successed")
    else:
        # logging.error("Failed to send mails, reason: %s" % reason)
        print("send email failed")


# def get_package(prj_ver, prj_info, apk_url, apk_path):
#     # 如果apk_url不为空，优先下载该apk
#     if apk_url != "":
#         logging.info("[get_package] get apk from url: {}".format(apk_url))
#         apk_path = get_apk.get_apk_from_url(apk_url, prj_ver)
#     # 如果apk_url为空，apk_path不为空，直接使用该路径的apk
#     elif apk_path != "":
#         logging.info("[get_package] get apk from local: {}".format(apk_path))
#     # 如果apk_url和apk_path均为空，则通过prj_info下载最新包
#     else:
#         logging.info("[get_package] get latest apk...")
#         apk_path = get_apk.get_latest_apk()
#     # 如果apk_path为None，则报错，否则返回包
#     if apk_path is None:
#         logging.error("[get_package] failed to get package")
#         sys.exit(-1)
#     return Package(apk_path)

if __name__ == '__main__':
    print(rcpt_list)
