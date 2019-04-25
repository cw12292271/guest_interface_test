import re
import time

from BI.data.basic import *
from BI.data.BI_SQL_02 import *

end = (datetime.strptime(end,"%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")

#
# start = '2018-12-13'
# end = '2018-12-14'
#
# format_data['start'] = start
# format_data['end'] = end


def query_sql(sql_statement):
    con = pymysql.connect(**config)
    try:
        with con.cursor() as cursor:
            cursor.execute(sql_statement.format(**format_data))
            result = cursor.fetchall()
        return result
    finally:
        con.close()


def statustimes(sqldata):
    db_result = {}
    for index_name, sql_statement in sqldata.items():
        sql_query_result = query_sql(sql_statement.format(**format_data))
        actionlist = []
        createdlist = []
        status_name = re.findall(r'(.+?)总时长', index_name)
        try:
            if sql_query_result[0]['action'] == status_name[0]:
                sql_query_result[0]['created'] = start + " " + "00:00:00"
            else:
                sql_query_result.pop(0)

            if sql_query_result:
                for dr in sql_query_result:
                    actionlist.append(dr['action'])
                    createdlist.append(dr['created'])

                j = 0
                m = len(actionlist)
                online_actionlist = []
                online_createdlist = []
                while j < m:
                    j = j + 1
                    if actionlist[j - 1] == status_name[0]:
                        online_actionlist.append(actionlist[j - 1])
                        online_createdlist.append(createdlist[j - 1])
                        try:
                            online_actionlist.append(actionlist[j])
                            online_createdlist.append(createdlist[j])
                        except IndexError:
                            online_actionlist.append('终点')
                            online_createdlist.append(end + " " + "00:00:00")
                    else:
                        continue

                if online_actionlist[-1] == status_name[0]:
                    online_actionlist.append('终点')
                    online_createdlist.append(end + " " + "00:00:00")

                i = 0
                duration = 0
                while i < len(online_createdlist):
                    eachtime = (datetime.strptime(online_createdlist[i + 1], "%Y-%m-%d %H:%M:%S") - datetime.strptime(
                        online_createdlist[i], "%Y-%m-%d %H:%M:%S")).total_seconds()
                    duration = duration + eachtime
                    i = i + 2
                dur = second_transform(duration)
                db_result[index_name] = dur
            else:
                db_result[index_name] = '0秒'
        except IndexError:
            db_result[index_name] = '0秒'
    return db_result


def servicetimes(sqldata):
    db_result = {}
    for index_name, sql_statement in sqldata.items():
        sql_query_result = query_sql(sql_statement.format(**format_data))
        createdlist = []
        stoplist = []
        seviceduration = 0
        if sql_query_result:
            for sqr in sql_query_result:
                createdlist.append(sqr['created'])
                stoplist.append(sqr['stop_time'])
            while len(createdlist) > 1:
                j = 0
                j = j + 1
                if stoplist[j - 1] >= createdlist[j]:
                    createdlist.pop(j)
                    if stoplist[j - 1] >= stoplist[j]:
                        stoplist.pop(j)
                    else:
                        stoplist.pop(j - 1)
                elif stoplist[j - 1] < createdlist[j]:
                    eachtime = (stoplist[j - 1] - createdlist[j - 1]).total_seconds()
                    seviceduration = seviceduration + eachtime
                    createdlist.pop(j - 1)
                    stoplist.pop(j - 1)
            seviceduration = seviceduration + (stoplist[0] - createdlist[0]).total_seconds()
            dur = second_transform(seviceduration)
            db_result = {index_name: dur}
        else:
            db_result = {index_name: '0秒'}
    return db_result


def visitordata(sqldata):
    db_result = {}
    for index_name, sql_statement in sqldata.items():
        sql_query_result = query_sql(sql_statement.format(**format_data))
        for sqr in sql_query_result:
            for sqr_values in sqr.values():
                db_result[index_name] = sqr_values

    return db_result


def visitordistributiondata(sqldata):
    db_result = {}
    for index_name, sql_statement in sqldata.items():
        sql_query_result = query_sql(sql_statement.format(**format_data))
        slist = {}
        for sqr in sql_query_result:
            slist[list(sqr.values())[0]] = list(sqr.values())[1]
            # slist.append({list(sqr.values())[0]: list(sqr.values())[1]})
        db_result[index_name] = slist
    return db_result


# pprint(visitordistributiondata(sql_访客分布))

