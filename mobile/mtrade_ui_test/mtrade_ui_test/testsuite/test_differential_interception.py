import allure
import warnings
import pytest

from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import get_interception_news, get_interception_status

warnings.filterwarnings('ignore')


class Testnegative_comment_interception:

    @allure.feature('差评拦截')
    @allure.story('开关开启校验')
    # @pytest.mark.skip(reason="bug")
    def test_interception_status(self, go_to_negative_comment_interception_page):
        """

        :param go_to_negative_comment_interception_page:
        :return:
        """
        interception_page = go_to_negative_comment_interception_page
        interception_page.check_MasterSwitchStatus()
        interception_page.set_interception_status()
        interception_page.check_give_me_mid_seller()
        interception_page.check_give_me_bad_seller()
        interception_page.check_black_block()
        interception_page.check_automatic_add_bad()
        #interception_page.check_cloud_bad()
        interception_page.check_than_actual_payment()
        interception_page.check_less_than_actual_payment()
        interception_page.page_swipe_for_custom(-0.7)
        interception_page.check_than_order_num()
        interception_page.check_less_than_order_num()
        interception_page.check_than_order_common_num()
        interception_page.check_less_than_order_common_num()
        interception_page.check_buyer_no_alipay()
        interception_page.check_following_keywords()
        interception_page.check_recipient_block()
        interception_page.check_area_interception()
        interception_page.check_white_ww()
        interception_page.check_white_baby()
        results = get_interception_status()
        assert results[0],'所有开关开启失败'

    @allure.feature('差评拦截')
    @allure.story('旺旺黑名单')
    # @pytest.mark.skip(reason="bug")
    def test_ww_blcaklist(self, go_to_negative_comment_interception_page):
        """

        :param go_to_negative_comment_interception_page:
        :return:
        """
        interception_page = go_to_negative_comment_interception_page
        status = interception_page.black_block_operation()
        assert status['add'], '添加失败'
        assert status['move'], '删除失败'

    @allure.feature('差评拦截')
    @allure.story('实付金额大于')
    # @pytest.mark.skip(reason="bug")
    def test_than_actual_payment(self, go_to_negative_comment_interception_page):
        """

        :param go_to_negative_comment_interception_page:
        :return:
        """
        interception_page = go_to_negative_comment_interception_page
        #interception_page.page_swipe()
        interception_page.set_than_actual_payment()
        money = interception_page.get_than_actual_payment()
        assert money == '10000元', '金额设置失败，实际为{}，预计为10000元'.format(money)

    @allure.feature('差评拦截')
    @allure.story('实付金额小于')
    # @pytest.mark.skip(reason="bug")
    def test_less_than_actual_payment(self, go_to_negative_comment_interception_page):
        """

        :param go_to_negative_comment_interception_page:
        :return:
        """
        interception_page = go_to_negative_comment_interception_page
        interception_page.page_swipe()
        interception_page.set_less_than_actual_payment()
        money = interception_page.get_less_than_actual_payment()
        assert money == '10元', '金额设置失败，实际为{}，预计为10元'.format(money)

    @allure.feature('差评拦截')
    @allure.story('订单总件数大于')
    # @pytest.mark.skip(reason="bug")
    def test_than_order_num(self, go_to_negative_comment_interception_page):
        """

        :param go_to_negative_comment_interception_page:
        :return:
        """
        interception_page = go_to_negative_comment_interception_page
        interception_page.page_swipe()
        interception_page.set_than_order_num()
        num = interception_page.get_than_order_num()
        assert num == '10件', '数量设置失败，实际为{}，预计为10件'.format(num)

    @allure.feature('差评拦截')
    @allure.story('一个订单中同一宝贝数大于')
    # @pytest.mark.skip(reason="bug")
    def test_than_common_order_num(self, go_to_negative_comment_interception_page):
        """

        :param go_to_negative_comment_interception_page:
        :return:
        """
        interception_page = go_to_negative_comment_interception_page
        interception_page.page_swipe()
        interception_page.set_than_order_common_num()
        num = interception_page.get_than_order_common_num()
        assert num == '15件', '数量设置失败，实际为{}，预计为15件'.format(num)

    @allure.feature('差评拦截')
    @allure.story('地址或留言包含以下关键字')
    # @pytest.mark.skip(reason="bug")
    def test_following_keywords(self, go_to_negative_comment_interception_page):
        """

        :param go_to_negative_comment_interception_page:
        :return:
        """
        interception_page = go_to_negative_comment_interception_page
        interception_page.page_swipe()
        interception_page.set_following_keywords()
        news = interception_page.get_following_keywords()
        assert news == '新增地址关键字信息', '关键字设置失败，实际为{}，预计为新增地址关键字信息'.format(news)

    @allure.feature('差评拦截')
    @allure.story('拦截收件人')
    # @pytest.mark.skip(reason="bug")
    def test_recipient_block(self, go_to_negative_comment_interception_page):
        """

        :param go_to_negative_comment_interception_page:
        :return:
        """
        interception_page = go_to_negative_comment_interception_page
        interception_page.page_swipe_for_custom(-0.7)
        status = interception_page.recipient_block_operation()
        assert status['add'], '添加失败'
        assert status['move'], '删除失败'

    @allure.feature('差评拦截')
    @allure.story('区域拦截')
    # @pytest.mark.skip(reason="bug")
    def test_area_interception(self, go_to_negative_comment_interception_page):
        """

        :param go_to_negative_comment_interception_page:
        :return:
        """
        interception_page = go_to_negative_comment_interception_page
        interception_page.page_swipe_for_custom(-0.7)
        status = interception_page.area_interception_operation()
        assert status['add'], '添加失败'
        assert status['move'], '删除失败'

    @allure.feature('差评拦截')
    @allure.story('旺旺白名单')
    # @pytest.mark.skip(reason="bug")
    def test_white_ww(self, go_to_negative_comment_interception_page):
        """

        :param go_to_negative_comment_interception_page:
        :return:
        """
        interception_page = go_to_negative_comment_interception_page
        interception_page.page_swipe_for_custom(-0.7)
        status = interception_page.white_ww_operation()
        assert status['add'], '添加失败'
        assert status['move'], '删除失败'

    @allure.feature('差评拦截')
    @allure.story('宝贝白名单')
    # @pytest.mark.skip(reason="bug")
    def test_white_baby_operation(self, go_to_negative_comment_interception_page):
        """

        :param go_to_negative_comment_interception_page:
        :return:
        """
        interception_page = go_to_negative_comment_interception_page
        interception_page.page_swipe_for_custom(-0.7)
        status = interception_page.white_baby_operation()
        assert status['add'], '添加失败'
        assert status['move'], '删除失败'

    @allure.feature('差评拦截')
    @allure.story('关闭理由')
    # @pytest.mark.skip(reason="bug")
    def test_close_reason(self, go_to_negative_comment_interception_page):
        """

        :param go_to_negative_comment_interception_page:
        :return:
        """
        interception_page = go_to_negative_comment_interception_page
        interception_page.page_swipe_for_custom(-0.7)
        status = interception_page.set_close_reason()
        news = interception_page.close_reason()

        assert news in status[1], '设置理由异常'
        assert status[0], '设置失败'

    # @pytest.mark.skip(reason="bug")
    def test_Interception_record(self, go_to_negative_comment_interception_page):
        """

        :param go_to_negative_comment_interception_page:
        :return:
        """
        interception_page = go_to_negative_comment_interception_page
        interception_page.page_swipe_for_custom(-1)
        interception_page.Interception_record()
        tids = get_interception_news()
        results = True
        for i in tids:
            results = results and interception_page.check_Interception_record(i)
        assert results, '拦截记录显示异常'
