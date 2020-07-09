# -*- encoding=utf8 -*-
__author__ = 'xiaoxuan'

# import allure
# from airtest.core.api import *
# import warnings
from mobile.mitem_ui_test.mitem_ui_test.pages.first_page import *
import pytest

class TestMedetail(BasePage):

    @allure.feature('手机详情')
    @allure.story('有、无手机详情的宝贝数量显示正确')
    @pytest.mark.p2
    def test_mdetail_get_item_num(self, go_mdetail_scan):
        """
        1.进入手机详情首页
        2.判断出售中、有详情、无详情的数量是否正确
        3.切换至仓库中，判断仓库中、有详情、无详情的数量是否正确
        :param go_mdetail:
        :return:
        """
        mdetail_page = go_mdetail_scan
        assert int(mdetail_page.get_item_num(0)) == int(mdetail_page.get_item_num(1)) + int(mdetail_page.get_item_num(2)) , \
            '出售中宝贝，总数、有详情的宝贝、无详情的宝贝数量异常！'
        mdetail_page.change_item_scale(1)
        assert int(mdetail_page.get_item_num(0)) == int(mdetail_page.get_item_num(1)) + int(mdetail_page.get_item_num(2)) , \
            '仓库中宝贝，总数、有详情的宝贝、无详情的宝贝数量异常！'


    @allure.feature('手机详情')
    @allure.story('出售中，过滤开关开启时，发起全店任务，任务实际发起，并且数量正确')
    @pytest.mark.p1
    def test_mdetail_full_shop_submit_with_filter(self,go_mdetail_scan):
        """
        1.进入手机详情首页，记录出售中，无详情的宝贝数
        2.提交全店任务
        3.判断任务是否发起，并且发起的宝贝数量是否一致
        4.如果任务没执行完，终止任务
        :return:
        """
        mdetail_page = go_mdetail_scan
        excepted_num = mdetail_page.get_item_num(2)
        assert mdetail_page.start_full_shop_create().get('0'), '出售中，无详情的宝贝数=0，请调整测试数据'
        does_task_start = True
        try:
            init_element(mdetail_page.task_cancel_locator).wait_for_appearance(20) # 等待全店任务发起，20秒显示等待
        except Exception:
            does_task_start = False
        if mdetail_page.start_full_shop_create().get('1') is not None: #  如果图片空间不足，提交的是部分宝贝
            excepted_num = mdetail_page.start_full_shop_create().get('1')
        assert does_task_start and mdetail_page.get_mdetail_full_shop_total_num() == int(excepted_num), \
            '任务是否发起：{}，数量是否异常：actual{}，except{}'.format(does_task_start, mdetail_page.get_mdetail_full_shop_total_num()
                                                        , int(excepted_num))
        if does_element_exists(mdetail_page.task_cancel_locator):
            mdetail_page.cancel_full_shop_create_status()


    @allure.feature('手机详情')
    @allure.story('仓库中，过滤开关关闭时，发起全店任务，任务实际发起，并且数量正确')
    @pytest.mark.p1
    def test_mdetail_full_shop_submit_without_filter(self,go_mdetail_scan):
        """
        1.进入手机详情首页
        2.宝贝范围切换至仓库中
        3.关闭过滤开关
        4.提交全店任务
        5.判断任务是否发起，并且发起的宝贝数量是否一致
        6.如果任务没执行完，终止任务
        :param go_mdetail:
        :return:
        """
        mdetail_page = go_mdetail_scan
        mdetail_page.change_item_scale(1)
        mdetail_page.change_filter_item()
        excepted_num = mdetail_page.get_item_num(0)
        start_info = mdetail_page.start_full_shop_create()
        assert start_info.get('0'), '仓库中，宝贝数=0，请调整测试数据'
        does_task_start = True
        try:
            init_element(mdetail_page.task_cancel_locator).wait_for_appearance(20)  # 等待全店任务发起，20秒显示等待
        except Exception:
            does_task_start = False
        if start_info.get('1') is not None: # 如果图片空间不足，提交的是部分宝贝
            excepted_num = start_info.get('1')
        assert does_task_start and mdetail_page.get_mdetail_full_shop_total_num() == int(excepted_num), \
            '任务是否发起：{}，数量是否异常：actual{}，except{}'.format(does_task_start,mdetail_page.get_mdetail_full_shop_total_num()
                                                        ,int(excepted_num))
        if does_element_exists(mdetail_page.task_cancel_locator):
            mdetail_page.cancel_full_shop_create_status()



    @allure.feature('手机详情')
    @allure.story('全店任务终止后，可以正常重新执行')
    @pytest.mark.p2
    def test_mdetail_full_shop_submit_restart(self, go_mdetail_scan):
        """
        1.进入手机详情首页
        2.关闭过滤开关，提交全店任务
        3.终止任务
        4.重新执行任务，判断任务是否正常重启
        5.如果任务没执行完，终止任务
        :return:
        """
        mdetail_page = go_mdetail_scan
        excepted_num = mdetail_page.get_item_num(0)
        mdetail_page.change_filter_item()
        start_info = mdetail_page.start_full_shop_create()
        assert mdetail_page.start_full_shop_create().get('0'), '出售中，无详情的宝贝数=0，请调整测试数据'
        does_task_start = True
        try:
            init_element(mdetail_page.task_cancel_locator).wait_for_appearance(20)  # 等待全店任务发起，20秒显示等待
        except Exception:
            does_task_start = False
        if start_info.get('1') is not None:  # 如果图片空间不足，提交的是部分宝贝
            excepted_num = start_info.get('1')
        mdetail_page.cancel_full_shop_create_status()
        mdetail_page.restart_full_shop_create_status()
        try:
            init_element(mdetail_page.task_cancel_locator).wait_for_appearance(5)  # 等待全店任务发起，5秒显示等待
        except Exception:
            does_task_start = False
        assert does_task_start and mdetail_page.get_mdetail_full_shop_total_num() == int(excepted_num), \
            '任务是否发起：{}，数量是否异常：actual{}，except{}'.format(does_task_start, mdetail_page.get_mdetail_full_shop_total_num()
                                                        , int(excepted_num))
        if does_element_exists(mdetail_page.task_cancel_locator):
            mdetail_page.cancel_full_shop_create_status()


    @allure.feature('手机详情')
    @allure.story('出售中宝贝列表，搜索、排序、筛选后，可以正常批量生成手机详情')
    @pytest.mark.p1
    def test_mdetail_batch_create(self, go_mdetail_scan):
        """
        1.进入手机详情首页
        2.进入列表页
        3.搜索关键词“保温杯”，库存从低到高排序，筛选无详情宝贝
        4.勾选1个宝贝，然后全选
        5.批量提交任务
        6.判断任务是否发起
        :param go_mdetail:
        :return:
        """
        mdetail_page = go_mdetail_scan
        item_list = mdetail_page.go_mdetail_item_list()
        assert item_list.search_by_keyword('保温杯', init_element(item_list.single_submit_locator)), \
            '有沙雕把出售中的保温杯宝贝都下架了'
        item_list.sort_by(1, init_element(item_list.single_submit_locator))
        assert item_list.filter_by_condition('mdetail', init_element(item_list.single_submit_locator)), \
            '有沙雕把出售中的保温杯宝贝都生成详情了'
        item_list.choose_item(1)
        item_list.choose_all()
        sleep(0.5) # 提高用例稳定性，0.5sleep
        item_list.batch_submit()
        does_task_start = True
        try:
            poco(text = '预计剩余时间').wait_for_appearance(5)  # 等待单个任务发起，5秒显示等待
        except Exception:
            does_task_start = False
        assert does_task_start, '全选后，批量任务不能正常发起'


    @allure.feature('手机详情')
    @allure.story('仓库中宝贝列表，搜索后，可以正常单个生成手机详情')
    @pytest.mark.p2
    def test_mdetail_single_create(self, go_mdetail_scan):
        """
        1.进入手机详情首页
        2.切换仓库中
        3.进入列表页
        4.搜索“仓库中的保温杯”
        5.单个生成
        6.判断任务是否发起
        :param go_mdetail:
        :return:
        """
        mdetail_page = go_mdetail_scan
        mdetail_page.change_item_scale(1)
        item_list = mdetail_page.go_mdetail_item_list()
        assert item_list.search_by_keyword('仓库中的保温杯', init_element(item_list.single_submit_locator)), \
            '有沙雕把仓库中的保温杯搞没了'
        item_list.single_submit()
        does_task_start = True
        try:
            poco(text = '预计剩余时间').wait_for_appearance(5)  # 等待单个任务发起，5秒显示等待
        except Exception:
            does_task_start = False
        assert does_task_start, '单个生成任务不能正常发起'


    @allure.feature('手机详情')
    @allure.story('宝贝列表，详情生成失败后，失败原因能正常显示')
    @pytest.mark.p2
    def test_mdetail_fail_reason(self, go_mdetail_scan):
        """
         1.进入手机详情首页
         2.进入列表页
         3.搜索关键词“保温杯”
         4.单个生成
         5.失败后，查看失败原因，判断原因是否显示
        :param go_mdetail:
        :return:
        """
        mdetail_page = go_mdetail_scan
        item_list = mdetail_page.go_mdetail_item_list()
        assert item_list.search_by_keyword('保温杯', init_element(item_list.single_submit_locator)), \
            '有沙雕把出售中的保温杯宝贝都下架了'
        item_list.single_submit()
        does_task_finished = True
        fail_reason = None
        try:
            init_element(item_list.fail_reason_locator).wait_for_appearance(120) # 手机详情任务，120秒显示等待
            element_click(item_list.fail_reason_locator)
            fail_reason = item_list.get_fail_reason()
        except:
            does_task_finished = False
        assert does_task_finished and fail_reason == '属性值最大长度为32个字符(16个汉字) !' , \
            '手机详情任务2分钟内没有执行完，请检查队列！或者手机详情失败原因不能正常显示'



