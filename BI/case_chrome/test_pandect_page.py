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
        self.driver = webdriver.Chrome()

        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.base_url = 'http://admin.t5.site.webot.ai'

    def test_Robot_session(self):
        '''机器人服务数据-机器人会话量'''
        driver = self.driver
        driver.get(self.base_url)
        username = 'test1'
        password = '123456'
        Login().user_login(driver, username, password)
        time.sleep(2)
        print(driver.current_url)

        driver.find_element_by_xpath(
            '//*[@id="primaryNav"]/div[2]/div[1]/div/ul/li[2]/div/a/span[2]').click()
        time.sleep(2)
        print(driver.current_url)

        text_Robot_session = driver.find_element_by_xpath(
            '//*[@id="_content"]/div/div/div[1]/div/div[1]/div/div/div[2]').text
        print(text_Robot_session)
        self.assertEqual(text_Robot_session,'机器人会话量',msg="机器人会话量字段错误")
        text_Robot_session_data = driver.find_element_by_xpath(
            '//*[@id="_content"]/div/div/div[1]/div/div[1]/div/div/div[1]').text
        print(text_Robot_session_data)

        text_Robot_solution = driver.find_element_by_xpath(
            '//*[@id="_content"]/div/div/div[1]/div/div[2]/div/div[1]/div[2]').text
        print(text_Robot_solution)
        self.assertEqual(text_Robot_solution, '机器人解决量', msg="机器人解决量字段错误")
        text_Robot_solution_data = driver.find_element_by_xpath(
            '//*[@id="_content"]/div/div/div[1]/div/div[2]/div/div[1]/div[1]').text
        print(text_Robot_solution_data)
        text_Rttac = driver.find_element_by_xpath(
            '//*[@id="_content"]/div/div/div[1]/div/div[3]/div/div[1]/div[2]').text
        print(text_Rttac)
        self.assertEqual(text_Rttac, '机器人转人工会话量', msg="机器人转人工会话量字段错误")
        text_Rttac_data = driver.find_element_by_xpath(
            '//*[@id="_content"]/div/div/div[1]/div/div[3]/div/div[1]/div[1]').text
        print(text_Rttac_data)

        sa = int(text_Robot_solution_data) + int(text_Rttac_data)
        print('机器人解决量 + 机器人转人工会话量' + '=' + str(sa))
        self.assertEqual(int(text_Robot_session_data), sa , msg="数据矛盾")

        '''机器人解决率'''
        text_Rr = driver.find_element_by_xpath(
            '//*[@id="_content"]/div/div/div[1]/div/div[2]/div/div[2]').text
        print(text_Rr)
        text_Robot_resolution = text_Rr.split('：')[0]
        print(text_Robot_resolution)
        self.assertEqual(text_Robot_resolution, '机器人解决率', msg="机器人解决率字段错误")
        text_Robot_resolution_data1 = text_Rr.split('：')[1]
        print(text_Robot_resolution_data1)
        print(type(text_Robot_resolution_data1))
        text_Robot_resolution_data1 = ' '.join(text_Robot_resolution_data1.split())

        text_Robot_resolution_data2 = ('%.2f%%' % (int(text_Robot_solution_data)/int(text_Robot_session_data) * 100))
        print(text_Robot_resolution_data2)
        print(type(text_Robot_resolution_data2))

        self.assertEqual(text_Robot_resolution_data1, text_Robot_resolution_data2, msg="数据矛盾")

        '''机器人转人工率'''
        text_Rtr = driver.find_element_by_xpath(
            '//*[@id="_content"]/div/div/div[1]/div/div[3]/div/div[2]').text
        print(text_Rtr)
        text_Robot_transfer_rate = text_Rtr.split('：')[0]
        print(text_Robot_transfer_rate)
        self.assertEqual(text_Robot_transfer_rate, '机器人转人工率', msg="机器人解决率字段错误")
        text_Robot_transfer_rate_data1 = text_Rtr.split('：')[1]
        print(text_Robot_transfer_rate_data1)
        print(type(text_Robot_transfer_rate_data1))
        text_Robot_transfer_rate_data1 = ' '.join(text_Robot_transfer_rate_data1.split())

        text_Robot_transfer_rate_data2 = ('%.2f%%' % (int(text_Rttac_data) / int(text_Robot_session_data) * 100))
        print(text_Robot_transfer_rate_data2)
        print(type(text_Robot_transfer_rate_data2))

        self.assertEqual(text_Robot_transfer_rate_data1, text_Robot_transfer_rate_data2, msg="数据矛盾")


        float(text_Robot_transfer_rate_data1.strip('%')) + float(text_Robot_transfer_rate_data2.strip('%'))
        self.assertEqual(float(text_Robot_resolution_data1.strip('%'))/100 + float(text_Robot_transfer_rate_data2.strip('%'))/100, 1, msg="数据矛盾")


    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    #unittest.main()

    testunit = unittest.TestSuite()
    testunit.addTest(pandect_page("test_Robot_session"))
    #testunit.addTest(pandect_page("test_Robot_solution"))

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