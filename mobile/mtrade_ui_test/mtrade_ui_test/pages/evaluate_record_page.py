from time import sleep

from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import *
import requests

from mobile.mtrade_ui_test.mtrade_ui_test.pages.order_detail_page import OrderDetailPage


class EvaluateRecordPage(BasePage):

    records_to_be_executed_locator = ('and', (('attr=', ('text', '待执行记录')), ('attr=', ('name', 'android.view.View'))))  # 待执行记录
    failure_record_locator = ('and', (('attr=', ('text', '失败记录')), ('attr=', ('name', 'android.view.View'))))  # 失败记录
    success_record_locator = ('and', (('attr=', ('text', '成功记录')), ('attr=', ('name', 'android.view.View'))))  # 成功记录
    latest_record_card_locator = ('and', (('attr=', ('text', '订单编号')),))  # 最近的一次记录卡片
    latest_record_nick_locator = ('index', (('/', (('index', (('/', (('^', (('^', (('^', (('^', (('and', (('attr=', ('text', '订单编号')),)), ('and', ()))), ('and', ()))), ('and', ()))), ('and', ()))), ('and', ()))), 0)), ('and', ()))), 1)) # 最近一次记录的评价用户
    latest_record_orderid_locator = ('index', (('/', (('^', (('and', (('attr=', ('text', '订单编号')),)), ('and', ()))), ('and', ()))), 1))  # 最近一次记录的订单号
    latest_record_evaluate_time_locator = ('index', (('/', (('index', (('/', (('^', (('^', (('and', (('attr=', ('text', '订单编号')),)), ('and', ()))), ('and', ()))), ('and', ()))), 1)), ('and', ()))), 1))  # 最近一次记录的评价时间
    latest_failure_reason = ('/', (('index', (('/', (('^', (('^', (('^', (('^', (('and', (('attr=', ('text', '订单编号')),)), ('and', ()))), ('and', ()))), ('and', ()))), ('and', ()))), ('and', ()))), 2)), ('and', ()))) # 最近一次记录的失败原因

    # 方法：进入待执行记录列表
    def go_executed_list(self):
        ay_click(self.records_to_be_executed_locator)
        sleep(1)

    # 方法：进入成功记录列表
    def go_success_list(self):
        ay_click(self.success_record_locator)
        sleep(1)

    # 方法：进入失败记录列表
    def go_failure_list(self):
        ay_click(self.failure_record_locator)
        sleep(1)

    # 方法：获取列表下最新一条待执行记录的信息
    def get_latest_excited_record_info(self):
        record_info = {'nick': ay_get_text(self.latest_record_nick_locator),
                       'tid': ay_get_text(self.latest_record_orderid_locator),
                       'time': ay_get_text(self.latest_record_evaluate_time_locator)}
        return record_info

    # 方法：获取列表下最新一条成功记录的信息
    def get_latest_success_record_info(self):
        record_info = {'nick': ay_get_text(self.latest_record_nick_locator),
                       'tid': ay_get_text(self.latest_record_orderid_locator),
                       'time': ay_get_text(self.latest_record_evaluate_time_locator)}
        return record_info

    # 方法：获取列表下最新一条失败记录的信息
    def get_latest_failure_record_info(self):
        record_info = {'nick': ay_get_text(self.latest_record_nick_locator),
                       'tid': ay_get_text(self.latest_record_orderid_locator),
                       'time': ay_get_text(self.latest_record_evaluate_time_locator),
                       'reason': ay_get_text(self.latest_failure_reason)}
        return record_info

    # 方法：获取成功的评价记录
    def api_get_success_record(self):
        url = 'https://trade.aiyongbao.com/iytrade2/zdratelog'
        headers = {
            'User-Agent': 'python'
        }
        params = {
            'page': '1',
            'status': '1',
            'trade_source': 'TAO'
        }
        cookies = {'PHPSESSID': get_sessionId()}
        resp = requests.get(url, params=params, headers=headers, cookies=cookies)
        return resp.text

    # 方法：返回最新的一条成功的评价记录
    def api_get_latest_success_record(self):
        res_list = {}
        res = json.loads(self.api_get_success_record())['zdpj'][0]
        res_list['nick'] = res['buyer_nick']
        res_list['tid'] = res['tradeid']
        res_list['time'] = res['opttime']
        return res_list

    # 方法：获取所有失败的评价记录
    def api_get_fail_record(self):
        url = 'https://trade.aiyongbao.com/iytrade2/zdratelog'
        headers = {
            'User-Agent': 'python'
        }
        params = {
            'page': '1',
            'status': '0',
            'trade_source': 'TAO'
        }
        cookies = {'PHPSESSID': get_sessionId()}
        resp = requests.get(url, params=params, headers=headers, cookies=cookies)
        return resp.text
    
    # 方法：返回最新的一条失败的评价记录
    def api_get_latest_fail_record(self):
        res_list = {}
        res = json.loads(self.api_get_fail_record())['zdpj'][0]
        res_list['nick'] = res['buyer_nick']
        res_list['tid'] = res['tradeid']
        res_list['time'] = res['opttime']
        res_list['reason'] = res['content']
        return res_list

    # 方法：获取所有待执行的评价记录
    def api_get_to_be_excited_record(self):
        url = 'https://trade.aiyongbao.com/iytrade2/getevaluate'
        headers = {
            'User-Agent': 'python'
        }
        params = {
            'page': '1',
            'status': '0',
            'trade_source': 'TAO'
        }
        cookies = {'PHPSESSID': get_sessionId()}
        resp = requests.get(url, params=params, headers=headers, cookies=cookies)
        return resp.text
    
    # 方法：返回最新的一条待执行的评价记录
    def api_get_latest_to_be_excited_record(self):
        res_list = {}
        res = json.loads(self.api_get_to_be_excited_record())['zdpj'][0]
        res_list['nick'] = res['buyer_nick']
        res_list['tid'] = res['tid']
        res_list['time'] = res['optime']
        return res_list

    # 方法：进入列表下最新一条记录的订单详情页
    def go_order_detail(self):
        order_id = ay_get_text(self.latest_record_orderid_locator)
        ay_click(self.latest_record_card_locator)
        order_detail = OrderDetailPage()
        order_detail.self_check()
        return order_detail.check_order_no(order_id)


if __name__ == "__main__":
    x = EvaluateRecordPage()
    print(x.get_latest_success_record_info())
    # print(x.api_get_latest_to_be_excited_record())