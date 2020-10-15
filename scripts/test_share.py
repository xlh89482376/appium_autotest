import time, allure, pytest


class Test_share():

    # @pytest.fixture()
    # def fake_location(self, re_set_ll_obj, apm):
    #     apm.do_start_activity("com.glsx.ddbox", "com.example.mockgps.MockTrackActivity")
    #     re_set_ll_obj.click_clear_btn()
    #     re_set_ll_obj.click_input_btn()
    #     re_set_ll_obj.input_start_ll("116.41736,39.983787")
    #     re_set_ll_obj.input_end_ll("116.41735,39.983997")
    #     re_set_ll_obj.click_commit_btn()
    #     time.sleep(1)
    #     re_set_ll_obj.click_start_btn()
    #     time.sleep(10)
    #
    # @pytest.fixture()
    # def fake_location_1(self, re_set_ll_obj, apm):
    #     apm.do_start_activity("com.glsx.ddbox", "com.example.mockgps.MockTrackActivity")
    #     re_set_ll_obj.click_clear_btn()
    #     re_set_ll_obj.click_input_btn()
    #     re_set_ll_obj.input_start_ll("116.417371,39.983245")
    #     re_set_ll_obj.input_end_ll("116.417323,39.984585")
    #     re_set_ll_obj.click_commit_btn()
    #     time.sleep(1)
    #     re_set_ll_obj.click_start_btn()
    #     time.sleep(1)

    @pytest.fixture(name="点击分享按钮")
    @allure.step('点击分享按钮')
    @allure.feature('分享')
    @allure.story('验证点击分享按钮')
    @allure.severity('blocker')
    def test_share(self, re_share_obj, apm):
        # apm.do_start_activity("com.mogo.launcher.app",
        #                       "com.zhidao.mogo.module.main.independent.MainIndependentActivity")
        re_share_obj.click_share_btn()
        apm.do_sleep(2)

    @allure.step('点击事故按钮')
    @pytest.mark.usefixtures('点击分享按钮')
    @allure.feature('分享')
    @allure.story('验证分享事故')
    @allure.severity('blocker')
    def test_shigu(self, re_share_obj):
        re_share_obj.click_lukuang_btn()
        assert re_share_obj.find_toast()

    @allure.step('触发事故')
    # @pytest.mark.usefixtures()
    @allure.feature('触发')
    @allure.story('验证触发事故')
    @allure.severity('blocker')
    def test_trigger_shigu(self, apm, re_share_obj):
        # apm.do_start_activity("com.mogo.launcher.app",
        #                       "com.zhidao.mogo.module.main.independent.MainIndependentActivity")
        re_share_obj.click_report_true_btn()
        assert re_share_obj.find_report_toast()

    @allure.step('点击拥堵按钮')
    @pytest.mark.usefixtures('点击分享按钮')
    @allure.feature('分享')
    @allure.story('验证分享拥堵')
    @allure.severity('blocker')
    def test_yongdu(self, re_share_obj):
        re_share_obj.click_yongdu_btn()
        assert re_share_obj.find_toast()

    @allure.step('点击交通检查按钮')
    @pytest.mark.usefixtures('点击分享按钮')
    @allure.feature('分享')
    @allure.story('验证分享事故')
    @allure.severity('blocker')
    def test_jiancha(self, re_share_obj):
        re_share_obj.click_jiancha_btn()
        assert re_share_obj.find_toast()

    @allure.step('点击故障求助按钮')
    @pytest.mark.usefixtures('点击分享按钮')
    @allure.feature('分享')
    @allure.story('验证分享故障求助')
    @allure.severity('blocker')
    def test_qiuzhu(self, re_share_obj):
        re_share_obj.click_qiuzhu_btn()
        assert re_share_obj.find_toast()

    @allure.step('点击封路按钮')
    @pytest.mark.usefixtures('点击分享按钮')
    @allure.feature('分享')
    @allure.story('验证分享封路')
    @allure.severity('blocker')
    def test_fenglu(self, re_share_obj):
        re_share_obj.click_fenglu_btn()
        assert re_share_obj.find_toast()

    @allure.step('点击积水按钮')
    @pytest.mark.usefixtures('点击分享按钮')
    @allure.feature('分享')
    @allure.story('验证分享道路积水')
    @allure.severity('blocker')
    def test_jishui(self, re_share_obj):
        re_share_obj.click_jishui_btn()
        assert re_share_obj.find_toast()

    @allure.step('点击结冰按钮')
    @pytest.mark.usefixtures('点击分享按钮')
    @allure.feature('分享')
    @allure.story('验证分享道路结冰')
    @allure.severity('blocker')
    def test_jiebing(self, re_share_obj):
        re_share_obj.click_jiebing_btn()
        assert re_share_obj.find_toast()

    @allure.step('点击施工按钮')
    @pytest.mark.usefixtures('点击分享按钮')
    @allure.feature('分享')
    @allure.story('验证分享施工')
    @allure.severity('blocker')
    def test_shigong(self, re_share_obj):
        re_share_obj.click_shigong_btn()
        assert re_share_obj.find_toast()

    @allure.step('点击浓雾按钮')
    @pytest.mark.usefixtures('点击分享按钮')
    @allure.feature('分享')
    @allure.story('验证分享浓雾')
    @allure.severity('blocker')
    def test_nongwu(self, re_share_obj):
        re_share_obj.click_nongwu_btn()
        assert re_share_obj.find_toast()


    @allure.step('点击事故按钮')
    @pytest.mark.usefixtures('fake_location','点击分享按钮')
    @allure.feature('分享')
    @allure.story('验证分享事故')
    @allure.severity('blocker')
    def test_shigu(self, re_share_obj):
        re_share_obj.click_shigu_btn()
        assert re_share_obj.find_toast()

    @allure.step('点击事故按钮')
    @pytest.mark.usefixtures("fake_location_1")
    @allure.feature('触发')
    @allure.story('验证触发分享事故')
    @allure.severity('blocker')
    def test_trigger_shigu(self, apm, re_share_obj):
        apm.do_start_activity("com.mogo.launcher.app",
                              "com.zhidao.mogo.module.main.independent.MainIndependentActivity")
        re_share_obj.click_report_true_btn()
        assert re_share_obj.find_report_toast()









