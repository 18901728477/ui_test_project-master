import allure

from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import get_pending_bad_evalution_number, get_to_be_evaluated_number, \
    get_pending_interim_evalution_number, get_missing_evalution_number, get_interim_evaluation_number, \
    get_bad_evaluation_number, get_to_others_evaluation_number, get_good_evaluation_number, date_90


class TestEvaluationManagement:

    @allure.feature('评价管理')
    @allure.story('检查评价管理页面各项数值是否与接口一致')
    def test_pending_bad_evalution(self, evalution_management_page):
        """
        1.点击待处理差评按钮
        2.获取订单数量
        3.检查订单数量是否和接口一致
        :return:
        """
        expected_number = get_pending_bad_evalution_number(date_2)
        actual_number = evalution_management_page.show_pending_bad_evalution_number()
        if expected_number != actual_number:
            assert False, '接口获取待处理差评数量为{},实际数量为{}'.format(expected_number, actual_number)
        expected_number = get_pending_interim_evalution_number(date_2)
        actual_number = evalution_management_page.show_pending_interim_evalution_number()
        if expected_number != actual_number:
            assert False, '接口获取待处理中评数量为{},实际数量为{}'.format(expected_number, actual_number)
        expected_number = get_to_be_evaluated_number()
        actual_number = evalution_management_page.show_to_be_evaluated_number()
        if expected_number != actual_number:
            assert False, '接口获取待评价数量为{},实际数量为{}'.format(expected_number, actual_number)
        expected_number = get_missing_evalution_number(date_90)
        actual_number = evalution_management_page.show_missing_evalution_number()
        if expected_number != actual_number:
            assert False, '接口获取近90天漏评数量为{},实际数量为{}'.format(expected_number, actual_number)
        expected_number = get_bad_evaluation_number()
        actual_number = evalution_management_page.show_bad_evalution_number()
        if expected_number != actual_number:
            assert expected_number == actual_number, '接口获取差评数量为{},实际数量为{}'.format(expected_number, actual_number)
        expected_number = get_interim_evaluation_number()
        actual_number = evalution_management_page.show_interim_evalution_number()
        if expected_number != actual_number:
            assert expected_number == actual_number, '接口获取中评数量为{},实际数量为{}'.format(expected_number, actual_number)
        expected_number = get_good_evaluation_number()
        actual_number = evalution_management_page.show_good_evalution_number()
        if expected_number != actual_number:
            assert expected_number == actual_number, '接口获取好评数量为{},实际数量为{}'.format(expected_number, actual_number)
        expected_number = get_to_others_evaluation_number()
        actual_number = evalution_management_page.show_to_others_evalution_number()
        if expected_number != actual_number:
            assert expected_number == actual_number, '接口获取给他人的评价数量为{},实际数量为{}'.format(expected_number, actual_number)
        assert True

    @allure.feature('评价管理')
    @allure.story('差评页面')
    def test_bad_evalution_page(self, evalution_management_page):
        """
        1.点击差评按钮
        2.检查页面是否跳转成功
        :param evalution_management_page:
        :return:
        """
        result = evalution_management_page.go_bad_evalution_page()
        assert result, '页面跳转失败'

    @allure.feature('评价管理')
    @allure.story('中评页面')
    def test_interim_evalution_page(self, evalution_management_page):
        """
        1.点击中评按钮
        2.检查页面是否跳转成功
        :param evalution_management_page:
        :return:
        """
        result = evalution_management_page.go_interim_evalution_page()
        assert result, '页面跳转失败'

    @allure.feature('评价管理')
    @allure.story('好评页面')
    def test_good_evalution_page(self, evalution_management_page):
        """
        1.点击好评按钮
        2.检查页面是否跳转成功
        :param evalution_management_page:
        :return:
        """
        expected_result = 'False'
        actual_result = evalution_management_page.go_good_evalution_page()
        assert expected_result != actual_result, '页面跳转失败'

    @allure.feature('评价管理')
    @allure.story('给他人的评价页面')
    def test_to_others_evalution_page(self, evalution_management_page):
        """
        1.点击给他人的评价按钮
        2.检查页面是否跳转成功
        :param evalution_management_page:
        :return:
        """
        expected_result = 'False'
        actual_result = evalution_management_page.go_to_others_evalution_page()
        assert expected_result != actual_result, '页面跳转失败'

    @allure.feature('评价管理')
    @allure.story('待处理差评页面')
    def test_pending_bad_evalution_page(self, evalution_management_page):
        """
        1.点击给待处理差评按钮
        2.检查页面是否跳转成功
        :param evalution_management_page:
        :return:
        """
        result = evalution_management_page.go_pending_bad_evalution_page()
        assert result, '页面跳转失败'

    @allure.feature('评价管理')
    @allure.story('待评价页面')
    def test_to_be_evaluated_page(self, evalution_management_page):
        """
        1.点击给待评价按钮
        2.检查页面是否跳转成功
        :param evalution_management_page:
        :return:
        """
        result = evalution_management_page.go_to_be_evaluated_page()
        assert result, '页面跳转失败'

    @allure.feature('评价管理')
    @allure.story('近90天漏评页面')
    def test_missing_evalution_page(self, evalution_management_page):
        """
        1.点击给待评价按钮
        2.检查页面是否跳转成功
        :param evalution_management_page:
        :return:
        """
        result = evalution_management_page.go_missing_evalution_page()
        assert result, '页面跳转失败'

    @allure.feature('评价管理')
    @allure.story('提升店铺等级页面')
    def test_missing_evalution_page(self, evalution_management_page):
        """
        1.点击快速提升店铺等级按钮
        2.检查页面是否跳转成功
        :param evalution_management_page:
        :return:
        """
        result = evalution_management_page.go_shop_level_up_page()
        assert result, '页面跳转失败'
