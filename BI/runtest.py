
import time
from HTMLTestRunner_PY3 import HTMLTestRunner
import unittest


#定义测试用例的目录为当前目录
# test_dir = './case_api'
# discover = unittest.defaultTestLoader.discover(test_dir,pattern='test_overview_api.py')

if __name__ == '__main__':
    test_dir = './case_api'
    test_report = './report'

    discover = unittest.defaultTestLoader.discover(test_dir, pattern='test_*.py')

    # 按照一定格式获取当地时间
    now_time = time.strftime("%Y-%m-%d %A %H_%M_%S ")

    # 定义报告存放路径
    filename = test_report + '\\' + now_time + 'result.html'

    #定义报告存放路径
    fp = open(filename,'wb')
    # 定义测试报告
    runner = HTMLTestRunner(stream=fp,title="test_project测试报告",description="用例执行情况：")

    #执行测试
    # runner = unittest.TextTestRunner()
    runner.run(discover)
    fp.close()  #关闭报告文件