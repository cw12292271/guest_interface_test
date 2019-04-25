import time
from HTMLTestRunner_PY3 import HTMLTestRunner

import unittest
import requests

url = "https://admin.t5.site.webot.ai"

class first_page(unittest.TestCase):


    '''首页接口测试'''
    def setUp(self):
        login_data = {
        "account": "cw-api",
        "password": "123",
        "code": "nvrW6OD4",
        "t": ""
        }
        headers = None
        r = requests.post(url +'/api/user', headers, login_data)
        r = r.json()
        token = r['data']['token']
        headers = {'Auth': token}
        return headers

    def test_first_page_immediate(self):
        '''首页实时数据接口'''
        immediate_data = {'cid': '1'}
        headers = self.setUp()
        r = requests.get(url=url + '/api/statistic/first_page/immediate', headers=headers, params=immediate_data)
        result = r.json()
        print(result)
        print(result['data']['机器人解决量'])
        print(r.status_code)

    def tearDown(self):
        headers = self.setUp()
        r = requests.get(url=url + '/api/user/logout', headers=headers)
        print(r.status_code)

if __name__ == '__main__':
    #unittest.main()

    testunit = unittest.TestSuite()

    testunit.addTest(first_page("test_first_page_immediate"))


    # 按照一定格式获取当地时间
    now_time = time.strftime("%Y-%m-%d %A %H_%M_%S ")

    # 定义报告存放路径
    fp = open('D:\\PycharmProjects\\webot2.0\\BI\\report\\' + now_time + 'overview_page_result.html', 'wb')
    # 定义测试报告
    runner = HTMLTestRunner(stream=fp,
                            title="test_first_page测试报告",
                            description="用例执行情况：")
    runner.run(testunit)
    fp.close()

