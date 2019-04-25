from selenium import webdriver
import time

'''
利用cookies值登录
{'domain': 'admin.t5.site.webot.ai',
'expiry': 1525510095, 'httpOnly': False,
'name': 'Auth',
'path': '/',
'secure': False,
'value': 'e6fae2fa-4ac0-11e8-b4d2-0242ac110007'}
'''
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("http://admin.t5.site.webot.ai")
time.sleep(3)

#设置cookies值,基本格式
c1 = {'domain': 'admin.t5.site.webot.ai',
'expiry': 1525510095, 'httpOnly': False,
'name': 'Auth',
'path': '/',
'secure': False,
'value': 'e6fae2fa-4ac0-11e8-b4d2-0242ac110007'}

#添加cookies
driver.add_cookie(c1)
time.sleep(3)

#刷新之后观察是否已经登录成功
driver.refresh()
time.sleep(5)

driver.quit()