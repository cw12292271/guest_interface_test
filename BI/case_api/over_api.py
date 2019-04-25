import random
import time
from HTMLTestRunner_PY3 import HTMLTestRunner

import datetime

from decimal import Decimal

import unittest
import requests
import pandas

url = "https://admin.t5.site.webot.ai"
mysql_str = 'mysql+pymysql://root:ZEGAhuDP@webot2dingdang.c1t9kbuexy3c.rds.cn-north-1.amazonaws.com.cn:3306/webot2-t5?charset=utf8mb4'


# ==========定义查询时间=========
def query_time():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    now = datetime.datetime(year=year, month=month, day=day)
    while True:
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        start = now - datetime.timedelta(days=a)
        end = now - datetime.timedelta(days=b)
        if start <= end:
            start1 = start.strftime('%Y-%m-%d %H_%M_%S')
            start1 = start1.split(' ')[0]
            end1 = end.strftime('%Y-%m-%d %H_%M_%S')
            end1 = end1.split(' ')[0]
            print(start1, end1)
            return start, end, start1, end1


class Test_Overview_Page(unittest.TestCase):
    '''总览页面接口测试'''

    def setUp(self):
        login_data = {
            "account": "cw-api",
            "password": "123",
            "code": "nvrW6OD4",
            "t": ""
        }
        headers = None
        r = requests.post(url + '/api/user', headers, login_data)
        r = r.json()
        token = r['data']['token']
        headers = {'Auth': token}
        return headers

    def test_客服会话量_01(self):
        '''客服会话量 '''
        start, end, start1, end1 = query_time()
        headers = self.setUp()
        overview_data = {'cid': '1',
                         'start': start1,
                         'end': end1
                         }
        r = requests.get(url=url + '/api/statistic/overview', headers=headers, params=overview_data)
        result = r.json()
        # print(result)
        result = result['data']['客服服务数据']['客服会话量']
        print('接口' + ':' + str(result))
        print(r.status_code)

        end = end + datetime.timedelta(days=1)
        sql = "select count(*) from chat_session where  created >= '{}' and created <= '{}' and cid = 1 and last_session is null and user_id is not null".format(
            start, end)
        print(sql)
        query_result = pandas.read_sql_query(sql, mysql_str)
        print(query_result)
        json_obj = query_result.to_dict(orient="records")  # 字典格式
        print(json_obj)
        json_obj = json_obj[0]['count(*)']
        print('数据库' + ':' + str(json_obj))

        self.assertEqual(result, json_obj, msg="客服会话量 数据错误")
        self.assertTrue(result >= 0, msg="客服会话量 为负数")
        return result

    def test_客服接待量_02(self):
        '''客服接待量 '''
        start, end, start1, end1 = query_time()
        headers = self.setUp()
        overview_data = {'cid': '1',
                         'start': start1,
                         'end': end1
                         }
        r = requests.get(url=url + '/api/statistic/overview', headers=headers, params=overview_data)
        result = r.json()
        # print(result)
        result = result['data']['客服服务数据']['客服接待量']
        print('接口' + ':' + str(result))
        print(r.status_code)

        end = end + datetime.timedelta(days=1)
        sql = "select count(*) from chat_session where  created >= '{}' and created <= '{}' and cid = 1 and user_id is not null".format(
            start, end)
        print(sql)
        query_result = pandas.read_sql_query(sql, mysql_str)
        print(query_result)
        json_obj = query_result.to_dict(orient="records")  # 字典格式
        print(json_obj)
        json_obj = json_obj[0]['count(*)']
        print('数据库' + ':' + str(json_obj))

        self.assertEqual(result, json_obj, msg="客服接待量 数据错误")
        self.assertTrue(result >= 0, msg="客服接待量 为负数")
        return result

    def test_问题解决效率_03(self):
        '''问题解决效率 '''
        start, end, start1, end1 = query_time()
        headers = self.setUp()
        overview_data = {'cid': '1',
                         'start': start1,
                         'end': end1
                         }
        r = requests.get(url=url + '/api/statistic/overview', headers=headers, params=overview_data)
        result = r.json()
        # print(result)
        result = result['data']['客服服务数据']['问题解决效率']
        print('接口' + ':' + str(result))
        print(r.status_code)

        end = end + datetime.timedelta(days=1)
        sql1 = "select count(*) from chat_session where  created >= '{}' and created <= '{}' and last_session is null and cid = 1 and user_id is not null".format(
            start, end)
        客服会话量 = pandas.read_sql_query(sql1, mysql_str)
        客服会话量 = 客服会话量.to_dict(orient="records")  # 字典格式
        客服会话量 = 客服会话量[0]['count(*)']
        print('客服会话量:', sql1)
        sql2 = "select count(*) from chat_session where  created >= '{}' and created <= '{}' and cid = 1 and user_id is not null".format(
            start, end)
        客服接待量 = pandas.read_sql_query(sql2, mysql_str)
        客服接待量 = 客服接待量.to_dict(orient="records")  # 字典格式
        客服接待量 = 客服接待量[0]['count(*)']
        print('客服接待量:', sql2)
        问题解决效率 = 客服会话量 / 客服接待量
        问题解决效率 = Decimal('{}'.format(问题解决效率)).quantize(Decimal('0.0000'))
        print('数据库' + ':' + str(问题解决效率))
        print(str(问题解决效率) + '=' + str(客服会话量) + '/' + str(客服接待量))
        self.assertEqual(result, float(问题解决效率), msg="问题解决效率 数据错误")
        self.assertTrue(result >= 0, msg="问题解决效率 为负数")
        return result

    def tearDown(self):
        headers = self.setUp()
        r = requests.get(url=url + '/api/user/logout', headers=headers)
        print(r.status_code)


if __name__ == '__main__':
    # unittest.main()
    testunit = unittest.TestSuite()
    testunit.addTest(Test_Overview_Page("test_客服会话量_01"))
    testunit.addTest(Test_Overview_Page("test_客服接待量_02"))
    testunit.addTest(Test_Overview_Page("test_问题解决效率_03"))



    # 按照一定格式获取当地时间
    now_time = time.strftime("%Y-%m-%d %A %H_%M_%S ")
    # 定义报告存放路径
    fp = open('D:\\PycharmProjects\\webot2.0\\BI\\report\\' + now_time + 'overview_page_result.html', 'wb')
    # 定义测试报告
    runner = HTMLTestRunner(stream=fp,
                            title="test_overview_page测试报告",
                            description="用例执行情况：")
    runner.run(testunit)
    fp.close()
