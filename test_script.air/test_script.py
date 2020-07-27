import sys, os
sys.path.append(os.getcwd())

from page.page_obj import page_obj
from common.initdriver.InitDriver import InitDriver
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from common.base.Command import Cmd

cmd = Cmd()

class Test_admin_create():


    def setup_class(self):
        pass

    def teardown_class(self):
        pass

    def test_music(self):
        self.driver = InitDriver().init_driver()
        self.admin_create_obj = page_obj(self.driver).re_admin_create()

        self.driver.start_activity("com.android.music", "com.android.music.ui.MusicBrowserActivity")
        time.sleep(10)
        self.driver.quit()


    def test_settings(self):
        auto_setup(__file__)
        connect_device('Android:///')

        start_app("com.android.settings")

        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

        poco(text="声音和振动").click()
        poco(text="电话铃声").click()
        touch(Template(r"tpl1592039192974.png", record_pos=(-0.329, 0.21), resolution=(1440, 2560)))

        cmd.do_stop_and_restart_5037()


    def test_music2(self):
        self.driver = InitDriver().init_driver()
        self.admin_create_obj = page_obj(self.driver).re_admin_create()

        self.driver.start_activity("com.android.music", "com.android.music.ui.MusicBrowserActivity")
        time.sleep(10)
        self.driver.quit()



















