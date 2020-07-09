from poco.exceptions import PocoNoSuchNodeException

from mobile.mtrade_ui_test.mtrade_ui_test.data import ITEM_INFO, ORDER_INFO
from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import BasePage, ay_click, poco, locate_by_anchor, init_element, get_text_of_view
from mobile.mtrade_ui_test.mtrade_ui_test.pages.order_list_page import OrderListPage
from mobile.mtrade_ui_test.mtrade_ui_test.pages.ww_chat_page import WwChatPage


class OrderDetailPage(OrderListPage):
    check_address_locator = ('and', (('attr=', ('text', '核对地址')),))  # 核对地址
    ww_remind_locator = ('and', (('attr=', ('text', '旺旺催付')),))  # 旺旺催付
    modify_price_locator = ('and', (('attr=', ('text', '修改价格')),))  # 修改价格
    block_ta_locator = ('and', (('attr=', ('text', '阻止Ta拍单')),))  # 阻止Ta拍单
    remark_locator = ('and', (('attr=', ('text', '备注')),))  # 备注
    message_locator = ('and', (('attr=', ('text', '留言')),))  # 留言
    addressee_locator = ('and', (('attr=', ('text', '收件人')),))  # 收件人
    address_locator = ('and', (('attr=', ('text', '收货地址')),))  # 收货地址
    send_logtics_locator = ('and', (('attr=', ('text', '发送物流')),))  # 发送物流
    logistics_company_locator = ('and', (('attr=', ('text', '物流公司')),))  # 物流公司
    order_no_lab_locator = ('and', (('attr=', ('text', '订单编号')),))  # 订单编号

    def ww_remind(self):
        ay_click(self.ww_remind_locator)
        res = WwChatPage().get_chat_text_and_return()
        return res

    # 发送物流消息
    def send_logtics(self):
        ay_click(self.send_logtics_locator)
        res = WwChatPage().get_chat_text_and_return()
        return res

    def check_order_no(self, _order_no):
        order_no_lab = init_element(self.order_no_lab_locator)
        order_no_info = locate_by_anchor(order_no_lab, parent_lv=1, child_lv='l1l0')
        order_no_text = order_no_info.get_text()
        if order_no_text != _order_no:
            return False
        else:
            return True

    # 核对普通订单信息
    def check_order_info_detail_page(self):
        return self.check_order_info()

    def check_order_item_detail_page(self, _item_view):
        return self.check_order_first_item(_item_view)

    def check_order_remark_detail_page(self, _remark_view):
        return self.check_order_remark(_remark_view)

    def check_order_addressee_detail_page(self, _addressee_view):
        try:
            addressee_info = locate_by_anchor(_addressee_view, child_lv='v0l1')
            addressee_info_text = get_text_of_view(addressee_info)
            mobile_info = locate_by_anchor(_addressee_view, child_lv='v0l1l1l0')
            mobile_info_text = get_text_of_view(mobile_info)
            address_info = locate_by_anchor(_addressee_view, child_lv='v1l1')
            address_info_text = get_text_of_view(address_info)
            if addressee_info_text != ORDER_INFO.get('收件人姓名'):
                return False, '订单的收件人姓名信息显示不正确'
            if mobile_info_text != ORDER_INFO.get('收件人手机f'):
                return False, '订单的收件人手机号信息显示不正确'
            if address_info_text != ORDER_INFO.get('收货地址'):
                return False, '订单的收货地址信息显示不正确'
            return True, ''
        except PocoNoSuchNodeException:
            return False, '订单收货信息部分界面异常或者数据异常，请重新检查用例设计'


if __name__ == '__main__':
    o = OrderDetailPage()
    remark = init_element(o.remark_locator)
    remark_view = remark.parent().parent()
    item_name = init_element(o.item_name_locator)
    item_view = locate_by_anchor(item_name, parent_lv=4)
    addressee = init_element(o.addressee_locator)
    addressee_view = locate_by_anchor(addressee, parent_lv=2)
    print(o.check_order_item_detail_page(item_view))
    print(o.check_order_remark_detail_page(remark_view))
    print(o.check_order_addressee_detail_page(addressee_view))
