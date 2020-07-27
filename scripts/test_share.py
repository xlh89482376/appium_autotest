import time, allure, pytest


class Test_share():

    @allure.step('启动应用，点击开启行程')
    @allure.feature('分享')
    @allure.story('启动APP')
    def test_start(self, re_share_obj, apm):
        re_share_obj.click_start_btn()
        apm.do_sleep(2)

    @pytest.fixture(name="点击分享按钮")
    # @allure.step('点击分享按钮')
    @allure.feature('分享')
    @allure.story('验证点击分享按钮')
    @allure.severity('blocker')
    def test_share(self, re_share_obj, apm):
        re_share_obj.click_share_btn()
        apm.do_sleep(2)

    @allure.step('点击事故按钮')
    @pytest.mark.usefixtures('点击分享按钮')
    @allure.feature('分享')
    @allure.story('验证分享事故')
    @allure.severity('blocker')
    def test_shigu(self, re_share_obj):
        re_share_obj.click_shigu_btn()
        assert re_share_obj.find_toast()

    @allure.step('点击实时路况按钮')
    @pytest.mark.usefixtures('点击分享按钮')
    @allure.feature('分享')
    @allure.story('验证分享实时路况')
    @allure.severity('blocker')
    def test_lukuang(self, re_share_obj):
        re_share_obj.click_lukuang_btn()
        assert re_share_obj.find_toast()
