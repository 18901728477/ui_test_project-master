# -*- encoding=utf8 -*-
__author__ = 'xiaoxuan'

from mobile.mitem_ui_test.mitem_ui_test.pages.common_list_page import *
from mobile.mitem_ui_test.mitem_ui_test.pages.title_improve_detail_page import *


class TitleImproveList(CommonList):
    amount_of_bad_title_locator = ('and', (('attr.*=', ('text', '差 \d*')),))
    amount_of_good_title_locator = ('and', (('attr.*=', ('text', '良 \d*')),))
    amount_of_best_title_locator = ('and', (('attr.*=', ('text', '优 \d*')),))
    check_again_locator = ('and', (('attr.*=', ('text', '重新检测')),))
    latest_check_time_anchor = ('and', (('attr.*=', ('text', '上次检测时间：')),))
    latest_update_time_anchor = ('and', (('attr.*=', ('text', '上次优化时间：')),))
    scale_locator = '\ue911' # 宝贝出售中、仓库中图标

    # 方法：获取差、良、优宝贝总数
    def get_item_amout(self) -> str:
        """

        :return:
        差、良、优宝贝总数
        """
        return str(int(get_text_of_view(init_element(self.amount_of_bad_title_locator))[2:]) +
                   int(get_text_of_view(init_element(self.amount_of_good_title_locator))[2:]) +
                   int(get_text_of_view(init_element(self.amount_of_best_title_locator))[2:]))

    # 方法：进入标题优化，宝贝详情页面
    def go_title_improve_detail_page(self, item_title: str) -> TitleImproveDetail():
        """

        :param item_title:
        宝贝标题
        :return:
        """
        element_click(self.latest_update_time_anchor)
        poco(text=item_title).wait_for_appearance(5)  # 跳转详情页，5s显示等待
        return TitleImproveDetail()

    # 方法：获取上一次检测时间
    def get_latest_check_time(self) -> str:
        time_ele = locate_by_anchor(init_element(self.latest_check_time_anchor), 1, 'l1')
        return get_text_of_view(time_ele)

    # 方法：获取上一次优化时间
    def get_lastest_update_time(self) -> str:
        time_ele = locate_by_anchor(init_element(self.latest_update_time_anchor), 1, 'l1')
        return get_text_of_view(time_ele)

    # 方法：切换状态
    def switch_scale(self,index:int):
        """

        :param index:
        0:出售中
        1：仓库中
        :return:
        """
        scale_dict = {
            0: '出售中',
            1: '仓库中'
        }
        poco(text=self.scale_locator).click()
        poco(text=scale_dict.get(index)).click()
        sleep(3)

    # 方法：立即重新检测
    def check_again(self):
        element_click(self.check_again_locator)
        sleep(6)


if __name__ == '__main__':
    x = TitleImproveList()
    print(x.get_item_amout())
