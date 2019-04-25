import random
import time
from HTMLTestRunner_PY3 import HTMLTestRunner

import datetime

from decimal import Decimal

import unittest
import requests
import pandas

url = "https://admin.t5.site.webot.ai"
cid = 1
mysql_str = (
    "mysql+pymysql://root:ZEGAhuDP@webot2dingdang.c1t9kbuexy3c.rds.cn-north-1.amazonaws.com.cn:3306/webot2-t5?charset=utf8mb4"
)


login_data = {
    "account": "cw-api",
    "password": "123",
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

# ==========定义查询时间=========
def query_time():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    start = datetime.datetime(year=year, month=month, day=day)
    end = datetime.datetime(year=year, month=month, day=day,hour=hour)
    print(start,end)
    return start,end


class Test_immediate_api(unittest.TestCase):
    """首页数据immediate接口测试"""
    def setUp(self):
        print("用例开始")

    def test_01_正在咨询人数(self):
        """正在咨询人数 """
        start, end = query_time()
        not_immediate_data = {"cid": str(cid)}
        r = requests.get(
            url=url + "/api/statistic/first_page/immediate",
            headers=headers,
            params=not_immediate_data,
        )
        requests.get(url=url + "/api/user/logout", headers=headers)
        result = r.json()
        print(result)
        self.assertEqual(r.status_code, 200, msg="接口返回码 错误")

        # ==========正在咨询人数===========
        正在咨询人数 = result["data"]["正在咨询人数"]
        sql1 = "select count(distinct uid) from chat_session where cid = '{}' and created >= '{}' and status != 2".format(
            cid,start
        )
        print("正在咨询人数:", sql1)
        query_result1 = pandas.read_sql_query(sql1, mysql_str)
        # print(query_result1)
        query_result1 = query_result1.to_dict(orient="records")  # 字典格式
        # print(query_result1)
        query_result1 = query_result1[0]["count(distinct uid)"]
        print("数据库-正在咨询人数" + ":" + str(query_result1))
        print("接口-正在咨询人数" + ":" + str(正在咨询人数))

        # ==========当前在线客服===========
        当前在线客服 = result["data"]["当前在线客服"]
        sql2 = "select count(user_id) from (select t.user_id,  substring_index(group_concat( t.content ),',',1) lastest_content,t.raw,t.created from (select * from log where action = '客服上下线' and cid = '{}' order by user_id asc,created desc) t group by user_id) q where q.lastest_content = '上线'".format(
            cid
        )
        print("当前在线客服:", sql2)
        query_result2 = pandas.read_sql_query(sql2, mysql_str)
        # print(query_result1)
        query_result2 = query_result2.to_dict(orient="records")  # 字典格式
        # print(query_result1)
        query_result2 = query_result2[0]["count(user_id)"]
        print("数据库-当前在线客服" + ":" + str(query_result2))
        print("接口-当前在线客服" + ":" + str(当前在线客服))

        # ==========今日总会话时长===========
        今日总会话时长 = result["data"]["今日总会话时长"]
        sql_今日会话时长 = "select sum(t2.dif_second),count(distinct t2.ori_session),sum(t2.dif_second)/count(distinct t2.ori_session) from (select *,(UNIX_TIMESTAMP(t.stop_time) - UNIX_TIMESTAMP(t.created)) dif_second from (select * from chat_session where cid = '{}' and created >= '{}' and user_id is not null and status = 2) t) t2".format(
            cid,start
        )
        print("今日总会话时长:", sql_今日会话时长)
        query_今日会话时长 = pandas.read_sql_query(sql_今日会话时长, mysql_str)
        query_今日会话时长 = query_今日会话时长.to_dict(orient="records")  # 字典格式
        print(query_今日会话时长)
        query_今日总会话时长 = int(query_今日会话时长[0]["sum(t2.dif_second)"])
        print("数据库-今日总会话时长" + ":" + str(query_今日总会话时长))
        print("接口-今日总会话时长" + ":" + str(今日总会话时长))
        # ==========今日平均会话时长===========
        今日平均会话时长 = result["data"]["今日平均会话时长"]
        print(query_今日会话时长[0]["sum(t2.dif_second)/count(distinct t2.ori_session)"])
        query_今日平均会话时长 = (query_今日会话时长[0]["sum(t2.dif_second)/count(distinct t2.ori_session)"])
        print(query_今日平均会话时长)
        print("数据库-今日平均会话时长" + ":" + str(query_今日平均会话时长))
        print("接口-今日平均会话时长" + ":" + str(今日平均会话时长))

        self.assertEqual(int(正在咨询人数), query_result1, msg="正在咨询人数 数据错误")
        self.assertTrue(int(正在咨询人数) >= 0, msg="正在咨询人数 为负数")
        self.assertEqual(int(当前在线客服), query_result2, msg="当前在线客服 数据错误")
        self.assertTrue(int(当前在线客服) >= 0, msg="当前在线客服 为负数")
        self.assertEqual(int(今日总会话时长), query_今日总会话时长, msg="今日总会话时长 数据错误")
        self.assertTrue(int(今日总会话时长) >= 0, msg="今日总会话时长 为负数")
        self.assertEqual(int(今日平均会话时长), query_今日平均会话时长, msg="今日平均会话时长 数据错误")
        self.assertTrue(int(今日平均会话时长) >= 0, msg="今日平均会话时长 为负数")





    def tearDown(self):
        time.sleep(1)
        print("用例结束")


class Test_not_immediate_api(unittest.TestCase):
    """首页数据not_immediate接口测试"""

    def login(self):
        login_data = {
            "account": "cw-api",
            "password": "123",
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

    def setUp(self):
        #time.sleep(1)
        print("测试开始")
    def test_01_今日机器人服务数据趋势(self):
        """今日机器人服务数据趋势 """
        start, end = query_time()
        headers = self.login()
        not_immediate_data = {"cid": str(cid)}
        r = requests.get(
            url=url + "/api/statistic/first_page/not_immediate",
            headers=headers,
            params=not_immediate_data,
        )
        requests.get(url=url + "/api/user/logout", headers=headers)
        result = r.json()
        print(result)
        self.assertEqual(r.status_code, 200, msg="接口返回码 错误")
        print(result["data"]["今日机器人服务数据趋势"])

        # ==========今日机器人总会话量===========
        今日机器人总会话量 = result["data"]["今日机器人服务数据趋势"]["今日机器人总会话量"]
        sql1 = "select count(id) from chat_session where cid = '{}' and created >= '{}' and last_session is null and user_id is null".format(
            cid,start
        )
        print("今日机器人总会话量:", sql1)
        query_result1 = pandas.read_sql_query(sql1, mysql_str)
        # print(query_result1)
        query_result1 = query_result1.to_dict(orient="records")  # 字典格式
        # print(query_result1)
        query_result1 = query_result1[0]["count(id)"]
        print("数据库-今日机器人总会话量" + ":" + str(query_result1))
        print("接口-今日机器人总会话量" + ":" + str(今日机器人总会话量))

        # ==========今日机器人解决量===========
        今日机器人解决量 = result["data"]["今日机器人服务数据趋势"]["今日机器人解决量"]
        sql2 = "select count(id) from chat_session where cid = '{}' and created >= '{}' and  user_id is null and status = 2 and robot_question_status = 1".format(
            cid,start
        )
        print("今日机器人解决量:", sql2)
        query_result2 = pandas.read_sql_query(sql2, mysql_str)
        # print(query_result1)
        query_result2 = query_result2.to_dict(orient="records")  # 字典格式
        # print(query_result1)
        query_result2 = query_result2[0]["count(id)"]
        print("数据库-今日机器人解决量" + ":" + str(query_result2))
        print("接口-今日机器人解决量" + ":" + str(今日机器人解决量))

        # ==========今日机器人解决率===========
        今日机器人解决率 = result["data"]["今日机器人服务数据趋势"]["今日机器人解决率"]
        print(r.status_code)
        query_result21 = query_result1 != 0 and query_result2 / query_result1 or 0
        # if query_result1 == 0:
        #     query_result21 = 0
        # else:
        #     query_result21 = query_result2 / query_result1
        query_result21 = Decimal("{}".format(query_result21)).quantize(
            Decimal("0.0000")
        )
        print(
            str(query_result21) + "=" + str(query_result2) + "/" + str(query_result1)
        )
        print("数据库-今日机器人解决率" + ":" + str(query_result21))
        print("接口-今日机器人解决率" + ":" + str(今日机器人解决率))

        self.assertEqual(今日机器人总会话量, query_result1, msg="今日机器人总会话量 数据错误")
        self.assertTrue(今日机器人总会话量 >= 0, msg="今日机器人总会话量 为负数")
        self.assertEqual(今日机器人解决量, query_result2, msg="今日机器人解决量 数据错误")
        self.assertTrue(今日机器人解决量 >= 0, msg="今日机器人解决量 为负数")
        self.assertEqual(今日机器人解决率, float(query_result21), msg="今日机器人解决率 数据错误")
        self.assertTrue(今日机器人解决率 >= 0, msg="今日机器人解决率 为负数")

    def test_02_今日机器人聊天数据趋势(self):
        """今日机器人聊天数据趋势 """
        start, end = query_time()
        headers = self.login()
        not_immediate_data = {"cid": str(cid)}
        r = requests.get(
            url=url + "/api/statistic/first_page/not_immediate",
            headers=headers,
            params=not_immediate_data,
        )
        requests.get(url=url + "/api/user/logout", headers=headers)
        result = r.json()
        print(result)
        self.assertEqual(r.status_code, 200, msg="接口返回码 错误")
        print(result["data"]["今日机器人聊天数据趋势"])

        # ==========今日访客提问数===========
        今日访客提问数 = result["data"]["今日机器人聊天数据趋势"]["今日访客提问数"]
        sql1 = '''select count(id) from chat_log where cid = '{}' and created >= '{}' and raw regexp '"from_code"(: 8,|: 17,|: 21,|: 9,|: 20,|: 16,|: 2,|: 3,|: 19,|: 7,|: 22,|: 1,|: 15,|: 10,|: 18,|: 5,|: 25,|: 26,|: 27,|: 6,|: 4,|: 13,|: 23,|: 12,|: 28,)' and source = "1"'''.format(
            cid,start
        )
        print("今日访客提问数:", sql1)
        query_result1 = pandas.read_sql_query(sql1, mysql_str)
        # print(query_result1)
        query_result1 = query_result1.to_dict(orient="records")  # 字典格式
        # print(query_result1)
        query_result1 = query_result1[0]["count(id)"]
        print("数据库-今日访客提问数" + ":" + str(query_result1))
        print("接口-今日访客提问数" + ":" + str(今日访客提问数))

        # ==========今日匹配提问数===========
        今日匹配提问数 = result["data"]["今日机器人聊天数据趋势"]["今日匹配提问数"]
        sql2 = '''select count(id) from chat_log where cid = '{}' and created >= '{}' and raw regexp '"from_code"(: 8,|: 17,|: 21,|: 9,|: 20,|: 16,|: 2,|: 3,|: 19,|: 7,|: 22,|: 1,|: 15,|: 10,|: 18,|: 5,|: 25,|: 26,|: 27,)' and source = "1"'''.format(
            cid,start
        )
        print("今日匹配提问数:", sql2)
        query_result2 = pandas.read_sql_query(sql2, mysql_str)
        # print(query_result1)
        query_result2 = query_result2.to_dict(orient="records")  # 字典格式
        # print(query_result1)
        query_result2 = query_result2[0]["count(id)"]
        print("数据库-今日匹配提问数" + ":" + str(query_result2))
        print("接口-今日匹配提问数" + ":" + str(今日匹配提问数))

        # ==========今日匹配率===========
        今日匹配率 = result["data"]["今日机器人聊天数据趋势"]["今日匹配率"]
        print(r.status_code)
        query_result21 = query_result1 != 0 and query_result2 / query_result1 or 0
        # if query_result1 == 0:
        #     query_result21 = 0
        # else:
        #     query_result21 = query_result2 / query_result1
        query_result21 = Decimal("{}".format(query_result21)).quantize(
            Decimal("0.0000")
        )
        print(
            str(query_result21) + "=" + str(query_result2) + "/" + str(query_result1)
        )
        print("数据库-今日匹配率" + ":" + str(query_result21))
        print("接口-今日匹配率" + ":" + str(今日匹配率))

        self.assertEqual(今日访客提问数, query_result1, msg="今日访客提问数 数据错误")
        self.assertTrue(今日访客提问数 >= 0, msg="今日访客提问数 为负数")
        self.assertEqual(今日匹配提问数, query_result2, msg="今日匹配提问数 数据错误")
        self.assertTrue(今日匹配提问数 >= 0, msg="今日匹配提问数 为负数")
        self.assertEqual(今日匹配率, float(query_result21), msg="今日匹配率 数据错误")
        self.assertTrue(今日匹配率 >= 0, msg="今日匹配率 为负数")

    def test_03_今日客服服务数据趋势(self):
        """今日客服服务数据趋势 """
        start, end = query_time()
        headers = self.login()
        not_immediate_data = {"cid": str(cid)}
        r = requests.get(
            url=url + "/api/statistic/first_page/not_immediate",
            headers=headers,
            params=not_immediate_data,
        )
        requests.get(url=url + "/api/user/logout", headers=headers)
        result = r.json()
        print(result)
        self.assertEqual(r.status_code, 200, msg="接口返回码 错误")
        print(result["data"]["今日客服服务数据趋势"])

        # ==========今日客服总会话量===========
        今日客服总会话量 = result["data"]["今日客服服务数据趋势"]["今日客服服务总会话量"]
        sql1 = "select count(id) from chat_session where cid = '{}' and created >= '{}' and last_session is null and user_id is not null".format(
            cid,start
        )
        print("今日客服总会话量:", sql1)
        query_result1 = pandas.read_sql_query(sql1, mysql_str)
        # print(query_result1)
        query_result1 = query_result1.to_dict(orient="records")  # 字典格式
        # print(query_result1)
        query_result1 = query_result1[0]["count(id)"]
        print("数据库-今日客服总会话量" + ":" + str(query_result1))
        print("接口-今日客服总会话量" + ":" + str(今日客服总会话量))

        # ==========今日客服总接待量===========
        今日客服总接待量 = result["data"]["今日客服服务数据趋势"]["今日客服总接待量"]
        sql2 = "select count(id) from chat_session where cid = '{}' and created >= '{}' and user_id is not null".format(
            cid,start
        )
        print("今日客服总接待量:", sql2)
        query_result2 = pandas.read_sql_query(sql2, mysql_str)
        # print(query_result1)
        query_result2 = query_result2.to_dict(orient="records")  # 字典格式
        # print(query_result1)
        query_result2 = query_result2[0]["count(id)"]
        print("数据库-今日客服总接待量" + ":" + str(query_result2))
        print("接口-今日客服总接待量" + ":" + str(今日客服总接待量))

        self.assertEqual(今日客服总会话量, query_result1, msg="今日客服总会话量 数据错误")
        self.assertTrue(今日客服总会话量 >= 0, msg="今日客服总会话量 为负数")
        self.assertEqual(今日客服总接待量, query_result2, msg="今日客服总接待量 数据错误")
        self.assertTrue(今日客服总接待量 >= 0, msg="今日客服总接待量 为负数")
        self.assertTrue(今日客服总接待量 >= 今日客服总会话量, msg="今日客服总接待量 小于 今日客服总会话量")

    def tearDown(self):
        # headers = self.login()
        # r = requests.get(url=url + "/api/user/logout",headers=headers)
        #time.sleep(1)
        print("退出登录")


