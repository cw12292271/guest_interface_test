from decimal import Decimal
from selenium import webdriver
import unittest
import time
from HTMLTestRunner_PY3 import HTMLTestRunner
from selenium.webdriver.common.keys import Keys

import string

class overview_page(unittest.TestCase):

    '''总览页面测试'''
    def setUp(self):

        profile_ff = "C:\\Users\\Lenovo\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\ppw6wgub.default"
        fp = webdriver.FirefoxProfile(profile_ff)
        self.driver = webdriver.Firefox(fp)

        self.driver.get("https://admin.t5.site.webot.ai")
        time.sleep(5)

        print(self.driver.current_url)
        self.driver.find_element_by_xpath(
            '//*[@id="primaryNav"]/div[2]/div[1]/div/ul/li[2]/div/a/span[2]').click()
        time.sleep(1)
        print(self.driver.current_url)


    def test_Robot_service_data_week(self):

        # '''机器人服务数据  2018年04月25日 - 2018年04月26日'''
        #
        # driver = self.driver
        # driver.find_element_by_xpath('//*[@id="_content"]/div/div/h1[1]/div[2]/input').clear()
        # driver.find_element_by_xpath('//*[@id="_content"]/div/div/h1[1]/div[2]/input').send_keys(
        #     "2018年04月25日 - 2018年04月26日")
        # driver.find_element_by_xpath('//*[@id="_content"]/div/div/h1[1]/div[2]/input').send_keys(Keys.ENTER)
        # time.sleep(1)

        '''机器人服务数据--过去一周的数据'''
        driver = self.driver
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/h1[1]/div[2]/i').click()
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/button[2]').click()
        time.sleep(2)

        '''机器人服务数据-机器人会话量字段校验'''
        text_Robot_session = driver.find_element_by_xpath(
            '//*[@id="_content"]/div/div/div[1]/div/div[1]/div/div/div[2]').text
        print(text_Robot_session)
        self.assertEqual(text_Robot_session,'机器人会话量',msg="机器人会话量字段错误")

        '''机器人服务数据-机器人会话量数据非负校验'''
        text_Robot_session_data = driver.find_element_by_xpath(
            '//*[@id="_content"]/div/div/div[1]/div/div[1]/div/div/div[1]').text
        print(text_Robot_session_data)
        self.assertTrue(int(text_Robot_session_data) >= 0, msg="机器人会话量数据为负数")

        '''机器人服务数据-机器人解决量字段错误校验'''
        text_Robot_solution = driver.find_element_by_xpath(
             '//*[@id="_content"]/div/div/div[1]/div/div[2]/div/div[1]/div[2]').text
        print(text_Robot_solution)
        self.assertEqual(text_Robot_solution, '机器人解决量', msg="机器人解决量字段错误")

        '''机器人服务数据-机器人解决量数据非负校验'''
        text_Robot_solution_data = driver.find_element_by_xpath(
             '//*[@id="_content"]/div/div/div[1]/div/div[2]/div/div[1]/div[1]').text
        print(text_Robot_solution_data)
        self.assertTrue(int(text_Robot_solution_data) >= 0, msg="机器人解决量数据为负数")

        '''机器人服务数据-机器人转人工会话量字段校验'''
        text_Rttac = driver.find_element_by_xpath(
            '//*[@id="_content"]/div/div/div[1]/div/div[3]/div/div[1]/div[2]').text
        print(text_Rttac)
        self.assertEqual(text_Rttac, '机器人转人工会话量', msg="机器人转人工会话量字段错误")

        '''机器人服务数据-机器人转人工会话量数据非负校验'''
        text_Rttac_data = driver.find_element_by_xpath(
            '//*[@id="_content"]/div/div/div[1]/div/div[3]/div/div[1]/div[1]').text
        print(text_Rttac_data)
        self.assertTrue(int(text_Rttac_data) >= 0, msg="机器人转人工会话量数据为负数")

        '''机器人服务数据-数据间校验'''
        sa = int(text_Robot_solution_data) + int(text_Rttac_data)
        print('机器人会话量 = 机器人解决量 + 机器人转人工会话量')
        print(text_Robot_session_data + '=' + text_Robot_solution_data + '+' + text_Rttac_data)
        self.assertEqual(int(text_Robot_session_data), sa , msg="数据矛盾")

        '''机器人解决率'''
        text_Rr = driver.find_element_by_xpath(
            '//*[@id="_content"]/div/div/div[1]/div/div[2]/div/div[2]').text
        print(text_Rr)
        # 机器人解决率 字段
        text_Robot_resolution = text_Rr.split('：')[0]
        print(text_Robot_resolution)
        self.assertEqual(text_Robot_resolution, '机器人解决率', msg="机器人解决率字段错误")
        # 机器人解决率 数值
        text_Robot_resolution_data1 = text_Rr.split('：')[1]
        print(text_Robot_resolution_data1)
        print(type(text_Robot_resolution_data1))
        # 去掉数值前空字符
        text_Robot_resolution_data1 = ' '.join(text_Robot_resolution_data1.split())
        # 机器人解决率=机器人解决量/机器人会话量
        text_Robot_resolution_data2 = ('%.2f%%' % (int(text_Robot_solution_data) / int(text_Robot_session_data) * 100))
        print('机器人解决率=机器人解决量/机器人会话量')
        print(text_Robot_resolution_data2 + '=' + text_Robot_solution_data + '/' + text_Robot_session_data)
        print(type(text_Robot_resolution_data2))
        self.assertEqual(text_Robot_resolution_data1, text_Robot_resolution_data2, msg="数据矛盾")

        '''机器人转人工率'''
        text_Rtr = driver.find_element_by_xpath(
            '//*[@id="_content"]/div/div/div[1]/div/div[3]/div/div[2]').text
        print(text_Rtr)
        # 机器人转人工率 字段
        text_Robot_transfer_rate = text_Rtr.split('：')[0]
        print(text_Robot_transfer_rate)
        self.assertEqual(text_Robot_transfer_rate, '机器人转人工率', msg="机器人转人工率字段错误")
        # 机器人转人工率 数值
        text_Robot_transfer_rate_data1 = text_Rtr.split('：')[1]
        print(text_Robot_transfer_rate_data1)
        print(type(text_Robot_transfer_rate_data1))
        # 去掉数值前空字符
        text_Robot_transfer_rate_data1 = ' '.join(text_Robot_transfer_rate_data1.split())
        # 机器人转人工率=机器人转人工量/机器人会话量
        text_Robot_transfer_rate_data2 = ('%.2f%%' % (int(text_Rttac_data) / int(text_Robot_session_data) * 100))
        print('机器人转人工率=机器人转人工量/机器人会话量')
        print(text_Robot_transfer_rate_data2 + '=' + text_Rttac_data + '/' + text_Robot_session_data)
        print(type(text_Robot_transfer_rate_data2))
        self.assertEqual(text_Robot_transfer_rate_data1, text_Robot_transfer_rate_data2, msg="数据矛盾")

        '''数值归一校验'''
        # 限制小数位数4位
        f1 = float(text_Robot_resolution_data1.strip('%')) / 100 + float(text_Robot_transfer_rate_data2.strip('%')) / 100
        f1 = Decimal('{}'.format(f1)).quantize(Decimal('0.0000'))
        print(f1)
        self.assertEqual(f1, 1, msg="机器人解决率+机器人转人工率 数值不能归一")

    def test_Robot_service_data_yesterday(self):

        # '''机器人服务数据  2018年04月25日 - 2018年04月25日'''
        #
        # driver = self.driver
        # driver.find_element_by_xpath('//*[@id="_content"]/div/div/h1[1]/div[2]/input').clear()
        # driver.find_element_by_xpath('//*[@id="_content"]/div/div/h1[1]/div[2]/input').send_keys(
        #     "2018年04月25日 - 2018年04月25日")
        # driver.find_element_by_xpath('//*[@id="_content"]/div/div/h1[1]/div[2]/input').send_keys(Keys.ENTER)
        # time.sleep(10)

        '''机器人服务数据--昨天的数据'''
        driver = self.driver
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/h1[1]/div[2]/i').click()
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/button[1]').click()
        time.sleep(2)

        '''机器人服务数据-机器人会话量字段校验'''
        text_Robot_session = driver.find_element_by_xpath(
            '//*[@id="_content"]/div/div/div[1]/div/div[1]/div/div/div[2]').text
        print(text_Robot_session)
        self.assertEqual(text_Robot_session,'机器人会话量',msg="机器人会话量字段错误")

        '''机器人服务数据-机器人会话量数据非负校验'''
        text_Robot_session_data = driver.find_element_by_xpath(
            '//*[@id="_content"]/div/div/div[1]/div/div[1]/div/div/div[1]').text
        print(text_Robot_session_data)
        self.assertTrue(int(text_Robot_session_data) >= 0, msg="机器人会话量数据为负数")

        '''机器人服务数据-机器人解决量字段错误校验'''
        text_Robot_solution = driver.find_element_by_xpath(
             '//*[@id="_content"]/div/div/div[1]/div/div[2]/div/div[1]/div[2]').text
        print(text_Robot_solution)
        self.assertEqual(text_Robot_solution, '机器人解决量', msg="机器人解决量字段错误")

        '''机器人服务数据-机器人解决量数据非负校验'''
        text_Robot_solution_data = driver.find_element_by_xpath(
             '//*[@id="_content"]/div/div/div[1]/div/div[2]/div/div[1]/div[1]').text
        print(text_Robot_solution_data)
        self.assertTrue(int(text_Robot_solution_data) >= 0, msg="机器人解决量数据为负数")

        '''机器人服务数据-机器人转人工会话量字段校验'''
        text_Rttac = driver.find_element_by_xpath(
            '//*[@id="_content"]/div/div/div[1]/div/div[3]/div/div[1]/div[2]').text
        print(text_Rttac)
        self.assertEqual(text_Rttac, '机器人转人工会话量', msg="机器人转人工会话量字段错误")

        '''机器人服务数据-机器人转人工会话量数据非负校验'''
        text_Rttac_data = driver.find_element_by_xpath(
            '//*[@id="_content"]/div/div/div[1]/div/div[3]/div/div[1]/div[1]').text
        print(text_Rttac_data)
        self.assertTrue(int(text_Rttac_data) >= 0, msg="机器人转人工会话量数据为负数")

        '''机器人服务数据-数据间校验'''
        sa = int(text_Robot_solution_data) + int(text_Rttac_data)
        print('机器人会话量' '=' '机器人解决量 + 机器人转人工会话量')
        print(text_Robot_session_data + '=' + text_Robot_solution_data + '+' + text_Rttac_data)
        self.assertEqual(int(text_Robot_session_data), sa , msg="数据矛盾")

        '''机器人解决率'''
        text_Rr = driver.find_element_by_xpath(
            '//*[@id="_content"]/div/div/div[1]/div/div[2]/div/div[2]').text
        print(text_Rr)
        # 机器人解决率 字段
        text_Robot_resolution = text_Rr.split('：')[0]
        print(text_Robot_resolution)
        self.assertEqual(text_Robot_resolution, '机器人解决率', msg="机器人解决率字段错误")
        # 机器人解决率 数值
        text_Robot_resolution_data1 = text_Rr.split('：')[1]
        print(text_Robot_resolution_data1)
        print(type(text_Robot_resolution_data1))
        # 去掉数值前空字符
        text_Robot_resolution_data1 = ' '.join(text_Robot_resolution_data1.split())
        # 机器人解决率=机器人解决量/机器人会话量
        text_Robot_resolution_data2 = ('%.2f%%' % (int(text_Robot_solution_data) / int(text_Robot_session_data) * 100))
        print('机器人解决率=机器人解决量/机器人会话量')
        print(text_Robot_resolution_data2 + '=' + text_Robot_solution_data + '/' + text_Robot_session_data)
        print(type(text_Robot_resolution_data2))
        self.assertEqual(text_Robot_resolution_data1, text_Robot_resolution_data2, msg="数据矛盾")

        '''机器人转人工率'''
        text_Rtr = driver.find_element_by_xpath(
            '//*[@id="_content"]/div/div/div[1]/div/div[3]/div/div[2]').text
        print(text_Rtr)
        # 机器人转人工率 字段
        text_Robot_transfer_rate = text_Rtr.split('：')[0]
        print(text_Robot_transfer_rate)
        self.assertEqual(text_Robot_transfer_rate, '机器人转人工率', msg="机器人转人工率字段错误")
        # 机器人转人工率 数值
        text_Robot_transfer_rate_data1 = text_Rtr.split('：')[1]
        print(text_Robot_transfer_rate_data1)
        print(type(text_Robot_transfer_rate_data1))
        # 去掉数值前空字符
        text_Robot_transfer_rate_data1 = ' '.join(text_Robot_transfer_rate_data1.split())
        # 机器人转人工率=机器人转人工量/机器人会话量
        text_Robot_transfer_rate_data2 = ('%.2f%%' % (int(text_Rttac_data) / int(text_Robot_session_data) * 100))
        print('机器人转人工率=机器人转人工量/机器人会话量')
        print(text_Robot_transfer_rate_data2 + '=' + text_Rttac_data + '/' + text_Robot_session_data)
        print(type(text_Robot_transfer_rate_data2))
        self.assertEqual(text_Robot_transfer_rate_data1, text_Robot_transfer_rate_data2, msg="数据矛盾")

        '''数值归一校验'''
        # 限制小数位数4位
        f1 = float(text_Robot_resolution_data1.strip('%')) / 100 + float(
            text_Robot_transfer_rate_data2.strip('%')) / 100
        f1 = Decimal('{}'.format(f1)).quantize(Decimal('0.0000'))
        print(f1)
        self.assertEqual(f1, 1, msg="机器人解决率+机器人转人工率 数值不能归一")

    def test_Customer_service_data_week(self):

        '''客服服务数据--过去一周的数据'''
        driver = self.driver
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/h1[1]/div[2]/i').click()
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/button[2]').click()
        time.sleep(2)

        '''客服服务数据-客服会话量字段校验'''
        客服会话量 = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[4]/div/div[1]/div/div/div[2]').text
        print(客服会话量)
        self.assertEqual(客服会话量,'客服会话量',msg="客服会话量字段错误")

        '''客服服务数据-客服会话量数据非负校验'''
        Customer_session_data = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[4]/div/div[1]/div/div/div[1]').text
        print(Customer_session_data)
        self.assertTrue(int(Customer_session_data) >= 0, msg="客服会话量数据为负数")

        '''客服服务数据-客服接待量字段错误校验'''
        客服接待量 = driver.find_element_by_xpath(
             '/html/body/div[1]/div[2]/div[2]/div/div/div[4]/div/div[2]/div/div/div[2]').text
        print(客服接待量)
        self.assertEqual(客服接待量, '客服接待量', msg="客服接待量字段错误")

        '''客服服务数据-客服接待量数据非负校验'''
        Customer_reception_data = driver.find_element_by_xpath(
             '/html/body/div[1]/div[2]/div[2]/div/div/div[4]/div/div[2]/div/div/div[1]').text
        print(Customer_reception_data)
        self.assertTrue(int(Customer_reception_data) >= 0, msg="客服接待量数据为负数")

        '''问题解决效率 字段校验'''
        问题解决效率 = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[4]/div/div[3]/div/div/div[2]').text
        print(问题解决效率)
        self.assertEqual(问题解决效率, '问题解决效率', msg="问题解决效率字段错误")

        '''问题解决效率 数据校验'''
        Problem_solving_efficiency_data1 = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[4]/div/div[3]/div/div/div[1]').text
        print(Problem_solving_efficiency_data1)
        #Problem_solving_efficiency_data1 = float(Problem_solving_efficiency_data1.strip('%'))/100
        # 问题解决效率=客服会话量/客服接待量
        Problem_solving_efficiency_data2 = ('%.2f%%' % (int(Customer_session_data) / int(Customer_reception_data) * 100))
        print('问题解决效率=客服会话量/客服接待量')
        print(Problem_solving_efficiency_data2 + '=' + Customer_session_data + '/' + Customer_reception_data)
        self.assertEqual(Problem_solving_efficiency_data1, Problem_solving_efficiency_data2, msg="数据矛盾")

    def test_Customer_service_data_yesterday(self):

        '''客服服务数据--昨天的数据'''
        driver = self.driver
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/h1[1]/div[2]/i').click()
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/button[1]').click()
        time.sleep(2)

        '''客服服务数据-客服会话量字段校验'''
        客服会话量 = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[4]/div/div[1]/div/div/div[2]').text
        print(客服会话量)
        self.assertEqual(客服会话量,'客服会话量',msg="客服会话量字段错误")

        '''客服服务数据-客服会话量数据非负校验'''
        Customer_session_data = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[4]/div/div[1]/div/div/div[1]').text
        print(Customer_session_data)
        self.assertTrue(int(Customer_session_data) >= 0, msg="客服会话量数据为负数")

        '''客服服务数据-客服接待量字段错误校验'''
        客服接待量 = driver.find_element_by_xpath(
             '/html/body/div[1]/div[2]/div[2]/div/div/div[4]/div/div[2]/div/div/div[2]').text
        print(客服接待量)
        self.assertEqual(客服接待量, '客服接待量', msg="客服接待量字段错误")

        '''客服服务数据-客服接待量数据非负校验'''
        Customer_reception_data = driver.find_element_by_xpath(
             '/html/body/div[1]/div[2]/div[2]/div/div/div[4]/div/div[2]/div/div/div[1]').text
        print(Customer_reception_data)
        self.assertTrue(int(Customer_reception_data) >= 0, msg="客服接待量数据为负数")

        '''问题解决效率 字段校验'''
        问题解决效率 = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[4]/div/div[3]/div/div/div[2]').text
        print(问题解决效率)
        self.assertEqual(问题解决效率, '问题解决效率', msg="问题解决效率字段错误")

        '''问题解决效率 数据校验'''
        Problem_solving_efficiency_data1 = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[4]/div/div[3]/div/div/div[1]').text
        print(Problem_solving_efficiency_data1)
        #Problem_solving_efficiency_data1 = float(Problem_solving_efficiency_data1.strip('%'))/100
        # 问题解决效率=客服会话量/客服接待量
        Problem_solving_efficiency_data2 = ('%.2f%%' % (int(Customer_session_data) / int(Customer_reception_data) * 100))
        print('问题解决效率=客服会话量/客服接待量')
        print(Problem_solving_efficiency_data2 + '=' + Customer_session_data + '/' + Customer_reception_data)
        self.assertEqual(Problem_solving_efficiency_data1, Problem_solving_efficiency_data2, msg="数据矛盾")

    def test_Customer_advices_data_week(self):

        '''客服服务消息量--过去一周的数据'''
        driver = self.driver
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/h1[1]/div[2]/i').click()
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/button[2]').click()
        time.sleep(2)

        '''客服服务消息量-总消息量字段校验'''
        总消息量 = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[7]/div/div[1]/div/div/div[2]').text
        print(总消息量)
        self.assertEqual(总消息量,'总消息量',msg="总消息量字段错误")

        '''客服服务消息量-总消息量数据非负校验'''
        Total_advices_data = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[7]/div/div[1]/div/div/div[1]').text
        print(Total_advices_data)
        self.assertTrue(int(Total_advices_data) >= 0, msg="总消息量数据为负数")

        '''客服服务消息量-客服消息量字段错误校验'''
        客服消息量 = driver.find_element_by_xpath(
             '/html/body/div[1]/div[2]/div[2]/div/div/div[7]/div/div[2]/div/div/div[2]').text
        print(客服消息量)
        self.assertEqual(客服消息量, '客服消息量', msg="客服消息量字段错误")

        '''客服服务消息量-客服消息量数据非负校验'''
        Customer_advices_data = driver.find_element_by_xpath(
             '/html/body/div[1]/div[2]/div[2]/div/div/div[7]/div/div[2]/div/div/div[1]').text
        print(Customer_advices_data)
        self.assertTrue(int(Customer_advices_data) >= 0, msg="客服消息量数据为负数")

        '''客服服务消息量-访客消息量字段错误校验'''
        访客消息量 = driver.find_element_by_xpath(
             '/html/body/div[1]/div[2]/div[2]/div/div/div[7]/div/div[3]/div/div/div[2]').text
        print(访客消息量)
        self.assertEqual(访客消息量, '访客消息量', msg="访客消息量字段错误")

        '''客服服务消息量-访客消息量数据非负校验'''
        Client_advices_data = driver.find_element_by_xpath(
             '/html/body/div[1]/div[2]/div[2]/div/div/div[7]/div/div[3]/div/div/div[1]').text
        print(Client_advices_data)
        self.assertTrue(int(Client_advices_data) >= 0, msg="访客消息量数据为负数")

        '''答问比 字段校验'''
        答问比 = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[7]/div/div[4]/div/div/div[2]').text
        print(答问比)
        self.assertEqual(答问比, '答问比', msg="答问比字段错误")

        '''答问比 数据校验'''
        Answered_questions_than_data1 = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[7]/div/div[4]/div/div/div[1]').text
        print(Answered_questions_than_data1)
        #Answered_questions_than_data1 = float(Answered_questions_than_data1.strip('%'))/100
        # 答问比=客服消息量/访客消息量
        Answered_questions_than_data2 = ('%.2f%%' % (int(Customer_advices_data) / int(Client_advices_data) * 100))
        print('答问比=客服消息量/访客消息量')
        print(Answered_questions_than_data2 + '=' + Customer_advices_data + '/' + Client_advices_data)
        self.assertEqual(Answered_questions_than_data1, Answered_questions_than_data2, msg="数据矛盾")

    def test_Customer_advices_data_yesterday(self):

        '''客服服务消息量--昨天的数据'''
        driver = self.driver
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/h1[1]/div[2]/i').click()
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/button[1]').click()
        time.sleep(2)

        '''客服服务消息量-总消息量字段校验'''
        总消息量 = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[7]/div/div[1]/div/div/div[2]').text
        print(总消息量)
        self.assertEqual(总消息量,'总消息量',msg="总消息量字段错误")

        '''客服服务消息量-总消息量数据非负校验'''
        Total_advices_data = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[7]/div/div[1]/div/div/div[1]').text
        print(Total_advices_data)
        self.assertTrue(int(Total_advices_data) >= 0, msg="总消息量数据为负数")

        '''客服服务消息量-客服消息量字段错误校验'''
        客服消息量 = driver.find_element_by_xpath(
             '/html/body/div[1]/div[2]/div[2]/div/div/div[7]/div/div[2]/div/div/div[2]').text
        print(客服消息量)
        self.assertEqual(客服消息量, '客服消息量', msg="客服消息量字段错误")

        '''客服服务消息量-客服消息量数据非负校验'''
        Customer_advices_data = driver.find_element_by_xpath(
             '/html/body/div[1]/div[2]/div[2]/div/div/div[7]/div/div[2]/div/div/div[1]').text
        print(Customer_advices_data)
        self.assertTrue(int(Customer_advices_data) >= 0, msg="客服消息量数据为负数")

        '''客服服务消息量-访客消息量字段错误校验'''
        访客消息量 = driver.find_element_by_xpath(
             '/html/body/div[1]/div[2]/div[2]/div/div/div[7]/div/div[3]/div/div/div[2]').text
        print(访客消息量)
        self.assertEqual(访客消息量, '访客消息量', msg="访客消息量字段错误")

        '''客服服务消息量-访客消息量数据非负校验'''
        Client_advices_data = driver.find_element_by_xpath(
             '/html/body/div[1]/div[2]/div[2]/div/div/div[7]/div/div[3]/div/div/div[1]').text
        print(Client_advices_data)
        self.assertTrue(int(Client_advices_data) >= 0, msg="访客消息量数据为负数")

        '''答问比 字段校验'''
        答问比 = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[7]/div/div[4]/div/div/div[2]').text
        print(答问比)
        self.assertEqual(答问比, '答问比', msg="答问比字段错误")

        '''答问比 数据校验'''
        Answered_questions_than_data1 = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[7]/div/div[4]/div/div/div[1]').text
        print(Answered_questions_than_data1)
        #Answered_questions_than_data1 = float(Answered_questions_than_data1.strip('%'))/100
        # 答问比=客服消息量/访客消息量
        Answered_questions_than_data2 = ('%.2f%%' % (int(Customer_advices_data) / int(Client_advices_data) * 100))
        print('答问比=客服消息量/访客消息量')
        print(Answered_questions_than_data2 + '=' + Customer_advices_data + '/' + Client_advices_data)
        self.assertEqual(Answered_questions_than_data1, Answered_questions_than_data2, msg="数据矛盾")

    def test_Visitor_status_week(self):

        '''访客来访情况--过去一周的数据'''
        driver = self.driver
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/h1[1]/div[2]/i').click()
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/button[2]').click()
        time.sleep(2)

        '''访客来访情况-历史访客 字段校验'''
        历史访客 = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[13]/div[1]/div[1]/div/div/div[2]').text
        print(历史访客)
        self.assertEqual(历史访客,'历史访客',msg="历史访客 字段错误")

        '''访客来访情况-历史访客 非负校验'''
        Total_visitors_data = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[13]/div[1]/div[1]/div/div/div[1]').text
        print(Total_visitors_data)
        self.assertTrue(int(Total_visitors_data) >= 0, msg="历史访客 数据为负数")

        '''访客来访情况-新访客 字段错误校验'''
        新访客 = driver.find_element_by_xpath(
             '/html/body/div[1]/div[2]/div[2]/div/div/div[13]/div[1]/div[2]/div/div[1]/div[2]').text
        print(新访客)
        self.assertEqual(新访客, '新访客', msg="新访客 字段错误")

        '''访客来访情况-新访客 数据非负校验'''
        New_visitors_data = driver.find_element_by_xpath(
             '/html/body/div[1]/div[2]/div[2]/div/div/div[13]/div[1]/div[2]/div/div[1]/div[1]').text
        print(New_visitors_data)
        self.assertTrue(int(New_visitors_data) >= 0, msg="新访客 数据为负数")

        '''访客来访情况-老访客 字段校验'''
        老访客 = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[13]/div[1]/div[3]/div/div[1]/div[2]').text
        print(老访客)
        self.assertEqual(老访客, '老访客', msg="老访客 字段错误")

        '''访客来访情况-老访客 数据非负校验'''
        Old_visitors_data = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[13]/div[1]/div[3]/div/div[1]/div[1]').text
        print(Old_visitors_data)
        self.assertTrue(int(Old_visitors_data) >= 0, msg="老访客 数据为负数")

        '''访客来访情况-数据间校验'''
        sa = int(New_visitors_data) + int(Old_visitors_data)
        print('历史访客 = 新访客 + 老访客')
        print(Total_visitors_data + '=' + New_visitors_data + '+' + Old_visitors_data)
        self.assertEqual(int(Total_visitors_data), sa , msg="历史访客 = 新访客 + 老访客 数据矛盾")

        '''访客来访情况-新访客占比'''
        新访客占比字段 = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[13]/div[1]/div[2]/div/div[2]').text
        print(新访客占比字段)
        # 新访客占比 字段
        新访客占比 = 新访客占比字段.split('：')[0]
        print(新访客占比)
        self.assertEqual(新访客占比, '新访客占比', msg="新访客占比 错误")
        # 新访客占比 数值
        Proportion_of_new_visitors_data1 = 新访客占比字段.split('：')[1]
        print(Proportion_of_new_visitors_data1)
        # 去掉数值前空字符
        Proportion_of_new_visitors_data1 = ' '.join(Proportion_of_new_visitors_data1.split())
        # 新访客占比=新访客/历史访客
        Proportion_of_new_visitors_data2 = ('%.2f%%' % (int(New_visitors_data) / int(Total_visitors_data) * 100))
        print('新访客占比=新访客/历史访客')
        print(Proportion_of_new_visitors_data2 + '=' + New_visitors_data + '/' + Total_visitors_data)
        self.assertEqual(Proportion_of_new_visitors_data1, Proportion_of_new_visitors_data2, msg="新访客占比=新访客/历史访客 数据矛盾")

        '''访客来访情况-老访客占比'''
        老访客占比字段 = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[13]/div[1]/div[3]/div/div[2]').text
        print(老访客占比字段)
        # 老访客占比 字段
        老访客占比 = 老访客占比字段.split('：')[0]
        print(新访客占比)
        self.assertEqual(老访客占比, '老访客占比', msg="老访客占比 错误")
        # 老访客占比 数值
        Proportion_of_old_visitors_data1 = 老访客占比字段.split('：')[1]
        print(Proportion_of_old_visitors_data1)
        # 去掉数值前空字符
        Proportion_of_old_visitors_data1 = ' '.join(Proportion_of_old_visitors_data1.split())
        # 老访客占比=老访客/历史访客
        Proportion_of_old_visitors_data2 = ('%.2f%%' % (int(Old_visitors_data) / int(Total_visitors_data) * 100))
        print('老访客占比=老访客/历史访客')
        print(Proportion_of_old_visitors_data2 + '=' + Old_visitors_data + '/' + Total_visitors_data)
        self.assertEqual(Proportion_of_old_visitors_data1, Proportion_of_old_visitors_data2, msg="老访客占比=老访客/历史访客 数据矛盾")

        '''数值归一校验'''
        # 限制小数位数4位
        f1 = float(Proportion_of_new_visitors_data1.strip('%')) / 100 + float(Proportion_of_old_visitors_data1.strip('%')) / 100
        f1 = Decimal('{}'.format(f1)).quantize(Decimal('0.0000'))
        print(f1)
        self.assertEqual(f1, 1, msg="新访客占比+老访客占比 数值不能归一")

    def test_Visitor_status_yesterday(self):

        '''访客来访情况--昨天的数据'''
        driver = self.driver
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/h1[1]/div[2]/i').click()
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/button[1]').click()
        time.sleep(2)

        '''访客来访情况-历史访客 字段校验'''
        历史访客 = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[13]/div[1]/div[1]/div/div/div[2]').text
        print(历史访客)
        self.assertEqual(历史访客,'历史访客',msg="历史访客 字段错误")

        '''访客来访情况-历史访客 非负校验'''
        Total_visitors_data = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[13]/div[1]/div[1]/div/div/div[1]').text
        print(Total_visitors_data)
        self.assertTrue(int(Total_visitors_data) >= 0, msg="历史访客 数据为负数")

        '''访客来访情况-新访客 字段错误校验'''
        新访客 = driver.find_element_by_xpath(
             '/html/body/div[1]/div[2]/div[2]/div/div/div[13]/div[1]/div[2]/div/div[1]/div[2]').text
        print(新访客)
        self.assertEqual(新访客, '新访客', msg="新访客 字段错误")

        '''访客来访情况-新访客 数据非负校验'''
        New_visitors_data = driver.find_element_by_xpath(
             '/html/body/div[1]/div[2]/div[2]/div/div/div[13]/div[1]/div[2]/div/div[1]/div[1]').text
        print(New_visitors_data)
        self.assertTrue(int(New_visitors_data) >= 0, msg="新访客 数据为负数")

        '''访客来访情况-老访客 字段校验'''
        老访客 = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[13]/div[1]/div[3]/div/div[1]/div[2]').text
        print(老访客)
        self.assertEqual(老访客, '老访客', msg="老访客 字段错误")

        '''访客来访情况-老访客 数据非负校验'''
        Old_visitors_data = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[13]/div[1]/div[3]/div/div[1]/div[1]').text
        print(Old_visitors_data)
        self.assertTrue(int(Old_visitors_data) >= 0, msg="老访客 数据为负数")

        '''访客来访情况-数据间校验'''
        sa = int(New_visitors_data) + int(Old_visitors_data)
        print('历史访客 = 新访客 + 老访客')
        print(Total_visitors_data + '=' + New_visitors_data + '+' + Old_visitors_data)
        self.assertEqual(int(Total_visitors_data), sa , msg="历史访客 = 新访客 + 老访客 数据矛盾")

        '''访客来访情况-新访客占比'''
        新访客占比字段 = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[13]/div[1]/div[2]/div/div[2]').text
        print(新访客占比字段)
        # 新访客占比 字段
        新访客占比 = 新访客占比字段.split('：')[0]
        print(新访客占比)
        self.assertEqual(新访客占比, '新访客占比', msg="新访客占比 错误")
        # 新访客占比 数值
        Proportion_of_new_visitors_data1 = 新访客占比字段.split('：')[1]
        print(Proportion_of_new_visitors_data1)
        # 去掉数值前空字符
        Proportion_of_new_visitors_data1 = ' '.join(Proportion_of_new_visitors_data1.split())
        # 新访客占比=新访客/历史访客
        Proportion_of_new_visitors_data2 = ('%.2f%%' % (int(New_visitors_data) / int(Total_visitors_data) * 100))
        print('新访客占比=新访客/历史访客')
        print(Proportion_of_new_visitors_data2 + '=' + New_visitors_data + '/' + Total_visitors_data)
        self.assertEqual(Proportion_of_new_visitors_data1, Proportion_of_new_visitors_data2, msg="新访客占比=新访客/历史访客 数据矛盾")

        '''访客来访情况-老访客占比'''
        老访客占比字段 = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div/div[13]/div[1]/div[3]/div/div[2]').text
        print(老访客占比字段)
        # 老访客占比 字段
        老访客占比 = 老访客占比字段.split('：')[0]
        print(新访客占比)
        self.assertEqual(老访客占比, '老访客占比', msg="老访客占比 错误")
        # 老访客占比 数值
        Proportion_of_old_visitors_data1 = 老访客占比字段.split('：')[1]
        print(Proportion_of_old_visitors_data1)
        # 去掉数值前空字符
        Proportion_of_old_visitors_data1 = ' '.join(Proportion_of_old_visitors_data1.split())
        # 老访客占比=老访客/历史访客
        Proportion_of_old_visitors_data2 = ('%.2f%%' % (int(Old_visitors_data) / int(Total_visitors_data) * 100))
        print('老访客占比=老访客/历史访客')
        print(Proportion_of_old_visitors_data2 + '=' + Old_visitors_data + '/' + Total_visitors_data)
        self.assertEqual(Proportion_of_old_visitors_data1, Proportion_of_old_visitors_data2, msg="老访客占比=老访客/历史访客 数据矛盾")

        '''数值归一校验'''
        # 限制小数位数4位
        f1 = float(Proportion_of_new_visitors_data1.strip('%')) / 100 + float(Proportion_of_old_visitors_data1.strip('%')) / 100
        f1 = Decimal('{}'.format(f1)).quantize(Decimal('0.0000'))
        print(f1)
        self.assertEqual(f1, 1, msg="新访客占比+老访客占比 数值不能归一")


    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    #unittest.main()

    testunit = unittest.TestSuite()

    testunit.addTest(overview_page("test_Robot_service_data_week"))
    testunit.addTest(overview_page("test_Robot_service_data_yesterday"))
    testunit.addTest(overview_page("test_Customer_service_data_week"))
    testunit.addTest(overview_page("test_Customer_service_data_yesterday"))
    testunit.addTest(overview_page("test_Customer_advices_data_week"))
    testunit.addTest(overview_page("test_Customer_advices_data_yesterday"))
    testunit.addTest(overview_page("test_Visitor_status_week"))
    testunit.addTest(overview_page("test_Visitor_status_yesterday"))

    # 按照一定格式获取当地时间
    now_time = time.strftime("%Y-%m-%d %A %H_%M_%S ")

    # 定义报告存放路径
    fp = open('D:\\PycharmProjects\\webot2.0\\BI\\report\\' + now_time + 'overview_page_result.html', 'wb')
    # 定义测试报告
    runner = HTMLTestRunner(stream=fp,
                            title="test_project测试报告",
                            description="用例执行情况：")
    runner.run(testunit)
    fp.close()