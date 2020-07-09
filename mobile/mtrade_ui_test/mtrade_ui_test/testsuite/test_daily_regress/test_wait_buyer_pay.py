import pytest

from mobile.mtrade_ui_test.mtrade_ui_test.data import WW_REMIND, CHECK_ADDRESS_PHRASE
from mobile.mtrade_ui_test.mtrade_ui_test.pages.order_detail_page import OrderDetailPage
from mobile.mtrade_ui_test.mtrade_ui_test.pages.order_list_page import OrderListPage
import allure


class TestWaitBuyerPay:

    @allure.feature('待付款订单列表')
    @allure.story('检查订单详细信息')
    def test_check_order(self, wait_buyer_pay):
        """
        pass
        检查逻辑：
        1、通过订单号搜索订单
        2、校验订单收件人、商品名称、属性，编码等信息显示是否与预期指定文本一致
        :param wait_buyer_pay: fixture
        """
        res = wait_buyer_pay.check_order_info()
        assert res[0], res[1]

    # @allure.feature('待付款订单列表')
    # @allure.story('购物车订单旺旺催付')
    # def test_check_order_cart(self, wait_buyer_pay_cart):
    #     """
    #     pass
    #     检查逻辑：
    #     1、通过订单号搜索订单
    #     2、点击旺旺催付按钮，跳转旺旺
    #     3、获取旺旺聊天窗短语内容
    #     4、检查旺旺聊天窗催付内容与默认设置短语是否一致
    #     :param wait_buyer_pay_cart:
    #     :return:
    #     """
    #     res = wait_buyer_pay_cart.check_order_info()
    #     assert res[0], res[1]

    @allure.feature('待付款订单列表')
    @allure.story('复制收件人手机号')
    def test_copy_mobile_number(self, wait_buyer_pay):
        """
        pass
        测试复制手机号码功能
        1、点击收件人手机号
        2、选择复制号码
        3、将号码粘贴到搜索栏
        4、验证搜索栏中文本是否与收件人手机号一致
        :param wait_buyer_pay:
        :return:
        """
        order_list_page = wait_buyer_pay
        expected = order_list_page.copy_mobile_number()
        result, actual = order_list_page.ensure_copy_info(expected)
        assert result, '期望值为{},剪贴版中值为{},两者不相等'.format(expected, actual)

    @allure.feature('待付款订单列表')
    @allure.story('复制收货信息')
    def test_copy_receiver_info(self, wait_buyer_pay):
        """
        pass
        1、点击收货地址
        2、选择复制收货信息
        3、将信息粘贴到搜索栏
        4、验证搜索栏中文本是否与收货地址一致
        :param wait_buyer_pay:
        :return:
        """
        order_list_page = wait_buyer_pay
        expected = order_list_page.copy_receiver_info()
        result, actual = order_list_page.ensure_copy_info(expected)
        assert result, '期望值为{},剪贴版中值为{},两者不相等'.format(expected, actual)

    @allure.feature('待付款订单列表')
    @allure.story('查看买家所有订单')
    def test_show_all_order(self, wait_buyer_pay):
        """
        pass
        1、进入订单列表
        2、点击Ta所有订单
        3、检查订单列表中的订单号数量与买家昵称的数量是否一致
        :param wait_buyer_pay:
        :return:
        """
        order_list_page = wait_buyer_pay
        buy_nick_counts = order_list_page.show_all_orders_of_buyer() - 1  # 搜索框中会显示买家昵称，所以需要减1
        order_counts = order_list_page.get_order_counts()  # 统计当前页面上的订单数量
        assert order_counts == buy_nick_counts, '当前页面存在{}条订单，其中只有{}条订单买家昵称显示正确'.format(order_counts,
                                                                                       buy_nick_counts)

    @allure.feature('待付款订单列表')
    @allure.story('查看待发货订单')
    def test_choose_wait_seller_send_goods(self, wait_buyer_pay):
        """
        pass
        1、进入订单列表
        2、滑动导航栏点击待发货
        3、查看订单列表中应只显示待发货订单或者无订单
        :param
        :return:
        """
        res = wait_buyer_pay.choose_wait_seller_send_goods()
        wait_buyer_pay.waiting_for_order(10)
        assert res[0], res[1]

    @allure.feature('待付款订单列表')
    @allure.story('查看待付款订单')
    def test_choose_wait_buyer_pay(self, wait_buyer_pay):
        """
        pass
        1、进入订单列表
        2、滑动导航栏点击待付款
        :param wait_buyer_pay:
        :return:
        """
        res = wait_buyer_pay.choose_wait_buyer_pay()
        wait_buyer_pay.waiting_for_order(10)
        assert res[0], res[1]

    @allure.feature('待付款订单列表')
    @allure.story('查看已关闭订单')
    def test_choose_all_closed(self, wait_buyer_pay):
        """
        pass
        1、进入订单列表
        2、滑动导航栏点击已关闭
        :param wait_buyer_pay:
        :return:
        """
        res = wait_buyer_pay.choose_all_closed()
        wait_buyer_pay.waiting_for_order(10)
        assert res[0], res[1]

    @allure.feature('待付款订单列表')
    @allure.story('查看已成功订单')
    def test_choose_trade_finished(self, wait_buyer_pay):
        """
        pass
        1、进入订单列表
        2、滑动导航栏点击已成功
        :param wait_buyer_pay:
        :return:
        """
        res = wait_buyer_pay.choose_trade_finished()
        wait_buyer_pay.waiting_for_order(10)
        assert res[0], res[1]

    @allure.feature('待付款订单列表')
    @allure.story('查看需要评价订单')
    def test_choose_need_rate(self, wait_buyer_pay):
        """
        pass
        1、进入订单列表
        2、滑动导航栏点击需要评价

        :param wait_buyer_pay:
        :return:
        """
        res = wait_buyer_pay.choose_need_rate()
        wait_buyer_pay.waiting_for_order(10)
        assert res[0], res[1]

    @allure.feature('待付款订单列表')
    @allure.story('查看已发货订单')
    def test_choose_wait_buyer_confirm_goods(self, wait_buyer_pay):
        """
        pass
        1、进入订单列表
        2、滑动导航栏点击已发货
        :param wait_buyer_pay:
        :return:
        """
        res = wait_buyer_pay.choose_wait_buyer_confirm_goods()
        wait_buyer_pay.waiting_for_order(10)
        assert res[0], res[1]

    @allure.feature('待付款订单列表')
    @allure.story('查看退款中订单')
    def test_choose_trade_refund(self, wait_buyer_pay):
        """
        1、进入订单列表
        2、滑动导航栏点击退款中
        :param wait_buyer_pay:
        :return:
        """
        res = wait_buyer_pay.choose_trade_refund()
        wait_buyer_pay.waiting_for_order(10)
        assert res[0], res[1]

    @allure.feature('待付款订单列表')
    @allure.story('查看近三个月订单')
    def test_choose_three_month(self, wait_buyer_pay):
        """
        pass
        1、进入订单列表
        2、滑动导航栏点击近三个月
        :param wait_buyer_pay:
        :return:
        """
        res = wait_buyer_pay.choose_three_month()
        wait_buyer_pay.waiting_for_order(10)
        assert res, '近三个月标签栏未处于选中状态'

    @allure.feature('待付款订单列表')
    @allure.story('普通订单旺旺催付')
    def test_ww_reminder(self, wait_buyer_pay):
        """
        pass
        检查逻辑：
        1、通过订单号搜索订单
        2、点击旺旺催付按钮，跳转旺旺
        3、获取旺旺聊天窗短语内容
        4、检查旺旺聊天窗催付内容与默认设置短语是否一致
        :param wait_buyer_pay:
        :return:
        """
        actual = wait_buyer_pay.ww_reminder()
        expect = WW_REMIND
        assert expect == actual, '期望旺旺催付短语为：{}，实际为：{}'.format(expect, actual)

    @allure.feature('待付款订单列表')
    @allure.story('修改价格')
    def test_modify_price(self, wait_buyer_pay):
        """
        pass
        检查逻辑：
        1、通过订单号搜索订单
        2、点击修改价格
        3、获取修改后的价格，判断是否修改成功
        :param wait_buyer_pay:
        :return:
        """
        wait_buyer_pay.modify_price('0.02')
        actual = wait_buyer_pay.get_price()
        assert actual == '0.02', '期望修改后的价格为0.02，实际为：{}'.format(actual)

    @allure.feature('待付款订单列表')
    @allure.story('核对地址')
    def test_check_address(self, wait_buyer_pay):
        """
        pass
        检查逻辑：
        1、通过订单号搜索订单
        2、点击 地址
        3、比对旺旺聊天窗口的内容是否与预期一致
        :param wait_buyer_pay:
        :return:
        """
        actual = wait_buyer_pay.check_address()
        expect = CHECK_ADDRESS_PHRASE
        assert expect == actual, '期望修改地址短语为:{}，实际为：{}'.format(expect, actual)

    @allure.feature('待付款订单列表')
    @allure.story('关闭订单')
    def test_close_order(self, wait_buyer_pay):
        """
        pass
        检查逻辑：
        1、通过订单号搜索订单
        2、点击关闭订单
        3、查看是否存在确认关闭按钮
        4、返回订单列表
        :param wait_buyer_pay:
        :return:
        """
        res = wait_buyer_pay.close_order()
        assert res, '关闭订单按钮功能异常'

    @allure.feature('待付款订单详情')
    @allure.story('检查订单信息')
    def test_check_order_detail_page(self, wait_buyer_pay):
        """
        pass
        检查逻辑：
        1、通过订单号搜索订单
        2、点击商品标题进入订单详情
        3、校验订单信息
        :param wait_buyer_pay:
        :return:
        """
        wait_buyer_pay.go_detail_page()
        res = OrderDetailPage().check_order_info()
        assert res[0], res[1]

    @allure.feature('待付款订单详情')
    @allure.story('核对地址')
    def test_check_address_detail_page(self, wait_buyer_pay):
        """
        pass
        检查逻辑：
        1、通过订单号搜索订单
        2、点击商品标题进入订单详情
        3、检查核对地址短语是否正确
        :param wait_buyer_pay:
        :return:
        """
        wait_buyer_pay.go_detail_page()
        actual = OrderDetailPage().check_address()
        expect = CHECK_ADDRESS_PHRASE
        assert expect == actual, '期望修改地址短语为:{}，实际为：{}'.format(expect, actual)

    @allure.feature('待付款订单详情')
    @allure.story('关闭订单')
    def test_close_order_detail_page(self, wait_buyer_pay):
        """
        pass
        检查逻辑：
        1、通过订单号搜索订单
        2、点击商品标题进入订单详情
        3、检查关闭订单按钮功能是否正常
        :param wait_buyer_pay:
        :return:
        """
        wait_buyer_pay.go_detail_page()
        res = OrderDetailPage().close_order()
        assert res, '关闭订单按钮功能异常'

    @allure.feature('待付款订单详情')
    @allure.story('旺旺催付')
    def test_ww_reminder_detail_page(self, wait_buyer_pay):
        """
        pass
        检查逻辑：
        1、通过订单号搜索订单
        2、点击商品标题进入订单详情
        3、点击旺旺催付按钮，跳转旺旺
        4、获取旺旺聊天窗短语内容
        5、检查旺旺聊天窗催付内容与默认设置短语是否一致
        :param wait_buyer_pay:
        :return:
        """
        wait_buyer_pay.go_detail_page()
        actual = OrderDetailPage().ww_reminder()
        expect = WW_REMIND
        assert expect == actual, '期望旺旺催付短语为：{}，实际为：{}'.format(expect, actual)

    @allure.feature('待付款订单详情')
    @allure.story('修改价格')
    def test_modify_price_detail_page(self, wait_buyer_pay):
        """
        pass
        检查逻辑：
        1、通过订单号搜索订单
        2、点击商品标题进入订单详情
        3、点击修改价格
        4、获取修改后的价格，判断是否修改成功
        :param wait_buyer_pay:
        :return:
        """
        wait_buyer_pay.go_detail_page()
        OrderDetailPage().modify_price('0.02')
        actual = OrderDetailPage().get_price()
        assert actual == '0.02', '期望修改后的价格为0.02，实际为：{}'.format(actual)
