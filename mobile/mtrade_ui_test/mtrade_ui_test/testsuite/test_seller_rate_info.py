import allure
import warnings
import pytest

from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import get_order_detail

warnings.filterwarnings('ignore')


class TestSellerrate_info:

    @allure.feature('待评价订单详情评价')
    @allure.story('选择短语评价订单')
    @pytest.mark.skip(reason="评价后会消耗测试数据")
    def test_ww_send_logistics(self, need_seller_rate):
        """

        :param need_seller_rate:
        :return:
        """
        order_page = need_seller_rate[0]
        order_page.to_order_detaiinfo()
        new_page = order_page.single_rate()
        choose_bad_news = new_page.choose_bad()
        choose_good_news = new_page.choose_good()
        choose_mid_news = new_page.choose_mid()
        set_rate_news = new_page.insert_phrase()
        new_page.evaluate_now()
        seller_rate = get_order_detail(need_seller_rate[1])['评价状态'][0]
        assert choose_good_news, '选择好评不可用'
        assert choose_bad_news, '选择差评不可用'
        assert choose_mid_news, '选择中评不可用'
        assert set_rate_news[0], '插入短语异常'
        assert seller_rate, '评价功能异常'

    @allure.feature('待评价订单详情评价')
    @allure.story('自定义短语评价订单')
    @pytest.mark.skip(reason="评价后会消耗测试数据")
    def test_ww_send_logistics(self, need_seller_rate):
        """

        :param need_seller_rate:
        :return:
        """
        order_page = need_seller_rate[0]
        order_page.to_order_detaiinfo()
        new_page = order_page.single_rate()
        set_rate_news = new_page.insert_phrase_by_custom()
        new_page.evaluate_now()
        seller_rate = get_order_detail(need_seller_rate[1])['评价状态'][0]
        assert set_rate_news, '填充短语异常'
        assert seller_rate, '评价功能异常'


