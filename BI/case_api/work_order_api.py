import unittest

import requests


from BI.case_api import login

# url = "https://admin.t5.site.webot.ai"
cid = 1
mysql_str = (
    "mysql+pymysql://root:ZEGAhuDP@webot2dingdang.c1t9kbuexy3c.rds.cn-north-1.amazonaws.com.cn:3306/webot2-t5?charset=utf8mb4"
)

# headers, kid= login.Login.login(url)
# print(headers)
class WorkOder(unittest.TestCase):
    """工单系统接口测试"""
    def setUp(self):
        self.url = "https://admin.t5.site.webot.ai"
        self.headers, self.kid = login.Login.login(self.url)

    def test_01_创建工单(self):
        """创建工单 """
        data = {"creator_id":self.kid,
                "title":"接口创建",
                "content":"接口测试创建工单"}
        r = requests.post(
            url=self.url + "/api/work_order",
            headers=self.headers,
            data=data
        )
        print(r)
        result = r.json()
        print(result)
        self.assertEqual(r.status_code, 200, msg="接口返回码 错误")




