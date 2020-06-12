import time, os, logging

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from common.init_driver import init_driver
from common.base import base
import subprocess
import functools

class tools(base):

    def __init__(self, driver):
        base.__init__(self, driver)

    def getTime(self):
        now = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime(time.time()))
        return now

    def getImage(function):
        @functools.wraps(function)
        def get_ErrImage(self, *args, **kwargs):
            try:
                result = function(self, *args, **kwargs)
            except:
                # timestr = time.strftime("%Y-%m-%d_%H_%M_%S")
                self.driver.get_screenshot_as_file("1111222.png")
            else:
                logging.info(" %s 脚本运行正常" %
                             (function.__name__)
                             )
            return result

        return get_ErrImage


    # logcat
    def logcat(self, filename):
        now = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime(time.time()))
        os.system('mkdir %s')
        filename = "./logs/" + now + r"log.txt"
        logcat_file = open(filename, "w")
        logcmd = "adb logcat -v time"
        Poplog = subprocess.Popen(logcmd, stdout=logcat_file, stderr=subprocess.PIPE)




    # 封装截图方法
    def take_screenShot(self, name="takeShot"):
        '''
        method explain:获取当前屏幕的截图
        parameter explain：【name】 截图的名称
        Usage:
            device.take_screenShot(u"个人主页")   #实际截图保存的结果为：2018-01-13_17_10_58_个人主页.png
        '''
        day = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        fq = "../screenShots/" + day
        # fq =os.getcwd()[:-4] +'screenShots\\'+day    根据获取的路径，然后截取路径保存到自己想存放的目录下
        tm = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime(time.time()))
        type = '.png'
        filename = ""
        if os.path.exists(fq):
            filename = fq + "//" + tm + "_" + name + type
        else:
            os.makedirs(fq)
            filename = fq + "//" + tm + "_" + name + type
        # c = os.getcwd()
        # r"\\".join(c.split("\\"))     #此2行注销实现的功能为将路径中的\替换为\\
        self.driver.get_screenshot_as_file(filename)

    def get_Toast(self, message):  # 查找toast值
        '''
        method explain:查找toast的值,与find_Toast实现方法一样，只是不同的2种写法
        parameter explain：【text】查找的toast值
        Usage:
            device.get_Toast('再按一次退出iBer')
        '''
        logging.info("查找toast值---'%s'" % (message))
        try:
            message = '//*[@text=\'{}\']'.format(message)
            ele = WebDriverWait(self.driver, 5, 0.5).until(
                expected_conditions.presence_of_element_located((By.XPATH, message)))
            return ele.get_attribute("text")
            logging.info("查找到toast----%s" % message)
        except:
            logging.error("未查找到toast----%s" % message)
            return False

        # 多点滑动，类似操作九宫格
        def multipoint_swipe(self, points):
            try:
                touch_action = TouchAction(self.driver)
                press_xy = points[0]
                touch_action.press(press_xy[0], press_xy[1])
                for i in points[1:]:
                    touch_action.move_to(i[0], i[1]).wait(1000)
                touch_action.release().perform()
            except:
                logging.info('zoom-in')

    # 放大地图的操作
    def zoom_in(self):
        try:
            x, y = self.get_size()
            action1 = TouchAction(self.driver)
            action2 = TouchAction(self.driver)
            zoom_action = MultiAction(self.driver)

            action1.press(x=x * 0.4, y=y * 0.4).wait(1000).move_to(x=x * 0.2, y=y * 0.2).wait(1000).release()
            action2.press(x=x * 0.6, y=y * 0.6).wait(1000).move_to(x=x * 0.8, y=y * 0.8).wait(1000).release()
            logging.info('start zoom-in...')
            zoom_action.add(action1, action2)
            zoom_action.perform()
        except:
            logging.info('zoom-in')

    # 缩小地图的操作
    def zoom_out(self):
        try:
            x, y = self.get_size()
            action1 = TouchAction(self.driver)
            action2 = TouchAction(self.driver)
            zoom_action = MultiAction(self.driver)

            action1.press(x=x * 0.2, y=y * 0.2).wait(1000).move_to(x=x * 0.4, y=y * 0.4).wait(1000).release()
            action2.press(x=x * 0.8, y=y * 0.8).wait(1000).move_to(x=x * 0.6, y=y * 0.6).wait(1000).release()

            logging.info('start zoom-out...')
            zoom_action.add(action1, action2)
            zoom_action.perform()
        except:
            logging.info('zoom-in')

    # 等待元素，10秒后未出现则结束寻找
    def waitForElementPresent(self, *loc):
        try:
            WebDriverWait(self.driver, 10, 0.5).until(EC.visibility_of_all_elements_located(loc))
        except NoSuchElementException:
            logging.info('no such element')
        else:
            logging.info("find_element")