from selenium import webdriver
import time
import unittest
import time
from HTMLTestRunner_PY3 import HTMLTestRunner

from public import Login
import string

class pandect_page(unittest.TestCase):

    '''总览页面测试'''
    def setUp(self):

        profile_ff = "C:\\Users\\Lenovo\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\ppw6wgub.default"
        fp = webdriver.FirefoxProfile(profile_ff)
        self.driver = webdriver.Firefox(fp)

        self.driver.get("http://admin.t5.site.webot.ai")
        time.sleep(2)

        print(self.driver.current_url)
        self.driver.find_element_by_xpath(
            '//*[@id="primaryNav"]/div[2]/div[1]/div/ul/li[2]/div/a/span[2]').click()
        time.sleep(1)
        print(self.driver.current_url)
        self.driver.find_element_by_xpath('//*[@id="_content"]/div/div/h1[1]/div[2]/input').clear()
        self.driver.find_element_by_xpath('//*[@id="_content"]/div/div/h1[1]/div[2]/input').send_keys("2018年04月25日 - 2018年04月26日")
        time.sleep(1)

    def test_01_Robot_session(self):
        '''机器人服务数据-机器人会话量字段校验'''
        driver = self.driver

        text_Robot_session = driver.find_element_by_xpath(
            '//*[@id="_content"]/div/div/div[1]/div/div[1]/div/div/div[2]').text
        print(text_Robot_session)
        self.assertEqual(text_Robot_session,'机器人会话量',msg="机器人会话量字段错误")


    def test_02_Robot_session_data(self):
        '''机器人服务数据-机器人会话量数据非负校验'''
        driver = self.driver

        text_Robot_session_data = driver.find_element_by_xpath(
            '//*[@id="_content"]/div/div/div[1]/div/div[1]/div/div/div[1]').text
        print(text_Robot_session_data)
        self.assertTrue(int(text_Robot_session_data) >= 0, msg="机器人会话量数据为负数")
        return int(text_Robot_session_data)

    def test_03_Robot_solution(self):
        '''机器人服务数据-机器人解决量字段错误校验'''
        driver = self.driver

        text_Robot_solution = driver.find_element_by_xpath(
             '//*[@id="_content"]/div/div/div[1]/div/div[2]/div/div[1]/div[2]').text
        print(text_Robot_solution)
        self.assertEqual(text_Robot_solution, '机器人解决量', msg="机器人解决量字段错误")

    def test_04_Robot_solution_data(self):
        '''机器人服务数据-机器人会话量数据非负校验'''
        driver = self.driver

        text_Robot_solution_data = driver.find_element_by_xpath(
             '//*[@id="_content"]/div/div/div[1]/div/div[2]/div/div[1]/div[1]').text
        print(text_Robot_solution_data)
        self.assertTrue(int(text_Robot_solution_data) >= 0, msg="机器人解决量数据为负数")
        return int(text_Robot_solution_data)

    def test_05_Rttac(self):
        '''机器人服务数据-机器人转人工会话量字段校验'''
        driver = self.driver

        text_Rttac = driver.find_element_by_xpath(
            '//*[@id="_content"]/div/div/div[1]/div/div[3]/div/div[1]/div[2]').text
        print(text_Rttac)
        self.assertEqual(text_Rttac, '机器人转人工会话量', msg="机器人转人工会话量字段错误")

    def test_06_Rttac_data(self):
        '''机器人服务数据-机器人转人工会话量数据非负校验'''
        driver = self.driver

        text_Rttac_data = driver.find_element_by_xpath(
            '//*[@id="_content"]/div/div/div[1]/div/div[3]/div/div[1]/div[1]').text
        print(text_Rttac_data)
        self.assertTrue(int(text_Rttac_data) >= 0, msg="机器人转人工会话量数据为负数")
        return int(text_Rttac_data)

    def test_07_Robot_service_data(self):
        '''机器人服务数据-数据间校验'''
        #driver = self.driver

        sa = self.test_04_Robot_solution_data() + self.test_06_Rttac_data()
        print('机器人会话量' '=' '机器人解决量 + 机器人转人工会话量')
        self.assertEqual(self.test_02_Robot_session_data(), sa , msg="数据矛盾")


    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    #unittest.main()

    testunit = unittest.TestSuite()
    testunit.addTest(pandect_page("test_01_Robot_session"))
    testunit.addTest(pandect_page("test_02_Robot_session_data"))
    testunit.addTest(pandect_page("test_03_Robot_solution"))
    testunit.addTest(pandect_page("test_04_Robot_solution_data"))
    testunit.addTest(pandect_page("test_05_Rttac"))
    testunit.addTest(pandect_page("test_06_Rttac_data"))
    testunit.addTest(pandect_page("test_07_Robot_service_data"))

    # 按照一定格式获取当地时间
    now_time = time.strftime("%Y-%m-%d %A %H_%M_%S ")

    # 定义报告存放路径
    fp = open('D:\\PycharmProjects\\webot2.0\\BI\\report\\' + now_time + 'result.html', 'wb')
    # 定义测试报告
    runner = HTMLTestRunner(stream=fp,
                            title="test_project测试报告",
                            description="用例执行情况：")
    runner.run(testunit)
    fp.close()