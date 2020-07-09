import allure
import pytest


class TestFirstPage:
    @pytest.mark.skip('108版本刷新')
    @allure.feature('首页')
    @allure.story('发微淘')
    def test_release_taobao_page(self, first_by_scan):
        """
        1.点击首页发微淘图标
        2.检查页面跳转是否成功
        :param first:
        :return:
        """
        result = first_by_scan.go_release_taobao_page()
        first_by_scan.close()
        assert result, '跳转发微淘页面失败'

    @allure.feature('首页')
    @allure.story('淘大直播')
    def test_taobao_broadcast_page(self, first_by_scan):
        """
          1.点击首页淘大直播图标root.-.
          ..
          .
          .
          2.检查页面跳转是否成功
          :param first:
          :return:
          """
        result = first_by_scan.go_taobao_broadcast_page()
        first_by_scan.back()
        assert result, '跳转淘大直播页面失败'

    @allure.feature('首页')
    @allure.story('违规词检测')
    def test_violation_words_check_page(self, first_by_scan):
        """
          1.点击首页违规词检测图标
          2.检查页面跳转是否成功
          :param first:
          :return:
          """
        result = first_by_scan.go_violation_words_check_page()
        first_by_scan.refresh()
        first_by_scan.close()
        assert result, '跳转违规词检测页面失败'

    @allure.feature('首页')
    @allure.story('批量评价')
    # @pytest.mark.skip(reason="避免消耗订单数据")
    def test_batch_rate(self, go_to_firstbatch_evaluation_page_by_scan):
        """

        :param go_to_firstbatch_evaluation_page:
        :return:
        检查逻辑：
        进入首页
        进入批量评价页面
        点击批量评价对订单进行评价
        验证能否选中好评、中评、差评，能否插入评价短语，能否使用自定义短语评价
        为避免消耗数据，没有点击立即评价按钮
        """
        info_rate_page = go_to_firstbatch_evaluation_page_by_scan
        rate_page = info_rate_page.click_batch_evaluate()
        choose_bad_news = rate_page.choose_bad_batch()
        choose_good_news = rate_page.choose_good_batch()
        choose_mid_news = rate_page.choose_mid_batch()
        set_rate_news = rate_page.insert_phrase()
        set_rate_news_custom = rate_page.insert_phrase_by_custom()
        rate_page.back()
        assert choose_good_news, '选择好评不可用'
        assert choose_bad_news, '选择差评不可用'
        assert choose_mid_news, '选择中评不可用'
        assert set_rate_news[0], '插入评价短语异常'
        assert set_rate_news_custom, '使用自定义短语评价异常'




