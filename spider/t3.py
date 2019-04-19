from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import time

driver = webdriver.Chrome()
driver.get("https://www.baidu.com/")
driver.implicitly_wait(20)

mouse = driver.find_element_by_link_text("设置")
ActionChains(driver).move_to_element(mouse).perform()
driver.find_element_by_link_text("搜索设置").click()
time.sleep(2)
# 实例化select
s = Select(driver.find_element_by_id("nr"))
# 定位选项
s.select_by_value("20")  # 选择value="20"的项：通过value属性
time.sleep(2)  # 为了明显的看出变化
s.select_by_index(0)  # 选择第一项选项：通过选项的顺序选择，第一个为 0
time.sleep(2)  # 为了明显的看出变化
s.select_by_visible_text("每页显示50条")  # 选择text="每页显示50条"的值，即在下拉时我们可以看到的文本