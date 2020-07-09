import allure
import warnings

from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import get_order_check_send

warnings.filterwarnings('ignore')


class TestMyPage:

    @allure.feature('我的页面')
    @allure.story('备注短语')
    def test_remarks(self, go_to_my_page):
        """

        :param go_to_my_page:
        :return:
        检查逻辑：
        进入我的页面
        点击备注短语
        执行添加删除修改操作
        """
        my_page = go_to_my_page
        my_page.to_remarks()
        results = my_page.add_del_refresh_remarks()
        assert results['添加备注短语'], '添加备注短语异常'
        assert results['修改结果'], '修改备注短语异常'
        assert results['信息校验'], '信息校验异常'
        assert results['删除结果'], '删除备注短语异常'

    @allure.feature('我的页面')
    @allure.story('默认备注短语')
    def test_default_remarks(self, go_to_my_page):
        """

        :param go_to_my_page:
        :return:
        检查逻辑：
        进入我的页面
        点击备注短语
        执行添加删除修改操作
        """
        my_page = go_to_my_page
        my_page.to_remarks()
        results = my_page.default_remarks()
        assert results[0], '默认备注短语异常,缺少的内容为{}'.format(results[1])

    @allure.feature('我的页面')
    @allure.story('催付短语')
    def test_default_reminder(self, go_to_my_page):
        """

        :param go_to_my_page:
        :return:
        检查逻辑：
        进入我的页面
        点击备注短语
        执行添加删除修改操作
        """
        my_page = go_to_my_page
        my_page.to_reminder()
        news_choice = my_page.choice_second_default_reminder()
        news = my_page.get_default_reminder()
        my_page.back()
        my_page.to_reminder()
        my_page.choice_first_default_reminder()
        my_page.back()
        assert news_choice == news, '选择的修改信息为{}，默认的信息为{}'.format(news_choice, news)

    @allure.feature('我的页面')
    @allure.story('卖家地址库')
    def test_seller_address(self, go_to_my_page):
        """

        :param go_to_my_page:
        :return:
        """
        my_page = go_to_my_page
        my_page.to_seller_address()
        results = my_page.check_address()
        assert results['name'], '姓名不存在'
        assert results['phone'], '电话不存在'
        assert results['address'], '地址信息不存在'

    @allure.feature('我的页面')
    @allure.story('订单检测设置')
    def test_check_order_send(self, go_to_my_page):
        """

        :param go_to_my_page:
        :return:
        """
        my_page = go_to_my_page
        my_page.to_order_checking()
        my_page.message_detection()
        my_page.cloud_blacklist_detection()
        my_page.receiving_address_detection()
        my_page.negative_comment_diagnosis_detection()
        my_page.click_sure()
        my_page.back()
        news_sure = get_order_check_send()
        my_page.to_order_checking()
        my_page.message_detection()
        my_page.cloud_blacklist_detection()
        my_page.receiving_address_detection()
        my_page.negative_comment_diagnosis_detection()
        my_page.click_sure()
        news_unsure = get_order_check_send()
        assert news_sure['中差评'], '开启成功'
        assert news_sure['留言信息'], '开启成功'
        assert news_sure['收货地址'], '开启成功'
        assert news_sure['5次差评'], '开启成功'
        assert news_unsure['中差评'] is not True, '关闭失败'
        assert news_unsure['留言信息'] is not True, '关闭失败'
        assert news_unsure['收货地址'] is not True, '关闭失败'
        assert news_unsure['5次差评'] is not True, '关闭失败'
