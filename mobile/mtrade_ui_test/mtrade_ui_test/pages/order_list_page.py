import time
from poco.exceptions import PocoNoSuchNodeException, PocoTargetTimeout
from poco.proxy import UIObjectProxy
from time import sleep
from mobile.mtrade_ui_test.mtrade_ui_test.data import RE_ORDER, WAIT_BUYER_PAY_ORDER, WAIT_BUYER_PAY_ORDER_CART, ITEM_INFO, ORDER_INFO, RECEIVER_INFO, \
    ITEM_INFO_CART, ORDER_INFO_CART
from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import BasePage, init_element, get_order_detail, get_offspring_by_index, locate_by_anchor, \
    ay_exists, ay_click, ay_get_text, ay_swipe, poco, get_text_of_view
from mobile.mtrade_ui_test.mtrade_ui_test.pages.evaluation_operation_page import EvaluationOperationPage
from mobile.mtrade_ui_test.mtrade_ui_test.pages.modify_price_page import ModifyPricePage
from mobile.mtrade_ui_test.mtrade_ui_test.pages.send_goods_page import SendGoodsPage
from mobile.mtrade_ui_test.mtrade_ui_test.pages.ww_chat_page import WwChatPage


def format_receiver_info(name, mobile, address):
    return name + '，' + mobile + '，' + address


class OrderListPage(BasePage):
    # 页面上的标签
    no_more_orders_locator = ('and', (('attr=', ('text', '没有更多订单了')),))  # 没有更多订单了
    risk_locator = ('and', (('attr.*=', ('text', '收货地址中含关键字.*')),))  # 风险提示信息
    remark_locator = ('and', (('attr=', ('text', '备注')),))  # 备注
    cancellation_of_closing_order_locator = ('and', (('attr=', ('text', '取消合单')),))  # 取消合单
    leaving_a_message_locator = ('and', (('attr=', ('text', '留言')),))  # 留言
    receiving_address_locator = ('and', (('attr=', ('text', '收货地址')),))  # 收货地址
    addressee_locator = ('and', (('attr=', ('text', '收件人')),))  # 收件人
    filter_locator = ('and', (('attr=', ('text', '筛选')),))  # 筛选
    logistics_company_locator = ('and', (('attr=', ('text', '物流公司')),))
    re_order_no_locator = ('and', (('attr.*=', ('text', RE_ORDER)),))  # 匹配正则表达式的订单号
    total_price_locator = ('and', (('attr=', ('text', '合计(含快递:￥0.00)')),))  # 订单总价左侧的标签
    print_history_locator = ('and', (('attr=', ('text', '打印信息')),))  # 部分订单存在打印信息标签

    # 订单属性
    addressee_info_locator = ('and', (('attr=', ('text', ORDER_INFO.get('收件人姓名'))),))  # 收件人姓名
    mobile_info_locator = ('and', (('attr=', ('text', ORDER_INFO.get('收件人手机f'))),))  # 收件人手机
    address_info_locator = ('and', (('attr=', ('text', ORDER_INFO.get('收货地址'))),))  # 收货地址
    remark_info_locator = ('and', (('attr=', ('text', ORDER_INFO.get('备注'))),))  # 备注
    message_info_locator = ('and', (('attr=', ('text', ORDER_INFO.get('留言'))),))  # 留言
    buyer_nick_info_locator = ('and', (('attr=', ('text', ORDER_INFO.get('买家昵称'))),))  # 买家昵称

    # 商品属性
    item_name_locator = ('and', (('attr=', ('text', ITEM_INFO.get('商品标题'))),))  # 商品标题
    item_name_cart1_locator = ('and', (('attr=', ('text', ITEM_INFO_CART[0].get('商品标题'))),))  # 商品标题
    item_name_cart2_locator = ('and', (('attr=', ('text', ITEM_INFO_CART[1].get('商品标题'))),))  # 商品标题
    # 功能按钮
    # 通用按钮
    tab_wait_buyer_confirm_goods_locator = ('and', (('attr.*=', ('text', r'已发货 \d*')),))  # 标签栏中的已发货
    tab_wait_seller_send_goods_locator = ('and', (('attr.*=', ('text', r'待发货 \d*')),))  # 标签栏中的待发货
    tab_pending_payment_locator = ('and', (('attr.*=', ('text', r'待付款 \d*')),))  # 标签栏中的待付款
    tab_need_rate_locator = ('and', (('attr.*=', ('text', r'待评价 \d*')),))  # 标签栏中的需要评价
    tab_refund_locator = ('and', (('attr.*=', ('text', r'退款中 \d*')),))  # 标签栏中的退款中
    tab_succeeded_locator = ('and', (('attr.*=', ('text', r'已成功 \d*')),))  # 标签栏中的已成功
    tab_closed_locator = ('and', (('attr.*=', ('text', r'已关闭 \d*')),))  # 标签栏中的已关闭
    tab_three_month_locator = ('and', (('attr.*=', ('text', r'近三个月 \d*')),))  # 标签栏中的近三个月
    my_merchandise_locator = ('and', (('attr=', ('text', '我的商品')),))  # 标签栏中的我的商品
    ta_all_orders_locator = ('and', (('attr=', ('text', 'Ta所有订单')),))  # 查看买家所有订单
    block_buyer_locator = ('and', (('attr=', ('text', '阻止Ta拍单')),))  # 阻止买家拍单
    delivery_time_locator = ('and', (('attr=', ('text', '发货时间')),))  # 发货时间排序按钮
    payment_time_locator = ('and', (('attr=', ('text', '付款时间')),))  # 付款时间排序按钮
    take_time_locator = ('and', (('attr=', ('text', '拍下时间')),))  # 拍下时间排序按钮
    # 弹窗中的菜单
    dial_locator = ('and', (('attr=', ('text', '拨打号码')),))  # 弹窗中的拨打号码选项
    copy_mobile_number_locator = ('and', (('attr=', ('text', '复制号码')),))  # 弹窗中的复制号码选项
    contact_by_wangwang_locator = ('and', (('attr=', ('text', '联系旺旺')),))  # 弹窗中的联系旺旺选项
    modify_attribute_locator = ('and', (('attr=', ('text', '修改属性')),))  # 弹窗中的修改属性选项
    modify_address_locator = ('and', (('attr=', ('text', '修改地址')),))  # 弹窗中的修改地址选项
    copy_receipt_information_locator = ('and', (('attr=', ('text', '复制收货信息')),))  # 弹窗中的复制收货信息选项
    check_address_locator = ('and', (('attr=', ('text', '核对地址')),))  # 弹窗中的核对地址选项
    # 待评价订单功能按钮
    batch_evaluation_locator = ('and', (('attr=', ('text', '批量评价')),))  # 批量评价
    wang_wang_urges_praise_locator = ('and', (('attr=', ('text', '旺旺催好评')),))  # 旺旺催好评
    immediate_evaluation_locator = ('and', (('attr=', ('text', '立即评价')),))  # 立即评价
    # 已发货订单功能按钮
    delayed_receipt_locator = ('and', (('attr=', ('text', '延时收货')),))  # 延时收货按钮
    change_logistics_locator = ('and', (('attr=', ('text', '修改物流')),))  # 修改物流按钮
    # 退款中订单功能按钮
    handling_refund_locator = ('and', (('attr=', ('text', '处理退款')),))  # 处理退款
    modify_refund_reason_locator = ('and', (('attr=', ('text', '修改退款原因')),))  # 修改退款原因
    # 待发货订单功能按钮
    send_goods_locator = ('and', (('attr=', ('text', '发货')),))  # 发货
    check_address_button_locator = ('and', (('attr=', ('text', '核对地址')),))  # 核对地址
    sweep_code_delivery_locator = ('and', (('attr=', ('text', '扫码发货')),))  # 扫码发货
    partial_shipment_locator = ('and', (('attr=', ('text', '部分发货')),))  # 部分发货
    cancel_combine_locator = ('and', (('attr=', ('text', '取消合单')),))  # 取消合单
    num_of_combining_order_locator = ('and', (('attr.*=', ('text', '\\d笔订单进行了合单')),))  # 合单订单的合单数量信息
    # 待付款订单功能按钮
    close_order_locator = ('and', (('attr=', ('text', '关闭订单')),))  # 关闭订单按钮
    modify_price_locator = ('and', (('attr=', ('text', '修改价格')),))  # 修改价格按钮
    ww_remind_locator = ('and', (('attr=', ('text', '旺旺催付')),))  # 旺旺催付

    def check_search_box_isempty(self):
        search_tid = poco(textMatches='\d{19}')[0]
        if locate_by_anchor(search_tid, parent_lv=1, child_lv='l2').get_text().encode()== b'\xee\x9a\xa3':
            locate_by_anchor(search_tid, parent_lv=1, child_lv='l2').click()
        else:
            pass

    def get_order_status(self):
        block_buyer = init_element(self.block_buyer_locator)
        temp = locate_by_anchor(block_buyer, parent_lv=3, child_lv='v0')
        if len(temp.child()) < 4:
            status = locate_by_anchor(temp, child_lv='l0')
        else:
            status = locate_by_anchor(temp, child_lv='l1')
        return get_text_of_view(status)

    def check_order_info(self):
        """
        普通订单检查订单信息是否正确
        :return:
        """
        msg = []
        remark = init_element(self.remark_locator)
        remark_view = remark.parent().parent()
        item_name = init_element(self.item_name_locator)
        if not item_name.exists():
            return False, '订单商品名称显示不正确'
        item_view = locate_by_anchor(item_name, parent_lv=4)
        addressee = init_element(self.addressee_locator)
        addressee_view = locate_by_anchor(addressee, parent_lv=2)
        res1 = self.check_order_first_item(item_view)
        res2 = self.check_order_remark(remark_view)
        res3 = self.check_order_addressee(addressee_view)
        if not res1[0]:
            msg.append(res1[1])
        if not res2[0]:
            msg.append(res2[1])
        if not res3[0]:
            msg.append(res3[1])
        return res1[0] and res2[0] and res3[0], ';'.join(msg)

    # 待付款订单
    def check_order_info_cart(self):
        """
        购物车订单应显示多个商品
        :param
        :return:
        """
        msg = []
        remark = init_element(self.remark_locator)
        remark_view = remark.parent().parent()
        item_name1 = init_element(self.item_name_cart1_locator)
        item_name2 = init_element(self.item_name_cart2_locator)
        if not item_name1.exists() or not item_name2.exists():
            return False, '购物车订单商品名称显示不正确'
        item_view1 = locate_by_anchor(item_name1, parent_lv=4)
        item_view2 = locate_by_anchor(item_name2, parent_lv=4)
        addressee = init_element(self.addressee_locator)
        addressee_view = locate_by_anchor(addressee, parent_lv=2)
        res1_1 = self.check_order_first_item(item_view1)
        res1_2 = self.check_order_second_item(item_view2)
        res2 = self.check_order_remark(remark_view)
        res3 = self.check_order_addressee(addressee_view)
        if not res1_1[0]:
            msg.append(res1_1[1])
        if not res1_2[0]:
            msg.append(res1_2[1])
        if not res2[0]:
            msg.append(res2[1])
        if not res3[0]:
            msg.append(res3[1])
        return res1_1[0] and res1_2[0] and res2[0] and res3[0], ';'.join(msg)

    @staticmethod
    def check_order_remark(_remark_view):
        try:
            #remark_info = locate_by_anchor(_remark_view, child_lv='v0l1l0l1')
            remark_info = poco(text = '自动化测试备注')
            #message_info = locate_by_anchor(_remark_view, child_lv='v1l1')
            message_info = poco(text = '自动化测试留言')
            remark_info_text = remark_info.get_text()
            message_info_text = message_info.get_text()
            if remark_info_text != ORDER_INFO.get('备注'):
                return False, '订单的备注信息显示不正确'
            if message_info_text != ORDER_INFO.get('留言'):
                return False, '订单的留言信息显示不正确'
            return True, ''
        except PocoNoSuchNodeException:
            return False, '订单备注部分界面异常或者数据异常，请重新检查用例设计'
        except IndexError:
            return False, '订单备注部分界面异常或者数据异常，请重新检查用例设计'

    @staticmethod
    def check_order_first_item(_item_view):
        """
        检查普通订单的商品信息，如果是购物车订单，该方法检查第一件商品的信息
        :return:
        """
        try:
            item_name_info = locate_by_anchor(_item_view, child_lv='v0l1l0v0')
            item_name_info_text = get_text_of_view(item_name_info)
            sku_id = locate_by_anchor(_item_view, child_lv='v0l1l0v1')
            sku_id_text = get_text_of_view(sku_id)
            sku_properties_name1 = locate_by_anchor(_item_view, child_lv='v0l1l0v2v0')
            sku_properties_name2 = locate_by_anchor(_item_view, child_lv='v0l1l0v2v1')
            sku_properties_name3 = locate_by_anchor(_item_view, child_lv='v0l1l0v2v2')
            sku_properties_name1_text = get_text_of_view(sku_properties_name1)
            sku_properties_name2_text = get_text_of_view(sku_properties_name2)
            sku_properties_name3_text = get_text_of_view(sku_properties_name3)
            res1 = sku_properties_name1_text == ITEM_INFO.get('属性')[0]
            res2 = sku_properties_name2_text == ITEM_INFO.get('属性')[1]
            res3 = sku_properties_name3_text == ITEM_INFO.get('属性')[2]
            res = res1 and res2 and res3
            if item_name_info_text != ITEM_INFO.get('商品标题'):
                return False, '订单商品标题显示不正确'
            if sku_id_text != ITEM_INFO.get('商家编码'):
                return False, '订单的商家编码信息显示不正确'
            if not res:
                return False, '订单的sku属性信息显示不正确'
            return True, ''
        except PocoNoSuchNodeException:
            return False, '订单商品部分界面异常或者数据异常，请重新检查用例设计'

    @staticmethod
    def check_order_second_item(_item_view):
        try:
            item_name_info = locate_by_anchor(_item_view, child_lv='v1l1l0v0')
            item_name_info_text = get_text_of_view(item_name_info)
            sku_id = locate_by_anchor(_item_view, child_lv='v1l1l0v1')
            sku_id_text = get_text_of_view(sku_id)
            sku_properties_name1 = locate_by_anchor(_item_view, child_lv='v1l1l0v2v0')
            sku_properties_name1_text = get_text_of_view(sku_properties_name1)
            res = sku_properties_name1_text == ITEM_INFO_CART[1].get('属性')
            if item_name_info_text != ITEM_INFO_CART[1].get('商品标题'):
                return False, '购物车订单第二件商品标题显示不正确{}，{}'.format(item_name_info_text, ITEM_INFO_CART[1].get('商品标题'))
            if sku_id_text != ITEM_INFO_CART[1].get('商家编码'):
                return False, '购物车订单第二件商品的商家编码信息显示不正确{}'.format(sku_id_text)
            if not res:
                return False, '购物车订单第二件商品的sku属性信息显示不正确'
            return True, ''
        except PocoNoSuchNodeException:
            return False, '购物车订单商品部分界面异常或者数据异常，请重新检查用例设计'

    @staticmethod
    def check_order_addressee(_addressee_view):
        try:
            #addressee_info = locate_by_anchor(_addressee_view, child_lv='v0l1')
            addressee_info_text= poco(text = '顾超').get_text()
            addressee_info_pos = poco(text = '顾超').get_position()[0]
            addressee_pos = poco(text = '收件人').get_position()[0]
            #addressee_info_text = get_text_of_view(addressee_info)
            #mobile_info = locate_by_anchor(_addressee_view, child_lv='v0l1l1')
            mobile_info = poco(text = '186-2172-9133')
            mobile_info_text = mobile_info.get_text()
            mobile_info_pos = poco(text = '186-2172-9133').get_position()[0]
            address_info = locate_by_anchor(_addressee_view, child_lv='v1l1')
            address_info_text = get_text_of_view(address_info)
            # address = poco(text = '收货地址')
            # address_pos = address.get_position()[0]
            # address_info_text = poco(text = '上海，上海市，宝山区，高境镇新二路55号皇冠，201900').get_text()
            if addressee_info_text != ORDER_INFO.get('收件人姓名') and addressee_info_pos != addressee_pos:
                return False, '订单的收件人姓名信息显示不正确'
            if mobile_info_text != ORDER_INFO.get('收件人手机f') and addressee_info_pos != mobile_info_pos:
                return False, '订单的收件人手机号信息显示不正确'
            if address_info_text != ORDER_INFO.get('收货地址'):
                return False, '订单的收货地址信息显示不正确'
            return True, ''
        except PocoNoSuchNodeException:
            return False, '订单收货信息部分界面异常或者数据异常，请重新检查用例设计'

    def self_check(self):
        remark = init_element(self.remark_locator)  # 通过风险提示判断页面是否加载完成
        try:
            remark.wait_for_appearance(5)
        except Exception:
            return '页面没有成功加载'

    def waiting_for_order(self, timeout: int) -> None:
        """
        等待订单列表中的订单显示
        :param timeout: 等待超时时间
        :return:
        """
        all_order = init_element(self.re_order_no_locator)
        all_order.wait(timeout)

    # 获取当前订单页面订单数量
    def get_order_counts(self):
        all_order = init_element(self.re_order_no_locator)
        return len(all_order)

    # 根据付款时间对订单列表排序
    def sort_by_pay_time(self):
        payment_time = init_element(self.payment_time_locator)
        payment_time.click()

    # 根据拍下时间对订单列表排序
    def sort_by_created_time(self):
        take_time = init_element(self.take_time_locator)
        take_time.click()

    # 根据发货时间对订单列表排序
    def sort_by_delivery_time(self):
        delivery_time = init_element(self.delivery_time_locator)
        delivery_time.click()

    def copy_receiver_info(self):
        """
        点击收货地址标签
        在弹窗菜单中选择复制收货信息
        :return: None
        """
        ay_click(self.address_info_locator)
        ay_click(self.copy_receipt_information_locator)
        return RECEIVER_INFO

    def copy_mobile_number(self):
        """
        点击手机号文本
        在弹窗菜单中选择复制号码信息
        :return: None
        """
        ay_click(self.mobile_info_locator)
        ay_click(self.copy_mobile_number_locator)
        return ORDER_INFO.get('收件人手机')

    def contact_by_wangwang(self):
        """
        点击收货地址标签
        在弹窗菜单中选择联系旺旺
        :return: None
        """
        ay_click(self.address_info_locator)
        ay_click(self.contact_by_wangwang_locator)

    def show_all_orders_of_buyer(self):
        """
        在订单列表页面点击Ta所有订单
        :return: None
        """
        ay_click(self.ta_all_orders_locator)
        buyer_nick = init_element(self.buyer_nick_info_locator)
        return len(buyer_nick)

    def choose_wait_seller_send_goods(self):
        """
        在订单列表页面点击'待发货'标签
        :return:None
        """
        wait_seller_send_goods = init_element(self.tab_wait_seller_send_goods_locator)
        ay_swipe(self.tab_wait_buyer_confirm_goods_locator, 'right')  # 选择已发货标签执行向右滑动滑动操作
        wait_seller_send_goods.invalidate()
        wait_seller_send_goods.click()
        check = wait_seller_send_goods.parent().child()
        if len(check) > 1:
            self.check_search_box_isempty()
            if ay_exists(self.block_buyer_locator):
                order_status = self.get_order_status()
                expected_status = ['待发货', '当前没有任何订单', '待发货合单', '部分发货']
                if order_status in expected_status:
                    return True, ''
                else:
                    return False, '订单状态不正确'
        else:
            return False, '待发货标签没有点中'

    def choose_wait_buyer_pay(self):
        """
        在订单列表页面点击'待付款'标签
        :return:None
        """
        pending_payment = init_element(self.tab_pending_payment_locator)
        ay_swipe(self.tab_wait_buyer_confirm_goods_locator, 'right')  # 选择已发货标签执行向左滑动滑动操作
        pending_payment.invalidate()
        pending_payment.click()
        check = pending_payment.parent().child()
        if len(check) > 1:
            self.check_search_box_isempty()
            if ay_exists(self.block_buyer_locator):
                order_status = self.get_order_status()
                expected_status = ['待付款']
                if order_status in expected_status:
                    return True, ''
                else:
                    return False, '订单状态不正确'
            else:
                return True, '当前没有待付款订单'
        else:
            return False, '待付款标签没有点中'

    def choose_all_closed(self):
        """
        在订单列表页面点击'已关闭'标签
        :return:None
        """
        all_closed = init_element(self.tab_closed_locator)
        ay_swipe(self.tab_wait_buyer_confirm_goods_locator, 'left')  # 选择已发货标签执行向左滑动滑动操作
        all_closed.invalidate()
        all_closed.click()
        check = all_closed.parent().child()
        if len(check) > 1:
            self.check_search_box_isempty()
            if ay_exists(self.block_buyer_locator):
                order_status = self.get_order_status()
                expected_status = ['已关闭']
                if order_status in expected_status:
                    return True, ''
                else:
                    return False, '订单状态不正确'
            else:
                return True, '当前没有已关闭订单'
        else:
            return False, '已关闭标签没有点中'

    def choose_trade_finished(self):
        """
        在订单列表页面点击'已成功'标签
        :return:None
        """
        trade_finished = init_element(self.tab_succeeded_locator)
        ay_swipe(self.tab_wait_buyer_confirm_goods_locator, 'left')  # 选择已发货标签执行向左滑动滑动操作
        trade_finished.invalidate()
        trade_finished.click()
        check = trade_finished.parent().child()
        if len(check) > 1:
            self.check_search_box_isempty()
            if ay_exists(self.block_buyer_locator):
                order_status = self.get_order_status()
                expected_status = ['已成功', '待评价', '双方未评', '买家已评']
                if order_status in expected_status:
                    return True, ''
                else:
                    return False, '订单状态不正确'
            else:
                return True, '当前没有已成功订单'
        else:
            return False, '已成功标签没有点中'

    def choose_need_rate(self):
        """
        在订单列表页面点击'待评价'标签
        :return:None
        """
        need_rate = init_element(self.tab_need_rate_locator)
        ay_swipe(self.tab_wait_buyer_confirm_goods_locator, 'right')  # 选择已发货标签执行向右滑动滑动操作
        need_rate.invalidate()
        need_rate.click()
        check = need_rate.parent().child()
        if len(check) > 1:
            self.check_search_box_isempty()
            if ay_exists(self.block_buyer_locator):
                order_status = self.get_order_status()
                expected_status = ['待评价', '双方未评', '买家已评']
                if order_status in expected_status:
                    return True, ''
                else:
                    return False, '订单状态不正确'
            else:
                return True, '当前没有待评价订单'
        else:
            return False, '待评价标签没有点中'

    def choose_wait_buyer_confirm_goods(self):
        """
        在订单列表页面点击'已发货'标签
        :return:None
        """
        wait_buyer_confirm_goods = init_element(self.tab_wait_buyer_confirm_goods_locator)
        wait_buyer_confirm_goods.click()
        check = wait_buyer_confirm_goods.parent().child()
        if len(check) > 1:
            self.check_search_box_isempty()
            if ay_exists(self.block_buyer_locator):
                order_status = self.get_order_status()
                expected_status = ['已发货', '已发货合单']
                if order_status in expected_status:
                    return True, ''
                else:
                    return False, '订单状态不正确'
            else:
                return True, '当前没有已发货订单'
        else:
            return False, '已发货标签没有点中'

    def choose_trade_refund(self):
        """
        在订单列表页面点击'退款中'标签
        :return:None
        """
        trade_refund = init_element(self.tab_refund_locator)
        ay_swipe(self.tab_wait_buyer_confirm_goods_locator, 'right')  # 选择已发货标签执行向左滑动滑动操作
        trade_refund.invalidate()
        trade_refund.click()
        check = trade_refund.parent().child()
        if len(check) > 1:
            self.check_search_box_isempty()
            if ay_exists(self.block_buyer_locator):
                order_status = self.get_order_status()
                expected_status = ['退款中', '已发货退款', '待发货退款']
                if order_status in expected_status:
                    return True, ''
                else:
                    return False, '订单状态不正确'
            else:
                return True, '当前没有退款中订单'
        else:
            return False, '退款中标签没有点中'

    def choose_three_month(self):
        """
        在订单列表页面点击'近三个月'标签，检查标签是否处于选中状态
        :return:None
        """
        three_month = init_element(self.tab_three_month_locator)
        ay_swipe(self.tab_wait_buyer_confirm_goods_locator, 'left')  # 选择已发货标签执行向左滑动滑动操作
        three_month.invalidate()
        three_month.click()
        check = three_month.parent().child()
        if len(check) > 1:
            return True
        else:
            return False

    def go_seller_rate_page(self):
        ay_click(self.immediate_evaluation_locator)

    # 旺旺催付
    def ww_reminder(self):
        ww_remind = init_element(self.ww_remind_locator)
        ww_remind.click()
        try:
            WwChatPage().self_check()
        except Exception:
            print('没点到')
            ww_remind.invalidate()
            ww_remind.click()
        res = WwChatPage().get_chat_text_and_return()
        return res

    def modify_price(self, my_price):
        ay_click(self.modify_price_locator)
        ModifyPricePage().modify_price(my_price)

    # 单笔关闭订单
    def close_order(self):
        close_order = init_element(self.close_order_locator)
        close_order.click()  # 关闭订单按钮点击后可能没有反应
        try:
            poco(text='确认关闭').wait_for_appearance(3)
            self.back()
            return True
        except Exception:
            if ay_exists(self.copy_mobile_number_locator):  # 可能会误点到收货地址
                ay_click(self.copy_mobile_number_locator)
            close_order.invalidate()
            close_order.click()
        res = poco(text='确认关闭').exists()
        self.back()
        return res

    # 获取列表中的实付款价格
    def get_price(self):
        """
        通过相对定位找到价格元素
        获取并返回文本内容，即订单总价
        :return:
        """
        anchor = init_element(self.total_price_locator)
        total_price = locate_by_anchor(anchor, parent_lv=1, child_lv='l3l1')
        total_price_text = get_text_of_view(total_price)
        return total_price_text

    # 延长收货时间
    def extended_receiving_time(self):
        """
        延时3天收货
        :return:
        """
        ay_click(self.delayed_receipt_locator)
        poco(text='3').click()
        poco(text='请选择延迟收货的天数').wait_for_disappearance(10)
        if poco('android:id/alertTitle').exists():
            poco('确认').click()

    # 刷新物流
    def refresh_logistics(self):
        logistics_company = init_element(self.logistics_company_locator)
        refresh_logistics = locate_by_anchor(logistics_company, parent_lv=2, child_lv='v1v0l3')
        refresh_logistics.click()

    # 复制物流信息
    def copy_order_logistics(self):
        pass

    # 复制物流信息及最新动态
    def copy_order_logisticsinfo(self):
        pass

    # 点击修改物流
    def click_change_logistics(self):
        ay_click(self.change_logistics_locator)
        return ChangeLogisticsPage()

    # 详情页点击发送物流
    def info_send_logtics_news(self):
        poco(text='发送物流').click()

    def ww_new_get(self):
        return WwChatPage().get_chat_text_and_return()


    # 下面列出需要评价订单独有方法
    # 批量评价
    def batch_rate(self):
        batch_rate_button = UIObjectProxy(poco)
        batch_rate_button.query = self.NEED_RATE['batch_evaluation_locator']
        batch_rate_button.click()
        return EvaluationOperationPage()

    # 单个评价
    def single_rate(self):
        single_rate_button = UIObjectProxy(poco)
        single_rate_button.query = self.NEED_RATE['evaluation_locator']
        single_rate_button.click()
        return EvaluationOperationPage()

    def ww_rate(self):
        ww_button = UIObjectProxy(poco)
        ww_button.query = self.NEED_RATE['ww_rate_locator']
        ww_button.click()

    # 获取待评价订单数量
    def get_need_rate_num(self):
        num_text = UIObjectProxy(poco)
        num_text.query = self.NEED_RATE['num_need_rate']
        num_text.get_text()

    # 刷新物流方法
    def info_refresh_logistics(self):
        refresh_logistics = init_element(self.logistics_company_locator)
        locate_by_anchor(refresh_logistics,parent_lv=2,child_lv='v1l2').click()


    def get_logistics(self):
        anchor = init_element(self.logistics_company_locator)
        a = locate_by_anchor(anchor, parent_lv=2, child_lv='v0l1l0')
        b = locate_by_anchor(anchor, parent_lv=2, child_lv='v0l1l1')
        c = locate_by_anchor(anchor, parent_lv=2, child_lv='v1l1l2')
        news = {'company': a.get_text().strip(), 'company_id': b.get_text().strip(),
                'company_info': c.get_text().strip()}
        return news

    # 点击商品标题进入详情页面
    def go_detail_page(self):
        enter_detail_page_element = init_element(self.item_name_locator)
        enter_detail_page_element.click()

    # 点击发货按钮进入发货页面
    def go_send_goods_page(self):
        ay_click(self.send_goods_locator)

    def check_address(self):
        """
        点击核对地址按钮
        获取旺旺聊天窗口中的核对地址文本
        :return:
        """
        ay_click(self.check_address_locator)
        try:
            res = WwChatPage().get_chat_text_and_return()
        except PocoNoSuchNodeException:
            ay_click(self.check_address_locator)
            res = WwChatPage().get_chat_text_and_return()
        return res

    #   待发货订单方法
    # 方法：检查订单的单号打印记录
    def check_order_print_history(self):
        print_history = init_element(self.print_history_locator)
        return print_history.exists()

    def is_combine(self):
        order_status = self.get_order_status()
        cancel_combine_status = ay_exists(self.cancel_combine_locator)
        number_status = ay_exists(self.num_of_combining_order_locator)
        return order_status, cancel_combine_status, number_status

    # 方法：点击发货按钮，进入发货page
    def go_to_deliver(self):
        ay_swipe(self.block_buyer_locator, 'up')
        ay_click(self.send_goods_locator)
        if poco(text='确认').exists():
            poco(text='确认').click()
        return SendGoodsPage()


if __name__ == '__main__':
    o = OrderListPage()
    # print(o.check_order_info())
    # addressee_locator = ('and', (('attr=', ('text', '收件人')),))
    # addressee = init_element(addressee_locator)
    # addressee_view = locate_by_anchor(addressee, parent_lv=2)
    # print(o.check_order_addressee(addressee_view))
    print(o.ww_reminder())







