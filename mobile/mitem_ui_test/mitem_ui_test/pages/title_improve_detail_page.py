# -*- encoding=utf8 -*-
__author__ = 'xiaoxuan'

from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import *
from  mobile.mitem_ui_test.mitem_ui_test.item_info import TEMPLATE_UPDATE_TITLE,TEMPLATE_ONE_CLICK_IMPOVR,TEMPLATE_UPDATE_TITLE_AFTER_IMPROVE


class TitleImproveDetail(BasePage):
    title_anchor = ('and', (('attr=', ('text', '宝贝类目：')),))
    edit_title_locator = ('and', (('attr=', ('name', 'android.widget.EditText')),))
    title_result_anchor = ('and', (('attr=', ('text', '检测结果')),))
    hot_search_word_locator = ('and', (('attr=', ('text', '热搜词')),))
    prom_word_locator = ('and', (('attr=', ('text', '促销词')),))
    props_word_locator = ('and', (('attr=', ('text', '属性词')),))
    one_click_improve_locator = ('and', (('attr=', ('text', '一键优化标题')),))
    update_title_locator = ('and', (('attr=', ('text', '更新标题')),))
    word_anchor = ('and', (('attr=', ('text', '搜索展现')),))

    # 方法：更新到淘宝
    def update_title(self):
        self.page_swipe_top()
        #touch(TEMPLATE_UPDATE_TITLE)
        poco(text='更新标题').click()
        try:
            poco(text='优化下一个').wait_for_appearance(3)
            poco(text='知道了').click()
        except PocoTargetTimeout:
            pass

    # 方法：一键优化后，更新到淘宝
    def update_title_after_improve(self):
        self.page_swipe_top()
        #touch(TEMPLATE_UPDATE_TITLE_AFTER_IMPROVE)
        poco(text = '更新标题').click()
        try:
            poco(text='优化下一个').wait_for_appearance(3)
            poco(text='知道了').click()
        except PocoTargetTimeout:
            pass

    # 方法：点击一键优化标题
    def one_click_improve(self):
        self.page_swipe_top()
        #touch(TEMPLATE_ONE_CLICK_IMPOVR)
        poco(text = '一键优化标题').click()
        sleep(3)

    # 方法：从词库中添加第一个词
    def add_one_word_from_table(self, index: int) -> str:
        """

        :param index:
        0:热搜词库
        1:促销词库
        2:属性词库
        :return:
        从词库中添加的词
        """
        tab_dict = {
            0: self.hot_search_word_locator,
            1: self.prom_word_locator,
            2: self.props_word_locator
        }
        init_element(tab_dict.get(index)).click()
        sleep(1)
        poco(text='添加')[1].click()
        loc_ele = init_element(self.word_anchor).parent().parent().offspring(text='添加')[1]
        word_ele = locate_by_anchor(loc_ele, 1, 'l0')
        return get_text_of_view(word_ele)

    # 方法：展开、收起检测项
    def show_all_resulut(self):
        locate_by_anchor(init_element(self.title_result_anchor), 2, 'l1').click()
        sleep(1)

    # 方法：检查检测结果
    def check_result_detail(self, check_word: str) -> bool:
        """

        :param check_word:
        特殊字符、重复词、违禁词
        如果特殊字符、重复词有多个词，英文逗号隔开
        如果违禁词有多个词，中文顿号隔开
        :return:
        检测结果中包含这些词，返回true；否则返回false
        """
        return poco(text='检测结果').parent().parent().parent().offspring(text=check_word).exists()
        #return poco(text='项存在问题').parent().parent().offspring(text=check_word).exists()

    # 方法：手动编辑标题
    def edit_title(self, my_title: str):
        element_sendtext(self.edit_title_locator, my_title)
        sleep(1)

    # 方法：获取检测结果
    def get_title_result(self) -> str:
        res_ele = locate_by_anchor(init_element(self.title_result_anchor), 1, 'l1')
        return get_text_of_view(res_ele)

    # 方法：清空标题文本框
    def clean_textbox(self):
        element_sendtext(self.edit_title_locator,'')

    # 方法：获取实际的标题
    def get_actual_title(self) -> str:
        title_ele = locate_by_anchor(init_element(self.title_anchor), 2, 'v0')
        return get_text_of_view(title_ele)

    # 方法：获取文本框里的标题
    def get_title(self) -> str:
        return poco(name='android.widget.EditText').get_text()


if __name__ == '__main__':
    x = TitleImproveDetail()
    # my_title = '！?正品top女装女装连衣裙连衣裙'
    # x.edit_title(my_title)
    # assert x.check_result_detail('！,?') and \
    #        x.check_result_detail('top、正品') and \
    #        x.check_result_detail('女装,连衣裙'), \
    #     '检测详情显示有误'
    x.add_one_word_from_table(0)
