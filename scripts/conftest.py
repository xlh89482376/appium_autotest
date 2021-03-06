import pytest, allure, subprocess
from airtest.core.api import *
from common.initdriver.InitDriver import InitDriver
from common.base.Command import Cmd
from common.utils.FileClearUtil import FileClearUtil
from common.utils.FilePathUtil import FilePathUtil
from page.page_obj import page_obj
from page_intel.share_page_obj import share_page_obj
from page_ddox.set_ll_obj import set_ll_page_obj
from common.utils.LoggingUtil import LoggingController
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from common.utils.DateTimeUtil import DateTimeManager
from common.baseapi.BaseAppiumApi import BaseAppiumApi


DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
driver = None

cmd = Cmd()
fc = FileClearUtil()
fp = FilePathUtil()
dt = DateTimeManager()
log = LoggingController()


# 初始化appium driver
@pytest.fixture(scope='session', name="初始化driver", autouse=True)
def get_driver():
    # cmd.do_stop_and_restart_5037()
    try:
        global driver
        if driver is None:
            driver = InitDriver().init_driver()
            log.debug("driver init:%s" % driver)
        return driver

    except Exception as e:
        print(e)
        log.error("driver init fail:%s" % e)
        return None

# 初始化airtest
@pytest.fixture(scope='function', autouse=False, name='poco')
def init_airtest():
    global driver
    if driver is not None:
        # driver = None
        driver.quit()
        driver = None

    auto_setup(__file__)
    connect_device('Android:///')
    poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

    return poco

# 传递page信息
@pytest.fixture(scope='session', autouse=False)
def re_obj():
    admin_create_obj = page_obj(driver).re_admin_create()
    return admin_create_obj

# 传递蘑菇出行页面信息
@pytest.fixture(scope='session', autouse=False)
def re_share_obj():
    share_obj = share_page_obj(driver).re_share()
    return share_obj

# 传递位置模拟器页面信息
@pytest.fixture(scope='session', autouse=False)
def re_set_ll_obj():
    set_ll_obj = set_ll_page_obj(driver).re_set_ll()
    return set_ll_obj

# 传递封装好的AppiumApi
@pytest.fixture(scope='function', name="apm", autouse=False)
def re_appium_api():
    apm = BaseAppiumApi(driver)
    return apm

# aqy = aqy(driver)
#
# @pytest.fixture(name='play')
# def search_and_play_video():
#     aqy.click_search()
#     aqy.click_search_edit_text()
#     aqy.input_search()
#     aqy.enter_search()
#     aqy.continue_play()

# 开始测试前的历史文件清理
@pytest.fixture(scope='session', name="清理历史数据", autouse=True)
def clear():
    fc.do_clear_script_log()
    fc.do_clear_report()
    fc.do_clear_logcat()
    fc.do_clear_crash_log()
    fc.do_clear_screenshot()
    fc.do_clear_anr()
    cmd.clear_logcat()
    cmd.clear_crash_log()
    cmd.clear_anr()
    log.debug("clear device logcat")
    log.debug("clear history file successed")

    yield

    cmd.get_crash_log()
    cmd.get_anr()
    driver.quit()

# 重启adb进程
@pytest.fixture(scope='function', name="re_adb", autouse=False)
def restart_adb_process():
    cmd.do_stop_and_restart_5037()

# 逐条抓取logcat
@pytest.fixture(scope='function', name="清理logcat", autouse=True)
def get_logcat():

    # path = fp.get_logcat_path() + dt.getCurrentDateTime() + r".txt"
    # logcat_file = open(path, 'w')
    # logcat_cmd = "adb logcat -v time"
    # logcat = subprocess.Popen(logcat_cmd, shell=True, stdout=logcat_file, stderr=subprocess.PIPE)
    # log.info("抓取logcat")

    yield

    # logcat.kill()
    # log.info("停止抓取logcat")
    os.popen('adb logcat -b all -c')
    log.debug("【logcat】清空设备logcat")

# 时间记录
@pytest.fixture(scope='session', name="记录时间", autouse=True)
def timer_session_scope():
    start = dt.get_timestamp()
    start_time = dt.formated_time(DATE_FORMAT)
    print(start_time)
    log.info("测试开始时间:%s" % start_time)

    yield

    finish = dt.get_timestamp()
    finish_time = dt.formated_time(DATE_FORMAT)
    print(finish_time)
    total_time = ("{:.2f}s".format(finish - start))
    log.info("测试结束时间:%s" % finish_time)
    log.info("测试用时:%s" % total_time)

# 失败截图log
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("failures") else "w"

        with open("failures", mode) as f:
            if "tmpdir" in item.fixturenames:
                extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                extra = ""
            f.write(rep.nodeid + extra + "\n")

        with allure.step('添加log信息...'):
            # file = driver.get_log('logcat')
            # print(file)
            # allure.attach(str(file), "失败log", attachment_type=allure.attachment_type.TEXT)
            # log_name = "dt.getCurrentDateTime() + r".txt"
            log_path = fp.get_logcat_path + dt.getCurrentDateTime() + r".txt"
            logcat_file = open(log_path, 'w')
            logcat_cmd = "adb logcat -v time"
            logcat = subprocess.Popen(logcat_cmd, shell=True, stdout=logcat_file, stderr=subprocess.PIPE)
            time.sleep(1)
            logcat.kill()
            log.debug("【logcat】抓取logcat 保存路径:%s" % log_path)

            with open(log_path, 'rb') as f:
                context1 = f.read()

            allure.attach(context1, "失败log", attachment_type=allure.attachment_type.TEXT)


        with allure.step('添加失败截图...'):

            screenshot_path = cmd.get_screenshot()
            time.sleep(3)
            log.debug("【screenshot】截图 保存路径:%s" % screenshot_path)
            with open(screenshot_path, 'rb') as f:
                context = f.read()

            allure.attach(context, "失败截图", attachment_type=allure.attachment_type.PNG)









