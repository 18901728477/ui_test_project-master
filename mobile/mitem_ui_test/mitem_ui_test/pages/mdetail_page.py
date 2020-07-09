# -*- encoding=utf8 -*-
__author__ = 'xiaoxuan'

from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import *
from mobile.mitem_ui_test.mitem_ui_test.pages.mdetail_item_list import *

class MdetailPage(BasePage):

    item_num_locator = ('and', (('attr.*=', ('text', '\\d{1,4}')),))
    task_cancel_locator = ('and', (('attr=', ('text', '终止任务')),))
    task_redo_locator = ('and', (('attr=', ('text', '重新执行')),))
    task_delete_locator = ('and', (('attr=', ('text', '删除任务')),))
    watch_record_locator = ('and', (('attr=', ('text', '查看详情')),))
    item_scale_locator = ('and', (('attr.*=', ('text', '.{2}中')),))
    filter_checkbox_locator = ('and', (('attr=', ('name', 'android.widget.CheckBox')),))
    single_submit_locator = ('and', (('attr=', ('text', '单个生成')),))
    full_shop_submit_locator = ('and', (('attr=', ('text', '全部生成')),))
    full_shop_partial_submit_locator = ('and', (('attr=', ('text', '部分提交')),))
    none_submit_locator = ('and', (('attr=', ('text', '确认')),))

    # 获取宝贝数量
    def get_item_num(self, scale:int) -> str:
        """
        scale:
        0:宝贝总数
        1：有详情的宝贝数
        2：无详情的宝贝数
        :param scale:
        :return:
        """
        # 宝贝数量过多时，数字加载耗时长的额外处理
        while(True):
            num1 = get_text_of_view(init_element(self.item_num_locator)[1])
            sleep(1.5) # 数字加载sleep1.5s
            num2 = get_text_of_view(init_element(self.item_num_locator)[1])
            if num1 == num2:
                break

        dict = {0: get_text_of_view(init_element(self.item_num_locator)[0]),
                1: get_text_of_view(init_element(self.item_num_locator)[1]),
                2: get_text_of_view(init_element(self.item_num_locator)[2])}
        return dict.get(scale)


    # 改变宝贝范围
    def change_item_scale(self,scale:int):
        """
        scale:
        0:宝贝范围改成出售中
        1：宝贝范围改成仓库中
        :param scale:
        :return:
        """
        dict = {0: '出售中', 1: '仓库中'}
        element_click(self.item_scale_locator)
        poco(text = dict.get(scale)).click()
        poco(textMatches = '\d{1,4}').wait_for_appearance(10) # 加载数量，10秒显示等待


    # 调整过滤无详情宝贝的开关
    def change_filter_item(self):
        element_click(self.filter_checkbox_locator)

    # 发起全店生成任务
    def start_full_shop_create(self) -> dict:
        """
        
        :return:
        submit_info = {'0': xxx, '1': xxx}
        0,does_task_submit:宝贝数=0，无法提交时，返回false;可以提交时，返回true
        1,partial_submit_num:全部提交时，is None;部分提交时，返回int
        """
        does_task_submit = True
        partial_submit_num = None
        element_click(self.full_shop_submit_locator)
        sleep(3) # 等待任务发起

        # 如果图片空间不足
        if does_element_exists(self.full_shop_partial_submit_locator):
            partial_submit_num = x = poco(textMatches='\d{1,4}')[-1].get_text()  # 页面4个数字，部分提交数为最后1个
            element_click(self.full_shop_partial_submit_locator)

        # 如果提交的宝贝数=0
        if does_element_exists(self.none_submit_locator):
            element_click(self.none_submit_locator)
            does_task_submit = False
        submit_info = {'0': does_task_submit, '1': partial_submit_num}
        return submit_info


    # 终止任务
    def cancel_full_shop_create_status(self):
        element_click(self.task_cancel_locator)


    # 重新执行任务
    def restart_full_shop_create_status(self):
        element_click(self.task_redo_locator)


    # 进入手机详情-宝贝列表
    def go_mdetail_item_list(self):
        element_click(self.single_submit_locator)
        poco(textMatches = '.*生成.*').wait_for_appearance(5) # 列表加载5秒显示等待
        return MdetailItemList()


        