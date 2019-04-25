from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("http://admin.t5.site.webot.ai")
time.sleep(3)
username = 'test1'
password = '123456'
driver.find_element_by_xpath('//*[@id="_content"]/div/section/div/div[3]/div/div[1]/input').clear()
driver.find_element_by_xpath('//*[@id="_content"]/div/section/div/div[3]/div/div[1]/input').send_keys(username)
driver.find_element_by_xpath('//*[@id="pwd1"]').clear()
driver.find_element_by_xpath('//*[@id="pwd1"]').send_keys(password)
time.sleep(5)
driver.find_element_by_xpath('//*[@id="_content"]/div/section/div/div[3]/div/div[6]/button').click()
time.sleep(5)

#获取cookies值
cookies = driver.get_cookies()
print(cookies)
driver.quit()

#删除cookies值
#driver.delete_all_cookies()