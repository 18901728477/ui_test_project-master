import allure
import warnings
import pytest

from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import get_order_detail, get_rate_num

warnings.filterwarnings('ignore')


class TestSeller_rate:

    @allure.feature('订单列表评价')
    @allure.story('旺旺催好评')
    @pytest.mark.skip(reason="评价后会消耗测试数据")
    def test_ww_give_rate(self, need_seller_rate):
        """

        :param need_seller_rate:
        :return:
        """
        ww_page = need_seller_rate[0]
        ww_page.ww_rate()
        news = ww_page.ww_new_get()
        assert need_seller_rate[1] in news, '核对订单号为{},链接中订单号为{}'.format(need_seller_rate[1], news)

    @allure.feature('订单列表评价')
    @allure.story('选择评价短语给予好评')
    @pytest.mark.skip(reason="评价后会消耗测试数据")
    def test_give_good(self, need_seller_rate):
        """

        :param need_seller_rate:
        :return:
        检查逻辑:
        搜索订单
        点击立即评价
        选择填充短语后评价

        """
        need_seller_rate_page = need_seller_rate[0]
        new_page = need_seller_rate_page.single_rate()
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

    @allure.feature('订单列表评价')
    @allure.story('自定义填充评价短语给予好评')
    @pytest.mark.skip(reason="评价后会消耗测试数据")
    def test_give_good_free(self, need_seller_rate):
        """

        :param need_seller_rate:
        :return:
        搜索订单
        点击立即评价
        手动输入评价短语内容后评价
        """
        need_seller_rate_page = need_seller_rate[0]
        new_page = need_seller_rate_page.single_rate()
        set_rate_news = new_page.insert_phrase_by_custom()
        new_page.evaluate_now()
        seller_rate = get_order_detail(need_seller_rate[1])['评价状态'][0]
        assert set_rate_news, '填充短语异常'
        assert seller_rate, '评价功能异常'

    @allure.feature('订单列表评价')
    @allure.story('批量给予好评')
    @pytest.mark.skip(reason="评价后会消耗测试数据")
    def test_batch_give_good(self, need_seller_rate_list):
        """

        :param need_seller_rate_list:
        :return:
        点击批量评价
        选择填充短语后评价
        """
        need_seller_rate_page = need_seller_rate_list
        new_page = need_seller_rate_page.batch_rate()
        choose_bad_news = new_page.choose_bad_batch()
        choose_good_news = new_page.choose_good_batch()
        choose_mid_news = new_page.choose_mid_batch()
        set_rate_news = new_page.insert_phrase()
        new_page.evaluate_now()
        assert choose_good_news, '选择好评不可用'
        assert choose_bad_news, '选择差评不可用'
        assert choose_mid_news, '选择中评不可用'
        assert set_rate_news[0], '插入短语异常'
        assert get_rate_num() == 0, '批量评价失败'

    @allure.feature('订单列表评价')
    @allure.story('自定义批量给予好评')
    @pytest.mark.skip(reason="评价后会消耗测试数据")
    def test_batch_give_good_free(self, need_seller_rate_list):
        """

        :param need_seller_rate_list:
        :return:
        点击批量评价
        手动输入评价短语内容后评价
        """
        need_seller_rate_page = need_seller_rate_list
        new_page = need_seller_rate_page.batch_rate()
        set_rate_news = new_page.insert_phrase_by_custom()
        new_page.evaluate_now()
        assert set_rate_news, '填充短语异常'
        assert get_rate_num() == 0, '批量评价失败'
