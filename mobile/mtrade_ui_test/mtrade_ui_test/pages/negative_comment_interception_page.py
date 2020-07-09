from poco.proxy import UIObjectProxy
from time import sleep
from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import BasePage, poco, init_element, locate_by_anchor, get_text_of_view,super_click


def close_Elastic_frame(news):
    button = poco(text=news)
    return locate_by_anchor(button, parent_lv=2, child_lv='v2v1l0')


class NegativeCommentInterception(BasePage):
    quick_setting_of_interception_mode_locator = ('and', (('attr=', ('text', '快速设置拦截方式')),))
    medium_and_poor_evaluation_interception_locator = ('and', (('attr=', ('text', '中差评拦截')),))
    give_me_mid_seller_locator = ('and', (('attr=', ('text', '给过我中评的买家')),))
    give_me_bad_seller_locator = ('and', (('attr=', ('text', '给过我差评的买家')),))
    black_block_locator = ('and', (('attr=', ('text', '旺旺黑名单')),))
    automatic_add_bad_locator = ('and', (('attr=', ('text', '符合拦截条件的用户自动添加到旺旺黑名单')),))
    cloud_bad_locator = ('and', (('attr=', ('text', '云黑名单')),))
    order_information_interception_locator = ('and', (('attr=', ('text', '订单信息拦截')),))
    than_actual_payment_locator = ('and', (('attr=', ('text', '实付金额大于')),))
    less_than_actual_payment_locator = ('and', (('attr=', ('text', '实付金额小于')),))
    than_order_num_locator = ('and', (('attr=', ('text', '订单总件数大于')),))
    less_than_order_num_locator = ('and', (('attr=', ('text', '订单总件数小于')),))
    than_order_common_num_locator = ('and', (('attr=', ('text', '一个订单中同一宝贝数大于')),))
    less_than_order_common_num_locator = ('and', (('attr=', ('text', '一个订单中同一宝贝数小于')),))
    buyer_information_interception_locator = ('and', (('attr=', ('text', '买家信息拦截')),))
    buyer_no_alipay_locator = ('and', (('attr=', ('text', '没有绑定支付宝账户的买家')),))
    following_keywords_locator = ('and', (('attr=', ('text', '地址或留言包含以下关键字')),))
    recipient_block_locator = ('and', (('attr=', ('text', '收件人拦截')),))
    area_interception_locator = ('and', (('attr=', ('text', '区域拦截')),))
    ww_and_baby_locator = ('and', (('attr=', ('text', '放行旺旺和宝贝')),))
    white_ww_locator = ('and', (('attr=', ('text', '旺旺白名单')),))
    white_baby_locator = ('and', (('attr=', ('text', '宝贝白名单')),))
    close_reason_locator = ('and', (('attr=', ('text', '关闭理由')),))
    Interception_record_locator = ('and', (('attr=', ('text', '拦截记录')),))
    now_open_locator = ('and', (('attr=', ('text', '立即开启')),))

    # 检查差评拦截功能是否开启
    def check_MasterSwitchStatus(self):
        status = init_element(self.now_open_locator)
        if status.exists():
            status.click()
        else:
            pass

    # 获取差评拦截设置的方式
    def get_interception_status(self):
        status = init_element(self.quick_setting_of_interception_mode_locator)
        status_text = locate_by_anchor(status, 2, 'l1l0').get_text()
        return status_text

    # 初始化
    def set_interception_status(self):
        poco(text = '快速设置拦截方式').wait_for_appearance(5)
        #status = init_element(self.quick_setting_of_interception_mode_locator)
        #print(status.attr('pos'))
        # 初始化所有开关状态为关闭状态
        #status.click()
        #poco(text='自定义拦截模式').wait_for_appearance(5)
        poco(text = self.get_interception_status()).click()
        poco(text='自定义拦截模式').click()


    # 给过我中评的买家
    def check_give_me_mid_seller(self):
        mid_seller = init_element(self.give_me_mid_seller_locator)
        locate_by_anchor(mid_seller, 1, 'l0').click()
        if get_text_of_view(locate_by_anchor(mid_seller, 1, 'l0')).encode('utf-8') == b'\xee\x9a\x9d':
            return True
        else:
            return False

    # 给过我差评的买家
    def check_give_me_bad_seller(self):
        bad_seller = init_element(self.give_me_bad_seller_locator)
        locate_by_anchor(bad_seller, 1, 'l0').click()
        if get_text_of_view(locate_by_anchor(bad_seller, 1, 'l0')).encode('utf-8') == b'\xee\x9a\x9d':
            return True
        else:
            return False

    # 黑名单拦截
    def check_black_block(self):
        black_block = init_element(self.black_block_locator)
        locate_by_anchor(black_block, 2, 'l0l0').click()
        if get_text_of_view(locate_by_anchor(black_block, 2, 'l0l0')).encode('utf-8') == b'\xee\x9a\x9d':
            return True
        else:
            return False

    # 旺旺黑名单添加及删除
    @staticmethod
    def black_block_operation():
        poco(text='旺旺黑名单').click()
        ww_name = poco(text='买家旺旺')
        locate_by_anchor(ww_name, 1, 'l1l1').set_text('自动黑名单用户')
        black_reason = poco(text='拉黑原因')
        locate_by_anchor(black_reason, 1, 'l1l1').set_text('自动黑名单用户添加原因')
        poco(text='添加').click()
        locate_by_anchor(ww_name, 1, 'l1l0').set_text('')
        locate_by_anchor(black_reason, 1, 'l1l0').set_text('')
        name_status = {}
        if poco(text='自动黑名单用户'):
            name_status['add'] = True
        else:
            name_status['add'] = False
        # poco(text='自动黑名单用户').parent().parent().offspring("android.widget.Button")[0].click()
        auto_black_name = poco(text='自动黑名单用户')
        locate_by_anchor(auto_black_name, 2, 'l1').click()
        if poco(text='自动黑名单用户'):
            name_status['move'] = False
        else:
            name_status['move'] = True
        return name_status

    # 符合拦截条件的用户自动添加到旺旺黑名单
    def check_automatic_add_bad(self):
        automatic_add_bad = init_element(self.automatic_add_bad_locator)
        locate_by_anchor(automatic_add_bad, 1, 'l0').click()
        if get_text_of_view(locate_by_anchor(automatic_add_bad, 1, 'l0')).encode('utf-8') == b'\xee\x9a\x9d':
            return True
        else:
            return False

    # 云黑名单
    def check_cloud_bad(self):
        cloud_bad = init_element(self.cloud_bad_locator)
        locate_by_anchor(cloud_bad, 1, 'l0').click()
        if get_text_of_view(locate_by_anchor(cloud_bad, 1, 'l0')).encode('utf-8') == b'\xee\x9a\x9d':
            return True
        else:
            return False

    # 实付金额大于
    def check_than_actual_payment(self):
        than_actual_payment = init_element(self.than_actual_payment_locator)
        locate_by_anchor(than_actual_payment, 1, 'l0').click()
        close_Elastic_frame('大于该金额').click()
        if get_text_of_view(locate_by_anchor(than_actual_payment, 1, 'l0')).encode('utf-8') == b'\xee\x9a\x9d':
            return True
        else:
            return False

    # 获取实付金额大于
    def get_than_actual_payment(self):
        than_actual_payment = init_element(self.than_actual_payment_locator)
        than_actual_payment_news = locate_by_anchor(than_actual_payment, 2, 'l1l0').get_text()
        return than_actual_payment_news

    # 修改实付金额大于
    def set_than_actual_payment(self):
        than_actual_payment = init_element(self.than_actual_payment_locator)
        locate_by_anchor(than_actual_payment, 2, 'l1l0').click()
        than_payment = poco(text='大于该金额')
        locate_by_anchor(than_payment, 2, 'v1l0l0').set_text('10000')
        locate_by_anchor(than_payment, 2, 'v2v1l1').click()

    # 实付金额小于
    def check_less_than_actual_payment(self):
        less_than_actual_payment = init_element(self.less_than_actual_payment_locator)
        locate_by_anchor(less_than_actual_payment, 1, 'l0').click()
        close_Elastic_frame('小于该金额').click()
        if get_text_of_view(locate_by_anchor(less_than_actual_payment, 1, 'l0')).encode('utf-8') == b'\xee\x9a\x9d':
            return True
        else:
            return False

    # 获取实付金额小于
    def get_less_than_actual_payment(self):
        less_than_actual_payment = init_element(self.less_than_actual_payment_locator)
        less_than_actual_payment_news = locate_by_anchor(less_than_actual_payment, 2, 'l1l0').get_text()
        return less_than_actual_payment_news

    # 修改实付金额小于
    def set_less_than_actual_payment(self):
        less_than_actual_payment = init_element(self.less_than_actual_payment_locator)
        locate_by_anchor(less_than_actual_payment, 2, 'l1l0').click()
        less_payment = poco(text='小于该金额')
        locate_by_anchor(less_payment, 2, 'v1l0l0').set_text('10')
        locate_by_anchor(less_payment, 2, 'v2v1l1').click()

    # 订单总件数大于
    def check_than_order_num(self):
        than_order_num = init_element(self.than_order_num_locator)
        locate_by_anchor(than_order_num, 1, 'l0').click()
        close_Elastic_frame('大于该件数').click()
        if get_text_of_view(locate_by_anchor(than_order_num, 1, 'l0')).encode('utf-8') == b'\xee\x9a\x9d':
            return True
        else:
            return False

    # 订单总件数小于
    def check_less_than_order_num(self):
        less_than_order_num = init_element(self.less_than_order_num_locator)
        locate_by_anchor(less_than_order_num, 1, 'l0').click()
        close_Elastic_frame('小于该件数').click()
        if get_text_of_view(locate_by_anchor(less_than_order_num, 1, 'l0')).encode('utf-8') == b'\xee\x9a\x9d':
            return True
        else:
            return False


    # 获取订单总件数大于
    def get_than_order_num(self):
        than_order_num = init_element(self.than_order_num_locator)
        than_order_num_news = locate_by_anchor(than_order_num, 2, 'l1l0').get_text()
        return than_order_num_news

    # 获取订单总件数小于
    def get_less_than_order_num(self):
        less_than_order_num = init_element(self.than_order_num_locator)
        less_than_order_num_news = locate_by_anchor(less_than_order_num, 2, 'l1l0').get_text()
        return less_than_order_num_news

    # 修改订单总件数大于
    def set_than_order_num(self):
        than_order_num = init_element(self.than_order_num_locator)
        locate_by_anchor(than_order_num, 2, 'l1l0').click()
        than_order = poco(text='大于该件数')
        locate_by_anchor(than_order, 2, 'v1l0l0').set_text('10')
        locate_by_anchor(than_order, 2, 'v2v1l1').click()

    # 修改订单总件数小于
    def set_less_than_order_num(self):
        less_than_order_num = init_element(self.than_order_num_locator)
        locate_by_anchor(less_than_order_num, 2, 'l1l0').click()
        less_than_order = poco(text='小于该件数')
        locate_by_anchor(less_than_order, 2, 'v1l0l0').set_text('50')
        locate_by_anchor(less_than_order, 2, 'v2v1l1').click()

    # 一个订单中同一宝贝数大于
    def check_than_order_common_num(self):
        than_order_common_num = init_element(self.than_order_common_num_locator)
        locate_by_anchor(than_order_common_num, 1, 'l0').click()
        close_Elastic_frame('大于该件数').click()
        if get_text_of_view(locate_by_anchor(than_order_common_num, 1, 'l0')).encode('utf-8') == b'\xee\x9a\x9d':
            return True
        else:
            return False

    # 一个订单中同一宝贝数小于
    def check_less_than_order_common_num(self):
        less_than_order_common_num = init_element(self.less_than_order_common_num_locator)
        locate_by_anchor(less_than_order_common_num, 1, 'l0').click()
        close_Elastic_frame('小于该件数').click()
        if get_text_of_view(locate_by_anchor(less_than_order_common_num, 1, 'l0')).encode('utf-8') == b'\xee\x9a\x9d':
            return True
        else:
            return False


    # 获取一个订单中同一宝贝数大于
    def get_than_order_common_num(self):
        than_order_common_num = init_element(self.than_order_common_num_locator)
        than_order_common_num_news = locate_by_anchor(than_order_common_num, 2, 'l1l0').get_text()
        return than_order_common_num_news

    # 获取一个订单中同一宝贝数小于
    def get_less_than_order_common_num(self):
        less_than_order_common_num = init_element(self.than_order_common_num_locator)
        less_than_order_common_num_news = locate_by_anchor(less_than_order_common_num, 2, 'l1l0').get_text()
        return less_than_order_common_num_news


    # 修改一个订单中同一宝贝数大于
    def set_than_order_common_num(self):
        than_order_common_num = init_element(self.than_order_common_num_locator)
        locate_by_anchor(than_order_common_num, 2, 'l1l0').click()
        than_order = poco(text='大于该件数')
        locate_by_anchor(than_order, 2, 'v1l0l0').set_text('15')
        locate_by_anchor(than_order, 2, 'v2v1l1').click()

    # 修改一个订单中同一宝贝数小于
    def less_set_than_order_common_num(self):
        than_order_common_num = init_element(self.than_order_common_num_locator)
        locate_by_anchor(than_order_common_num, 2, 'l1l0').click()
        less_than_order = poco(text='小于该件数')
        locate_by_anchor(less_than_order, 2, 'v1l0l0').set_text('50')
        locate_by_anchor(less_than_order, 2, 'v2v1l1').click()

    # 没有绑定支付宝账户的买家
    def check_buyer_no_alipay(self):
        buyer_no_alipay = init_element(self.buyer_no_alipay_locator)
        locate_by_anchor(buyer_no_alipay, 1, 'l0').click()
        if get_text_of_view(locate_by_anchor(buyer_no_alipay, 1, 'l0')).encode('utf-8') == b'\xee\x9a\x9d':
            return True
        else:
            return False

    # 地址或留言包含以下关键字
    def check_following_keywords(self):
        following_keywords = init_element(self.following_keywords_locator)
        locate_by_anchor(following_keywords, 1, 'l0').click()
        close_Elastic_frame('以下关键字拦截').click()
        if get_text_of_view(locate_by_anchor(following_keywords, 1, 'l0')).encode('utf-8') == b'\xee\x9a\x9d':
            return True
        else:
            return False

    # 获取地址或留言包含以下关键字信息
    def get_following_keywords(self):
        following_keywords = init_element(self.following_keywords_locator)
        following_keywords_news = locate_by_anchor(following_keywords, 2, 'v1l0v0')
        following_keywords_news = get_text_of_view(following_keywords_news)
        return following_keywords_news

    # 编辑地址或留言包含以下关键字信息
    def set_following_keywords(self):
        following_keywords = init_element(self.following_keywords_locator)
        locate_by_anchor(following_keywords, 2, 'v1v0v0').click()
        keywords = poco(text='以下关键字拦截')
        locate_by_anchor(keywords, 2, 'v1v1v0v0').set_text('新增地址关键字信息')
        locate_by_anchor(keywords, 2, 'v2v1l1').click()

    # 收件人拦截
    def check_recipient_block(self):
        recipient_block = init_element(self.recipient_block_locator)
        locate_by_anchor(recipient_block, 1, 'l0').click()
        if get_text_of_view(locate_by_anchor(recipient_block, 1, 'l0')).encode('utf-8') == b'\xee\x9a\x9d':
            return True
        else:
            return False

    # 添加及删除收件人拦截
   # @staticmethod
    def recipient_block_operation(self):
        recipient_block = init_element(self.recipient_block_locator)
        locate_by_anchor(recipient_block,2,'l1v0').click()
        name = poco(text='收件人姓名')
        name.parent().offspring("android.widget.EditText").set_text('测试人员')
        mobile_phone = poco(text='收件人手机号码')
        mobile_phone.parent().offspring("android.widget.EditText").set_text('13911112222')
        phone = poco(text='收件人电话号码')
        phone.parent().offspring("android.widget.EditText").set_text('8510100')
        recive_add = poco(text='收件地址')[1]
        recive_add.parent().offspring("android.widget.EditText")[0].set_text('上海市')
        reason = poco(text='拦截原因（选填）')
        locate_by_anchor(reason, 1, 'l1').set_text('测试拦截')
        poco(text='添加').wait_for_appearance(3)
        poco(text='添加').click()
        sleep(3)
        operation_status = {}
        reason_added = poco(text='拦截原因：测试拦截')
        if reason_added.exists():
            operation_status['add'] = True
            locate_by_anchor(reason_added, 2, 'l1').click()
            poco(text='确认').click()
            if poco(text='拦截原因：测试拦截').exists():
                operation_status['move'] = False
            else:
                operation_status['move'] = True
            return operation_status
        else:
            operation_status['add'] = False


    # 区域拦截
    def check_area_interception(self):
        area_interception = init_element(self.area_interception_locator)
        locate_by_anchor(area_interception, 1, 'l0').click()
        if get_text_of_view(locate_by_anchor(area_interception, 1, 'l0')).encode('utf-8') == b'\xee\x9a\x9d':
            return True
        else:
            return False

    # 添加及删除区域拦截
    def area_interception_operation(self):
        operation_status = {}
        area_interception = init_element(self.area_interception_locator)
        area_interception_button = locate_by_anchor(area_interception, 2, 'l1v0')
        area_interception_button.click()
        poco(text='选择省').click()
        poco(text='海南省').click()
        poco(text='海口市').click()
        poco(text='龙华区').click()
        poco(type='android.widget.EditText').set_text('区域地址拦截')

        poco(text='添加').click()
        if poco(text='拦截原因：区域地址拦截'):
            operation_status['add'] = True
            reason = poco(text='拦截原因：区域地址拦截')
            locate_by_anchor(reason, 2, 'l1').click()
        else:
            operation_status['add'] = False
        if poco(text='拦截原因：区域地址拦截'):
            operation_status['move'] = False
        else:
            operation_status['move'] = True
        return operation_status

    # 旺旺白名单
    def check_white_ww(self):
        white_ww = init_element(self.white_ww_locator)
        locate_by_anchor(white_ww, 1, 'l0').click()
        if get_text_of_view(locate_by_anchor(white_ww, 1, 'l0')).encode('utf-8') == b'\xee\x9a\x9d':
            return True
        else:
            return False

    # 添加及删除旺旺白名单
    def white_ww_operation(self):
        poco(text='添加旺旺白名单').click()
        buyer_nick = poco(text='买家旺旺')
        buyer_nick.parent().offspring("android.widget.EditText").set_text('自动白名单用户')
        reason_white = poco(text='放行原因')
        reason_white.parent().offspring("android.widget.EditText").set_text('自动白名单用户添加原因')
        poco(text='添加').click()
        # 有问题，得这么处理一下
        buyer_nick.parent().offspring("android.widget.EditText").set_text('')
        reason_white.parent().offspring("android.widget.EditText").set_text('')
        operation_name_status = {}
        if poco(text='自动白名单用户'):
            operation_name_status['add'] = True
            auto_white_reason = poco(text='放行原因：自动白名单用户添加原因')
            auto_white_reason.parent().parent().offspring("android.widget.Button")[0].click()
        else:
            operation_name_status['add'] = False
        if poco(text='自动白名单用户'):
            operation_name_status['move'] = False
        else:
            operation_name_status['move'] = True
        return operation_name_status

    # 宝贝白名单
    def check_white_baby(self):
        white_baby = init_element(self.white_baby_locator)
        locate_by_anchor(white_baby, 1, 'l0').click()
        button = poco(text='黑名单中买家依旧拦截')
        locate_by_anchor(button, 1, 'l0').click()
        if get_text_of_view(locate_by_anchor(button, 1, 'l0')).encode('utf-8') == b'\xee\x9a\x9d':
            return True
        else:
            return False

    # 添加及删除宝贝白名单
    @staticmethod
    def white_baby_operation():
        baby_status = {}
        poco(text='添加宝贝白名单').click()
        poco(text='添加宝贝白名单').wait_for_appearance(3)
        poco(text='添加宝贝白名单').click()
        first_baby = poco(text='添加')[0]
        baby_name_demo = locate_by_anchor(first_baby, parent_lv=2, child_lv='l0l1')
        baby_name = get_text_of_view(baby_name_demo)
        first_baby.click()
        if poco(text=baby_name).exists():
            baby_status['add'] = True
            locate_by_anchor(poco(text=baby_name), parent_lv=3, child_lv='l1').offspring(
                'android.widget.Button').click()
        else:
            baby_status['add'] = False
        if poco(text=baby_name).exists():
            baby_status['move'] = False
        else:
            baby_status['move'] = True
        return baby_status

    # 获取设置的关闭理由
    def close_reason(self):
        close_reason = init_element(self.close_reason_locator)
        close_reason_news = locate_by_anchor(close_reason, 2, 'l1l0').get_text()
        return close_reason_news

    # 设置关闭理由
    def set_close_reason(self):
        close_reason = init_element(self.close_reason_locator)
        close_reason.click()
        poco(text='未及时付款').click()
        reason = poco(text='请选择关闭理由')
        reason_click = locate_by_anchor(reason, parent_lv=2, child_lv='v2v1l1')
        reason_click.click()
        if poco(text='请选择关闭理由'):
            poco(text='买家不想买了').click()
            reason_click.click()
            return poco(text='买家不想买了').exists(), '买家不想买了'
        else:
            return poco(text='未及时付款').exists(), '未及时付款'

    # 拦截记录跳转
    def Interception_record(self):
        Interception_record = init_element(self.Interception_record_locator)
        Interception_record.click()

    @staticmethod
    def check_Interception_record(tid):
        result = poco(text=tid).exists()
        return result


if __name__ == '__main__':
    # results = True
    # i = utils.get_interception_news()[0]
    # print(utils.get_interception_news())
    # print(i)
    # for i in utils.get_interception_news():
    #     results = results and NegativeCommentInterception().check_Interception_record(i)
    # # print(NegativeCommentInterception().check_Interception_record(i))
    # print(results)
    #print(NegativeCommentInterception().check_recipient_block())
    #
    # poco(text = "差评拦截").click()
    # NegativeCommentInterception().check_MasterSwitchStatus()
    # NegativeCommentInterception().set_interception_status()
    # poco('android:id/content').swipe([0, -0.7])
    # sleep(2)
    # #NegativeCommentInterception().check_than_order_num()
    # NegativeCommentInterception().back()
    # NegativeCommentInterception().page_swipe_for_custom(-0.7)
    # print(NegativeCommentInterception().recipient_block_operation())
    # print(poco(text='拦截原因：测试拦截').exists())
    # if poco(text='拦截原因：测试拦截').exists():
    #     print(False)
    # else:
    #     print(True)
    # poco('android:id/content').swipe([0, -1])
    # sleep(2)
    l = ['1039417536888153634', '1039390720357871945', '1039412768329871945', '1039932578345153634', '1040043075747153634', '1040043075376153634', '1040042563873153634', '1039952290004153634', '1039899969544871945', '1040032515616871945', '1039929890192871945', '1039340000289871945', '1039857729389871945', '603714444645108200', '603892495737108200', '603829774798108200', '1037717729171729168', '1037845251191729168', '603586765964108200', '603807822735108200', '1012399616084651409', '1011939907415620411', '1011829922065620411', '989738624134620411', '990335107816620411', '990259842103620411', '990343011003620411', '988997505954926960', '988521506638420824', '600593326202108200']
    for i in l:
        res = NegativeCommentInterception().check_Interception_record(i)
        print(i)
        print(res)
    # print(poco(text='1040043075747153634').exists())