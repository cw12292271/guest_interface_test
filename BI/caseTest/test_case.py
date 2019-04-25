import unittest

from BI.data.BI_KFKQ import *
from BI.data.BI_db import *
from .test_bi import *


class TestRobotData(unittest.TestCase):
    """机器人总览数据接口测试"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_robot_data(self):
        api_result0 = api_robot_pandect()['solve_data']
        api_result1 = api_robot_pandect()['matching_data']
        db_result = sql_historical_trend_data(sql_机器人数据)

        self.assertEqual(db_result['机器人接待量'], api_result0['robot_reception'], msg='机器人接待量 数据错误')
        self.assertEqual(db_result['机器人解决量'], api_result0['robot_solution'], msg='机器人解决量 数据错误')
        self.assertEqual(db_result['机器人未解决量'], api_result0['robot_to_human'], msg='机器人未解决量 数据错误')
        self.assertEqual(db_result['访客提问数'], api_result1['matched_questions'], msg='访客提问数 数据错误')
        self.assertEqual(db_result['匹配提问数'], api_result1['visitor_questions'], msg='匹配提问数 数据错误')

        for tr in range(len(api_result0['trend'])):
            self.assertEqual(db_result['trend'][tr]['机器人接待量'], api_result0['trend'][tr]['robot_reception'], msg='{} 机器人接待量 数据错误'.format(db_result['trend'][tr]['datetime']))
            self.assertEqual(db_result['trend'][tr]['机器人解决量'], api_result0['trend'][tr]['robot_solution'], msg='{} 机器人解决量 数据错误'.format(db_result['trend'][tr]['datetime']))
            self.assertEqual(db_result['trend'][tr]['机器人未解决量'], api_result0['trend'][tr]['robot_to_human'], msg='{} 机器人未解决量 数据错误'.format(db_result['trend'][tr]['datetime']))
            self.assertEqual(db_result['trend'][tr]['访客提问数'], api_result1['trend'][tr]['matched_questions'], msg='{} 访客提问数 数据错误'.format(db_result['trend'][tr]['datetime']))
            self.assertEqual(db_result['trend'][tr]['匹配提问数'], api_result1['trend'][tr]['visitor_questions'], msg='{} 匹配提问数 数据错误'.format(db_result['trend'][tr]['datetime']))


class TestServiceOverview(unittest.TestCase):
    """客服数据总览接口测试"""

    @classmethod
    def setUpClass(cls):
        cls.db_result1 = sql_historical_trend_data(sql_客服数据总览)
        cls.db_result2 = sql_historical_no_trend_data(sql_客服数据时长总览)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_service_turn_to_manual_reception(self):
        """客服总览-转人工数量"""

        api_result = api_kf_overview()['conversational_volume']
        db_result = self.db_result1

        self.assertEqual(db_result['转人工数量'], api_result['turn_to_manual_reception'], msg='转人工数量 数据错误')

        for tr in range(len(api_result['trend'])):
            self.assertEqual(db_result['trend'][tr]['转人工数量'], api_result['trend'][tr]['turn_to_manual_reception'], msg='{} 转人工数量 数据错误'.format(db_result['trend'][tr]['datetime']))

    def test_service_enter_queues_nums(self):
        """客服总览-进入排队人数"""

        api_result = api_kf_overview()['conversational_volume']
        db_result = self.db_result1

        self.assertEqual(db_result['进入排队人数'], api_result['enter_queues_nums'], msg='进入排队人数 数据错误')

    def test_service_access_session(self):
        """客服总览-接入会话量"""

        api_result = api_kf_overview()['conversational_volume']
        db_result = self.db_result1

        self.assertEqual(db_result['接入会话量'], api_result['access_session'], msg='接入会话量 数据错误')

        for tr in range(len(api_result['trend'])):
            self.assertEqual(db_result['trend'][tr]['接入会话量'], api_result['trend'][tr]['access_session'], msg='{} 接入会话量 数据错误'.format(db_result['trend'][tr]['datetime']))

    def test_service_reception_session(self):
        """客服总览-接待会话量"""

        api_result = api_kf_overview()['conversational_volume']
        db_result = self.db_result1


        self.assertEqual(db_result['接待会话量'], api_result['reception_session'], msg='接待会话量 数据错误')

        for tr in range(len(api_result['trend'])):
            self.assertEqual(db_result['trend'][tr]['接待会话量'], api_result['trend'][tr]['reception_session'], msg='{} 接待会话量 数据错误'.format(db_result['trend'][tr]['datetime']))

    def test_service_independent_reception(self):
        """客服总览-独立接待量"""

        api_result = api_kf_overview()['conversational_volume']
        db_result = self.db_result1

        self.assertEqual(db_result['独立接待量'], api_result['independent_reception'], msg='独立接待量 数据错误')

        for tr in range(len(api_result['trend'])):
            self.assertEqual(db_result['trend'][tr]['独立接待量'], api_result['trend'][tr]['independent_reception'], msg='{} 独立接待量 数据错误'.format(db_result['trend'][tr]['datetime']))

    def test_service_total_message(self):
        """客服总览-总消息量"""

        api_result = api_kf_overview()['message_quantity']
        db_result = self.db_result1

        self.assertEqual(db_result['总消息量'], api_result['total_message'], msg='总消息量 数据错误')

        for tr in range(len(api_result['trend'])):
            self.assertEqual(db_result['trend'][tr]['总消息量'], api_result['trend'][tr]['total_message'], msg='{} 总消息量 数据错误'.format(db_result['trend'][tr]['datetime']))

    def test_service_customer_information(self):
        """客服总览-客服消息量"""

        api_result = api_kf_overview()['message_quantity']
        db_result = self.db_result1

        self.assertEqual(db_result['客服消息量'], api_result['customer_information'], msg='客服消息量 数据错误')

        for tr in range(len(api_result['trend'])):
            self.assertEqual(db_result['trend'][tr]['客服消息量'], api_result['trend'][tr]['customer_information'], msg='{} 客服消息量 数据错误'.format(db_result['trend'][tr]['datetime']))

    def test_service_visitor_message(self):
        """客服总览-访客消息量"""

        api_result = api_kf_overview()['message_quantity']
        db_result = self.db_result1

        self.assertEqual(db_result['访客消息量'], api_result['visitor_message'], msg='访客消息量 数据错误')

        for tr in range(len(api_result['trend'])):
            self.assertEqual(db_result['trend'][tr]['访客消息量'], api_result['trend'][tr]['visitor_message'], msg='{} 访客消息量 数据错误'.format(db_result['trend'][tr]['datetime']))

    def test_service_session_length(self):
        """客服总览-平均会话时长"""

        api_result = api_kf_overview()['length_of_service']
        db_result = self.db_result2

        self.assertEqual(db_result['平均会话时长'], transform_second(api_result['average_session_length']), msg='平均会话时长 数据错误')
        self.assertEqual(db_result['会话时长大于8min'], percent_decimal(api_result['session_length'][0]['one']), msg='会话时长大于8min 数据错误')
        self.assertEqual(db_result['会话时长介于6min到8min'], percent_decimal(api_result['session_length'][1]['two']), msg='会话时长介于6min到8min 数据错误')
        self.assertEqual(db_result['会话时长介于4min到6min'], percent_decimal(api_result['session_length'][2]['three']), msg='会话时长介于4min到6min 数据错误')
        self.assertEqual(db_result['会话时长介于2min到4min'], percent_decimal(api_result['session_length'][3]['four']), msg='会话时长介于2min到4min 数据错误')
        self.assertEqual(db_result['会话时长小于等于2min'], percent_decimal(api_result['session_length'][4]['five']), msg='会话时长小于等于2min 数据错误')

    def test_service_first_response_time(self):
        """客服总览-平均首次响应时长"""

        api_result = api_kf_overview()['length_of_service']
        db_result = self.db_result2

        self.assertEqual(db_result['平均首次响应时长'], transform_second(api_result['average_first_response_time']), msg='平均首次响应时长 数据错误')
        self.assertEqual(db_result['首次响应时长大于1min占比'], percent_decimal(api_result['first_response_time'][0]['one']), msg='平均首次响应时长大于1min占比 数据错误')
        self.assertEqual(db_result['首次响应时长介于45s到1min占比'], percent_decimal(api_result['first_response_time'][1]['two']), msg='平均首次响应时长介于45s到1min占比 数据错误')
        self.assertEqual(db_result['首次响应时长介于30s到45s占比'], percent_decimal(api_result['first_response_time'][2]['three']), msg='平均首次响应时长介于30s到45s占比 数据错误')
        self.assertEqual(db_result['首次响应时长介于15s到30s占比'], percent_decimal(api_result['first_response_time'][3]['four']), msg='平均首次响应时长介于15s到30s占比 数据错误')
        self.assertEqual(db_result['首次响应时长小于等于15s占比'], percent_decimal(api_result['first_response_time'][4]['five']), msg='平均首次响应时长小于等于15s占比 数据错误')

    def test_service_response_time_length(self):
        """客服总览-平均首次响应时长"""

        api_result = api_kf_overview()['length_of_service']
        db_result = self.db_result2

        self.assertEqual(db_result['平均响应时长'], transform_second(api_result['average_response_time_length']), msg='平均响应时长 数据错误')
        self.assertEqual(db_result['响应时长大于1min占比'], percent_decimal(api_result['response_time'][0]['one']), msg='响应时长大于1min占比 数据错误')
        self.assertEqual(db_result['响应时长介于45s到1min占比'], percent_decimal(api_result['response_time'][1]['two']), msg='响应时长介于45s到1min占比 数据错误')
        self.assertEqual(db_result['响应时长介于30s到45s占比'], percent_decimal(api_result['response_time'][2]['three']), msg='响应时长介于30s到45s占比 数据错误')
        self.assertEqual(db_result['响应时长介于15s到30s占比'], percent_decimal(api_result['response_time'][3]['four']), msg='响应时长介于15s到30s占比 数据错误')
        self.assertEqual(db_result['响应时长小于等于15s占比'], percent_decimal(api_result['response_time'][4]['five']), msg='响应时长小于等于15s占比 数据错误')


class TestServiceWorkload(unittest.TestCase):
    """客服工作量接口测试"""

    @classmethod
    def setUpClass(cls):
        cls.db_result = sql_historical_no_trend_data(sql_客服工作量)
        cls.api_result = api_kf_work_load()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_access_session(self):
        """接入会话量"""

        db_result = self.db_result
        api_result = self.api_result

        self.assertEqual(db_result['接入会话量'], api_result['access_session'], msg='接入会话量 数据错误')

    def test_reception_session(self):
        """接待会话量"""

        db_result = self.db_result
        api_result = self.api_result

        self.assertEqual(db_result['接待会话量'], api_result['reception_session'], msg='接待会话量 数据错误')

    def test_independent_reception(self):
        """独立接待量"""

        db_result = self.db_result
        api_result = self.api_result

        self.assertEqual(db_result['独立接待量'], api_result['independent_reception'], msg='独立接待量 数据错误')

    def test_non_reception_session(self):
        """未接待会话量"""

        db_result = self.db_result
        api_result = self.api_result

        self.assertEqual(db_result['接入会话量'] - db_result['接待会话量'], api_result['non_reception_session'] , msg='未接待会话量 数据错误')

    def test_first_response_timeout_session(self):
        """首次未响应会话量"""

        db_result = self.db_result
        api_result = self.api_result

        self.assertEqual(db_result['首次未响应会话量'], api_result['first_response_timeout_session'], msg='首次未响应会话量 数据错误')

    def test_invalid_session(self):
        """无效会话量"""

        db_result = self.db_result
        api_result = self.api_result

        self.assertEqual(db_result['接入会话量'] - db_result['有效会话量'], api_result['invalid_session'], msg='无效会话量 数据错误')

    def test_end_session(self):
        """结束会话量"""

        db_result = self.db_result
        api_result = self.api_result

        self.assertEqual(db_result['结束会话量'], api_result['end_session'], msg='结束会话量 数据错误')

    def test_active_transfer(self):
        """主动转接量"""

        db_result = self.db_result
        api_result = self.api_result

        self.assertEqual(db_result['主动转接量'], api_result['active_transfer'], msg='主动转接量 数据错误')

    def test_active_session(self):
        """主动会话量"""

        db_result = self.db_result
        api_result = self.api_result

        self.assertEqual(db_result['主动会话量'], api_result['active_session'], msg='主动会话量 数据错误')


class TestServiceQualityOfWork(unittest.TestCase):
    """客服工作质量接口测试"""

    @classmethod
    def setUpClass(cls):
        cls.db_result = sql_historical_no_trend_data(sql_客服工作质量)
        cls.api_result = api_kf_quality_work()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_average_first_response_time(self):
        """平均首次响应时长"""

        db_result = self.db_result
        api_result = self.api_result

        self.assertEqual(db_result['平均首次响应时长'], transform_second(api_result['average_first_response_time']), msg='平均首次响应时长 数据错误')

    def test_average_response_time_length(self):
        """平均响应时长"""

        db_result = self.db_result
        api_result = self.api_result

        self.assertEqual(db_result['平均响应时长'], transform_second(api_result['average_response_time_length']), msg='平均响应时长 数据错误')

    def test_response_rate(self):
        """客服30秒应答率"""

        db_result = self.db_result
        api_result = self.api_result

        self.assertEqual(float('%.4f' % float(db_result['客服30秒应答率'])), percent_decimal(api_result['response_rate']), msg='客服30秒应答率 数据错误')

    def test_length_of_reception(self):
        """接待总时长"""

        db_result = self.db_result
        api_result = self.api_result

        self.assertEqual(db_result['接待总时长'], transform_second(api_result['length_of_reception']), msg='接待总时长 数据错误')

    def test_average_length_of_reception(self):
        """平均接待时长"""

        db_result = self.db_result
        api_result = self.api_result

        self.assertEqual(db_result['平均接待时长'], transform_second(api_result['average_length_of_reception']), msg='平均接待时长 数据错误')

    def test_customer_service_information(self):
        """客服消息量"""

        db_result = self.db_result
        api_result = self.api_result

        self.assertEqual(db_result['客服消息量'], api_result['customer_service_information'], msg='客服消息量 数据错误')

    def test_answer_to_question_ratio(self):
        """答问比"""

        db_result = self.db_result
        api_result = self.api_result

        self.assertEqual(float('%.4f' % float(db_result['客服消息量']/db_result['访客消息量'])), percent_decimal(api_result['answer_to_question_ratio']), msg='答问比 数据错误')

    def test_one_time_resolution_rate(self):
        """一次性解决量"""

        db_result = self.db_result
        api_result = self.api_result

        self.assertEqual(db_result['一次性解决量'], percent_decimal(api_result['one-time_resolution_rate']), msg='一次性解决量 数据错误')

    def test_rate_of_comment(self):
        """参评率"""

        db_result = self.db_result
        api_result = self.api_result

        self.assertEqual(float('%.4f' % float(db_result['参评率'])), percent_decimal(api_result['rate_of_comment']), msg='参评率 数据错误')

    def test_satisfaction_very_satisfied(self):
        """非常满意数"""

        db_result = self.db_result
        api_result = self.api_result

        self.assertEqual(db_result['非常满意'], api_result['satisfaction']['very_satisfied'], msg='非常满意数 数据错误')

    def test_satisfaction_satisfied(self):
        """满意数"""

        db_result = self.db_result
        api_result = self.api_result

        self.assertEqual(db_result['满意'], api_result['satisfaction']['satisfied'], msg='满意数 数据错误')

    def test_satisfaction_comment(self):
        """一般数"""

        db_result = self.db_result
        api_result = self.api_result

        self.assertEqual(db_result['一般'], api_result['satisfaction']['commonly'], msg='一般数 数据错误')

    def test_satisfaction_dissatisfied(self):
        """不满意数"""

        db_result = self.db_result
        api_result = self.api_result

        self.assertEqual(db_result['不满意'], api_result['satisfaction']['dissatisfied'], msg='不满意数 数据错误')

    def test_satisfaction_very_dissatisfied(self):
        """非常不满意数"""

        db_result = self.db_result
        api_result = self.api_result

        self.assertEqual(db_result['非常不满意'], api_result['satisfaction']['very_dissatisfied'], msg='非常不满意数 数据错误')


class TestAttendanceOfService(unittest.TestCase):
    """客服考勤信息接口测试"""

    @classmethod
    def setUpClass(cls):
        cls.db_result = statustimes(sql_客服考勤_状态)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_login_time(self):
        """客服考勤状态时长"""

        api_result = api_kf_attendance()
        db_result = self.db_result

        self.assertEqual(db_result['登录总时长'], api_result['登录总时长'], msg="登录总时长 数据错误")

    def test_reception_time(self):
        """客服考勤状态时长"""

        api_result = api_kf_attendance()
        db_result = self.db_result

        self.assertEqual(db_result['可接待总时长'], api_result['可接待总时长'], msg="可接待总时长 数据错误")

    def test_online_time(self):
        """客服考勤状态时长"""

        api_result = api_kf_attendance()
        db_result = self.db_result

        self.assertEqual(db_result['在线总时长'], api_result['在线总时长'], msg="在线总时长 数据错误")

    def test_service_time(self):
        """客服考勤服务时长"""

        api_result = api_kf_attendance()
        db_result = servicetimes(sql_客服考勤_服务)

        self.assertEqual(db_result['服务总时长'], api_result['服务总时长'], msg="服务总时长 数据错误")


class TestVistorData(unittest.TestCase):
    """访客数据接口测试"""

    @classmethod
    def setUpClass(cls):
        cls.db_result = visitordata(sql_访客)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_visitors_visit(self):
        """访客来访情况测试"""

        api_result = api_visitor_overview()['visitors_visit']
        db_result = self.db_result

        self.assertEqual(db_result['访问量'], api_result['amount_of_access'], msg='访问量 数据错误')
        self.assertEqual(db_result['新访客'], api_result['new_visitor'], msg='新访客 数据错误')
        self.assertEqual(db_result['老访客'], api_result['old_visitors'], msg='老访客 数据错误')


    def test_visitor_channel(self):
        """访客来访情况测试"""

        db_result = self.db_result
        api_result = {}
        api_result0 = api_visitor_overview()['visitor_channel']
        for ar in api_result0:
            api_result[ar['channel']] = ar['num']

        self.assertEqual(db_result['微信访客'], api_result['微信'], msg='微信访客 数据错误')
        self.assertEqual(db_result['网页访客'], api_result['网页'], msg='网页访客 数据错误')


    def test_visitor_satisfaction(self):
        """访客满意度情况测试"""

        db_result = self.db_result
        api_result = {}
        api_result0 = api_visitor_overview()['satisfaction']
        for ar in api_result0:
            api_result[ar['degree']] = ar['num']

        self.assertEqual(db_result['非常满意'], api_result['非常满意'], msg='非常满意 数据错误')
        self.assertEqual(db_result['满意'], api_result['满意'], msg='满意 数据错误')
        self.assertEqual(db_result['一般'], api_result['一般'], msg='一般 数据错误')
        self.assertEqual(db_result['不满意'], api_result['不满意'], msg='不满意 数据错误')
        self.assertEqual(db_result['非常不满意'], api_result['非常不满意'], msg='非常不满意 数据错误')


    def test_visitor_distribution(self):
        """访客分布情况测试"""

        api_result = api_visitor_overview()
        api_result0 = api_result['visitor_source']
        api_result1 = api_result['visitor_nums']
        api_result2 = api_result['visitor_access']
        db_result = visitordistributiondata(sql_访客分布)

        if api_result0[-1]['source'] == '其它':
            api_result0.pop()
        for ar0 in api_result0:
            self.assertEqual(db_result['访客来源'][ar0['source']], ar0['amount_of_access'], msg='{} 数据错误'.format(ar0['source']))

        for ar1 in api_result1:
            if ar1['province'] == '未识别来源':
                api_result1.remove(ar1)
                break
            self.assertEqual(db_result['访客地域'][ar1['province']], ar1['amount_of_access'], msg='{} 数据错误'.format(ar1['province']))

        for ar2 in api_result2:
            if ar2['province'] == '未识别来源':
                api_result2.remove(ar2)
                break
            self.assertEqual(db_result['访问量地域'][ar2['province']], ar2['amount_of_access'], msg='{} 数据错误'.format(ar2['province']))


class TestServiceDetails(unittest.TestCase):
    """客服详情接口测试"""

    @classmethod
    def setUpClass(cls):
        cls.db_result_trend = sql_historical_trend_data(sql_客服详情_趋势)
        cls.db_result_no_trend = sql_historical_no_trend_data(sql_客服详情_非趋势)
        cls.api_result = api_kf_work_load_details()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_service_access_session(self):
        """客服详情-接入会话量"""

        api_result = self.api_result['conversational_volume']
        db_result = self.db_result_trend

        self.assertEqual(db_result['接入会话量'], api_result['access_session'], msg='接入会话量 数据错误')

        for tr in range(len(api_result['trend'])):
            self.assertEqual(db_result['trend'][tr]['接入会话量'], api_result['trend'][tr]['access_session'], msg='{} 接入会话量 数据错误'.format(db_result['trend'][tr]['datetime']))

    def test_service_reception_session(self):
        """客服详情-接待会话量"""

        api_result = self.api_result['conversational_volume']
        db_result = self.db_result_trend


        self.assertEqual(db_result['接待会话量'], api_result['reception_session'], msg='接待会话量 数据错误')

        for tr in range(len(api_result['trend'])):
            self.assertEqual(db_result['trend'][tr]['接待会话量'], api_result['trend'][tr]['reception_session'], msg='{} 接待会话量 数据错误'.format(db_result['trend'][tr]['datetime']))

    def test_service_independent_reception(self):
        """客服详情-独立接待量"""

        api_result = self.api_result['conversational_volume']
        db_result = self.db_result_trend

        self.assertEqual(db_result['独立接待量'], api_result['independent_reception'], msg='独立接待量 数据错误')

        for tr in range(len(api_result['trend'])):
            self.assertEqual(db_result['trend'][tr]['独立接待量'], api_result['trend'][tr]['independent_reception'], msg='{} 独立接待量 数据错误'.format(db_result['trend'][tr]['datetime']))

    def test_service_non_reception_session(self):
        """客服详情-未接待会话量"""

        api_result = self.api_result['conversational_volume']
        db_result = self.db_result_trend


        self.assertEqual(db_result['接入会话量'] - db_result['接待会话量'], api_result['non_reception_session'], msg='接待会话量 数据错误')

        for tr in range(len(api_result['trend'])):
            self.assertEqual(db_result['trend'][tr]['接入会话量'] - db_result['trend'][tr]['接待会话量'], api_result['trend'][tr]['non_reception_session'], msg='{} 接待会话量 数据错误'.format(db_result['trend'][tr]['datetime']))

    def test_invalid_session(self):
        """无效会话量"""

        db_result = self.db_result_no_trend
        api_result = self.api_result['conversational_volume']

        self.assertEqual(db_result['接入会话量'] - db_result['有效会话量'], api_result['invalid_session'], msg='无效会话量 数据错误')

    def test_end_session(self):
        """结束会话量"""

        db_result = self.db_result_no_trend
        api_result = self.api_result['conversational_volume']

        self.assertEqual(db_result['结束会话量'], api_result['end_session'], msg='结束会话量 数据错误')

    def test_active_transfer(self):
        """主动转接量"""

        db_result = self.db_result_no_trend
        api_result = self.api_result['conversational_volume']

        self.assertEqual(db_result['主动转接量'], api_result['active_transfer'], msg='主动转接量 数据错误')

    def test_active_session(self):
        """主动会话量"""

        db_result = self.db_result_no_trend
        print()
        api_result = self.api_result['conversational_volume']

        self.assertEqual(db_result['主动会话量'], api_result['active_session'], msg='主动会话量 数据错误')

    def test_customer_information(self):
        """客服消息量"""

        db_result = self.db_result_trend
        api_result = self.api_result['message_quantity']

        self.assertEqual(db_result['客服消息量'], api_result['customer_information'], msg='客服消息量 数据错误')
        for tr in range(len(api_result['trend'])):
            self.assertEqual(db_result['trend'][tr]['客服消息量'], api_result['trend'][tr]['customer_information'], msg='{} 客服消息量 数据错误'.format(db_result['trend'][tr]['datetime']))

    def test_visitor_message(self):
        """访客消息量"""

        db_result = self.db_result_trend
        api_result = self.api_result['message_quantity']

        self.assertEqual(db_result['访客消息量'], api_result['visitor_message'], msg='客服消息量 数据错误')
        for tr in range(len(api_result['trend'])):
            self.assertEqual(db_result['trend'][tr]['访客消息量'], api_result['trend'][tr]['visitor_message'], msg='{} 访客消息量 数据错误'.format(db_result['trend'][tr]['datetime']))

    def test_total_message(self):
        """总消息量"""

        db_result = self.db_result_trend
        api_result = self.api_result['message_quantity']

        self.assertEqual(db_result['客服消息量'] + db_result['访客消息量'], api_result['total_message'], msg='总消息量 数据错误')
        for tr in range(len(api_result['trend'])):
            self.assertEqual(db_result['trend'][tr]['客服消息量'] + db_result['trend'][tr]['访客消息量'], api_result['trend'][tr]['total_message'], msg='{} 总消息量 数据错误'.format(db_result['trend'][tr]['datetime']))

    def test_answer_to_question_ratio(self):
        """答问比"""

        db_result = self.db_result_trend
        api_result = self.api_result['message_quantity']
        try:
            self.assertEqual(float('%.4f' % float(db_result['客服消息量']/db_result['访客消息量'])), percent_decimal(api_result['answer_to_question_ratio']), msg='答问比 数据错误')
        except ZeroDivisionError:
            self.assertEqual('--', percent_decimal(api_result['answer_to_question_ratio']), msg='答问比 数据错误')

        for tr in range(len(api_result['trend'])):
            try:
                self.assertEqual(float('%.4f' % float(db_result['trend'][tr]['客服消息量']/db_result['trend'][tr]['访客消息量'])), percent_decimal(api_result['trend'][tr]['answer_to_question_ratio']), msg='{} 答问比 数据错误'.format(db_result['trend'][tr]['datetime']))
            except ZeroDivisionError:
                self.assertEqual('--', api_result['trend'][tr]['answer_to_question_ratio'], msg='{} 答问比 数据错误'.format(db_result['trend'][tr]['datetime']))

    def test_average_length_of_reception(self):
        """客服详情-平均接待接待时长"""

        db_result = self.db_result_no_trend
        api_result = self.api_result['length_of_service']

        self.assertEqual(db_result['平均接待时长'], transform_second(api_result['average_length_of_reception']), msg='平均接待时长 数据错误')
        self.assertEqual(float(db_result['接待时长大于8min']), percent_decimal(api_result['length_of_reception'][0]['one']), msg='接待时长大于8min 数据错误')
        self.assertEqual(float(db_result['接待时长介于6min到8min']), percent_decimal(api_result['length_of_reception'][1]['two']), msg='接待时长介于6min到8min 数据错误')
        self.assertEqual(float(db_result['接待时长介于4min到6min']), percent_decimal(api_result['length_of_reception'][2]['three']), msg='接待时长介于4min到6min 数据错误')
        self.assertEqual(float(db_result['接待时长介于2min到4min']), percent_decimal(api_result['length_of_reception'][3]['four']), msg='接待时长介于2min到4min 数据错误')
        self.assertEqual(float(db_result['接待时长小于等于2min']), percent_decimal(api_result['length_of_reception'][4]['five']), msg='接待时长小于等于2min 数据错误')

    def test_service_first_response_time(self):
        """客服详情-平均首次响应时长"""

        db_result = self.db_result_no_trend
        api_result = self.api_result['length_of_service']

        self.assertEqual(db_result['平均首次响应时长'], transform_second(api_result['average_first_response_time']), msg='平均首次响应时长 数据错误')
        self.assertEqual(float(db_result['首次响应时长大于1min占比']), percent_decimal(api_result['first_response_time'][0]['one']), msg='平均首次响应时长大于1min占比 数据错误')
        self.assertEqual(float(db_result['首次响应时长介于45s到1min占比']), percent_decimal(api_result['first_response_time'][1]['two']), msg='平均首次响应时长介于45s到1min占比 数据错误')
        self.assertEqual(float(db_result['首次响应时长介于30s到45s占比']), percent_decimal(api_result['first_response_time'][2]['three']), msg='平均首次响应时长介于30s到45s占比 数据错误')
        self.assertEqual(float(db_result['首次响应时长介于15s到30s占比']), percent_decimal(api_result['first_response_time'][3]['four']), msg='平均首次响应时长介于15s到30s占比 数据错误')
        self.assertEqual(float(db_result['首次响应时长小于等于15s占比']), percent_decimal(api_result['first_response_time'][4]['five']), msg='平均首次响应时长小于等于15s占比 数据错误')

    def test_service_response_time_length(self):
        """客服详情-平均响应时长"""

        db_result = self.db_result_no_trend
        api_result = self.api_result['length_of_service']

        self.assertEqual(db_result['平均响应时长'], transform_second(api_result['average_response_time_length']), msg='平均响应时长 数据错误')
        self.assertEqual(float(db_result['响应时长大于1min占比']), percent_decimal(api_result['response_time'][0]['one']), msg='响应时长大于1min占比 数据错误')
        self.assertEqual(float(db_result['响应时长介于45s到1min占比']), percent_decimal(api_result['response_time'][1]['two']), msg='响应时长介于45s到1min占比 数据错误')
        self.assertEqual(float(db_result['响应时长介于30s到45s占比']), percent_decimal(api_result['response_time'][2]['three']), msg='响应时长介于30s到45s占比 数据错误')
        self.assertEqual(float(db_result['响应时长介于15s到30s占比']), percent_decimal(api_result['response_time'][3]['four']), msg='响应时长介于15s到30s占比 数据错误')
        self.assertEqual(float(db_result['响应时长小于等于15s占比']), percent_decimal(api_result['response_time'][4]['five']), msg='响应时长小于等于15s占比 数据错误')

    def test_problem_solving_rate(self):
        """客服详情-问题解决率"""

        db_result = self.db_result_no_trend
        api_result = self.api_result['problem_solving_rate']

        self.assertEqual(db_result['已解决'], api_result['resolved'], msg='已解决 数据错误')
        self.assertEqual(db_result['未解决'], api_result['unsolved'], msg='未解决 数据错误')

    def test_rate_of_comment(self):
        """参评率"""

        db_result = self.db_result_no_trend
        api_result = self.api_result['satisfaction']
        for ar in api_result:
            if ar['degree'] == '参评率':
                api_res = ar['ratio']
        try:
            self.assertEqual(float('%.4f' % float(db_result['参评率'])), percent_decimal(api_res), msg='参评率 数据错误')
        except ZeroDivisionError:
            self.assertEqual('--', api_res, msg='参评率 数据错误')

    def test_satisfaction_very_satisfied(self):
        """非常满意数"""

        db_result = self.db_result_no_trend
        api_result = self.api_result['satisfaction']
        for ar in api_result:
            if ar['degree'] == '非常满意':
                api_res = ar['num']

        self.assertEqual(float('%.4f' % float(db_result['非常满意'])), api_res, msg='非常满意 数据错误')

    def test_satisfaction_satisfied(self):
        """满意数"""

        db_result = self.db_result_no_trend
        api_result = self.api_result['satisfaction']
        for ar in api_result:
            if ar['degree'] == '满意':
                api_res = ar['num']

        self.assertEqual(float('%.4f' % float(db_result['满意'])), api_res, msg='满意 数据错误')

    def test_satisfaction_comment(self):
        """一般数"""

        db_result = self.db_result_no_trend
        api_result = self.api_result['satisfaction']
        for ar in api_result:
            if ar['degree'] == '一般':
                api_res = ar['num']

        self.assertEqual(float('%.4f' % float(db_result['一般'])), api_res, msg='一般 数据错误')

    def test_satisfaction_dissatisfied(self):
        """不满意数"""

        db_result = self.db_result_no_trend
        api_result = self.api_result['satisfaction']
        for ar in api_result:
            if ar['degree'] == '不满意':
                api_res = ar['num']

        self.assertEqual(float('%.4f' % float(db_result['不满意'])), api_res, msg='满意 数据错误')

    def test_satisfaction_very_dissatisfied(self):
        """非常不满意数"""

        db_result = self.db_result_no_trend
        api_result = self.api_result['satisfaction']
        for ar in api_result:
            if ar['degree'] == '非常不满意':
                api_res = ar['num']

        self.assertEqual(float('%.4f' % float(db_result['非常不满意'])), api_res, msg='非常不满意 数据错误')
