from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import *
from mobile.mitem_ui_test.mitem_ui_test.pages.first_page import *
from mobile.mitem_ui_test.mitem_ui_test.pages.badword_detect_page import *

import allure
import pytest


class TestBadwordDetect:

    @allure.feature('违规词检测')
    @allure.story('状态可以正常切换')
    def test_choose_onsale_state(self, go_badword_detect_page):
        FirstPage().go_badword_detect()
        expected_state = BadwordDetect().choose_item_state(0)
        assert expected_state, '选择出售中状态错误！'
        expected_state = BadwordDetect().choose_item_state(1)
        assert expected_state, '选择仓库中状态错误！'

