from selenium.webdriver.common.by import By

# =============================================================================================================
# intelligentPliot
# start_btn = (By.XPATH, "//*[contains(@text, '开启')]")
share_btn = (By.ID, "module_entrance_id_upload")
# share_btn = (By.XPATH, "//*[contains(@text, '分享')]")
yongdu_btn = (By.ID, "tvBlock")
# shigu_btn = (By.ID, "tvAccident")
shigu_btn = (By.XPATH, "//*[contains(@text, '事故')]")
lukuang_btn = (By.ID, "tvRealTimeTraffic")
jiancha_btn = (By.ID, "tvTrafficCheck")
qiuzhu_btn = (By.ID, "tvSeekHelp")
fenglu_btn = (By.ID, "tvClosure")
jishui_btn = (By.ID, "tvStagnantWater")
jiebing_btn = (By.ID,"tvRoadIcy")
shigong_btn = (By.ID, "tvConstruction")
nongwu_btn = (By.ID, "tvDenseFog")

share_successd_toast = (By.XPATH, "//*[contains(@text, '分享成功')]")

# v2x
report_true_btn = (By.ID, "com.mogo.launcher.app:id/ivEventReportTrue")
report_err_btn = (By.ID, "com.mogo.launcher.app:id/ivEventReportErr")

report_toast = (By.XPATH, "//*[contains(@text, '已反馈')]")



