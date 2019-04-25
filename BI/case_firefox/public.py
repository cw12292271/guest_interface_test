from selenium import webdriver
import time



'''
自己的火狐浏览器的profile文件路径查看方法
火狐浏览器-帮助-故障排除信息-显示文件夹
必须手工登录一次,并记住密码之后再运行此代码才可以
'''

profile_ff = "C:\\Users\\Lenovo\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\ppw6wgub.default"

fp = webdriver.FirefoxProfile(profile_ff)

driver = webdriver.Firefox(fp)

driver.get("https://admin.t5.site.webot.ai")
time.sleep(5)
# handle = driver.current_window_handle
# driver.switch_to.window(handle)
driver.find_element_by_xpath(
    '//*[@id="primaryNav"]/div[2]/div[1]/div/ul/li[2]/div/a/span[2]').click()
time.sleep(2)
driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/h1[1]/div[2]/i').click()
time.sleep(5)
driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/button[1]').click()
time.sleep(5)
