import os, time, random
from selenium.webdriver.support.wait import WebDriverWait
from common.base.Command import Cmd
from common.utils.LoggingUtil import LoggingController
from selenium.webdriver.common.by import By
from common.utils.DateTimeUtil import DateTimeManager
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support import expected_conditions as EC

class BaseAppiumApi():
    def __init__(self, driver):
        self.adb = Cmd()
        self.driver = driver
        self.log4py = LoggingController()
        self.ta = TouchAction()
        self.pauseTime = 5

    # find_element_by_name 1.5以上的版本已弃用
    # 替代方法 BY.XPATH  "//*[contains(@text, '开启')]"
    def find_element_I(self,loc,timeout=10,poll=0.5):
        try:
            self.log4py.debug("【定位元素】元素:%s" % str(loc))
            return WebDriverWait(self.driver,timeout,poll).until(lambda x:x.find_element(*loc))
        except Exception as e:
            print(e)
            self.log4py.error("【定位元素失败】元素:%s 超时时间:%ds" % (str(loc), timeout))
            return None

    def find_elements_I(self,loc,timeout=10,poll=0.5):
        try:
            self.log4py.debug("【定位元素】元素:%s" % str(loc))
            return WebDriverWait(self.driver,timeout,poll).until(lambda x:x.find_elements(*loc))
        except Exception as e:
            print(e)
            self.log4py.error("【定位元素失败】元素:%s 超时时间:%ds" % (str(loc), timeout))
            return None

    def click_element(self,loc):
        self.find_element_I(loc).click()
        self.log4py.info("【点击】元素:%s" % str(loc))

    def click_elements(self,loc,num):
        self.find_elements_I(loc)[num].click()
        self.log4py.info("【点击】元素:%s 索引:%d" % (str(loc), num))

    def input_text(self,loc,text):
        """
        在元素中模拟输入（开启appium自带的输入法并配置了appium输入法后，可以输入中英文）
        """
        input = self.find_element_I(loc)
        self.do_clear(input)
        input.send_keys(text)
        self.log4py.info("【输入】元素:%s 文本:%s" % (str(loc), str(text)))

    def get_toast(self, loc, timeout=30, poll=0.5):
        """
        获取toast
        """
        if self.find_element_I(loc, timeout, poll) is None:
            self.log4py.error("Toast get fail")
            return False
        else:
            self.log4py.info("Toast get success")
            return True

    def swipe(self,start_x, start_y, end_x, end_y, duration):
        """
        滑动屏幕
        """
        self.log4py.info("【滑动】起:x-%s y-%s 止:x-%s y-%s" % (start_x, start_y, end_x, end_y))
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)

    def is_enabled(self, loc):
        """
        返回元素是否可用
        """
        element = self.find_element_I(loc)
        isEnabled = element.is_enabled()
        self.log4py.info("%s 是否可用： %s" % (loc, isEnabled))
        return isEnabled

    def is_selected(self, loc):
        """
        返回元素是否选择。
        可以用来检查一个复选框或单选按钮被选中。
        """
        is_selected = self.find_element_I(loc).is_selected()
        self.log4py.debug("%s 是否被选中： %s" % (loc, is_selected))
        return is_selected

    def is_element_exist(self, el):
        """
        判断元素是否存在
        """
        # element = self.find_element_I(loc)
        source = self.get_page_source()
        if el in source:
            self.log4py.debug("元素%s 存在" % el)
            return True
        else:
            self.log4py.error("元素%s 不存在" % el)
            return False

    def do_sleep(self, millisecond=3):
        """
        time.sleep
        """
        try:
            self.log4py.info("【sleep】%ss" % millisecond)
            time.sleep(millisecond)
        except Exception as e:
            self.log4py.error("sleep error:" + str(e))

    def do_navigate_back(self):
        """
        返回
        """
        self.driver.back()
        self.log4py.info("【返回】")

    def get_current_activity(self):
        """
        获取Activity，调用时不需要括号
        """
        activity = self.driver.current_activity
        self.log4py.debug("【当前Activity】%s" % activity)
        return activity

    def get_current_url(self):
        """
        获取当前页面的网址
        """
        url = self.driver.current_url()
        self.log4py.debug("【当前页面网址】%s" % url)
        return url

    def get_page_source(self):
        """
        获取当前页面的源
        """
        # source = self.driver.page_source()
        source = self.driver.page_source
        self.log4py.debug("【当前页面的源】%s" % source)
        return source

    def get_tag_name(self, loc):
        """
        经实践返回的是class name
        """
        tag_name = self.driver.find_element_I(loc).tag_name
        self.log4py.debug("%s TagName: %s" % (loc, tag_name))
        return tag_name

    def get_text(self, loc):
        """
        返回元素的文本值
        """
        text = self.driver.find_element_I(loc).text
        self.log4py.debug("%s text: %s" % (loc, str(text)))
        return text

    def get_screen_size(self):
        """
        返回屏幕分辨率（长和宽）
        """
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        self.log4py.debug("屏幕分辨率：x-%s y-%s" % (x, y))
        return (x, y)

    def do_clear(self, loc):
        """
        清除输入的内容
        """
        element = self.find_element_I(loc)
        element.clear()
        self.log4py.info("【清空输入】%s" % str(loc))

    def do_swipe_up(self, duration_time):
        """
        向上滑动
        """
        size_screen = self.driver.get_screen_size()
        x_start = int(size_screen[0] * 0.5)
        x_end = x_start
        y_start = int(size_screen[1] * 0.75)
        y_end = int(size_screen[1] * 0.25)
        self.driver.swipe(x_start, y_start, x_end, y_end, duration_time)
        self.log4py.debug("【向上滑动屏幕】")

    def do_swipe_down(self, duration_time):
        """
        向下滑动
        """
        size_screen = self.driver.get_screen_size()
        x_start = int(size_screen[0] * 0.5)
        x_end = x_start
        y_start = int(size_screen[1] * 0.25)
        y_end = int(size_screen[1] * 0.75)
        self.driver.swipe(x_start, y_start, x_end, y_end, duration_time)
        self.log4py.debug("【向下滑动屏幕】")

    def do_swipe_left(self, duration_time):
        """
        向左滑动
        """
        size_screen = self.driver.get_screen_size()
        y_start = int(size_screen[1] * 0.5)
        y_end = y_start
        x_start = int(size_screen[0] * 0.75)
        x_end = int(size_screen[0] * 0.25)
        self.driver.swipe(x_start, y_start, x_end, y_end, duration_time)
        self.log4py.debug("【向左滑动屏幕】")

    def do_swipe_right(self, driver, duration_time):
        """
        向右滑动屏幕
        """
        size_screen = self.driver.get_screen_size()
        y_start = int(size_screen[0] * 0.5)
        y_end = y_start
        x_start = int(size_screen[0] * 0.25)
        x_end = int(size_screen[0] * 0.75)
        self.driver.swipe(x_start, y_start, x_end, y_end, duration_time)
        self.log4py.debug("【向右滑动屏幕】")

    def do_tap(self, x, y, count = 500) :
        """
        点击坐标位置
        """
        self.ta.tap(x, y, count)
        self.log4py.info("【点击】坐标:x-%s y-%s" % (x, y))

    def do_pinch(self,element):
        '''
        双指缩放屏幕
        '''
        self.driver.pinch(element=element)
        self.log4py.debug("【双指缩放屏幕】")

    def do_zoom(self, element):
        '''
        放大操作
        '''
        self.driver.zoom(element=element)
        self.log4py.debug("【放大操作】")

    def do_shake(self):
        """
        摇一摇设备
        """
        self.log4py.debug("【摇一摇设备】")
        self.driver.shake()

    def do_flick(self, start_x, start_y, end_x, end_y):
        """
        快速滑动
        """
        self.log4py.debug("x:%s  y:%s 快速滑动至 x：%s  y：%s" % (start_x, start_y, end_x, end_y))
        return self.driver.flick(start_x, start_y, end_x, end_y)

    def get_screenshot(self, filepath):
        """
        截取当前窗口的截图，如果有写入错误会返回False，其它返回True
        """
        try:
            self.driver.get_screenshot_as_file(filepath)
            self.log4py.debug("保存屏幕截图成功，地址：%s" % filepath)
        except Exception as e:
            self.log4py.error("保存屏幕截图失败，失败信息：%s " % str(e))

    def get_contexts(self):
        """
        返回当前会话的当前上下文
        """
        return self.driver.contexts

    def get_current_context(self):
        """
        返回当前会话的当前上下文
        """
        return self.driver.current_context

    def get_context(self):
        """
        返回当前会话中的上下文，使用后可以识别H5页面的控件
        """
        return self.driver.contexts

    def do_reset(self):
        """
        删除应用数据
        """
        self.driver.reset()

    def do_hide_keyboard(self, key_name=None, key=None, strategy=None):
        """
        隐藏键盘，安卓不需要参数。ios使用key_name隐藏
        """
        self.driver.hide_keyboard()

    def do_keyevent(self, keycode, metastate=None):
        """
        发送按键码,Android特有
        按键码可参考：http://developer.android.com/reference/android/view/KeyEvent.html
        """
        self.driver.keyevent(keycode)
        self.log4py.info("【发送按键码】keycode:%s" % keycode)

    def do_press_keycode(self, keycode, metastate=None):
        """
        发送按钮码，Android独有
        参考：http://developer.android.com/reference/android/view/KeyEvent.html
        """
        self.driver.press_keycode(keycode)

    def do_long_press_keycode(self, keycode, metastate=None):
        """
        发送一个长按的按键码
        """
        self.driver.long_press_keycode(keycode)

    def do_background_app(self, seconds):
        """
        后台运行app多少秒
        """
        self.log4py.info("将app放置后台%s秒" % str(seconds))
        self.driver.background_app(seconds)

    def is_app_installed(self, bundle_id):
        """
        检查app是否安装
        """
        is_installed = self.driver.is_app_installed(bundle_id)
        self.log4py.debug("%s 是否安装: %s" % (bundle_id, is_installed))
        return is_installed

    def do_install_app(self, app_path):
        """
        安装app
        """
        self.driver.install_app(app_path)
        self.log4py.debug("已安装应用: %s" % app_path)

    def do_remove_app(self, app_id):
        """
        删除app
        """
        self.log4py.debug("删除app：%s" % app_id)
        self.driver.remove_app(app_id)

    def do_launch_app(self):
        """
        启动app
        """
        self.log4py.debug("启动app")
        self.driver.launch_app()

    def do_close_app(self):
        """
        关闭app
        """
        self.log4py.debug("关闭app")
        self.driver.close_app()

    def do_start_activity(self, app_package, app_activity, **opts):
        """
        在测试过程中打开任意活动。如果活动属于另一个应用程序，该应用程序的启动和活动被打开。安卓独有
        """
        # self.log4py.info("【启动应用】package：%s activity：%s" % (app_package, app_activity))
        self.driver.start_activity(app_package, app_activity)

    def do_lock(self, seconds):
        """
        锁屏一段时间，ios独有
        """
        self.log4py.debug("锁屏%s秒" % seconds)
        self.driver.lock(seconds)

    def do_open_notifications(self):
        """
        打系统通知栏（仅支持API 18 以上的安卓系统）
        """
        self.log4py.debug("打开系统通知栏")
        self.driver.open_notifications()

    def get_network_connection(self):
        """
        返回网络类型 数值
        """
        network_connection = self.driver.network_connection
        self.log4py.debug("网络类型： %s" % network_connection)
        return network_connection

    def set_network_connection(self, connectionType):
        """
        设置网络类型，安卓独有
        Possible values:
            Value (Alias)      | Data | Wifi | Airplane Mode
            -------------------------------------------------
            0 (None)           | 0    | 0    | 0
            1 (Airplane Mode)  | 0    | 0    | 1
            2 (Wifi only)      | 0    | 1    | 0
            4 (Data only)      | 1    | 0    | 0
            6 (All network on) | 1    | 1    | 0
        用法：
        先加载from appium.webdriver.connectiontype import ConnectionType
        dr.set_network_connection(ConnectionType.WIFI_ONLY)
        """
        self.log4py.debug("网络切换为： %s" % connectionType)
        self.driver.set_network_connection(connectionType)

    def get_available_ime_engines(self):
        """
        返回安卓设备可用的输入法，安卓独有
        """
        available_ime = self.driver.available_ime_engines
        self.log4py.info("可见的输入法：%s" % available_ime)
        return available_ime

    def is_ime_active(self):
        """
        检查设备是否有输入法服务活动，安卓独有
        """
        is_active = self.driver.is_ime_active()
        self.log4py.debug("是否有输入法服务: %s" % is_active)
        return is_active

    def do_activate_ime_engine(self, engine):
        """
        激活安卓设备中的指定输入法，设备可用输入法可以从“available_ime_engines”获取
        """
        self.log4py.info("激活输入法： %s" % engine)
        self.driver.activate_ime_engine(engine)

    def deactivate_ime_engine(self):
        """
        关闭安卓设备当前的输入法,安卓独有
        """
        self.log4py.info("关闭当前输入法")
        self.driver.deactivate_ime_engine()

    def get_active_ime_engine(self):
        """
        返回当前输入法的包名
        """
        current_ime = self.driver.active_ime_engine
        self.log4py.info("获取到当前的输入法： %s" % current_ime)
        return current_ime

    def device_time(self):

        return self.driver.device_time()

    def toggle_location_services(self):
        """
        打开安卓设备上的位置定位设置,安卓独有
        """
        self.log4py.debug("打开位置定位设置")
        self.driver.toggle_location_services()

    def set_location(self, latitude, longitude, altitude):
        """
        设置经纬度
        """
        self.log4py.debug("设置纬度：%s 经度：%s  高度：%s" % (latitude, longitude, altitude))
        self.driver.set_location(latitude, longitude, altitude)