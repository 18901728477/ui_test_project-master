from mobile.mtrade_ui_test.mtrade_ui_test.data import WAIT_SELLER_SEND_GOODS_WITH_PRINT_HISTORY
from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import *


class SendGoodsPage:
    contact_myself_locator = ('and', (('attr=', ('text', '自己联系')),))  # 自己联系
    contact_online_locator = ('and', (('attr=', ('text', '在线下单')),))  # 在线下单
    without_contact_locator = ('and', (('attr=', ('text', '无需物流')),))  # 无需物流
    company_lab_locator = ('and', (('attr=', ('text', '快递公司')),))  # 快递公司
    now_button_locator = (
        'and', (('attr=', ('text', '立即发货')), ('attr=', ('name', 'android.widget.Button'))))  # 立即发货按钮
    input_number_lab_locator = ('and', (('attr=', ('text', '输入单号')),))  # 输入单号标签

    # 方法：获取快递公司
    def get_deliver_company(self):
        company_lab = init_element(self.company_lab_locator)
        company_info = locate_by_anchor(company_lab, parent_lv=2, child_lv='l1l0')
        return company_info.get_text()

    # 方法：获取快递单号
    def get_deliver_number(self):
        input_number_lab = init_element(self.input_number_lab_locator)
        express_number_text_box = input_number_lab.parent().parent().offspring('android.widget.EditText')
        return express_number_text_box.get_text()

    # 方法：检查订单的单号打印记录
    def check_order_print_history(self):
        ay_click(self.contact_myself_locator)
        print_history_info = get_order_print_history(WAIT_SELLER_SEND_GOODS_WITH_PRINT_HISTORY)
        does_print_record_right = True
        except_print_history_company = print_history_info['绑定的物流公司'][0]
        actual_print_history_company = self.get_deliver_company()
        except_print_history_no = print_history_info['绑定的单号'][0]
        actual_print_history_no = self.get_deliver_number()
        if actual_print_history_no != except_print_history_no or actual_print_history_company != except_print_history_company:
            does_print_record_right = False
        return does_print_record_right, except_print_history_company, actual_print_history_company, except_print_history_no, actual_print_history_no

    # 方法：获取自己联系、在线下单的默认物流
    def get_default_logistic(self):
        url = 'https://trade.aiyongbao.com/iytrade2/getSend'
        headers = {
            'User-Agent': 'python'
        }
        params = {
            'trade_source': 'TAO',
        }
        cookies = {'PHPSESSID': get_sessionId()}
        r = requests.get(url, params=params, headers=headers, cookies=cookies)
        default_logistic = {'自己联系默认物流': jsonpath.jsonpath(r.json(), '$..name')[0],
                            '在线下单默认物流': jsonpath.jsonpath(r.json(), '$..name')[1]}
        return default_logistic

    # 方法：检查默认物流是否正确
    def check_default_logistic(self):
        does_default_logistic_right = True
        # 检查自己联系的默认物流
        ay_click(self.delivery_contact_myself_locator)
        ay_click(self.change_logistics_company_locator)
        default_company = poco(name='android:id/select_dialog_listview').children()
        for i in range(0, len(default_company) - 1):
            actual_info = self.get_default_logistic()['自己联系默认物流']
            if x[i].get_text() in actual_info != True:
                does_default_logistic_right = False
        # 检查在线下单的默认物流
        ay_click(self.delivery_contact_online_locator)
        ay_click(self.change_logistics_company_locator)
        default_company = poco(name='android:id/select_dialog_listview').children()
        for i in range(0, len(default_company) - 1):
            actual_info = self.get_default_logistic()['在线下单默认物流']
            if x[i].get_text() in actual_info != True:
                does_default_logistic_right = False
        return does_default_logistic_right

    # 方法：自己联系物流
    def contact_myself(self):
        ay_click(self.contact_myself_locator)

    # 方法：在线下单物流
    def contact_online(self):
        ay_click(self.contact_online_locator)

    # 方法：无需物流
    def without_contact(self):
        ay_click(self.without_contact_locator)

    # 方法：自己联系，选择快递公司
    def choose_logistics_company_contact_myself(self, my_company):
        if my_company in self.get_default_logistic()['自己联系默认物流']:
            poco(text=my_company).click()
        else:
            poco(text='更多').click()
            poco(text=my_company).click()

    # 方法：在线下单，选择快递公司
    def choose_logistics_company_contact_online(self, my_company):
        if my_company in self.get_default_logistic()['在线下单默认物流']:
            poco(text=my_company).click()
        else:
            poco(text='更多').click()
            poco(text=my_company).click()

    # 方法：输入单号
    def enter_logistics_no(self, my_deliver_no):
        ay_set_text(self.order_number_text_box_locator, my_deliver_no)

    # 方法：点击扫码发货
    def scan_deliver(self):
        ay_click(self.get_delivery_number_by_scanning_locator)
        poco("com.taobao.qianniu:id/btn_album").click()
        poco("android.widget.FrameLayout").offspring("com.android.documentsui:id/drawer_layout").offspring(
            "com.android.documentsui:id/container_directoty").offspring(
            "com.android.documentsui:id/container_directory").offspring("com.android.documentsui:id/dir_list").child(
            "android.widget.RelativeLayout")[0].offspring("com.android.documentsui:id/icon_thumb").click()

    # 方法：点击立即发货按钮
    def push_deliver_button(self):
        ay_click(self.deliver_now_button_locator)

    def check_order_detail_deliver(self, order_no):
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        detail = self.get_order_detail_deliver(order_no)
        result = {}
        flag = True
        for k, v in detail.items():
            if v:
                if not isinstance(v, list):
                    if poco(text=str(v)).exists():  # 千牛工作台使用desc属性，小程序使用text属性,卖家昵称未显示，订单状态未显示，
                        result[k] = {'结果': '正确'}
                    else:
                        result[k] = {'结果': '错误', '期望值': v}
                        flag = False
                elif isinstance(v, list):
                    for x in v:
                        if poco(text=x).exists():  # 千牛工作台使用desc属性，小程序使用text属性,卖家昵称未显示，订单状态未显示，
                            result[k] = {'结果': '正确'}
                        else:
                            result[k] = {'结果': '错误', '期望值': x}
                            flag = False

        # 排除接口响应的地址里带有空格的干扰
        if result.get('收件地址').get('结果') == '错误':  # 如果地址信息有误
            print('收件地址结果错误！')
            print('地址页面获取：{}，接口获取：{}'.format(ay_get_text(self.address_info_locator).replace(' ', ''),
                                             result.get('收件地址').get('期望值')))
            if result.get('收件地址').get('期望值') == ay_get_text(self.address_info_locator).replace(' ',
                                                                                               ''):  # 页面显示的地址去除空格，再做一次校验
                print('收件地址结果修改为正确！')
                result['收件地址']['结果'] = '正确'  # 校验通过后，结果改为正确
            res = ''
            for k1, v1 in result.items():
                for k2, v2 in v1.items():
                    res = res + v2
            print('获取res结果：', res)
            flag2 = '错误' in res
            if flag2 is False:  # 取出result里，所有结果数据，不存在“错误”时，flag从False改为True
                print('所有结果都正确，flag改为True')
                flag = True
        return flag, result


if __name__ == '__main__':
    x = SendGoodsPage()
    r = x.check_order_print_history()
    print(r)
