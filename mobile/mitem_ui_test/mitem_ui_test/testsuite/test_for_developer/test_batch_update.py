from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import *
import allure
from mobile.mitem_ui_test.mitem_ui_test.item_info import *
from mobile.mitem_ui_test.mitem_ui_test import utils
import random
import pytest


class TestBatchUpdate(BasePage):

    @allure.feature('批量修改')
    @allure.story('批量修改价格')
    @pytest.mark.p1
    def test_batch_price(self, first_page_wait_scan):
        batch_update_page = first_page_wait_scan.go_batch_update()
        bymath_result = batch_update_page.change_baby_price(method='bymath')
        byint_result = batch_update_page.change_baby_price(method='byint')
        byfloat_result = batch_update_page.change_baby_price(method='byfloat')
        batch_update_page.change_baby_price('bymath')
        batch_update_page.restore_price()
        assert bymath_result, '按公式修改失败'
        assert byint_result, '修改整体价格失败'
        assert byfloat_result, '修改小数价格失败'
        assert batch_update_page.check_task_detail_price(), '价格无法正常还原'

    @allure.feature('批量修改')
    @allure.story('批量修改标题')
    @pytest.mark.p2
    def test_batch_title(self, first_page_wait_scan):
        batch_updata_page = first_page_wait_scan.go_batch_update()
        title_replace_result = batch_updata_page.change_baby_title_replace()
        title_delete_result = batch_updata_page.change_baby_title_delete()
        title_add_result = batch_updata_page.change_baby_title_add()
        assert title_replace_result, '替换标题内容失败'
        assert title_delete_result, '删除标题内容失败'
        assert title_add_result, '添加标题内容失败'

    @allure.feature('批量修改')
    @allure.story('批量修改库存')
    @pytest.mark.p2
    def test_batch_stock(self, first_page_wait_scan):
        batch_update_page = first_page_wait_scan.go_batch_update()
        unified_result = batch_update_page.change_baby_num(method='unified')
        increase_result = batch_update_page.change_baby_num(method='increase')
        reduce_result = batch_update_page.change_baby_num(method='reduce')
        assert unified_result, '统一库存设置失败'
        assert increase_result, '增加库存失败'
        assert reduce_result, '减少库存失败'

    @allure.feature('批量修改')
    @allure.story('可以正常批量添加文字')
    @pytest.mark.p1
    def test_update_desc(self, first_page_wait_scan):
        """
        1.进入批量修改-添加描述tab
        2.添加描述：我添加的描述+时间戳
        3.进入宝贝列表,筛选分类，搜索关键词,勾选宝贝，提交任务
        4.等待任务执行完后，调用api判断是否实际添加成功
        5.进入批量修改-替换描述tab
        6.替换描述：我添加的描述+时间戳 -> 我替换的描述+时间戳
        7.进入宝贝列表,搜索关键词,勾选宝贝，提交任务
        8.等待任务执行完后，调用api判断是否实际删除成功
        :param first_page_wait:
        :return:
        """
        CURRENT_TIME = utils.get_current_time()
        ADD_WORD = "我添加的描述" + CURRENT_TIME
        REPLACE_WORD = "我替换的描述" + CURRENT_TIME
        self.page_swipe_buttom()
        batch_update_page = first_page_wait_scan.go_batch_update()
        # 添加详情
        list_page = batch_update_page.go_update_detail_add_word(ADD_WORD)
        assert list_page.filter_by_class(0, {'一级分类': '批量修改专用分类'}, poco(textMatches='编码:.*')), '宝贝不存在'
        assert list_page.search_by_keyword(ITEM_UPDATE_DETAIL_TITLE, poco(textMatches='编码:.*')), '宝贝不存在'
        list_page.choose_item(1)
        list_page.start_update_task()
        assert ADD_WORD in batch_update_page.tb_api_get_item_desc(ITEM_UPDATE_DETAIL_NUMID)
        # 替换详情
        batch_update_page.go_update_detail_replace(old_content=ADD_WORD, new_content=REPLACE_WORD)
        assert list_page.search_by_keyword(ITEM_UPDATE_DETAIL_TITLE, poco(textMatches='编码:.*')), '宝贝不存在'
        list_page.choose_item(1)
        list_page.start_update_task()
        assert ADD_WORD not in batch_update_page.tb_api_get_item_desc(ITEM_UPDATE_DETAIL_NUMID) and \
               REPLACE_WORD in batch_update_page.tb_api_get_item_desc(ITEM_UPDATE_DETAIL_NUMID)
        # 删除详情
        batch_update_page.go_update_detail_delete(my_delete=REPLACE_WORD)
        assert list_page.search_by_keyword(ITEM_UPDATE_DETAIL_TITLE, poco(textMatches='编码:.*')), '宝贝不存在'
        list_page.choose_item(1)
        list_page.start_update_task()
        assert REPLACE_WORD not in batch_update_page.tb_api_get_item_desc(ITEM_UPDATE_DETAIL_NUMID)

    @allure.feature('批量修改')
    @allure.story('可以正常批量上下架')
    @pytest.mark.p2
    def test_list_delist(self, first_page_wait_scan):
        """
        1.进入批量修改首页，点击批量下架
        2.筛选分类“批量修改专用分类”，搜索关键字“批量修改”
        3.选择第一个宝贝，然后全选3个宝贝，点击批量下架
        4.判断成功弹窗中宝贝数量=3
        5.关闭弹窗后,返回批量修改首页
        6.点击批量上架
        7.切换按分类选择tab，选择分类“批量修改专用分类”，点击批量上架
        8.判断成功弹窗中宝贝数量=3
        :param first_page_wait:
        :return:
        """
        batch_update_page = first_page_wait_scan.go_batch_update()
        list_page = batch_update_page.go_list(1)
        assert list_page.filter_by_class(0, {'一级分类': '批量修改上下架'}, poco(textMatches='编码:.*')), '宝贝不存在'
        assert list_page.search_by_keyword('批量修改专用上下架宝贝', poco(textMatches='编码:.*')), '宝贝不存在'
        list_page.choose_item(1)
        list_page.choose_all()
        list_page.click_delist_button()
        assert poco(textMatches='计划下架宝贝3个，下架成功3个！').exists(), '宝贝无法正常批量下架'
        poco(text='确定').click()
        self.turn_back()
        batch_update_page.go_list(0)
        list_page.choose_one_class(class_level=0, class_dict={'一级分类': '批量修改上下架'})
        list_page.click_list_button()
        assert poco(textMatches='计划上架宝贝3个，上架成功3个！').exists(), '宝贝无法正常批量上架'
        poco(text='确定').click()