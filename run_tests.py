import time, sys
sys.path.append('./interface')
sys.path.append('./db_fixture')
from HTMLTestRunner_PY3 import HTMLTestRunner
import unittest
from db_fixture import test_data


# 指定测试用例为当前文件夹下的interface目录
test_dir = './interface'
discover = unittest.defaultTestLoader.discover(test_dir, pattern='*_test.py')


if __name__ == "__main__":
    test_data.init_data() # 初始化接口测试数据

    now = time.strftime("%Y-%m-%d %H-%M-%S")
    filename = './report/' + now + '_result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp,
                            title='发布会签到系统接口测试报告',
                            description='用例执行情况: ')
    runner.run(discover)
    fp.close()
