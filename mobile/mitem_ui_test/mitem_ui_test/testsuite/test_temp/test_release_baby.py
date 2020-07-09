import allure
import pytest
from mobile.mitem_ui_test.mitem_ui_test.pages.first_page import *
from mobile.mitem_ui_test.mitem_ui_test.pages.release_baby_page import *


class TestRelease(BasePage):
    """
    1.进入普通发布
    2.添加必填信息, 点击'立即发布'
    3.判断发布成功的文本是否存在
    """

    @allure.feature('发布宝贝')
    @allure.story('普通发布宝贝成功')
    @pytest.mark.p1
    def test_release_baby_success(self, go_release_page):
        release_successful = ReleasePage().release_baby_success()
        assert release_successful, '普通发布宝贝失败'

    @allure.feature('发布宝贝')
    @allure.story('极速发布宝贝成功')
    @pytest.mark.p2
    def test_fast_release_baby_success(self, go_release_page):
        """
        1.进入极速发布
        2.添加宝贝主图,点击'立即发布'
        3.判断发布成功的文本是否存在
        :param go_release_page:
        :return:
        """
        fast_release_successful = ReleasePage().speed_post_success()
        assert fast_release_successful is True

    # @allure.feature('发布宝贝')
    # @allure.story('不添加主图,发布宝贝失败')
    # @pytest.mark.p3
    # def test_not_add_pictures(self, go_release_page):
    #     release_defeated = ReleasePage().no_pictures()
    #     assert release_defeated is False

    @allure.feature('发布宝贝')
    @allure.story('不输入价格和库存,发布宝贝失败')
    @pytest.mark.p3
    def test_not_enter_price_and_quantity(self, go_release_page):
        """
        1.进入普通发布
        2.不输入必填信息(库存和价格),点击'立即发布'
        3.判断是否存在发布成功的文本
        :param go_release_page:
        :return:
        """
        release_defeated = ReleasePage().no_price_num()
        assert release_defeated is False

    @allure.feature('发布宝贝')
    @allure.story('极速发布,定时发布宝贝成功')
    @pytest.mark.p4
    def test_time_release_baby(self, go_release_page):
        """
        1.进入极速发布
        2.添加宝贝主图,点击'定时发布'
        3.设置时间为当前时间之后
        4.判断发布到仓库成功的文本是否存在
        :param go_release_page:
        :return:
        """
        time_release_baby = ReleasePage().time_release_baby()
        assert time_release_baby is True

    @allure.feature('发布宝贝')
    @allure.story('极速发布,宝贝放入仓库成功')
    @pytest.mark.p5
    def test_in_the_warehouse(self, go_release_page):
        """
        1.进入极速发布
        2.添加宝贝主图,点击'放入仓库'
        3.判断放入到仓库成功的文本是否存在
        :param go_release_page:
        :return:
        """
        in_warehouse = ReleasePage().baby_in_warehouse()
        assert in_warehouse is True
