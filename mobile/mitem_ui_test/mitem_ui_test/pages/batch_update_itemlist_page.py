# -*- encoding=utf8 -*-
__author__ = 'xiaoxuan'

from mobile.mitem_ui_test.mitem_ui_test.pages.common_list_page import *


class BatchUpdateItemList(CommonList):
    choose_item_locator = '\ue6ba'
    buttom_button1 = ('and', (('attr=', ('text', '确定')),))
    list_button = ('and', (('attr=', ('text', '批量上架')),))
    delist_button = ('and', (('attr=', ('text', '批量下架')),))

    def start_update_task(self):
        element_click(self.buttom_button1)
        poco(name='com.taobao.qianniu:id/center_panel').child(text='批量修改').wait_for_appearance(20)
        sleep(3)

    def click_list_button(self):
        element_click(self.list_button)

    def click_delist_button(self):
        element_click(self.delist_button)
