import jsonpath
from airtest.core.api import *
from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import BasePage, poco, init_element, locate_by_anchor, get_text_of_view, ay_click, \
    get_seller_address
import time


class MyPage(BasePage):
    remarks_phrase_locator = ('and', (('attr=', ('text', '备注短语')),))
    evaluation_phrase_locator = ('and', (('attr=', ('text', '评价短语')),))
    reminder_phrase_locator = ('and', (('attr=', ('text', '催付短语')),))
    default_reminder_locator = ('and', (('attr=', ('text', '默认催付短语')),))
    recommended_phrase_locator = ('and', (('attr=', ('text', '推荐短语')),))
    check_address_phrases_locator = ('and', (('attr=', ('text', '核对地址短语')),))
    seller_address_library_locator = ('and', (('attr=', ('text', '卖家地址库')),))
    common_logistics_locator = ('and', (('attr=', ('text', '常用物流')),))
    order_checking_setup_locator = ('and', (('attr=', ('text', '订单检测设置')),))
    add_text_locator = ('and', (('attr=', ('text', '请输入您的自定义短语')),))
    preservation_locator = ('and', (('attr=', ('text', '保存')),))
    message_detection_locator = ('and', (('attr=', ('text', '留言中包含有害信息，疑似诈骗')),))
    receiving_address_detection_locator = ('and', (('attr=', ('text', '收货地址中包含敏感关键字')),))
    negative_comment_diagnosis_locator = ('and', (('attr=', ('text', '该买家给过你中差评')),))
    cloud_blacklist_detection_locator = ('and', (('attr=', ('text', '云黑名单中该买家发出的中差评数高于5个')),))
    check_address_anchor = ('and', (('attr=', ('text', '核对地址短语')),))
    check_address_phase_anchor = ('and', (('attr=', ('text', '设为默认短语')),))
    auto_combine_button_anchor = ('and', (('attr=', ('text', '自动合并订单')),))
    default_logistic_locator = ('and', (('attr=', ('text', '常用物流')),))  # 常用物流
    version_number_locator = ('and', (('attr.*=', ('text', '版本号.*')),))  # 版本号

    # 方法：更改默认的核对地址短语
    def change_phrase(self, index=0):
        check_address_element = locate_by_anchor(init_element(self.check_address_anchor), 2, 'l1')
        check_address_element.click()
        poco(text='设为默认短语')[1].click()
        self.refresh()

    # 方法：核对地址短语恢复默认第一项
    def recover_phrase(self):
        check_address_element = locate_by_anchor(init_element(self.check_address_anchor), 2, 'l1')
        check_address_element.click()
        first_phase_element = locate_by_anchor(init_element(self.check_address_phase_anchor), 5, 'v0v2v0v0l0')
        first_phase_element.click()
        self.refresh()

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
        ay_click(self.default_logistic_locator)
        poco(text="安能物流").parent().child()[0].click()
        poco(text='在线下单').click()
        poco(text="安能物流").parent().child()[0].click()
        poco(text='保存').click()
        self.back()

    # 方法：常用物流初始化
    def recover_default_logistic(self):
        poco(text='常用物流').click()
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

    # 前往备注短语
    def to_remarks(self):
        remarks_button = init_element(self.remarks_phrase_locator)
        remarks_button.click()

    # 默认备注短语是否存在
    def default_remarks(self):
        a = poco(text='缺货').exists()
        b = poco(text='周末不收货').exists()
        c = poco(text='发EMS').exists()
        d = poco(text='老客户').exists()
        e = poco(text='送赠品').exists()
        default_remarks = {'缺货': a, '周末不收货': b, '发EMS': c, '老客户': d, '送赠品': e}
        if a and b and c and d and e:
            return True, default_remarks
        else:
            return False, default_remarks

    # 备注短语添加\删除\修改
    def add_del_refresh_remarks(self):
        sure_button = init_element(self.preservation_locator)
        poco(text='新建').click()
        text_edit = init_element(self.preservation_locator)
        text_edit = locate_by_anchor(text_edit, parent_lv=2, child_lv='l0').offspring("android.widget.EditText")[0]
        text_edit.set_text('新增的备注短语')
        sure_button.click()
        time.sleep(1)
        results = {}
        results['添加备注短语'] = poco(text='新增的备注短语').exists()
        poco(text='新增的备注短语').click()
        text_edit.invalidate()
        text_edit.set_text(str(text_edit.get_text()) + '修改内容')
        sure_button.click()
        results['修改结果'] = poco(text='新增的备注短语修改内容').exists()
        poco(text='新增的备注短语修改内容').click()
        text_edit.invalidate()
        if text_edit.get_text() == '新增的备注短语修改内容':
            results['信息校验'] = True
        else:
            results['信息校验'] = False
        poco(text='删除').click()
        poco(text='确认').click()
        if poco(text='新增的备注短语修改内容').exists():
            results['删除结果'] = False
        else:
            results['删除结果'] = True

        return results

    # 前往评价短语
    def to_evaluation(self):
        evaluation_button = init_element(self.evaluation_phrase_locator)
        evaluation_button.click()

    # 默认评价短语是否存在
    def default_evaluation(self):
        a = poco(text='谢谢，很好的买家！').exists()
        b = poco(text='谢谢，欢迎下次惠顾小店！').exists()
        c = poco(text='谢谢亲的支持！欢迎下次惠顾！').exists()
        d = poco(text='期待您的下次光临，我们会做得更好！').exists()
        e = poco(text='谢谢您的光临，新款随时上请继续关注小店！').exists()
        if a and b and c and d and e:
            return True
        else:
            return False

    # 前往催付短语
    def to_reminder(self):
        reminder_button = init_element(self.reminder_phrase_locator)
        reminder_button.click()

    # 获取默认催付短语内容
    def get_default_reminder(self):
        news = init_element(self.default_reminder_locator)
        default_news = locate_by_anchor(news, parent_lv=4, child_lv='v0')
        default_news = get_text_of_view(default_news)
        return default_news

    # 选择第一条默认催付短语
    def choice_first_default_reminder(self):
        new = init_element(self.recommended_phrase_locator)
        # 第一条短语的选择按钮
        change_one = locate_by_anchor(new, parent_lv=2, child_lv='v1v2v0v0l0')
        change_one.click()
        chang_one_text = locate_by_anchor(change_one, parent_lv=4, child_lv='v0')
        chang_one_text = get_text_of_view(chang_one_text)
        return chang_one_text

    # 选择第二条默认催付短语
    def choice_second_default_reminder(self):
        new = init_element(self.recommended_phrase_locator)
        # 第二条短语的选择按钮
        chang_two = locate_by_anchor(new, parent_lv=2, child_lv='v2v2v0v0l0')
        chang_two.click()
        chang_two_text = locate_by_anchor(chang_two, parent_lv=4, child_lv='v0')
        chang_two_text = get_text_of_view(chang_two_text)
        return chang_two_text

    # 前往卖家地址库
    def to_seller_address(self):
        seller_address_button = init_element(self.seller_address_library_locator)
        seller_address_button.click()

    def add_seller_address(self):
        pass

    # 检查淘宝接口地址是否存在
    @staticmethod
    def check_address():
        news = get_seller_address()
        results = {'name': True, 'address': True, 'phone': True}
        for i in news[0]:
            results['name'] = poco(text=i) and results['name']
        for i in news[1]:
            results['address'] = poco(text=i) and results['name']
        for i in news[2]:
            results['phone'] = poco(text=i) and results['name']
        return results

    # 前往订单检测设置

    def to_order_checking(self):
        order_checking_button = init_element(self.order_checking_setup_locator)
        order_checking_button.click()

    # 留言检测
    def message_detection(self):
        button = init_element(self.message_detection_locator)
        locate_by_anchor(button, parent_lv=1, child_lv='l1').click()

    # 收货地址检测
    def receiving_address_detection(self):
        button = init_element(self.receiving_address_detection_locator)
        locate_by_anchor(button, parent_lv=1, child_lv='l1').click()

    # 差评检测
    def negative_comment_diagnosis_detection(self):
        button = init_element(self.negative_comment_diagnosis_locator)
        locate_by_anchor(button, parent_lv=1, child_lv='l1').click()

    # 云黑名单检测
    def cloud_blacklist_detection(self):
        button = init_element(self.cloud_blacklist_detection_locator)
        locate_by_anchor(button, parent_lv=1, child_lv='l1').click()

    # 点击保存
    def click_sure(self):
        button = init_element(self.preservation_locator)
        button.click()

    # 获取版本号
    def get_version(self):
        version_number = init_element(self.version_number_locator)
        version_number_text = version_number.get_text()
        result = version_number_text.split('：')[-1]
        return result


if __name__ == '__main__':
    # check_address_element = locate_by_anchor(init_element(self.check_address_anchor), 2, 'l1')
    # check_address_element.click()
    # third_phase_element = locate_by_anchor(init_element(self.check_address_phase_anchor), 5, 'v2v0v0l0')
    m = MyPage()
    print(m.get_version())
