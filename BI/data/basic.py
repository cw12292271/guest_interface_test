import re
from datetime import *
from decimal import Decimal
import time
from pprint import pprint

import pymysql

base_url = 'http://cwtest.t8.site.webot.ai'

apis = dict(
    机器人总览=base_url + '/api/statistic/robot',
    客服总览=base_url + '/api/statistic/customer_service_data_overview',
    客服工作量=base_url + '/api/statistic/kf_service_work_load',
    客服工作质量=base_url + '/api/statistic/customer_service_quality_work',
    客服考勤=base_url + '/api/statistic/customer_attendance',
    访客=base_url + '/api/statistic/visitor',
)

cid = 149
user_id = 329
now = datetime.now()
zeroToday = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,microseconds=now.microsecond)
zeroToday = zeroToday - timedelta(days=14)
starttime = zeroToday - timedelta(days=2)
endtime = zeroToday - timedelta(days=1)
start = starttime.strftime("%Y-%m-%d")
end = endtime.strftime("%Y-%m-%d")
print(start, end)

format_data = {'cid': cid,
               'user_id': user_id,
               'start': start,
               'end': end,
               'today': zeroToday.strftime("%Y-%m-%d"),
               'to_kf': '{"to_kf": 1}'
               }

config = {'host': 'webot2dingdang.c1t9kbuexy3c.rds.cn-north-1.amazonaws.com.cn',
          'user': 'root',
          'password': 'ZEGAhuDP',
          'port': 3306,
          'db': 'webot2-t8',
          'charset': 'utf8mb4',
          'cursorclass': pymysql.cursors.DictCursor,
          }

login_data = {
    "account": "cw-api",
    "password": "123",
    "code": "nvrW6OD4",
    "force_login": True,
    "t": "",
}


def second_transform(second):
    m, s = divmod(second, 60)
    h, m = divmod(m, 60)
    if h == 0:
        if m == 0:
            result = "{}秒".format(int(s))
        else:
            result = "{}分{}秒".format(int(m), int(s))
    else:
        result = "{}时{}分{}秒".format(int(h), int(m), int(s))

    return result


def transform_second(duration):
    res = re.findall(r"\d+\.?\d*", duration)
    s = int(res[-1])
    try:
        m = int(res[-2])
    except IndexError:
        m = 0
    try:
        h = int(res[-3])
    except IndexError:
        h = 0
    result = str(h*60*60 + m*60 + s)
    return result


def percent_decimal(decimal):
    res = re.findall(r"\d+\.?\d*", decimal)
    result = float('%.4f' % (float(res[0])/100))
    return result

