from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import *
from mobile.mitem_ui_test.mitem_ui_test.pages.first_page import *
from mobile.mitem_ui_test.mitem_ui_test.pages.badword_detect_page import *

import allure
import pytest


class TestBadwordDetect:

    @allure.feature('违规词检测')
    @allure.story('检测结果页面，可以正常全选，一键删除')
    @pytest.mark.p1
    def test_start_detect(self, go_badword_detect_page):
        FirstPage().go_badword_detect()
        BadwordDetect().choose_item_state(0)
        detect_state = BadwordDetect().start_detect()
        assert detect_state, '出售中宝贝无违规词、有沙雕把出售中的保温杯全部下架了！'

    @allure.feature('违规词检测')
    @allure.story('宝贝信息页面，可以正常全选，删除所有宝贝的违规词')
    @pytest.mark.p2
    def test_delete_detail_page(self, go_badword_detect_page):
        FirstPage().go_badword_detect()
        BadwordDetect().choose_item_state(0)
        detect_state = BadwordDetect().delete_detail_page()
        assert detect_state, '出售中宝贝无违规词、有沙雕把出售中的保温杯全部下架了！'
