import allure
import pytest

from mobile.mtrade_ui_test.mtrade_ui_test.data import WW_REMIND
from mobile.mtrade_ui_test.mtrade_ui_test.pages.order_list_page import OrderListPage


class TestOrderInfo:

    @allure.feature('待付款详情')
    @allure.story('单笔旺旺催付')
    def test_ww_reminder_info(self, wait_buyer_pay):
        """
        检查逻辑：
        1、通过订单号搜索订单
        2、点击旺旺催付按钮，跳转旺旺
        3、获取旺旺聊天窗短语内容
        4、检查旺旺聊天窗催付内容与默认设置短语是否一致
        :param wait_buyer_pay:
        :return:
        """
        order_list_page = wait_buyer_pay
        order_list_page.list_buyer_nick_jump()
        order_list_page.clear_ww_chat_box()
        order_list_page.ww_return()
        order_list_page.jump_to_order_info()
        order_list_page.ww_reminder()
        actual_reminder_text = order_list_page.get_ww_chat_box()
        actual_reminder_text = actual_reminder_text.strip()
        expected_reminder_text = order_list_page.get_remind_text()
        order_list_page.clear_ww_chat_box()
        order_list_page.ww_return()
        assert actual_reminder_text == expected_reminder_text, '旺旺催付短语为：{}，实际为：{}'.format(expected_reminder_text,
                                                                                          actual_reminder_text)

    @allure.feature('待付款详情')
    @allure.story('购物车旺旺催付')
    def test_shopping_cart_ww_reminder_info(self, shopping_cart_wait_buyer_pay):
        """
        检查逻辑：
        1、通过订单号搜索订单
        2、进入订单详情页面
        3、点击旺旺催付按钮，跳转旺旺
        4、获取旺旺聊天窗短语内容
        5、检查旺旺聊天窗催付内容与默认设置短语是否一致
        :param shopping_cart_wait_buyer_pay:
        :return:
        订单状态已关闭
        """
        order_list_page = shopping_cart_wait_buyer_pay
        detail_page = order_list_page.go_order_detail_page()
        actual = detail_page.ww_remind()
        expected = WW_REMIND
        assert actual == expected, '期望旺旺催付短语为：{}，实际为：{}'.format(expected, actual)

    @allure.feature('待付款详情')
    @allure.story('单个关闭订单')
    @pytest.mark.skip(reason="关闭后会消耗测试数据")
    def test_close_order_info(self, wait_buyer_pay):
        """
        检查逻辑：
        1、通过订单号搜索订单
        2、点击关闭订单按钮，返回待付款列表
        3、获取订单状态
        4、检查订单状态是否为已关闭状态
        :param wait_buyer_pay:
        :return:
        """
        order_list_page = wait_buyer_pay
        order_list_page.jump_to_order_info()
        result = order_list_page.close_order()
        assert result, '订单关闭失败'

    @allure.feature('待付款详情')
    @allure.story('部分关闭订单')
    @pytest.mark.skip(reason="关闭后会消耗测试数据")
    def test_shopping_cart_close_order_info(self, shopping_cart_wait_buyer_pay):
        """
        检查逻辑：
        1、通过订单号搜索订单
        2、选择一个宝贝，点击关闭订单按钮，返回待付款列表
        3、获取订单状态
        4、检查订单状态是否为已关闭状态
        :param shopping_cart_wait_buyer_pay:
        :return:
        """
        order_list_page = shopping_cart_wait_buyer_pay
        order_list_page.jump_to_order_info()
        result = order_list_page.shopping_cart_close_order()
        assert result, '部分关闭订单失败'

    @allure.feature('待付款详情')
    @allure.story('修改单个订单价格')
    def test_modify_price_info(self, wait_buyer_pay):
        """
        检查逻辑：
        1、通过订单号搜索订单
        2、点击修改价格按钮，跳转修改价格页面
        3、修改订单价格，返回列表
        4、检查订单价格是否与与预期一致
        :param wait_buyer_pay: func
        :return:
        """
        wait_buyer_pay.modify_price('0.05')  # 修改价格
        actual = wait_buyer_pay.get_price()  # 获取页面上的价格
        assert actual == '0.05', '期望修改价格为0.05，实际得到价格为{}'.format(actual)

    @allure.feature('待付款详情')
    @allure.story('修改购物车订单价格')
    def test_shopping_cart_modify_price_info(self, shopping_cart_wait_buyer_pay):
        """
        检查逻辑：
        1、通过订单号搜索订单
        2、点击修改价格按钮，跳转修改价格页面
        3、修改订单价格，返回列表
        4、检查订单价格是否与与预期一致
        :param shopping_cart_wait_buyer_pay: func
        :return:
        """
        order_list_page = shopping_cart_wait_buyer_pay
        order_list_page.jump_to_order_info()
        expected_price = order_list_page.shopping_cart_modify_price()
        actual_price = order_list_page.get_price()
        order_list_page.shopping_cart_ini_price()
        assert actual_price == expected_price, '初始价格为{}，修改后价格为{}'.format(actual_price, expected_price)
