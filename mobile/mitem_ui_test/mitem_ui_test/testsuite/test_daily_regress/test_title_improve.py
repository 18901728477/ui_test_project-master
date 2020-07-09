# -*- encoding=utf8 -*-
__author__ = 'xiaoxuan'

from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import *
from mobile.mitem_ui_test.mitem_ui_test.item_info import *
import pytest

class TestTitleImprove(BasePage):

    @allure.feature('标题优化')
    @allure.story('标题优化，重新检测后，能搜索出、筛选出宝贝，能正常跳转优化详情页，上次优化时间正常同步')
    @pytest.mark.p2
    def test_check_update_time(self, go_title_improve_list):
        """
        1.进入标题优化列表页
        2.重新检测，判断上次检测时间是否同步
        3.筛选分类、搜索宝贝
        4.点击宝贝，判断是否正常进入标题优化详情页
        5.更新标题后返回，判断上次优化时间是否同步
        :param go_title_improve_list:
        :return:
        """
        title_improve_list_page = go_title_improve_list
        origin_check_time = title_improve_list_page.get_latest_check_time()
        title_improve_list_page.check_again()
        new_check_time = title_improve_list_page.get_latest_check_time()
        assert new_check_time != origin_check_time, '上次检测时间没更新'
        assert title_improve_list_page.filter_by_class(0, {'一级分类': '一级分类00'}, poco(text='上次优化时间：')), '宝贝不存在'
        assert title_improve_list_page.search_by_keyword(ITEM_TITLE_IMPROVE_TITLE, poco(text='上次优化时间：')), '宝贝不存在'
        origin_update_time = title_improve_list_page.get_lastest_update_time()
        title_improve_detail_page = title_improve_list_page.go_title_improve_detail_page(ITEM_TITLE_IMPROVE_TITLE)
        assert poco(text=ITEM_TITLE_IMPROVE_TITLE).exists(), '优化详情页不显示宝贝信息'
        title_improve_detail_page.update_title()
        BasePage().turn_back()
        new_update_time = title_improve_list_page.get_lastest_update_time()
        assert origin_update_time != new_update_time, '上次优化时间没更新'

    @allure.feature('标题优化')
    @allure.story('标题优化，列表页，获取的宝贝数量正常')
    @pytest.mark.p2
    def test_amout_item(self, go_firstpage):
        """
        1.进入首页，记录出售中、仓库中宝贝总数
        2.进入标题优化列表页，记录出售中总数
        3.切换仓库中，记录仓库中总数
        4.判断数量与首页的是否一致
        :param go_firstpage:
        :return:
        """
        first_page = go_firstpage
        except_num_onsale = first_page.get_item_num(0)
        except_num_inventory = first_page.get_item_num(1)
        title_improve_list_page = first_page.go_title_improve()
        title_improve_list_page.check_again()
        actual_num_onsale = title_improve_list_page.get_item_amout()
        title_improve_list_page.switch_scale(1)
        actual_num_inventory = title_improve_list_page.get_item_amout()
        assert except_num_onsale == actual_num_onsale and except_num_inventory == actual_num_inventory, \
            '标题优化列表页，出售、仓库中的宝贝数与实际不符'

    @allure.feature('标题优化')
    @allure.story('标题优化，优化详情页，宝贝检测结果显示正确')
    @pytest.mark.p2
    def test_title_result(self, go_title_improve_detail):
        """
        1.进入标题优化，优化详情页
        2.依次输入差、良、优的标题，判断检测结果是否正确
        :return:
        """
        bad_title = '差标题'
        good_title = '测试多sku属性宝贝背带裙女秋冬dvf吊带连衣裙套装两件套 洋气'
        best_title = '测试多sku属性宝贝背带裙女秋冬dv吊带连年终大促别名品牌甜美1'
        title_improve_detail_page = go_title_improve_detail
        title_improve_detail_page.edit_title(bad_title)
        assert title_improve_detail_page.get_title_result() == '差', '差标题无法正常检测'
        sleep(1)
        title_improve_detail_page.edit_title(good_title)
        sleep(1)
        assert title_improve_detail_page.get_title_result() == '良', '良标题无法正常检测'
        title_improve_detail_page.edit_title(best_title)
        sleep(1)
        assert title_improve_detail_page.get_title_result() == '优', '差标题无法正常检测'

    @allure.feature('标题优化')
    @allure.story('标题优化，优化详情页，检测结果的详情，显示正确')
    @pytest.mark.p2
    def test_result_detail(self, go_title_improve_detail):
        """
        1.进入标题优化，优化详情页
        2.输入一个含有多个特殊字符、违禁词和重复词的标题
        :param go_title_improve_detail:
        :return:
        """
        my_title = '！?正品top女装女装连衣裙连衣裙'
        title_improve_detail_page = go_title_improve_detail
        title_improve_detail_page.edit_title(my_title)
        sleep(1.5)
        assert title_improve_detail_page.check_result_detail('！,?') and \
               title_improve_detail_page.check_result_detail('top、正品') and \
               title_improve_detail_page.check_result_detail('女装,连衣裙'), \
            '检测详情显示有误'

    @allure.feature('标题优化')
    @allure.story('标题优化，优化详情页，手动从热搜词、促销词、属性词添加词语，能正常更新到淘宝')
    @pytest.mark.p1
    def test_add_one_word_from_table(self, go_title_improve_detail):
        """
          1.进入标题优化，优化详情页
          2.清空文本框，添加第一个热搜词、促销词、属性词
          3.点击更新到淘宝后，还原标题
          4.判断标题是否实际更新成功
        :param go_title_improve_detail:
        :return:
        """
        title_improve_detail_page = go_title_improve_detail
        title_improve_detail_page.show_all_resulut()
        title_improve_detail_page.clean_textbox()
        except_title = ''
        for num in range(3):
            except_title = except_title + title_improve_detail_page.add_one_word_from_table(num)
        title_improve_detail_page.update_title()
        sleep(1.5)  # sleep1.5秒等待页面更新
        actual_title = title_improve_detail_page.get_actual_title()
        title_improve_detail_page.edit_title(ITEM_TITLE_IMPROVE_TITLE)
        title_improve_detail_page.update_title()
        assert except_title == actual_title, '标题实际没有更新'

    @allure.feature('标题优化')
    @allure.story('标题优化，优化详情页，可以正常一键优化标题')
    @pytest.mark.p1
    def test_one_click_improve(self, go_title_improve_detail):
        """
         1.进入标题优化，优化详情页
         2.一键优化标题
         3.点击更新到淘宝，还原标题
         4.判断标题是否实际更新成功
        :param go_title_improve_detail:
        :return:
        """
        title_improve_detail_page = go_title_improve_detail
        title_improve_detail_page.show_all_resulut()
        title_improve_detail_page.one_click_improve()
        title_improve_detail_page.update_title_after_improve()
        actual_title = title_improve_detail_page.get_actual_title()
        title_improve_detail_page.edit_title(ITEM_TITLE_IMPROVE_TITLE)
        title_improve_detail_page.update_title_after_improve()
        assert ITEM_TITLE_IMPROVE_TITLE != actual_title, '标题一键优化失败'
