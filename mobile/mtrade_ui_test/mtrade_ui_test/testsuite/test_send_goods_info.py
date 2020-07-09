import allure
import warnings
import pytest

from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import get_logistics_choose, get_order_detail,time_calculation


class TestWaiBuyerConfirmGoods:

    @allure.feature('已发货订单详情页面')
    @allure.story('发送物流消息')
    def test_ww_send_logistics(self, wait_buyer_confirm_goods):
        """
        已发货订单需补充检查物流信息
        :param wait_buyer_confirm_goods:
        :return:
        """
        order_page = wait_buyer_confirm_goods
        order_page.go_detail_page()
        page_news = order_page.get_logistics()
        order_page.info_send_logtics_news()
        news = order_page.ww_new_get()
        assert page_news['company'] in news, '物流公司不匹配，预计为{}，实际为{}'.format(page_news['company'], news)
        assert page_news['company_id'] in news, '物流单号不匹配，预计为{}，实际为{}'.format(page_news['company_id'], news)
        assert page_news['company_info'] in news, '物流信息不匹配，预计为{}，实际为{}'.format(page_news['company_info'], news)

    @allure.feature('已发货订单详情页面')
    @allure.story('刷新物流消息')
    def test_info_refresh_logistics(self, wait_buyer_confirm_goods):
        """
        1、根据订单号搜索已发货订单
        2、点击商品标题进入订单详情页面
        3、点击刷新物流按钮
        4、校验物流公司，运单号，状态是否正确
        5、目前已知物流状态存在BUG
        :param shipped_orderlist:
        :return:
        """
        order_page = wait_buyer_confirm_goods[0]
        order_page.go_detail_page()
        order_page.info_refresh_logistics()
        page_news = order_page.get_logistics()
        news = get_logistics_choose(wait_buyer_confirm_goods[1])
        assert page_news['company'] in news['物流公司'], '刷新物流异常，预计为{}，实际为{}'.format(page_news['company'], news['物流公司'])
        assert page_news['company_id'] in news['运单号'], '刷新物流异常，预计为{}，实际为{}'.format(page_news['company_id'], news['运单号'])

    @allure.feature('已发货订单详情页面')
    @allure.story('延长收货时间')
    @pytest.mark.skip(reason="影响订单数据")
    def test_info_suretime(self, wait_buyer_confirm_goods):
        """

        :param wait_buyer_confirm_goods:
        :return:
        """
        order_page = wait_buyer_confirm_goods[0]
        order_page.go_detail_page()
        start_time = get_order_detail(wait_buyer_confirm_goods[1])['预计结束时间']
        order_page.extended_receiving_time()
        end_time = get_order_detail(wait_buyer_confirm_goods[1])['预计结束时间']
        time_difference = time_calculation(start_time, end_time)
        assert str(time_difference) == '3', '延长收货时间为{}'.format(time_difference)
