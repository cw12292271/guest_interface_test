import datetime

import pandas

mysql_str = (
    "mysql+pymysql://root:ZEGAhuDP@webot2dingdang.c1t9kbuexy3c.rds.cn-north-1.amazonaws.com.cn:3306/webot2-t6?charset=utf8mb4"
)


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

cid = 1
start,end = query_time()

# ==========首页===========

sql_正在咨询人数 = "select count(distinct uid) from chat_session where cid = '{}' and created >= '{}' and status != 2".format(
    cid, start
)
sql_当前在线客服 = "select count(user_id) from (select t.user_id,  substring_index(group_concat( t.content ),',',1) lastest_content,t.raw,t.created from (select * from log where action = '客服上下线' and cid = '{}' order by user_id asc,created desc) t group by user_id) q where q.lastest_content = '上线'".format(
    cid
)
sql_今日会话时长 = "select sum(t2.dif_second),count(distinct t2.ori_session),sum(t2.dif_second)/count(distinct t2.ori_session) from (select *,(UNIX_TIMESTAMP(t.stop_time) - UNIX_TIMESTAMP(t.created)) dif_second from (select * from chat_session where cid = '{}' and created >= '{}' and user_id is not null and status = 2) t) t2".format(
    cid, start
)

sql_满意度参评数 = '''select count(sid) from (select l.sid,l.raw ,s.user_id from chat_session s , chat_log l where l.cid = '{}' and l.created >= '{}' and l.raw regexp '"text"(: "满意"|: "非常满意"|: "一般"|: "不满意"|: "非常不满意")' and l.sid = s.sid) t '''.format(
    cid, start
)
sql_满意数 = '''select count(sid) from (select l.sid,l.raw ,s.user_id from chat_session s , chat_log l where l.cid = '{}' and l.created >= '{}' and l.raw regexp '"text"(: "满意"|: "非常满意"|: "一般"|: "不满意"|: "非常不满意")' and l.sid = s.sid) t '''.format(
    cid, start
)


sql_今日客服总会话量 = "select count(id) from chat_session where cid = '{}' and created >= '{}' and last_session is null and user_id is not null".format(
    cid, start
)
sql_今日客服总接待量 = "select count(id) from chat_session where cid = '{}' and created >= '{}' and user_id is not null".format(
    cid, start
)
sql_今日机器人总会话量 = "select count(id) from chat_session where cid = '{}' and created >= '{}' and last_session is null and user_id is null".format(
    cid, start
)
sql_今日机器人解决量 = "select count(id) from chat_session where cid = '{}' and created >= '{}' and  user_id is null and status = 2 and robot_question_status = 1".format(
    cid, start
)
sql_今日访客提问数 = '''select count(id) from chat_log where cid = '{}' and created >= '{}' and raw regexp '"from_code"(: 8,|: 17,|: 21,|: 9,|: 20,|: 16,|: 2,|: 3,|: 19,|: 7,|: 22,|: 1,|: 15,|: 10,|: 18,|: 5,|: 25,|: 26,|: 27,|: 6,|: 4,|: 13,|: 23,|: 12,|: 28,)' and source = "1"'''.format(
    cid, start
)
sql_今日匹配提问数 = '''select count(id) from chat_log where cid = '{}' and created >= '{}' and raw regexp '"from_code"(: 8,|: 17,|: 21,|: 9,|: 20,|: 16,|: 2,|: 3,|: 19,|: 7,|: 22,|: 1,|: 15,|: 10,|: 18,|: 5,|: 25,|: 26,|: 27,)' and source = "1"'''.format(
    cid, start
)

# ==========总览===========

sql_机器人会话量 = "select count(*) from chat_session where cid = '{}' and created >= '{}' and created < '{}' and last_session is null and user_id is null".format(
    cid, start, end
)
sql_机器人解决量 = "select count(*) from chat_session where cid = '{}' and created >= '{}' and created < '{}' and user_id is null and status = 2 and robot_question_status = 1".format(
    cid, start, end
)
sql_机器人转人工会话量 = "select count(*) from chat_session where cid = '{}' and created >= '{}' and created < '{}'and creator = 1".format(
    cid, start, end
)  # creator ： 0: 机器人创建，1: 客户转人工, 2: 客服激活，3.客服工单发起, 4.客服转交客服， 5.客服转交客服组

sql_客服会话量 = "select count(*) from chat_session where cid = '{}' and created >= '{}' and created < '{}' and last_session is null and user_id is not null".format(
     cid, start, end
)
sql_客服接待量 = "select count(*) from chat_session where cid = '{}' and created >= '{}' and created < '{}' and user_id is not null".format(
    cid, start, end
)

sql_总消息量 = (
    """select count(*) from chat_log """
    """where source = "9" and (`raw` LIKE '%%"msg\_type": "text"%%') """
    """and (`raw` not LIKE '%%"is\_sys\_send": 1%%' or `raw` not LIKE '%%"is\_sys\_send": "1"%%')"""
    """and cid = '{}' and created >= '{}' and created < '{}' """.format(
        cid, start, end
    )
)
sql_客服消息量 = (
    """select count(*) from chat_log """
    """where source = "9" and `raw` LIKE '%%"from": "kf"%%' and (`raw` LIKE '%%"msg\_type": "text"%%') """
    """and (`raw` not LIKE '%%"is\_sys\_send": 1%%' or `raw` not LIKE '%%"is\_sys\_send": "1"%%') """
    """and cid = '{}' and created >= '{}' and created < '{}' """.format(
        cid, start, end
    )
)
sql_访客消息量 = (
    """select count(*) from chat_log """
    """where source = "9" and `raw` LIKE '%%"from": "user"%%' and (`raw` LIKE '%%"msg\_type": "text"%%') """
    """and (`raw` not LIKE '%%"is\_sys\_send": 1%%' or `raw` not LIKE '%%"is\_sys\_send": "1"%%')"""
    """and cid = '{}' and created >= '{}' and created < '{}' """.format(
        cid, start, end
    )
)
def _访客来访情况():
    sql_历史访客 = "select count(distinct uid) from chat_log where cid = '{}' and created >= '{}' and created < '{}' ".format(
        cid, start, end
    )
    sql_新访客 = "select count(distinct uid) from chat_user where cid = '{}' and created >= '{}' and created < '{}' ".format(
        cid, start, end
    )
    key = {k: v for k, v in locals().items() if not k.startswith("__")}
    key = list(key.keys())
    print(key)
    print('-----')
    sql_全 = [sql_历史访客, sql_新访客]
    for index, value in enumerate(sql_全):
        sql = value
        k = key[index]
        result = pandas.read_sql_query(sql, mysql_str)
        result = result.to_dict(orient="records")  # 字典格式
        result = result[0]["count(distinct uid)"]
        print(k,result)

def _访客渠道():
    sql_渠道_微信 = "select count(distinct uid) from chat_session where cid = '{}' and created >= '{}' and created < '{}' and source = 'weixin'".format(
        cid, start, end
    )
    sql_渠道_h5 = "select count(distinct uid) from chat_session where cid = '{}' and created >= '{}' and created < '{}' and source = 'h5'".format(
        cid, start, end
    )
    sql_全 = [sql_渠道_微信, sql_渠道_h5]
    for sql in sql_全:
        sql = sql
        key = sql.split('source = ')[1]
        result = pandas.read_sql_query(sql, mysql_str)
        result = result.to_dict(orient="records")  # 字典格式
        result = result[0]["count(distinct uid)"]
        print(key, result)

def _满意度():
    sql_满意度_非常满意 = '''select count(sid) from (select l.sid,l.raw ,s.user_id from chat_session s , chat_log l where l.cid = '{}' and l.created >= '{}' and l.raw regexp '"text"(: "非常满意")' and l.sid = s.sid) t '''.format(
        cid, start
    )
    sql_满意度_满意 = '''select count(sid) from (select l.sid,l.raw ,s.user_id from chat_session s , chat_log l where l.cid = '{}' and l.created >= '{}' and l.raw regexp '"text"(: "满意")' and l.sid = s.sid) t '''.format(
        cid, start
    )
    sql_满意度_一般 = '''select count(sid) from (select l.sid,l.raw ,s.user_id from chat_session s , chat_log l where l.cid = '{}' and l.created >= '{}' and l.raw regexp '"text"(: "一般")' and l.sid = s.sid) t '''.format(
        cid, start
    )
    sql_满意度_不满意 = '''select count(sid) from (select l.sid,l.raw ,s.user_id from chat_session s , chat_log l where l.cid = '{}' and l.created >= '{}' and l.raw regexp '"text"(: "不满意")' and l.sid = s.sid) t '''.format(
        cid, start
    )
    sql_满意度_非常不满意 = '''select count(sid) from (select l.sid,l.raw ,s.user_id from chat_session s , chat_log l where l.cid = '{}' and l.created >= '{}' and l.raw regexp '"text"(: "非常不满意")' and l.sid = s.sid) t '''.format(
        cid, start
    )

    key = {k: v for k, v in locals().items() if not k.startswith("__")}
    key = list(key.keys())
    print(key)
    print('-----')
    sql_全 = [sql_满意度_非常满意, sql_满意度_满意, sql_满意度_一般, sql_满意度_不满意, sql_满意度_非常不满意]
    for index, value in enumerate(sql_全):
        sql = value
        k = key[index]
        result = pandas.read_sql_query(sql, mysql_str)
        result = result.to_dict(orient="records")  # 字典格式
        result = result[0]["count(sid)"]
        print(k,result)

_访客来访情况()
#_访客渠道()
_满意度()
