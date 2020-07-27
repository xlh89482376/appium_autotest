from selenium.webdriver.common.by import By

# =============================================================================================================
# intelligentPliot
start_btn = (By.XPATH, "//*[contains(@text, '开启')]")
# share_btn = (By.ID, "com.mogo.launcher.app:id/module_entrance_id_upload")
share_btn = (By.XPATH, "//*[contains(@text, '分享')]")
shigu_btn = (By.ID, "com.mogo.launcher.app:id/tvAccident")
lukuang_btn = (By.ID, "com.mogo.launcher.app:id/tvRealTimeTraffic")
share_successd_toast = (By.XPATH, "//*[contains(@text, '分享成功')]")