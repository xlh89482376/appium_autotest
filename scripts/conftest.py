import sys, os
sys.path.append(os.getcwd())

import time, allure, pytest
from common.init_driver import init_driver
import subprocess

driver = None

@pytest.fixture(scope='function', autouse=True)
def android():
    global driver
    if driver is None:
        driver = init_driver()
    return driver

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


# 数据库连接
@pytest.fixture()
def db():
    print('Connection successful')

    yield

    print('Connection closed')

@pytest.fixture(scope='class')
def class_scope():
    pass

@pytest.fixture(scope='module')
def mod_scope():
    pass

@pytest.fixture(scope='session')
def sess_scope():
    pass

@pytest.fixture(scope='function')
def func_scope():
    pass



@pytest.fixture(scope='session', autouse=True)
def timer_session_scope():
    start = time.time()
    print('\nstart: {}'.format(time.strftime(DATE_FORMAT, time.localtime(start))))

    yield

    finished = time.time()
    print('finished: {}'.format(time.strftime(DATE_FORMAT, time.localtime(finished))))
    print('Total time cost: {:.3f}s'.format(finished - start))

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    '''
    hook pytest失败
    :param item:
    :param call:
    :return:
    '''
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    # we only look at actual failing test calls, not setup/teardown
    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode) as f:
            # let's also access a fixture for the fun of it
            if "tmpdir" in item.fixturenames:
                extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                extra = ""
            f.write(rep.nodeid + extra + "\n")
        # pic_info = adb_screen_shot()
        with allure.step('添加失败截图...'):
            allure.attach(driver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)

        now = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime(time.time()))
        filename = now + r"log.txt"
        os.system('touch %s' % filename)
        logcat_file = open(filename, "w")
        logcmd = "adb logcat -v time"
        Poplog = subprocess.Popen(logcmd, stdout=logcat_file, stderr=subprocess.PIPE)

        with allure.step('添加Logcat信息...'):
            allure.attach(logcat_file, "失败log", allure.attachment_type.TXT)

        logcat_file.close()
        Poplog.terminate()




