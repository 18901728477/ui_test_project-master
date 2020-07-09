__author__ = 'xiaoxuan'

from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import *
from poco.exceptions import *


class PicRoom(BasePage):
    submit_button_locator = ('and', (('attr=', ('text', '选择图片')),))

    # 方法：进入某个文件夹
    def enter_dict(self, dict_name: str) -> bool:
        """

        :param dict_name:
        文件夹全名
        :return:
        文件夹存在返回true，不存在返回false
        """
        does_dict_exsit = True
        try:
            poco(text=dict_name).click()
        except PocoNoSuchNodeException:
            does_dict_exsit = False
        return does_dict_exsit

    # 方法：选择某一张图片
    def choose_pic(self, pic_name: str) -> bool:
        """

        :param pic_name:
        所选图片全名：xxxxx.jpg
        :return:
        图片存在返回true，不存在返回false
        """
        does_pic_exsit = True
        try:
            poco(text=pic_name).invalidate()
            poco(text=pic_name).click()
        except PocoNoSuchNodeException:
            does_pic_exsit = False
        return does_pic_exsit

    # 方法：提交图片
    def submit_pic(self):
        element_click(self.submit_button_locator)
