import allure
import pytest
from mobile.mtrade_ui_test.mtrade_ui_test.pages.batch_send_goods_page import BatchSendGoodsPage
import time


class TestBatchSendGoods:

    @allure.feature('批量发货')
    @allure.story('跳转批量发货页面')
    # @pytest.mark.skip(reason='已知BUG')
    def test_go_batch_send_goods_page(self, batch_send_goods_page_by_scan):
        """
        1.点击首页批量发货按钮，进入批量发货列表
        2.点击列表全部发货按钮，跳转批量发货页面
        3.检查页面是否跳转成功
        :param batch_send_goods_page_by_scan:
        :return:
        """
        result = batch_send_goods_page_by_scan.go_batch_send_goods_page2()
        assert result, "跳转页面失败"

    @allure.feature('批量发货')
    @allure.story('选择自己联系发货')
    def test_choose_offline_delivery(self, batch_send_goods_page_by_scan):
        """
        1.批量发货列表进入批量发货页面
        2.选择自己联系发货方式
        3.检查发货方式是否选择成功
        :param batch_send_goods_page_by_scan:
        :return:
        """
        batch_send_goods_page_by_scan.go_batch_send_goods_page2()
        result = batch_send_goods_page_by_scan.choose_offline_delivery()
        assert result, "选择自己联系发货失败"

    @allure.feature('批量发货')
    @allure.story('选择在线下单发货')
    def test_choose_online_delivery(self, batch_send_goods_page_by_scan):
        """
         1.批量发货列表进入批量发货页面
         2.选择在线下单发货方式
         3.检查发货方式是否选择成功
         :param batch_send_goods_page_by_scan:
         :return:
         """
        BatchSendGoodsPage().go_batch_send_goods_page2()
        time.sleep(5)
        result = BatchSendGoodsPage().choose_online_delivery()
        assert result, "选择在线下单发货失败"

    @allure.feature('批量发货')
    @allure.story('选择无需物流发货')
    def test_choose_dummy_delivery(self, batch_send_goods_page_by_scan):
        """
         1.批量发货列表进入批量发货页面
         2.选择无需物流发货方式
         3.检查发货方式是否选择成功
         :param batch_send_goods_page_by_scan:
         :return:
         """
        BatchSendGoodsPage().go_batch_send_goods_page2()
        result = BatchSendGoodsPage().choose_dummy_delivery()
        assert result, "选择无需物流发货失败"

    @allure.feature('批量发货')
    @allure.story('稍后处理')
    def test_pending_handle(self, batch_send_goods_page_by_scan):
        """
        1.进入批量发货列表，选择单笔订单，跳转批量发货页面
        2.点击稍后处理
        3.检查订单是否消失
        :param batch_send_goods_page_by_scan:
        :return:
        """
        batch_send_goods_page_by_scan.choose_single_order()
        batch_send_goods_page_by_scan.go_batch_send_goods_page2()
        result = batch_send_goods_page_by_scan.pending_handle()
        batch_send_goods_page_by_scan.refresh()
        assert result, "稍后处理失败"

    @allure.feature('批量发货')
    @allure.story('选择快递公司')
    def test_choose_deliver_company(self, batch_send_goods_page_by_scan):
        """
        1.进入批量发货列表，选择单笔订单，跳转批量发货页面
        2.选择快递公司为顺丰速运
        3.检查快递公司是否选择成功
        :param batch_send_goods_page_by_scan:
        :return:
        """
        batch_send_goods_page_by_scan.choose_single_order()
        batch_send_goods_page_by_scan.go_batch_send_goods_page2()
        result = batch_send_goods_page_by_scan.choose_deliver_company()
        assert result, "选择快递失败"

    @allure.feature('批量发货')
    @allure.story('全部发货')
    @pytest.mark.skip(reason="避免消耗所有订单数据")
    def test_all_deliver(self, init_app_by_scan):
        """
        1.进入批量发货列表，选择单笔订单，跳转批量发货页面
        2.点击全部发货
        3.检查待发货数量是否发生变化，判断是否发货成功
        :param init_app:
        :return:
        """
        first_page = init_app
        batch_send_goods_list = first_page.go_batch_send_goods_page2()
        BatchSendGoodsPage().choose_single_order()
        actual_number = get_wait_send_goods_number()
        expected_number = batch_send_goods_list.all_deliver()
        first_page.refresh()
        assert expected_number != actual_number, '发货前订单数量为{},发货后订单数量为{}'.format(actual_number, expected_number)
