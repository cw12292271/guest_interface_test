
from BI.data.BI_SQL_02 import *
from BI.data.basic import *


def statistics_sql(sql):
    con = pymysql.connect(**config)
    try:
        with con.cursor() as cursor:
            # print(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
            # print(result)
            for index_values in result[0].values():
                result = index_values
        return result
    finally:
        con.close()


def create_query_time(startt, endt):
    queretimes = {'total': [], 'divide': []}
    if startt == endt:
        start_time = startt
        end_time = endt + timedelta(days=1)
        queretimes['total'].append({start_time.strftime("%Y-%m-%d"): end_time.strftime("%Y-%m-%d")})
        while start_time < endt + timedelta(days=1):
            end_time = start_time + timedelta(hours=1)
            queretimes['divide'].append({start_time.strftime("%Y-%m-%d %H:%M:%S"): end_time.strftime("%Y-%m-%d %H:%M:%S")})
            start_time = start_time + timedelta(hours=1)
    else:
        if startt < endt + timedelta(days=1):
            start_time = startt
            end_time = endt + timedelta(days=1)
        else:
            start_time = endt
            end_time = startt + timedelta(days=1)
        queretimes['total'].append({start_time.strftime("%Y-%m-%d"): end_time.strftime("%Y-%m-%d")})
        while start_time < max(startt, endt) + timedelta(days=1):
            end_time = start_time + timedelta(days=1)
            queretimes['divide'].append({start_time.strftime("%Y-%m-%d"): end_time.strftime("%Y-%m-%d")})
            start_time = start_time + timedelta(days=1)
    return queretimes


def sql_historical_trend_data(sqldata):
    db_result = {}
    for cqt in create_query_time(starttime, endtime)['total']:
        for start_time, end_time in cqt.items():
            format_data['start'] = start_time
            format_data['end'] = end_time
            for index_name, sql_statement in sqldata.items():
                sql_query_result_total = statistics_sql(sql_statement.format(**format_data))
                db_result[index_name] = sql_query_result_total

    db_result['trend'] = []
    for cqt in create_query_time(starttime, endtime)['divide']:
        for start_time, end_time in cqt.items():
            format_data['start'] = start_time
            format_data['end'] = end_time
            db_result_divide = {'datetime': start_time}
            for index_name, sql_statement in sqldata.items():
                sql_query_result_divide = statistics_sql(sql_statement.format(**format_data))
                db_result_divide[index_name] = sql_query_result_divide
            db_result['trend'].append(db_result_divide)

    return db_result


def sql_historical_no_trend_data(sqldata):
    db_result = {}
    for cqt in create_query_time(starttime, endtime)['total']:
        for start_time, end_time in cqt.items():
            format_data['start'] = start_time
            format_data['end'] = end_time
            for index_name, sql_statement in sqldata.items():
                # print('前',sql_statement.format(**format_data))
                sql_query_result_total = statistics_sql(sql_statement.format(**format_data))
                # print(sql_statement.format(**format_data))
                if sql_query_result_total is None:
                    sql_query_result_total = '0'
                db_result[index_name] = sql_query_result_total

    return db_result


# pprint(sql_historical_no_trend_data(sql_客服详情_非趋势))


# if __name__ == '__main__':
#     i = 1
#     if i != 0:
#         for query_time in query_time():
#             for start, end in query_time.items():
#                 data = sql_data(cid, start, end, user_id,today)[i]
#                 sql_results = {}
#                 for k, v in data.items():
#                     k1, sql_result1 = query_sql(k, v, mysql_str)
#                     sql_results[k1] = sql_result1
#                 print(start,'  ', end,'  ', sql_results)
#     else:
#         start,end = today,today
#         data = sql_data(cid, start, end,user_id, today)[i]
#         sql_results = {}
#         for k, v in data.items():
#             k1, sql_result1 = query_sql(k, v, mysql_str)
#             sql_results[k1] = sql_result1
#         print(today, sql_results)


