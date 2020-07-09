
from mobile.mitem_ui_test.mitem_ui_test.pages.first_page import *
import pytest

class TestFirstPage:

    @allure.feature('首页')
    @allure.story('活动日历跳转')
    @pytest.mark.p1
    # @pytest.mark.skip(reason="bug:活动日历到期后，首页、列表、详情部分手机还是会显示")
    def test_activity_calendar(self, first_page_wait):
        assert first_page_wait.test_activity_calendar_first_page(), '首页活动日历，无法正常跳转'
