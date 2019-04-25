import pandas

# mysql_str = 'mysql+pymysql://root:ZEGAhuDP@webot2dingdang.c1t9kbuexy3c.rds.cn-north-1.amazonaws.com.cn:3306/webot2-t5?charset=utf8mb4'
#
# order_df = pandas.read_sql_query("select * from work_order where cid = 1 and created > '2018-04-20'", mysql_str)
#
# col = ["tag1"]
# order_df = order_df[col].fillna(-1)
# print(order_df["tag1"])



mysql_str = 'mysql+pymysql://root:ZEGAhuDP@webot2dingdang.c1t9kbuexy3c.rds.cn-north-1.amazonaws.com.cn:3306/webot2-t5?charset=utf8mb4'

#query_result = pandas.read_sql_query("select * from work_order where cid = 1 and created > '2018-04-20'", mysql_str)
query_result = pandas.read_sql_query("select * from chat_session where  created >= '2018-05-03' and created <= '2018-05-04 01:00:00' and cid = 1 group by(uid) ", mysql_str)
json_obj = query_result.to_dict(orient="records")  # 字典格式
json_obj = query_result.to_json(orient="records")  # json格式
print(json_obj,)