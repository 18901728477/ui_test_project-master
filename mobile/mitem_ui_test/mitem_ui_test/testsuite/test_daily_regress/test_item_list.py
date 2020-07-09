from mobile.mitem_ui_test.mitem_ui_test.pages.first_page import *
from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import *
from mobile.mitem_ui_test.mitem_ui_test.pages.item_list_page import *
from mobile.mitem_ui_test.mitem_ui_test.item_info import TAOBAO_LINK, WEIXIN_LINK
from mobile.mitem_ui_test.mitem_ui_test.item_info import *
import pytest

class TestItemList:

    @allure.feature('宝贝列表')
    @allure.story('下架宝贝')
    @pytest.mark.p1
    def test_off_shelf(self, go_onsale_list):
        list_page = go_onsale_list
        assert list_page.search_by_keyword(ITEM_LIST_TITLE, poco(text=ITEM_LIST_TITLE)), '宝贝不存在'
        list_page.off_shelf_list()
        list_page.switch_tab(1)
        list_page.page_swipe_top()
        list_page.on_shelf_list()
        list_page.switch_tab(0)
        list_page.page_swipe_top()
        assert poco(text=ITEM_LIST_TITLE).exists(), '单个宝贝不能正常上下架'

    @allure.feature('宝贝列表')
    @allure.story('复制链接')
    @pytest.mark.p2
    def test_copy_link(self, go_onsale_list):
        link = go_onsale_list.copy_link_list()
        assert link[0] == TAOBAO_LINK, '淘宝链接不一致'
        assert link[1] == WEIXIN_LINK, '微信链接不一致'

    @allure.feature('宝贝列表')
    @allure.story('查看详情')
    @pytest.mark.p2
    def test_view_detail(self, go_onsale_list):
        list_page = go_onsale_list
        assert list_page.search_by_keyword(ITEM_ONSALE_TITLE, poco(text=ITEM_ONSALE_TITLE)), '宝贝不存在'
        res = go_onsale_list.view_detail_list(ITEM_ONSALE_TITLE)
        assert res, '跳转详情失败'

    @allure.feature('宝贝列表')
    @allure.story('二维码')
    @pytest.mark.p2
    @pytest.mark.skip(reason="下载二维码后影响本地相册扫码时的图片选择，暂时没有想到好的解决办法")
    def test_two_dimensional_code(self, go_onsale_list):
        res = go_onsale_list.two_dimensional_code_list()
        assert res, '二维码下载失败'

    @allure.feature('宝贝列表')
    @allure.story('促销推广')
    @pytest.mark.p1
    def test_promotion(self, go_onsale_list):
        res = go_onsale_list.promotion_list()
        assert res, 'ump不能正常跳转、创建活动'

    @allure.feature('宝贝列表')
    @allure.story('标题优化')
    @pytest.mark.p1
    def test_title_optimization(self, go_inventory_list):
        go_inventory_list.search_by_keyword(ITEM_INVENTORY_TITLE, poco(text=ITEM_INVENTORY_TITLE))
        res = go_inventory_list.title_optimization_list()
        assert res, '不能正常一键优化'

    @allure.feature('宝贝列表')
    @allure.story('手机详情')
    @pytest.mark.p1
    def test_mobile_detail(self, go_inventory_list):
        res = go_inventory_list.mobile_detail_list()
        assert res, '手机详情跳转失败'

    @allure.feature('宝贝列表')
    @allure.story('宝贝可以正常批量上下架')
    @pytest.mark.p1
    def test_batch_uplist_downlist(self, go_inventory_list):
        """
        1.进入仓库中列表
        2.筛选分类“列表专用分类”，排序按销量从高到低，搜索关键词“列表专用宝贝”
        3.点击“批量”按钮，全选宝贝
        4.点击上架按钮，上架成功后，判断仓库中宝贝数量是否-30
        5.进入出售中列表
        6.点击“批量”按钮，全选宝贝
        7.点击下架按钮，下架成功后，判断出售中宝贝数量是否-30
        :return:
        """
        list_page = go_inventory_list
        assert list_page.filter_by_class(0, {'一级分类': '列表专用分类'}, poco(text='促销推广')), '宝贝不存在'
        list_page.sort_by(2, poco(text='促销推广'))
        assert list_page.search_by_keyword('列表专用宝贝', poco(text='促销推广')), '宝贝不存在'
        poco(text='批量').click()
        list_page.choose_all()
        poco(text='上架').click()
        poco(text='正在上架宝贝,请稍后...').wait_for_appearance(5)
        flag = poco(textMatches='计划上架30个宝贝.*').exists()
        sleep(15)  # 30个宝贝上架，15秒sleep
        assert flag, '实际上架的宝贝数量异常'
        # 进入出售中列表，批量下架宝贝
        list_page.switch_tab(0)
        poco(text='批量').click()
        list_page.choose_all()
        poco(text='下架').click()
        poco(text='正在下架宝贝,请稍后...').wait_for_appearance(5)
        flag = poco(textMatches='计划下架30个宝贝.*').exists()
        sleep(15)  # 30个宝贝下架，15秒sleep
        assert flag, '实际下架的宝贝数量异常'

    @allure.feature('宝贝列表')
    @allure.story('活动日历、店铺体检入口跳转正常')
    @pytest.mark.p1
    def test_activity_calendar(self, go_inventory_list):
        assert go_inventory_list.activity_calendar_shop_test_enter()

    @allure.feature('宝贝列表')
    @allure.story('可以正常批量生成手机详情')
    @pytest.mark.p1
    def test_batch_mdetail(self, go_onsale_list):
        """
        1.进入出售中列表
        2.搜索关键词“保温杯”
        3.点击批量，全选宝贝，点击“手机详情”
        4.点击查看进度跳转手机详情页面
        5.判断任务正常发起，接口报错
        """
        list_page = go_onsale_list
        list_page.search_by_keyword('保温杯', poco(textMatches='.*保温杯.*'))
        poco(text='批量').click()
        list_page.choose_all()
        poco(text='手机详情').click()
        poco(text='查看生成进度').click()
        flag = True
        try:
            poco(text='失败原因').wait_for_appearance(10)
        except PocoTargetTimeout:
            flag = False
        assert flag, '列表页无法正常批量提交手机详情任务'

