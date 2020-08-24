from common.baseapi.BaseAppiumApi import BaseAppiumApi
import page_intel

class share(BaseAppiumApi):
    def __init__(self, driver):
        BaseAppiumApi.__init__(self, driver)

    def click_share_btn(self):
        self.click_element(page_intel.share_btn)

    def click_shigu_btn(self):
        self.click_element(page_intel.shigu_btn)

    def click_lukuang_btn(self):
        self.click_element(page_intel.lukuang_btn)

    def click_yongdu_btn(self):
        self.click_element(page_intel.yongdu_btn)

    def click_jiancha_btn(self):
        self.click_element(page_intel.jiancha_btn)

    def click_qiuzhu_btn(self):
        self.click_element(page_intel.qiuzhu_btn)

    def click_fenglu_btn(self):
        self.click_element(page_intel.fenglu_btn)

    def click_jishui_btn(self):
        self.click_element(page_intel.jishui_btn)

    def click_jiebing_btn(self):
        self.click_element(page_intel.jiebing_btn)

    def click_shigong_btn(self):
        self.click_element(page_intel.shigong_btn)

    def click_nongwu_btn(self):
        self.click_element(page_intel.nongwu_btn)

    def find_toast(self):
        return self.get_toast(page_intel.share_successd_toast)

    def click_report_true_btn(self):
        self.click_element(page_intel.report_true_btn)

    def click_report_err_btn(self):
        self.click_element(page_intel.report_err_btn)

    def find_report_toast(self):
        return self.get_toast(page_intel.report_toast)