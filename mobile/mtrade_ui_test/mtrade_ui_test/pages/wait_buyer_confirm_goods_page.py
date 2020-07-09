from mobile.mtrade_ui_test.mtrade_ui_test.pages.send_goods_page import *
from mobile.mtrade_ui_test.mtrade_ui_test.pages.modify_address_page import *
from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import get_order_print_history


class WaitBuyerConfirmGoods:
    order_status_anchor = ('and', (('attr=', ('text', '阻止Ta拍单')),))
    check_address_button_locator = ('and', (('attr=', ('text', '核对地址')),))  # 核对地址
    scan_delivery_button_locator = ('and', (('attr=', ('text', '扫码发货')),))  # 扫码发货按钮
    delivery_button_locator = ('and', (('attr=', ('text', '发货')),))  # 发货按钮
    modify_address_button_anchor = ('and', (('attr=', ('text', '收货地址')),))
    bound_print_history_anchor = ('and', (('attr=', ('text', '打印信息')),))
    num_of_combining_order_locator = ('and', (('attr.*=', ('text', '\\d笔订单进行了合单')),))  # 合单订单的合单数量信息
    cancel_combine_button_locator = ('and', (('attr=', ('text', '取消合单')),))  # 取消合单按钮
    enter_detail_page_anchor = ('and', (('attr=', ('text', '备注')),))
    detail_check_address_locator = ('and', (('attr=', ('text', '核对地址')),))  # 详情页核对地址图标
    detail_delivery_locator = ('and', (('attr=', ('text', '立即发货')),))  # 详情页立即发货图标
    detail_check_order_locator = ('and', (('attr=', ('text', '核对订单')),))  # 详情页核对订单图标
    detail_modify_address_button_locator = ('and', (('attr=', ('text', '修改地址')),))  # 详情页修改地址图标
    detail_modify_property_locator = ('and', (('attr=', ('text', '修改属性')),))  # 详情页修改地址图标
    detail_check_locator = ('and', (('attr=', ('text', '阻止Ta拍单')),))

    # 方法：获取订单状态文本
    def get_order_status(self):
        order_status_element = locate_by_anchor(init_element(self.order_status_anchor))
        return get_text_of_view(locate_by_anchor(order_status_element, 3, 'v0l0'))

    # 方法：列表，跳转旺旺，获取核对地址短语
    def get_list_check_address_phrase(self):
        check = init_element(self.order_status_anchor)
        check.wait_for_appearance(5)
        ay_click(self.check_address_button_locator)
        poco("com.taobao.qianniu:id/chat_inputtext").wait_for_appearance(5)
        wangwang_check_address_info = poco("com.taobao.qianniu:id/chat_inputtext").get_text()
        poco("com.taobao.qianniu:id/chat_send").click()
        if poco('com.taobao.qianniu:id/alert_title').exists():
            poco('com.taobao.qianniu:id/alert_positivebutton').click()
            poco("com.taobao.qianniu:id/chat_send").click()
        poco("com.taobao.qianniu:id/display").click()
        return wangwang_check_address_info

    def go_detail_page(self):
        """
        订单列表，点击商品标题进入详情页面
        :return:
        """
        enter_detail_page_element = locate_by_anchor(init_element(self.enter_detail_page_anchor), 3, 'v2')
        enter_detail_page_element.click()
        detail_check = init_element(self.detail_check_locator)
        detail_check.wait_for_appearance(5)

    # 方法：详情，跳转旺旺，获取核对地址短语
    def get_detail_check_address_phrase(self):
        # ay_click(self.detail_check_address_locator)
        address = init_element(self.modify_address_button_anchor)
        check_address = locate_by_anchor(address, 2, 'v2l0')
        check_address.click()
        wangwang_check_address_info = poco("com.taobao.qianniu:id/chat_inputtext").get_text()
        poco("com.taobao.qianniu:id/chat_send").click()
        if poco('com.taobao.qianniu:id/alert_title').exists():
            poco('com.taobao.qianniu:id/alert_positivebutton').click()
            poco("com.taobao.qianniu:id/chat_send").click()
        poco("com.taobao.qianniu:id/display").click()
        return wangwang_check_address_info

    # 方法：列表页，检查核对地址内容
    def check_list_page_send_check_address_phrase(self):
        wangwang_check_address_info = self.get_list_check_address_phrase()
        check_element = [self.order_detail['收件人姓名'], self.order_detail['收件人手机'], self.order_detail['收件地址']]
        does_check_address_right = True
        for x in check_element:
            if x not in wangwang_check_address_info:
                does_check_address_right = False
        return does_check_address_right, wangwang_check_address_info, check_element

    # 方法：详情页，检查核对地址内容
    def check_detail_page_send_check_address_phrase(self, order_no):
        self.go_detail_page()
        wangwang_check_address_info = self.get_detail_check_address_phrase()
        check_element = [self.order_detail['收件人姓名'], self.order_detail['收件人手机'], self.order_detail['收件地址']]
        does_check_address_right = True
        for x in check_element:
            if x not in wangwang_check_address_info:
                does_check_address_right = False
        return does_check_address_right, wangwang_check_address_info, check_element

    # 方法：已经绑定过单号的订单，对比打印信息
    def check_order_print_history(self):
        print_history_info = get_order_print_history(self.order_detail['订单号'])
        does_order_print_history_right = True
        actual_print_history = None
        my_print_history = None
        # 没有绑定打印记录的订单
        if not print_history_info['绑定的单号']:
            if poco(text='打印信息').exists():
                does_order_print_history_right = False
        # 绑定了打印记录的订单
        else:
            actual_print_history = print_history_info['绑定的物流公司'][0] + ' ' + print_history_info['绑定的单号'][0]
            bound_print_history_element = locate_by_anchor(init_element(self.bound_print_history_anchor), 1, 'l1')
            my_print_history = get_text_of_view(bound_print_history_element)
            if my_print_history != actual_print_history:
                does_order_print_history_right = False
        return does_order_print_history_right, actual_print_history, my_print_history

    # 方法：点击扫码发货按钮，扫码后进入发货page
    def scan_to_deliver(self):
        ay_swipe(self.order_status_anchor, 'up')
        ay_click(self.scan_delivery_button_locator)
        if poco(text='同意').exists():
            poco(text='同意').click()

        poco("com.taobao.qianniu:id/btn_album").click()
        poco(name='com.android.documentsui:id/thumbnail').click()
        if poco(text='确认').exists():
            poco(text='确认').click()

        return SendGoodsPage()

    # 方法：详情页点击扫码发货按钮，扫码后进入发货page
    def detail_scan_to_deliver(self):
        self.go_detail_page()
        ay_click(self.scan_delivery_button_locator)
        poco("com.taobao.qianniu:id/btn_album").click()
        poco(name='com.android.documentsui:id/thumbnail').click()
        if poco(text='确认').exists():
            poco(text='确认').click()

        return SendGoodsPage()

    # 方法：点击发货按钮，进入发货page
    def go_to_deliver(self):
        ay_swipe(self.order_status_anchor, 'up')
        ay_click(self.delivery_button_locator)
        if poco(text='确认').exists():
            poco(text='确认').click()
        return SendGoodsPage()

    # 方法：详情页，点击发货按钮，进入发货page
    def detail_go_to_deliver(self):
        self.go_detail_page()
        ay_click(self.detail_delivery_locator)
        if poco(text='确认').exists():
            poco(text='确认').click()

        return SendGoodsPage()

    # 方法：点击修改地址，进入修改地址page
    def go_to_modify_address(self):
        ay_swipe(self.order_status_anchor, 'up')
        modify_address_button_element = locate_by_anchor(init_element(self.modify_address_button_anchor), 1, 'l3')
        modify_address_button_element.click()
        if poco(text='温馨提示').exists():  # 之前用例层复制地址，这里可能会存在弹窗提示
            poco(text='确认').click()
        return ModifyAddressPage()

    # 方法：详情页点击修改地址，进入修改地址page
    def detail_go_to_modify_address(self):
        ay_swipe(self.order_status_anchor, 'up')  # 手指上滑保证能找到修改地址按钮
        self.go_detail_page()
        ay_click(self.detail_modify_address_button_locator)
        if poco(text='温馨提示').exists():  # 之前用例层复制地址，这里可能会存在弹窗提示
            poco(text='确认').click()
        modify_address_page = ModifyAddressPage()
        return modify_address_page

    # 方法：发送核对订单短语
    def send_check_order_phrase(self):
        ay_swipe(self.order_status_anchor, 'up')
        ay_click(self.detail_check_order_locator)
        wangwang_check_order_info = poco("com.taobao.qianniu:id/chat_inputtext").get_text()
        poco("com.taobao.qianniu:id/chat_send").click()
        if poco('com.taobao.qianniu:id/alert_title').exists():
            poco('com.taobao.qianniu:id/alert_positivebutton').click()
            poco("com.taobao.qianniu:id/chat_send").click()
        poco("com.taobao.qianniu:id/display").click()
        return wangwang_check_order_info

    # 方法：详情页点击修改属性，进入修改属性页
    def detail_go_to_modify_property(self):
        self.go_detail_page()
        ay_swipe(self.order_status_anchor, 'up')
        ay_click(self.detail_modify_property_locator)

    def modify_sku(self):
        size_locator = ('and', (('attr=', ('text', SKU[0])),))
        material_locator = ('and', (('attr=', ('text', SKU[2])),))
        ay_click(size_locator)
        ay_click(material_locator)
        ay_click(self.modify_sku_now_locator)


if __name__ == '__main__':
    o = WaitBuyerConfirmGoods()
    o.send_check_order_phrase()
