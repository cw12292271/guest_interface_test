import datetime
import random
import MySQLdb
import requests
import pandas
url = "https://admin.t5.site.webot.ai"
mysql_str = 'mysql+pymysql://root:ZEGAhuDP@webot2dingdang.c1t9kbuexy3c.rds.cn-north-1.amazonaws.com.cn:3306/webot2-t5?charset=utf8mb4'

def time():
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
            # end = end + datetime.timedelta(days=1)
            # sql = "select count(*) from chat_session where  created >= '{}' and created <= '{}' and cid = 1 and last_session is null and user_id is not null".format(start, end)
            # end = end - datetime.timedelta(days=1)
            #return start, end,sql
            start1 = start.strftime('%Y-%m-%d %H_%M_%S')
            start1 = start1.split(' ')[0]
            end1 = end.strftime('%Y-%m-%d %H_%M_%S')
            end1 = end1.split(' ')[0]
            return start, end, start1, end1


start, end,start1, end1 = time()
print(start, end,start1, end1)
login_data = {
    "account": "cw-api",
    "password": "123",
    "code": "nvrW6OD4",
    "t": ""
}

print(url +'/api/user')
headers = None
r = requests.post(url +'/api/user', headers, login_data)
r = r.json()
print(r)
token = r['data']['token']
print(token)
headers = {'Auth': token}

overview_data = {'cid':'1',
                 'start':start1,
                 'end':end1
                 }
print(overview_data)
r = requests.get(url=url + '/api/statistic/overview', headers=headers,params=overview_data)
result = r.json()
#print(result)
result1 = result['data']['客服服务数据']['客服会话量']
print('接口' + ':' + str(result1))
print(r.status_code)
assertEqual(r.status_code, 200, msg="接口返回码 错误")

# end = end + datetime.timedelta(days=1)
# sql = "select count(*) from chat_session where  created >= '{}' and created <= '{}' and cid = 1 and last_session is null and user_id is not null".format(
#     start, end)
# print(sql)
# query_result = pandas.read_sql_query(sql,mysql_str)
# print(query_result)
# json_obj = query_result.to_dict(orient="records")  # 字典格式
# print(json_obj)
# json_obj = json_obj[0]['count(*)']
# print('数据库' + ':' + str(json_obj))

result2 = result['data']['客服服务数据']['趋势']
print(result2)
result3 = [('客服会话量', sum([x['客服会话量'] for x in result2])) ]
result3 = result3[0][1]
print('趋势之和' + ':' + str(result3))

r = requests.get(url=url +'/api/user/logout',headers=headers)
print(r.status_code)