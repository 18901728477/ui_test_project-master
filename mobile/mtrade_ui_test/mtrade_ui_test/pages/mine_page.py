from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import *
from time import sleep
from airtest.core.api import *
import requests
import jsonpath


class MinePage(BasePage):
    check_address_anchor = ('and', (('attr=', ('text', '核对地址短语')),))
    check_address_phase_anchor = ('and', (('attr=', ('text', '设为默认短语')),))
    auto_combine_button_anchor = ('and', (('attr=', ('text', '自动合并订单')),))
    default_logistic_locator = ('and', (('attr=', ('text', '常用物流')),))  # 常用物流

    # 方法：更改默认的核对地址短语
    def change_phrase(self):
        check_address_element = locate_by_anchor(init_element(self.check_address_anchor), 2, 'l1')
        check_address_element.click()
        third_phase_element = locate_by_anchor(init_element(self.check_address_phase_anchor), 5, 'v2v2v0v0l0')
        third_phase_element.click()
        self.back()

    # 方法：核对地址短语恢复默认第一项
    def recover_phrase(self):
        check_address_element = locate_by_anchor(init_element(self.check_address_anchor), 2, 'l1')
        check_address_element.click()
        first_phase_element = locate_by_anchor(init_element(self.check_address_phase_anchor), 5, 'v0v2v0v0l0')
        first_phase_element.click()
        self.back()

    # 方法：判断自动合单的开关状态
    def status_auto_combine(self):
        flag = True
        try:
            loop_find(Template(r"pic_data/tpl1581324272913.png", record_pos=(0.002, -0.388), resolution=(1080, 2340),
                               threshold=0.95))
        except:
            flag = False
        return flag

    # 方法：开启自动合单
    def open_auto_combine(self):
        auto_combine_button_element = locate_by_anchor(init_element(self.auto_combine_button_anchor), 2, 'l1')
        if self.status_auto_combine():
            pass
        else:
            auto_combine_button_element.click()

    # 方法：关闭自动合单
    def close_auto_combine(self):
        auto_combine_button_element = locate_by_anchor(init_element(self.auto_combine_button_anchor), 2, 'l1')
        if self.status_auto_combine():
            auto_combine_button_element.click()
        else:
            pass

    # 方法：获取自己联系、在线下单的默认物流
    def get_default_logistic(self):
        url = 'https://trade.aiyongbao.com/iytrade2/getSend'
        headers = {
            'User-Agent': 'python'
        }
        params = {
            'trade_source': 'TAO',
        }
        cookies = {'PHPSESSID': self.get_sessionId()}
        r = requests.get(url, params=params, headers=headers, cookies=cookies)
        default_logistic = {}
        default_logistic['自己联系默认物流'] = jsonpath.jsonpath(r.json(), '$..name')[0]
        default_logistic['在线下单默认物流'] = jsonpath.jsonpath(r.json(), '$..name')[1]
        return default_logistic

    # 方法：更改常用物流
    def change_default_logistic(self):
        element_click(self.default_logistic_locator)
        poco(text='安能物流').wait_for_appearance(5)
        poco(text="安能物流").parent().child()[0].click()
        poco(text='在线下单').click()
        poco(text="安能物流").parent().child()[0].click()
        poco(text='保存').click()
        self.back()

    # 方法：常用物流初始化
    def recover_default_logistic(self):
        poco(text='常用物流').click()
        poco(text='安能物流').wait_for_appearance(5)
        try:
            loop_find(Template(r"pic_data/tpl1581424887698.png", record_pos=(-0.001, -0.757), resolution=(1080, 2340),
                               threshold=0.95))
            poco(text="安能物流").parent().child()[0].click()
        except:
            pass
        poco(text='在线下单').click()
        try:
            loop_find(Template(r"pic_data/tpl1581424887698.png", record_pos=(-0.001, -0.757), resolution=(1080, 2340),
                               threshold=0.95))
            poco(text="安能物流").parent().child()[0].click()
        except:
            pass
        poco(text='保存').click()
        self.back()

    # 方法：订单检测设置恢复默认
    def recover_check_order(self):
        poco(text="订单检测设置").click()
        try:
            loop_find(Template(r"pic_data/tpl1581074983830.png", record_pos=(-0.001, -0.757), resolution=(1080, 2340),
                               threshold=0.95))
        except:
            poco(text='留言中包含有害信息，疑似诈骗').parent().child()[1].click()
        try:
            loop_find(Template(r"pic_data/tpl1581074992063.png", record_pos=(-0.008, -0.643), resolution=(1080, 2340),
                               threshold=0.95))
        except:
            poco(text='收货地址中包含敏感关键字').parent().child()[1].click()
        try:
            loop_find(Template(r"pic_data/tpl1581074998058.png", record_pos=(-0.001, -0.521), resolution=(1080, 2340),
                               threshold=0.95))
        except:
            poco(text='该买家给过你中差评').parent().child()[1].click()
        try:
            loop_find(Template(r"pic_data/tpl1581075003402.png", record_pos=(-0.002, -0.381), resolution=(1080, 2340),
                               threshold=0.95))
        except:
            poco(text='云黑名单中该买家发出的中差评数高于5个').parent().child()[1].click()
        poco(text='保存').click()
        self.back()

    def white_ww_operation(self):
        # poco(text='添加旺旺白名单').click()
        poco(text='买家旺旺').parent().offspring("android.widget.EditText")[0].set_text('自动白名单用户')
        poco(text='放行原因').parent().offspring("android.widget.EditText")[0].set_text('自动白名单用户添加原因')
        operation_name_status = {}
        if poco(text='自动白名单用户'):
            operation_name_status['add'] = True
        else:
            operation_name_status['add'] = False
        poco(text='自动白名单用户').parent().parent().offspring("android.widget.Button")[0].click()
        if poco(text='自动白名单用户'):
            operation_name_status['move'] = False
        else:
            operation_name_status['move'] = True
        return operation_name_status


if __name__ == '__main__':
    x = MinePage()
    x.white_ww_operation()
