# -*- encoding=utf8 -*-
__author__ = 'xiaoxuan'

from mobile.mitem_ui_test.mitem_ui_test.pages.common_list_page import *
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

poco = AndroidUiautomationPoco(device=device(), screenshot_each_action=False)

class MdetailItemList(CommonList):

    batch_submit_locator = ('and', (('attr=', ('text', '批量生成手机详情')),))
    single_submit_locator = ('and', (('attr.*=', ('text', '.*生成.*')),))
    fail_reason_locator = ('and', (('attr=', ('text', '失败原因')),))
    fail_reason_anchor = ('and', (('attr=', ('text', '知道了')),))
    filter_anchor = ('and', (('attr=', ('text', '仅显示无手机详情的宝贝')),))

    # 批量生成
    def batch_submit(self):
        element_click(self.batch_submit_locator)


    # 单个宝贝立即、重新生成
    def single_submit(self):
        element_click(self.single_submit_locator)


    # 获取失败原因
    def get_fail_reason(self) -> str:
        element_click(self.fail_reason_locator)
        reason_element = locate_by_anchor(init_element(self.fail_reason_anchor), 3, 'v0v1')
        return reason_element.get_text()







