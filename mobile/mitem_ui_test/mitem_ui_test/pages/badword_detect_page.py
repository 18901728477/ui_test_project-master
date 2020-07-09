from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import *


class BadwordDetect(BasePage):
    start_detect_locator = ('and', (('attr=', ('text', '开始检测')),))
    choose_detected_item_locator = ('and', (('attr=', ('text', '选择检测宝贝:')),))
    cancel_button_locator = ('and', (('attr=', ('text', '取消')),))
    all_choose_locator = ('and', (('attr=', ('text', '全选')),))
    bad_word_anchor = ('and', (('attr=', ('text', '包含违规词"top"')),))

    # 选择宝贝状态
    def choose_item_state(self, state: int):
        """

        :param state:
        0:出售中宝贝，1：仓库中宝贝
        :return:
        """
        if state == 0:
            poco(text='出售中').click()
        elif state == 1:
            poco(text='仓库中').click()

    def check_now(self):
        element_click(self.start_detect_locator)

    def close_no_item_window(self) -> bool:
        try:
            poco(text='恭喜您，未检测到违规词，请继续保持，有宝贝更新再检测~').wait_for_appearance(10)
        except PocoTargetTimeout:
            return False
        poco(text='确定').click()
        return True

    # 开始检测
    def start_detect(self) -> bool:
        """

        :return:
        出售中宝贝无违规词时，返回false
        出售中宝贝违规词全部删除成功，返回false
        """
        start_detect = init_element(self.start_detect_locator)
        start_detect.click()
        try:
            poco(text='全选').wait_for_appearance(10)  # 等待检测完毕，10秒显示等待
        except PocoTargetTimeout:
            poco(text='确定').click()
            return False
        else:
            all_choose_button = locate_by_anchor(init_element(self.all_choose_locator), 1, 'l0')
            delete_button = locate_by_anchor(init_element(self.all_choose_locator), 2, 'l1')
            all_choose_button.click()
            delete_button.click()
            try:
                poco(text='前往修改').wait_for_appearance(10)  # 删除失败后，10秒显示等待
            except PocoTargetTimeout:
                return False
            return poco(text='原因：属性值最大长度为32个字符(16个汉字) !').exists()

    # 宝贝信息页，删除违规词
    def delete_detail_page(self):
        start_detect = init_element(self.start_detect_locator)
        start_detect.click()
        try:
            poco(text='全选').wait_for_appearance(10)  # 等待检测完毕，10秒显示等待
        except PocoTargetTimeout:
            poco(text='确定').click()
            return False
        else:
            locate_by_anchor(init_element(self.bad_word_anchor), 2, 'v1l2').click()
            all_choose_button = locate_by_anchor(init_element(self.all_choose_locator), 1, 'l0')
            all_choose_button.click()
            poco(textMatches='.*删除违规词.*').click()
            try:
                poco(text='前往修改').wait_for_appearance(10)  # 删除失败后，10秒显示等待
                return poco(text='原因： 属性值最大长度为32个字符(16个汉字) !').exists()
            except PocoTargetTimeout:
                return False


if __name__ == '__main__':
    print(BadwordDetect().start_detect())
# poco(text = '确定').click()
