from selenium import webdriver
import time

class Login():
    def user_login(self,driver,username,password):
        driver.find_element_by_xpath('//*[@id="_content"]/div/section/div/div[3]/div/div[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="_content"]/div/section/div/div[3]/div/div[1]/input').send_keys(username)
        driver.find_element_by_xpath('//*[@id="pwd1"]').clear()
        driver.find_element_by_xpath('//*[@id="pwd1"]').send_keys(password)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="_content"]/div/section/div/div[3]/div/div[6]/button').click()
        handle = driver.current_window_handle
        driver.switch_to.window(handle)



