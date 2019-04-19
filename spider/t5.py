import re

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import time
import requests

import xlwt

options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'D:\PycharmProjects\webot2.0\spider\data_pdf'}
options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(executable_path='C:\ProgramData\Anaconda3\chromedriver.exe', chrome_options=options)



driver.implicitly_wait(10)
#driver.maximize_window()
base_url = 'http://www.iachina.cn/IC/tkk/01/3f8f9627-f3fb-4576-8039-5a324935f728.html'
driver.get(base_url)
time.sleep(1)

first_windows = driver.current_window_handle

frames2 = driver.find_element_by_xpath('//*[@id="tr2"]/td/iframe')
#切换到frame1
driver.switch_to_frame(frames2)

driver.find_element_by_id("download").click()
time.sleep(3)