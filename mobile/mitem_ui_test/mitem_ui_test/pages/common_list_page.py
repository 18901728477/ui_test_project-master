# -*- encoding=utf8 -*-
__author__ = 'xiaoxuan'

from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import *


class CommonList(BasePage):
    search1_locator = ('and', (('attr=', ('text', '搜索...')),))
    search2_locator = ('and', (('attr=', ('text', '搜索')),))
    restore_search_locator = ('and', (('attr=', ('text', '\ue917')),))
    search_by_keyword_locator = ('and', (('attr=', ('text', '关键词')),))
    search_by_code_locator = ('and', (('attr=', ('text', '商家编码')),))
    sort_locator = ('and', (('attr.*=', ('text', '按.*从.到.')),))
    filter_locator = ('and', (('attr=', ('text', '筛选')),))
    choose_item_locator = '\ue6ba'
    choose_by_class_locator = ('and', (('attr=', ('text', '按分类选择')),))

    # 关键字搜索
    def search_by_keyword(self, keyword: str, element_for_wait: UIObjectProxy) -> bool:
        """
        :param keyword:
        输入的搜索关键词
        :param element_for_wait:
        列表搜索时，显示等待的元素
        :return:
        搜索有结果时，返回true
        搜索无结果时，返回false
        """
        does_item_search = True
        if does_element_exists(self.search1_locator):
            init_element(self.search1_locator).click()
        # 如果有搜索记录，清空搜索记录
        else:
            element_click(self.restore_search_locator)
            element_click(self.search1_locator)
        sleep(1)
        # 输入搜索的关键字后，点击搜索
        poco(name='android.widget.EditText').set_text(keyword)
        element_click(self.search2_locator)
        try:
            sleep(3)  # 3秒sleep，搜索完成前，页面上存在的元素使显示等待无实际作用
            element_for_wait.wait_for_appearance(10)  # 列表搜索，10秒显示等待
        except:
            does_item_search = False
        return does_item_search

    # 商家编码搜索
    def search_by_code(self, code: str, element_for_wait: UIObjectProxy) -> bool:
        """
        :param code:
        输入的商家编码
        :param element_for_wait:
        列表搜索时，显示等待的元素
        :return:
        搜索有结果时，返回true
        搜索无结果时，返回false
        """
        does_item_search = True
        if does_element_exists(self.search1_locator):
            element_click(self.search1_locator)
        # 如果有搜索记录，清空搜索记录
        else:
            element_click(self.restore_search_locator)
            element_click(self.search1_locator)
        # 切换商家编码搜索
        element_click(self.search_by_keyword_locator)
        element_click(self.search_by_code_locator)
        # 输入搜索的编码后，点击搜索
        poco(name='android.widget.EditText').set_text(code)
        element_click(self.search2_locator)
        try:
            sleep(3)  # 3秒sleep，搜索完成前，页面上存在的元素使显示等待无实际作用
            element_for_wait.wait_for_appearance(10)  # 列表搜索，10秒显示等待
        except PocoTargetTimeout:
            does_item_search = False
        return does_item_search

    # 排序
    def sort_by(self, method: int, element_for_wait: UIObjectProxy):
        """
        method:
        0:库存从高到低
        1:库存从低到高
        2:销量从高到低
        3:销量从低到高
        :param method:
        :return:
        """
        my_dict = {0: '按库存从高到低', 1: '按库存从低到高', 2: '按销量从高到低', 3: '按销量从低到高'}
        element_click(self.sort_locator)
        poco(text=my_dict.get(method)).click()
        element_for_wait.wait_for_appearance(10)  # 列表排序后，10秒显示等待

    # 按特殊条件筛选
    def filter_by_condition(self, method: str, element_for_wait: UIObjectProxy) -> bool:
        """

        :param method:
        mdetail:手机详情
        shortvideo：主图视频
        :param element_for_wait:
        列表筛选完后，显示等待的元素
        :return:
        有筛选结果返回true
        无筛选结果返回false
        """
        does_element_filter = True
        element_click(self.filter_locator)
        # 主图视频待补充
        dict = {'mdetail': locate_by_anchor(poco(text='仅显示无手机详情的宝贝'), 1, 'l0'), 'shortvideo': None}
        if method == 'mdetail':
            dict.get('mdetail').click()
        try:
            sleep(3)  # 3秒sleep，搜索完成前，页面上存在的元素使显示等待无实际作用
            element_for_wait.wait_for_appearance(5)  # 列表筛选后，5秒显示等待
        except PocoTargetTimeout:
            does_element_filter = False
        return does_element_filter

    # 按分类筛选
    def filter_by_class(self, class_level: int, class_dict: dict, element_for_wait: UIObjectProxy) -> bool:
        """

        :param class_level:
        0：一级分类
        1：二级分类
        :param class_dict:
        class_level=0,{'一级分类'：'xxx'}
        class_level=1,{'一级分类':'xxx','二级分类':'yyy'}
        :return:
        分类筛选有结果，返回true
        无结果返回false
        """
        does_element_filter = True
        element_click(self.filter_locator)
        class_level_dict = {0: '一级分类', 1: '二级分类'}
        class_text = class_dict.get('一级分类')
        if class_level_dict.get(class_level) == '一级分类':
            poco(text=class_text).click()
            try:
                element_for_wait.wait_for_appearance(5)  # 筛选分类后，5秒显示等待
            except PocoTargetTimeout:
                does_element_filter = False
        elif class_level_dict.get(class_level) == '二级分类':
            poco(text=class_text).parent().parent().offspring(text='\ue911').click()
            poco(text=class_dict.get('二级分类')).click()
            try:
                sleep(3)  # 3秒sleep，搜索完成前，页面上存在的元素使显示等待无实际作用
                element_for_wait.wait_for_appearance(5)  # 筛选分类后，5秒显示等待
            except PocoTargetTimeout:
                does_element_filter = False
        return does_element_filter

    # 选择n个宝贝
    def choose_item(self, choose_num: int):
        for x in range(choose_num):
            poco(text=self.choose_item_locator)[x].click()
            sleep(0.5)  # 每次勾选宝贝之间sleep0.5s

    # 全选
    def choose_all(self):
        poco(text='全选').parent().offspring(text=self.choose_item_locator).click()

    # 切换至按分类选择tab,选择1个分类
    def choose_one_class(self, class_level: int, class_dict: dict):
        """

        :param class_level:
        0：一级分类
        1：二级分类
        :param class_dict:
        class_level=0,{'一级分类'：'xxx'}
        class_level=1,{'一级分类':'xxx','二级分类':'yyy'}
        :return:
        """
        element_click(self.choose_by_class_locator)
        class_level_dict = {0: '一级分类', 1: '二级分类'}
        class_text = class_dict.get('一级分类')
        if class_level_dict.get(class_level) == '一级分类':
            poco(text=class_text).parent().parent().offspring(text=self.choose_item_locator).click()
        elif class_level_dict.get(class_level) == '二级分类':
            poco(text=class_text).parent().parent().offspring(text='\ue911').click()
            poco(text=class_dict.get('二级分类')).click()


if __name__ == '__main__':
    x = CommonList()
    poco(text='商品').click()
    x.search_by_keyword('西遇女鞋')
