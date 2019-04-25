import random
import time
from HTMLTestRunner_PY3 import HTMLTestRunner
import datetime
from decimal import Decimal
import unittest
import requests
import pandas

url = "https://admin.pre.site.webot.ai"
cid = 1
mysql_str = (
    "mysql+pymysql://root:ZEGAhuDP@webot2dingdang.c1t9kbuexy3c.rds.cn-north-1.amazonaws.com.cn:3306/webot2-t5?charset=utf8mb4"
)

for i in range(1, 9):
    # ==========定义查询时间=========
    def query_time():
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day
        now = datetime.datetime(year=year, month=month, day=day)
        while True:
            a = random.randint(1, 7)
            b = random.randint(1, 7)
            start = now - datetime.timedelta(days=i)
            end = now - datetime.timedelta(days=i)
            if start <= end:
                start1 = start.strftime("%Y-%m-%d %H_%M_%S")
                start1 = start1.split(" ")[0]
                end1 = end.strftime("%Y-%m-%d %H_%M_%S")
                end1 = end1.split(" ")[0]
                print(start1, end1)
                return start, end, start1, end1

    class Test_Overview_Page(unittest.TestCase):
        """总览页面接口测试"""

        def setUp(self):
            login_data = {
                "account": "cw-api",
                "password": "123456",
                "code": "nvrW6OD4",
                "force_login": True,
                "t": "",
            }
            headers = None
            r = requests.post(url + "/api/user", headers, login_data)
            print("登录账号", r.status_code)
            r = r.json()
            print(r)
            token = r["data"]["token"]
            headers = {"Auth": token}
            return headers

        def test_01_客服服务数据(self):
            """客服服务数据 """
            start, end, start1, end1 = query_time()
            headers = self.setUp()
            overview_data = {"cid": "1", "start": start1, "end": end1}
            r = requests.get(
                url=url + "/api/statistic/overview",
                headers=headers,
                params=overview_data,
            )
            result = r.json()
            print(result)
            self.assertEqual(r.status_code, 200, msg="接口返回码 错误")
            print(result["data"]["客服服务数据"])
            end = end + datetime.timedelta(days=1)  # sql数据跨0点
            # ==========客服会话量===========
            客服会话量 = result["data"]["客服服务数据"]["客服会话量"]
            sql1 = "select count(*) from chat_session where cid = '{}' and created >= '{}' and created < '{}' and last_session is null and user_id is not null".format(
                cid, start, end
            )
            print("客服会话量:", sql1)
            query_result1 = pandas.read_sql_query(sql1, mysql_str)
            # print(query_result1)
            query_result1 = query_result1.to_dict(orient="records")  # 字典格式
            # print(query_result1)
            query_result1 = query_result1[0]["count(*)"]
            print("数据库-客服会话量" + ":" + str(query_result1))
            print("接口-客服会话量" + ":" + str(客服会话量))

            # ==========客服接待量===========
            客服接待量 = result["data"]["客服服务数据"]["客服接待量"]
            sql2 = "select count(*) from chat_session where cid = '{}' and created >= '{}' and created < '{}' and user_id is not null".format(
                cid, start, end
            )
            print("客服接待量:", sql2)
            query_result2 = pandas.read_sql_query(sql2, mysql_str)
            # print(query_result2)
            query_result2 = query_result2.to_dict(orient="records")  # 字典格式
            # print(query_result2)
            query_result2 = query_result2[0]["count(*)"]
            print("数据库-客服接待量" + ":" + str(query_result2))
            print("接口-客服接待量" + ":" + str(客服接待量))

            # ==========问题解决效率===========
            问题解决效率 = result["data"]["客服服务数据"]["问题解决效率"]
            print(r.status_code)
            if query_result2 == 0:
                query_result3 = 0
            else:
                query_result3 = query_result1 / query_result2
            query_result3 = Decimal("{}".format(query_result3)).quantize(
                Decimal("0.0000")
            )
            print(
                str(query_result3) + "=" + str(query_result1) + "/" + str(query_result2)
            )
            print("数据库-问题解决效率" + ":" + str(query_result3))
            print("接口-问题解决效率" + ":" + str(问题解决效率))

            self.assertEqual(客服会话量, query_result1, msg="客服会话量 数据错误")
            self.assertTrue(客服会话量 >= 0, msg="客服会话量 为负数")
            self.assertEqual(客服接待量, query_result2, msg="客服接待量 数据错误")
            self.assertTrue(客服接待量 >= 0, msg="客服接待量 为负数")
            self.assertEqual(问题解决效率, float(query_result3), msg="问题解决效率 数据错误")
            self.assertTrue(问题解决效率 >= 0, msg="问题解决效率 为负数")

        def test_02_机器人服务数据(self):
            """机器人服务数据 """
            start, end, start1, end1 = query_time()
            headers = self.setUp()
            overview_data = {"cid": "1", "start": start1, "end": end1}
            r = requests.get(
                url=url + "/api/statistic/overview",
                headers=headers,
                params=overview_data,
            )
            result = r.json()
            print(result)
            self.assertEqual(r.status_code, 200, msg="接口返回码 错误")
            print(result["data"]["机器人服务数据"])
            end = end + datetime.timedelta(days=1)  # sql数据跨0点

            # ==========机器人会话量===========
            机器人会话量 = result["data"]["机器人服务数据"]["机器人会话量"]
            sql1 = "select count(*) from chat_session where cid = '{}' and created >= '{}' and created < '{}' and last_session is null and user_id is null".format(
                cid, start, end
            )
            print("机器人会话量:", sql1)
            query_result1 = pandas.read_sql_query(sql1, mysql_str)
            # print(query_result1)
            query_result1 = query_result1.to_dict(orient="records")  # 字典格式
            # print(query_result1)
            query_result1 = query_result1[0]["count(*)"]
            print("数据库-机器人会话量" + ":" + str(query_result1))
            print("接口-机器人会话量" + ":" + str(机器人会话量))

            # ==========机器人解决量===========
            机器人解决量 = result["data"]["机器人服务数据"]["机器人解决量"]
            sql2 = "select count(*) from chat_session where cid = '{}' and created >= '{}' and created < '{}' and user_id is null and status = 2 and robot_question_status = 1".format(
                cid, start, end
            )
            print("机器人解决量:", sql2)
            query_result2 = pandas.read_sql_query(sql2, mysql_str)
            # print(query_result2)
            query_result2 = query_result2.to_dict(orient="records")  # 字典格式
            # print(query_result2)
            query_result2 = query_result2[0]["count(*)"]
            print("数据库-机器人解决量" + ":" + str(query_result2))
            print("接口-机器人解决量" + ":" + str(机器人解决量))

            # ==========机器人解决率===========
            机器人解决率 = result["data"]["机器人服务数据"]["机器人解决率"]
            if query_result1 == 0:
                query_result3 = 0
            else:
                query_result3 = query_result2 / query_result1
            query_result3 = Decimal("{}".format(query_result3)).quantize(
                Decimal("0.0000")
            )
            print(
                str(query_result3) + "=" + str(query_result1) + "/" + str(query_result2)
            )
            print("数据库-机器人解决率" + ":" + str(query_result3))
            print("接口-机器人解决率" + ":" + str(机器人解决率))

            # ==========机器人转人工会话量===========
            机器人转人工会话量 = result["data"]["机器人服务数据"]["机器人转人工会话量"]
            sql3 = "select count(*) from chat_session where cid = '{}' and created >= '{}' and created < '{}'and creator = 1".format(
                cid, start, end
            )  # creator ： 0: 机器人创建，1: 客户转人工, 2: 客服激活，3.客服工单发起, 4.客服转交客服， 5.客服转交客服组
            print("机器人转人工会话量:", sql3)
            query_result4 = pandas.read_sql_query(sql3, mysql_str)
            # print(query_result4)
            query_result4 = query_result4.to_dict(orient="records")  # 字典格式
            # print(query_result4)
            query_result4 = query_result4[0]["count(*)"]
            print("数据库-机器人转人工会话量" + ":" + str(query_result4))
            print("接口-机器人转人工会话量" + ":" + str(机器人转人工会话量))

            # ==========机器人转人工率===========
            机器人转人工率 = result["data"]["机器人服务数据"]["机器人转人工率"]
            if query_result1 == 0:
                query_result5 = 0
            else:
                query_result5 = query_result4 / query_result1
            query_result5 = Decimal("{}".format(query_result5)).quantize(
                Decimal("0.0000")
            )
            print(
                str(query_result5) + "=" + str(query_result4) + "/" + str(query_result1)
            )
            print("数据库-机器人转人工率" + ":" + str(query_result5))
            print("接口-机器人转人工率" + ":" + str(机器人转人工率))

            self.assertEqual(机器人会话量, query_result1, msg="机器人会话量 数据错误")
            self.assertTrue(机器人会话量 >= 0, msg="机器人会话量 为负数")
            self.assertEqual(机器人解决量, query_result2, msg="机器人解决量 数据错误")
            self.assertTrue(机器人解决量 >= 0, msg="机器人解决量 为负数")
            self.assertEqual(机器人解决率, float(query_result3), msg="机器人解决率 数据错误")
            self.assertTrue(机器人解决率 >= 0, msg="机器人解决率 为负数")
            self.assertEqual(机器人转人工会话量, query_result4, msg="机器人转人工会话量 数据错误")
            self.assertTrue(机器人转人工会话量 >= 0, msg="机器人转人工会话量 为负数")
            self.assertEqual(机器人转人工率, float(query_result5), msg="机器人转人工率 数据错误")
            self.assertTrue(机器人转人工率 >= 0, msg="机器人转人工率 为负数")
            self.assertEqual(
                机器人会话量, 机器人转人工会话量 + 机器人解决量, msg="机器人会话量≠机器人解决量+机器人转人工会话量 数据错误"
            )

        def test_03_客服服务消息量(self):
            """客服服务消息量"""
            start, end, start1, end1 = query_time()
            headers = self.setUp()
            overview_data = {"cid": "1", "start": start1, "end": end1}
            r = requests.get(
                url=url + "/api/statistic/overview",
                headers=headers,
                params=overview_data,
            )
            result = r.json()
            print(result)
            self.assertEqual(r.status_code, 200, msg="接口返回码 错误")
            print(result["data"]["客服服务消息量"])
            end = end + datetime.timedelta(days=1)  # sql数据跨0点

            # ==========总消息量===========
            总消息量 = result["data"]["客服服务消息量"]["总消息量"]
            sql1 = (
                """select count(*) from chat_log """
                """where source = "9" and (`raw` LIKE '%%"msg\_type": "text"%%') """
                """and (`raw` not LIKE '%%"is\_sys\_send": 1%%' or `raw` not LIKE '%%"is\_sys\_send": "1"%%')"""
                """and cid = '{}' and created >= '{}' and created < '{}' """.format(
                    cid, start, end
                )
            )
            print("总消息量:", sql1)
            query_result1 = pandas.read_sql_query(sql1, mysql_str)
            # print(query_result1)
            query_result1 = query_result1.to_dict(orient="records")  # 字典格式
            # print(query_result1)
            query_result1 = query_result1[0]["count(*)"]
            print("数据库-总消息量" + ":" + str(query_result1))
            print("接口-总消息量" + ":" + str(总消息量))

            # ==========客服消息量===========
            客服消息量 = result["data"]["客服服务消息量"]["客服消息量"]
            sql2 = (
                """select count(*) from chat_log """
                """where source = "9" and `raw` LIKE '%%"from": "kf"%%' and (`raw` LIKE '%%"msg\_type": "text"%%') """
                """and (`raw` not LIKE '%%"is\_sys\_send": 1%%' or `raw` not LIKE '%%"is\_sys\_send": "1"%%') """
                """and cid = '{}' and created >= '{}' and created < '{}' """.format(
                    cid, start, end
                )
            )
            print("客服消息量:", sql2)
            query_result2 = pandas.read_sql_query(sql2, mysql_str)
            # print(query_result2)
            query_result2 = query_result2.to_dict(orient="records")  # 字典格式
            # print(query_result2)
            query_result2 = query_result2[0]["count(*)"]
            print("数据库-客服消息量" + ":" + str(query_result2))
            print("接口-客服消息量" + ":" + str(客服消息量))

            # ==========访客消息量===========
            访客消息量 = result["data"]["客服服务消息量"]["访客消息量"]
            sql3 = (
                """select count(*) from chat_log """
                """where source = "9" and `raw` LIKE '%%"from": "user"%%' and (`raw` LIKE '%%"msg\_type": "text"%%') """
                """and (`raw` not LIKE '%%"is\_sys\_send": 1%%' or `raw` not LIKE '%%"is\_sys\_send": "1"%%')"""
                """and cid = '{}' and created >= '{}' and created < '{}' """.format(
                    cid, start, end
                )
            )
            print("访客消息量:", sql3)
            query_result3 = pandas.read_sql_query(sql3, mysql_str)
            # print(query_result3)
            query_result3 = query_result3.to_dict(orient="records")  # 字典格式
            # print(query_result3)
            query_result3 = query_result3[0]["count(*)"]
            print("数据库-访客消息量" + ":" + str(query_result3))
            print("接口-访客消息量" + ":" + str(访客消息量))

            # ==========答问比===========
            答问比 = result["data"]["客服服务消息量"]["答问比"]
            if query_result3 == 0:
                query_result4 = 0
            else:
                query_result4 = query_result2 / query_result3
            query_result4 = Decimal("{}".format(query_result4)).quantize(
                Decimal("0.0000")
            )
            print(
                str(query_result4) + "=" + str(query_result2) + "/" + str(query_result3)
            )
            print("数据库-答问比" + ":" + str(query_result4))
            print("接口-答问比" + ":" + str(答问比))

            self.assertEqual(总消息量, query_result1, msg="总消息量 数据错误")
            self.assertTrue(总消息量 >= 0, msg="总消息量 为负数")
            self.assertEqual(客服消息量, query_result2, msg="客服消息量 数据错误")
            self.assertTrue(客服消息量 >= 0, msg="客服消息量 为负数")
            self.assertEqual(访客消息量, query_result3, msg="访客消息量 数据错误")
            self.assertTrue(访客消息量 >= 0, msg="访客消息量 为负数")
            self.assertEqual(总消息量, 客服消息量 + 访客消息量, msg="总消息量=客服消息量+访客消息量 数据错误")
            self.assertEqual(答问比, float(query_result4), msg="答问比 数据错误")
            self.assertTrue(答问比 >= 0, msg="答问比 为负数")

        def tearDown(self):
            headers = self.setUp()
            r = requests.get(url=url + "/api/user/logout", headers=headers)
            print("退出登录", r.status_code)

    if __name__ == '__main__':
        #unittest.main()
        testunit = unittest.TestSuite()
        testunit.addTest(Test_Overview_Page("test_01_客服服务数据"))
        testunit.addTest(Test_Overview_Page("test_02_机器人服务数据"))
        testunit.addTest(Test_Overview_Page("test_03_客服服务消息量"))
        # 按照一定格式获取当地时间
        now_time = time.strftime("%Y-%m-%d %A %H_%M_%S ")
        start = query_time()
        start = start[3]
        start = '(' + start + ')'
        # start = start.strftime("%Y-%m-%d %A %H_%M_%S ")
        # start = start.split(' ')[0]
        # 定义报告存放路径
        fp = open('D:\\PycharmProjects\\webot2.0\\BI\\report\\zonglan\\' + now_time + start + 'overview_page_api_result.html', 'wb')
        # 定义测试报告
        runner = HTMLTestRunner(stream=fp,
                                title="test_overview_page_api_接口测试报告",
                                description="用例执行情况：")
        runner.run(testunit)
        fp.close()
