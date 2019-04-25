import random
import re

# text = "site sea sue sweet see case sse ssee loses"
# m = re.findall(r"\bs\S*?e\b", text)
# if m:
#     print (m)
# else:
#     print ('not match')
#
# text = "(021)88776543 010-55667890 02584453362 0571 66345673 123 110"
# m = re.findall(r"\(0\d{2,3}\)\d{7,8}|0\d{2,3}[ -]?\d{7,8}", text)
# if m:
#     print (m)
# else:
#     print ('not match')

# for i in range(10):
#     n = random.randrange(1, 4)
#     print(n)

# ==========定义查询时间=========
import datetime
def query_time():

    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    start = datetime.datetime(year=year, month=month, day=day)
    end = datetime.datetime(year=year, month=month, day=day,hour=hour)
    print(type(start))
    print(start,end)
query_time()

cid = 1
data = {'cid': str(cid)}
print(data)

