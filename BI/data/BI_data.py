import datetime
import pandas as pd
import json
import numpy
import re


def default(o):  # numpy.int64 无法json化，因此在json.dumps时，要将其转化为int
    if isinstance(o, numpy.integer):
        return int(o)


class BaseStatis(object):
    def __init__(self, df, now, statis_type=1):
        self.df = df
        self.statis = dict()
        self.statis_type = statis_type
        self.now = now
        if "question_tag" in self.df:
            self.tags = self._get_tags
        else:
            self.tags = {}

    def _table(self, table):
        if table in self.df:
            return self.df[table]
        else:
            return pd.DataFrame({"id": []})

    def _count(self, ser):
        return int(ser.get("id").count())


    @property
    def _get_tags(self):
        return {
            _tag["id"]: _tag["name"] for idx, _tag in
            self.df["question_tag"].iterrows()
        }

    def _json_dumps(self, d):
        return json.dumps(d, ensure_ascii=False, default=default)

    def _会话量(self, table):
        df = table.loc[(table.last_session.isnull())]
        return self._count(df)

    def _人工会话量(self, table):
        df = table.loc[
            (table.last_session.isnull()) & (table.user_id.notnull())]
        return self._count(df)

    def _机器人会话量(self, table):
        df = table.loc[
            (table.last_session.isnull()) & (table.user_id.isnull())]
        return self._count(df)

    def _series_index(self, series, idx):
        """
        根据索引获取一个Series对象的值
        """
        if series.size > 0:
            return series.iloc[idx]
        else:
            return {}

    def _用户咨询分类(self, table):
        """
        :param table: chat_session
        :return: {"tag1": "id": tag1_id, "count": 0, "sub_tags": {"id": tag2_id, "count": 0}}
        """
        # 用户分类咨询
        # 加入筛选条件
        df = table.loc[table.user_id.notnull()]
        df = df.loc[df["status"] == 2]
        df = df.sort_values('created', ascending=False).groupby('ori_session',
                                                                as_index=False).first()
        df = df.fillna(value=0)
        total_num = df["tag1"].size

        classify, num1, num2 = {"未分类": 0}, 0, 0
        for idx, tag in df.iterrows():
            tag1_content = self.tags.get(int(tag["tag1"]))
            tag2_content = self.tags.get(int(tag["tag2"]))
            classify["分类总数"] = total_num

            if tag1_content:
                if tag1_content not in classify:
                    classify[tag1_content] = {
                        "id": int(tag["tag1"]),
                        "count": 1,
                        "sub_tags": {}
                    }

                else:
                    classify[tag1_content]["count"] += 1

                if tag2_content not in classify.get(tag1_content).get(
                        "sub_tags") and tag2_content:
                    sdict = {
                        tag2_content: {"id": int(tag["tag2"]), "count": 1}}
                    classify[tag1_content]["sub_tags"].update(sdict)
                elif tag2_content in classify.get(tag1_content).get(
                        "sub_tags") and tag2_content:
                    classify[tag1_content]["sub_tags"][tag2_content][
                        "count"] += 1
            else:
                classify["未分类"] += 1
        return classify

    def _人工消息量(self, table):
        msg = table.loc[(table["source"] == "9") & (
            table.raw.str.contains('"msg_type": "text"'))]

        human_msg = msg.loc[(~msg.raw.str.contains('"is_sys_send": 1')) | (
            ~msg.raw.str.contains('"is_sys_send": "1"'))]

        visitor_msg = human_msg.loc[
            (human_msg.raw.str.contains('"from": "user"'))]

        kf_msg = human_msg.loc[(human_msg.raw.str.contains('"from": "kf"'))]

        return {"总消息量": human_msg['id'].count(),
                "访客消息量": visitor_msg['id'].count(),
                "客服消息量": kf_msg['id'].count()}

    def _热点问题(self, table):
        def _merge(hot, tags):
            return {
                question: {"分类": tags.get(question, "未分类")[0],
                           "计数": hot.get(question, 0),
                           "分类id": tags.get(question, "未分类")[1],
                           "问题id": tags.get(question, "未分类")[2]}
                for question, count in hot.items()
            }

        hot, tags = {}, {}
        for idx, log in table.iterrows():
            question = re.findall(r'"match_question": "(\w+)"', log['raw'])
            if question:
                tag1 = re.findall(r'"tag1": (\w+)', log['raw'])

                qid_all = re.findall(r'"id": (\w+)', log['raw'])
                qid = qid_all
                rich_answer = re.findall(r'"rich_answer": \[(.*?)\]',
                                         log['raw'])
                if rich_answer:
                    rich_answer_content = rich_answer[0]
                    rich_answer_id = re.findall(r'"id": (\w+)',
                                                rich_answer_content)

                    if rich_answer_id:
                        qid = list(set(qid_all) - set(rich_answer_id))

                q_tag = int(tag1[0]) if tag1 and isinstance(tag1, list) else 0
                if qid:
                    tags.setdefault(question[0],
                                    [self.tags.get(q_tag, "未分类"), q_tag,
                                     qid[0]])
                    hot.setdefault(question[0], 0)
                    hot[question[0]] += 1

        return _merge(hot, tags)

    def _机器人消息量_匹配数_未匹配数(self, table):
        bot_msg = table.loc[table["source"] == "1"]

        robot_df = bot_msg["raw"].str.extract(
            '"from_code"(: 8,|: 17,|: 21,|: 9,|: 20,|: 16,|: 2,|: 3,|: 19,|: 7,|: 22,|: 1,|: 15,|: 10,|: 18,|: 5,|: 25,|: 6,|: 4,|: 13,|: 23,|: 12,)',
            expand=True)

        # df1 = bot_msg["raw"].str.extract(
        #     '"from_code"(: 8,|: 17,|: 21,|: 9,|: 20,|: 16,|: 2,|: 3,|: 19,|: 7,|: 22,|: 1,|: 15,|: 10,|: 18,|: 5,|: 25,)',
        #     expand=True)

        df2 = bot_msg["raw"].str.extract(
            r'"from_code"(: 6,|: 4,|: 13,|: 23,|: 12,)',
            expand=True)

        机器人消息量 = robot_df[robot_df.notnull()].count().values[0]
        未匹配数 = df2[df2.notnull()].count().values[0]
        匹配数 = 机器人消息量 - 未匹配数
        return 机器人消息量, 匹配数, 未匹配数

    def _接待量(self, table):
        df = table.loc[table.user_id.notnull()]
        return self._count(df)

    def _接入会话量(self, table):
        """
        接入的会话量，包含访客来访、主动发起和转接接入三种情况
        :param table: chat_session
        :return:
        """
        # table = table.loc[table.last_session.isnull()]
        df = table.loc[table["creator"] != 0]
        return self._count(df)

    def _超时会话量(self, table):
        df = table.loc[(table.user_id.notnull()) & (table.stop_way == 0)]
        return self._count(df)

    def _满意统计(self, table):
        df = table.loc[table.user_id.notnull()]
        df = df.loc[df["status"] == 2]
        df = df.sort_values('created', ascending=False).groupby('ori_session',
                                                                as_index=False).first()
        satisfaction = df["satisfaction"]
        size = satisfaction.size
        satis = satisfaction.value_counts()
        评价总量 = size
        非常满意 = satis.get(5, 0)
        满意 = satis.get(4, 0)
        一般 = satis.get(3, 0)
        不满意 = satis.get(2, 0)
        非常不满意 = satis.get(1, 0)
        未评价 = 评价总量 - (非常满意 + 满意 + 一般 + 不满意 + 非常不满意)

        if not size:
            return {"未评价": 0, "非常不满意": 0, "不满意": 0, "一般": 0, "满意": 0,
                    "非常满意": 0, "评价总量": 0}
        return {"未评价": 未评价, "非常不满意": 非常不满意, "不满意": 不满意, "一般": 一般, "满意": 满意,
                "非常满意": 非常满意, "评价总量": 评价总量}

    def _接待时长统计(self, table):
        """
        接待时长
        :param table: chat_log
        :return:
        """
        d = {
            ">8m": 0,
            "6m-8m": 0,
            "4m-6m": 0,
            "2m-4m": 0,
            "<2m": 0,
            "all": 0,
        }

        for sid, df_logs in table.groupby("sid"):  # 按照 sid 聚合聊天日志
            if df_logs.iloc[0]['source'] != '9':
                continue
            duration = 0
            if df_logs.size > 0:
                # last_log = df_logs.iloc[0]["created"]
                last_log = \
                    df_logs.sort_values('created', ascending=True).groupby(
                        'sid',
                        as_index=False).first()[
                        "created"].values[0]
            for idx, log in df_logs.iterrows():
                t = (log["created"] - last_log).total_seconds()
                last_log = log["created"]
                if t < 1800:  # 相差 30 十分钟的对话，则排除
                    duration += t
            if duration < 120:
                d["<2m"] += 1
            elif 120 <= duration < 240:
                d["2m-4m"] += 1
            elif 240 <= duration < 360:
                d["4m-6m"] += 1
            elif 360 <= duration < 480:
                d["6m-8m"] += 1
            elif duration >= 480:
                d[">8m"] += 1
            d["all"] += duration
        return {"接待时间分段统计": self._json_dumps(d), "接待时长": d["all"]}

    # def _接待时长统计(self, table):
    #     """
    #     接待时长
    #     :param table:
    #     :return:
    #     """
    #     d = {
    #         ">8m": 0,
    #         "6m-8m": 0,
    #         "4m-6m": 0,
    #         "2m-4m": 0,
    #         "<2m": 0,
    #         "all": 0,
    #     }
    #
    #     for sid, df_logs in table.groupby("sid"):  # 按照 sid 聚合聊天日志
    #         if df_logs.iloc[0]['source'] != '9':
    #             continue
    #         duration = 0
    #         if df_logs.size > 0:
    #             last_log = df_logs.iloc[0]["created"]
    #         for idx, log in df_logs.iterrows():
    #             t = (log["created"] - last_log).total_seconds()
    #             last_log = log["created"]
    #             if t < 1800:  # 相差 30 十分钟的对话，则排除
    #                 duration += t
    #         if duration < 120:
    #             d["<2m"] += 1
    #         elif 120 <= duration < 240:
    #             d["2m-4m"] += 1
    #         elif 240 <= duration < 360:
    #             d["4m-6m"] += 1
    #         elif 360 <= duration < 480:
    #             d["6m-8m"] += 1
    #         elif duration >= 480:
    #             d[">8m"] += 1
    #         d["all"] += duration
    #     return {"接待时间分段统计": self._json_dumps(d), "接待时长": d["all"]}

    def _解决方式(self, table):
        human_table = table.loc[
            (table["status"] == 2) & (table["question_status"] == 1)]
        human_deal = int(human_table["user_id"].describe()["count"])

        robot = table.loc[table.user_id.isnull()]
        robot_table = robot.loc[
            (robot["status"] == 2) & (robot["robot_question_status"] == 1)]

        return {"human": human_deal, "robot": robot_table["id"].size}

    def _聊天日志分段统计(self, table):
        def _time_statis(d, t):
            if t < 15:
                d["<15s"] += 1
            elif 15 <= t < 30:
                d["15s-30s"] += 1
            elif 30 <= t < 45:
                d["30s-45s"] += 1
            elif 45 <= t < 60:
                d["45s-1m"] += 1
            elif t >= 60:
                d[">1m"] += 1
            if t <= 1800:
                d["all"] += t

        all_duration = {
            ">8m": 0, "6m-8m": 0, "4m-6m": 0, "2m-4m": 0, "<2m": 0, "all": 0
        }
        d_t = {"<15s": 0, "15s-30s": 0, "30s-45s": 0,
               "45s-1m": 0, ">1m": 0, "all": 0}
        # df = table.loc[(table["source"] == "9") & (
        #     table.raw.str.contains('"msg_type": "text"'))]
        first_time, general_time, no_answer, invalid = d_t, d_t.copy(), 0, 0

        for sid, df_logs in table.groupby("sid"):  # 按照 sid 聚合聊天日志
            if df_logs.iloc[0]['source'] != '9':
                continue
            duration, response = self._响应时间_会话时长(df_logs)

            response_time = []
            if len(response) > 1:
                t1 = response[:: 2]
                t2 = response[1:: 2]
                response_time = [
                    (t2[i]["time"] - t1[i]["time"]).total_seconds()
                    for i in range(min(len(t1), len(t2)))]
            elif len(response) == 1:
                no_answer += 1
            else:
                invalid += 1
            if len(response_time) > 0:
                _time_statis(first_time, response_time[0])
                for times in response_time:
                    _time_statis(general_time, times)
            if duration < 120:
                all_duration["<2m"] += 1
            elif 120 <= duration < 240:
                all_duration["2m-4m"] += 1
            elif 240 <= duration < 360:
                all_duration["4m-6m"] += 1
            elif 360 <= duration < 480:
                all_duration["6m-8m"] += 1
            elif duration >= 480:
                all_duration[">8m"] += 1
            all_duration["all"] += duration
        return {
            '会话时间统计': self._json_dumps(all_duration),
            '首次响应时长': self._json_dumps(first_time),
            '响应时长': self._json_dumps(general_time),
            '30s应答数': general_time.get("15s-30s", 0) + general_time.get("<15s",
                                                                        0),
            '未回复会话量': no_answer,
            '无效会话量': invalid,
        }

    def _响应时间_会话时长(self, table):
        cache = []
        begin = False
        duration = 0
        if table.size > 0:
            last_log = table.iloc[0]["created"]
        for idx, log in table.iterrows():
            t = (log["created"] - last_log).total_seconds()
            last_log = log["created"]
            if t < 1800:  # 相差 30 十分钟的对话，则排除
                duration += t

            content = log["raw"]
            _type = re.search(r'"msg_type": "event"', content)
            _from = re.findall(r'"from": "(\w+)"', content)
            _sys = re.search(r'"is_sys_send": "1"', content) or re.search(
                r'"is_sys_send": 1', content)
            if not _type and _from and not begin:
                if _from[0] == 'user':
                    cache.append({"from": "user", "time": log["created"]})
                    begin = True
                    continue
            elif _type or _sys:
                continue
            if begin and _from and not _sys:
                if cache[-1]["from"] == _from[0]:  # 归并，同一方多个发言合为一次记录
                    cache[-1] = {"from": _from[0], "time": log["created"]}
                else:
                    cache.append(
                        {"from": _from[0], "time": log["created"]})

        return duration, cache

    def _在线时长(self, table):
        '''
        统计客服在线时长和上线时间
        '''
        df = table.loc[(table["action"] == "客服上下线")]
        if not df.size:
            return {"在线总时长": None, "首次上线时间": None, "最后离线时间": None}
        online_time, login, logout = self._时长统计(df, "content", '上线', '下线')
        return {
            "在线总时长": online_time,
            "首次上线时间": login.strftime('%H:%M:%S'),
            "最后离线时间": logout.strftime('%H:%M:%S')
        }

    def _登陆时长(self, table):
        df = table.loc[(table["action"] == "登录") | (table['action'] == '注销')]
        if not table.size:
            return {"登陆总时长": None, "首次登录时间": None, "最后注销时间": None}
        login_time, login, logout = self._时长统计(df, 'action', "登录", "注销")
        return {
            "登陆总时长": login_time,
            "首次登录时间": login.strftime('%H:%M:%S'),
            "最后注销时间": logout.strftime('%H:%M:%S')
        }

    def _时长统计(self, df, idx, _in='', _out=''):
        if idx == "action":
            登录 = self._series_index(df.loc[(df[idx] == _in) & (df["content"] == "成功")], 0)
            注销 = self._series_index(df.loc[(df[idx].str.contains(_out)) & (df["content"] == "成功")], -1)
        else:
            登录 = self._series_index(df.loc[df[idx] == _in], 0)
            注销 = self._series_index(df.loc[df[idx].str.contains(_out)], -1)
        first = self._series_index(df, 0)
        end = self._series_index(df, -1)
        login_time = self._login_time(df, idx, _in, _out)
        login, logout = 登录.get('created', None), 注销.get('created', None)
        today_start, today_end = self._get_today_date(
            self.statis_type, 'start'), self._get_today_date(self.statis_type,'end')
        print("----", login_time, login, logout)
        print("---==", self.now, today_start, today_end)
        if not login_time:
            if not login:
                login = today_start
            if not logout:
                logout = today_end
            if login > logout:  # 00:00:00 —— 注销（12:00:00） 登录（12:30:00） —— 23:59:59
                part1 = (logout - today_start).total_seconds()
                logout = today_end
                part2 = (logout - login).total_seconds()
                login = today_start
                login_time = part1 + part2
            else:
                login_time = (logout - login).total_seconds()
        else:  # 注销 —— 登录 —— 注销 —— 登录 —— 注销 —— 登录
            part1, part2 = 0, 0
            if _out in first.get(idx):
                login = today_start
                part1 = (first.get('created') - today_start).total_seconds()
            if end.get(idx) == _in:
                logout = today_end
                part2 = (logout - end.get('created')).total_seconds()
            login_time += (part1 + part2)
        return login_time, login, logout

    def _login_time(self, table, index, _in='', _out=''):
        time, login_start = 0, 0
        for idx, log in table.iterrows():
            if log["action"] in ["登录", "注销"] and log["content"] != "成功":
                continue
            if not login_start and _out in log[index]:
                continue
            if log[index] == _in:
                login_start = log["created"]
            if _out in log[index]:
                time += (log["created"] - login_start).total_seconds()
                login_start = 0
        return time

    def _留言处理量(self, table):
        df = table.loc[
            (table.status == 2) | (table.status == 1) | (table.status == 3)]
        return self._count(df)

    def _在线客服人数(self, table):
        df = table.loc[
            (table["action"] == "客服上下线") & (table["content"] == "上线")]
        df = df.sort_values('created', ascending=False).groupby('user_id',
                                                                as_index=False).first()
        return self._count(df)

    def _客服状态切换时间(self, table):
        """客服切换状态"""
        df = table.loc[table["action"] == "客服上下线"]
        if not df.size:
            return {"客服状态切换时间": ""}
        sort_df = df.sort_values(by=["created"], ascending=[False], )
        now = datetime.datetime.now()
        prev = self.now
        result = {}

        for idx, dataframe in sort_df.iterrows():
            raw = dataframe.raw
            # raw = raw if raw.startswith("") else "离线"
            if not dataframe.raw or dataframe.content in ["被强制下线", "被动下线"]:
                raw = "离线"
            diff = (prev - dataframe.created).total_seconds()
            if dataframe.raw not in result:
                result[raw] = 0
            result[raw] += diff
            prev = dataframe.created

        return {
            "客服状态切换时间": json.dumps(result, ensure_ascii=False)}

    def _访客统计_用户来源(self, table):
        session_df = table.get("session")
        总访客, 用户来源 = [], {"h5": [], "weixin": []}
        for uid, dataframe in session_df.groupby("uid"):
            总访客.append(uid)
            sess = self._series_index(dataframe, 0)
            用户来源[sess.get("source")].append(uid)

        新访客 = []
        for idx, row in table.get("user").iterrows():
            新访客.append(row["uid"])
        return {"总访客": 总访客, "新访客": 新访客, "用户来源": 用户来源}

    def _问题解决统计(self, table):
        """
        客服解决问题的数量以及
        :param table: chat_session
        :return:
        """
        table = table.loc[(table.last_session.isnull())
                          & (table.user_id.notnull())]
        df = table.loc[(table["question_status"] == 1)]
        cf = table.loc[table["question_status"] == 0]
        return self._count(df), self._count(cf)

    def _get_today_date(self, statis_type, start='start'):
        if start == 'start':
            if statis_type:
                return datetime.datetime.combine(
                    self.now or datetime.date.today(),
                    datetime.time.min) - datetime.timedelta(days=1)
            else:
                return (self.now or datetime.datetime.now()) - datetime.timedelta(
                    hours=1)
        elif start == 'end':
            if statis_type:
                return datetime.datetime.combine(
                    self.now or datetime.date.today(),
                    datetime.time.max) - datetime.timedelta(days=1)
            else:
                return self.now or datetime.datetime.now()


class StatisCompany(BaseStatis):
    def __init__(self, df, now):
        super(StatisCompany, self).__init__(df, now)

    def statistic(self):
        result = dict()
        for attr in ["session", "chat_log", "log", "work_order_updated"]:
            func = self.__getattribute__("statis_" + attr)
            result.update(func())
        return result

    def statis_session(self):
        result = dict()
        table = self._table("chat_session")
        咨询分类 = self._用户咨询分类(table)
        result["会话量"] = self._会话量(table)
        result["客服会话量"] = self._人工会话量(table)
        result["机器人会话量"] = self._机器人会话量(table)
        result["超时会话量"] = self._超时会话量(table)
        result["接入会话量"] = self._接入会话量(table)
        result["客服接待量"] = self._接待量(table)
        result["解决方式"] = self._解决方式(table)
        result["用户咨询分类"] = self._用户咨询分类(table)
        result["满意统计"] = self._满意统计(table)

        result["解决"], result["未解决"] = self._问题解决统计(table)

        mul_table = {
            "user": self._table("chat_user"),
            "session": self._table("chat_session"),
        }

        result.update(self._访客统计_用户来源(mul_table))
        return result

    def statis_chat_log(self):
        result = dict()
        table = self._table("chat_log")
        result["接待时长"] = self._接待时长统计(table)
        result.update(self._聊天日志分段统计(table))
        热点问题 = self._热点问题(table)
        result["热点问题"] = self._json_dumps(热点问题)
        result["访客提问数"], result["机器人匹配提问数"], result[
            "机器人未匹配提问数"] = self._机器人消息量_匹配数_未匹配数(table)
        result.update(self._人工消息量(table))
        return result

    def statis_log(self):
        result = dict()
        table = self._table("log")
        result.update(self._在线时长(table))
        result.update(self._登陆时长(table))
        result["在线客服人数"] = self._在线客服人数(table)
        result.update(self._客服状态切换时间(table))
        return result

    def statis_work_order_updated(self):
        result = dict()
        table = self._table("work_order_updated")
        result["留言处理量"] = self._留言处理量(table)
        return result


# mysql_str = "mysql+pymysql://root:khJps8IW@webot210x0319.c1t9kbuexy3c.rds.cn-north-1.amazonaws.com.cn/webot2?charset=utf8mb4"

# mysql_str = 'mysql+pymysql://root:khJps8IW@webot210.c1t9kbuexy3c.rds.cn-north-1.amazonaws.com.cn:3306/webot2?charset=utf8mb4'

mysql_str = 'mysql+pymysql://root:ZEGAhuDP@webot2dingdang.c1t9kbuexy3c.rds.cn-north-1.amazonaws.com.cn:3306/webot2-t5?charset=utf8mb4'

# mysql_str = 'mysql+pymysql://root:123456@192.168.3.120/webot2?charset=utf8mb4'

cid = 1
start = "2018-05-22"
end = "2018-05-23"

df = {
    "chat_session": pd.read_sql_query("""select * from chat_session 
                                      where cid = {} and created > '{}' and created <= '{}'""".format(
        cid, start, end), mysql_str),

    'work_order_updated': pd.read_sql_query(
        """SELECT * FROM {} WHERE cid = {} and updated > '{}' and updated <= '{}'""".format(
            'work_order', cid, start, end), mysql_str),

    'question_tag': pd.read_sql_query("""select * from question_tag where cid = {}""".format(cid), mysql_str),

    'users': pd.read_sql_query("""select * from user where cid = {}""".format(cid), mysql_str),

    "chat_log": pd.read_sql_query(
        "SELECT * FROM {} WHERE cid = {} and created > '{}' and created <= '{}'".format(
            "chat_log", cid, start, end), mysql_str),

    "log": pd.read_sql_query(
        "SELECT * FROM {} WHERE cid = {} and created > '{}' and created <= '{}'".format(
            "log", cid, start, end), mysql_str),

    "chat_user": pd.read_sql_query(
        "SELECT * FROM {} WHERE cid = {} and created > '{}' and created <= '{}'".format(
            "chat_user", cid, start, end), mysql_str),

    "work_order_created": pd.read_sql_query(
        "SELECT * FROM {} WHERE cid = {} and created > '{}' and created <= '{}'".format(
            "work_order", cid, start, end), mysql_str)
}

# 客服

kdf = {
        table: df[table].loc[df[table].user_id == 124]
        for table in ['chat_session', "work_order_updated", "log"]
    }

# print(kdf["log"])

#
kdf['ori_chat_session'] = df.get("chat_session")
session_ids = list(set(kdf['chat_session']['sid'].values))

logs = df['chat_log']
kdf['chat_log'] = logs.loc[logs['sid'].isin(session_ids)]
kdf['question_tag'] = df['question_tag']

now = datetime.datetime.strptime("2018-05-19 00:00:00", "%Y-%m-%d %H:%M:%S")
company = StatisCompany(df, now).statistic()
from pprint import pprint
pprint(company)
