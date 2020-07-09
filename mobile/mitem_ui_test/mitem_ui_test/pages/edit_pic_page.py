# -*- encoding=utf8 -*-
__author__ = 'xiaoxuan'

from mobile.mitem_ui_test.mitem_ui_test.pages.pic_room import *


class EditPic(BasePage):
    pic_anchor = ('and', (('attr=', ('text', '主图')),))
    delete_pic_locator = ('and', (('attr=', ('text', '删除图片')),))
    upload_pic_locator = ('and', (('attr=', ('text', '上传图片')),))
    update_locator = ('and', (('attr=', ('text', '更新到淘宝')),))
    fail_reason_locator = ('and', (('attr=', ('name', 'android:id/message')),))

    # 方法：点击指定位置的图片
    def choose_pic_position(self, pic_position: int):
        """

        :param pic_position:
        0:选择主图
        1:选择第一张子图
        2:选择第二张子图
        3:选择第三张子图
        4:选择白底图
        5:选择长图
        :return:
        """
        locate_by_anchor(init_element(self.pic_anchor), 2, 'l{}'.format(pic_position)).click()

    # 方法：删除所有图片
    def delete_all_pic(self):
        pic_amout = len(init_element(self.pic_anchor).parent().parent().child())  # 图片总数
        for x in range(pic_amout):
            self.choose_pic_position(x)
            element_click(self.delete_pic_locator)

    # 方法：进入图片空间
    def go_pic_zoom(self):
        element_click(self.upload_pic_locator)
        poco(text='图片空间').click()
        return PicRoom()

    # 方法：从本地相册选择一张图
    def choose_pic_from_ablum(self):
        element_click(self.upload_pic_locator)
        poco(text='本地相册').click()
        # 选择图片暂定
        pass
        poco(text='确定').click()

    # 方法：更新到淘宝
    def update_pic(self) -> bool:
        """

        :return:
        更新成功返回true，失败返回false
        """
        does_update_success = True
        element_click(self.update_locator)
        try:
            poco(text='温馨提示').wait_for_appearance(3)  # 等待接口结果，显示等待3s
        except PocoTargetTimeout:
            does_update_success = False
        return does_update_success

    # 方法：更新到淘宝失败后，获取失败原因
    def get_fail_reason(self) -> str:
        return get_text_of_view(init_element(self.fail_reason_locator))
