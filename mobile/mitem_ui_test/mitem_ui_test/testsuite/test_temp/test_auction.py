import allure
import pytest

from mobile.mitem_ui_test.mitem_ui_test.pages.auction_common_methods import AuctionCommonMethods
from mobile.mitem_ui_test.mitem_ui_test.pages.auction_page import AuctionPage


class TestAuction:
    auction_common = AuctionCommonMethods()

    @allure.feature('淘宝拍卖')
    @allure.story('九块九创建活动成功')
    @pytest.mark.run(order=1)
    def test_nine_activities_successful(self, go_auction_page):
        """
        1. 进入九块九页面
        2.选择宝贝,输入正确数据
        3.点击'上架预展',成功后返回拍卖主页
        4.获取预展中的数据,判断是否+1
        :return:
        """
        # 创建活动前获取预展中的数量
        pre_creation_quantity = self.auction_common.get_amount_in_preview()
        AuctionPage().nine_activities_successful()
        # 创建活动后获取预展中的数量
        amount_created = self.auction_common.get_amount_in_preview()
        # 断言: 预展中数量是否+1
        assert pre_creation_quantity != amount_created

    @allure.feature('淘宝拍卖')
    @allure.story('九块九创建,拍卖数量大于库存')
    @pytest.mark.run(order=2)
    def test_nine_activities_fail(self, go_auction_page):
        """
        1. 进入九块九页面
        2.选择宝贝,输入拍卖数量大于库存
        3.点击'上架预展'
        4.判断是否出现'确定上架预展'按钮
        :return:
        """
        nine_activities_fail = AuctionPage().nine_activities_fail()
        # 断言:
        assert nine_activities_fail is False

    @allure.feature('淘宝拍卖')
    @allure.story('任意降创建活动成功')
    @pytest.mark.run(order=3)
    def test_any_drop_successful(self, go_auction_page):
        """
        1.进入任意降页面
        2.选择宝贝,输入正确数据
        3.点击'上架预展'
        4.获取预展中的数据,判断是否+1
        该用例可能失败(默认时间为当前时间,提交可能一直提示开始时间错误,之后会优化)
        :return:
        """
        # 创建活动前获取预展中的数量
        pre_creation_quantity = self.auction_common.get_amount_in_preview()
        AuctionPage().any_drop_successful()
        # 创建活动后获取预展中的数量
        amount_created = self.auction_common.get_amount_in_preview()
        # 断言: 预展中数量是否+1
        assert pre_creation_quantity != amount_created

    @allure.feature('淘宝拍卖')
    @allure.story('任意降创建活动成功,放入仓库中')
    @pytest.mark.run(order=4)
    def test_any_drop_warehouse(self, go_auction_page):
        """
        1.进入任意降页面
        2.选择宝贝,输入正确数据
        3.点击'放入仓库中'
        4.获取仓库中的数据,判断是否+1
        该用例可能失败(默认时间为当前时间,提交可能一直提示开始时间错误,之后会优化)
        :return:
        """
        # 创建活动前获取仓库中的数量
        in_warehouse_quantity1 = self.auction_common.get_amount_in_warehouse()
        AuctionPage().any_drop_warehouse()
        # 创建活动后获取仓库中的数量
        in_warehouse_quantity2 = self.auction_common.get_amount_in_warehouse()
        assert in_warehouse_quantity1 != in_warehouse_quantity2

    @allure.feature('淘宝拍卖')
    @allure.story('任意降创建活动失败,降价周期小于等于1')
    @pytest.mark.run(order=5)
    def test_any_drop_fail(self, go_auction_page):
        """
        1. 进入任意降页面
        2.选择宝贝,计算降价周期小于等于1
        3.点击'上架预展'
        4.判断是否出现'确定上架预展'按钮
        :return:
        """
        any_drop_fail = AuctionPage().any_drop_fail()
        # 断言:
        assert any_drop_fail is False

    @allure.feature('淘宝拍卖')
    @allure.story('增价拍创建活动成功')
    @pytest.mark.run(order=6)
    def test_pat_successful(self, go_auction_page):
        """
        1. 进入增价拍页面
        2.选择宝贝,输入正确数据
        3.点击'上架预展',成功后返回拍卖主页
        4.获取预展中的数据,判断是否+1
        :return:
        """
        # 创建活动前获取预展中的数量
        pre_creation_quantity = self.auction_common.get_amount_in_preview()
        AuctionPage().pat_increase_successful()
        # 创建活动后获取预展中的数量
        amount_created = self.auction_common.get_amount_in_preview()
        # 断言: 预展中数量是否+1
        assert pre_creation_quantity != amount_created

    @allure.feature('淘宝拍卖')
    @allure.story('增价拍创建活动成功')
    @pytest.mark.run(order=7)
    def test_pat_warehouse(self, go_auction_page):
        """
        1. 进入增价拍页面
        2.选择宝贝,输入正确数据
        3.点击'放入仓库中',成功后返回拍卖主页
        4.获取仓库中的数据,判断是否+1
        :return:
        """
        # 获取创建活动之前仓库中的数量
        in_warehouse_quantity1 = self.auction_common.get_amount_in_warehouse()
        AuctionPage().pat_increase_warehouse()
        # 创建活动后获取仓库中的数量
        in_warehouse_quantity2 = self.auction_common.get_amount_in_warehouse()
        assert in_warehouse_quantity1 != in_warehouse_quantity2

    @allure.feature('淘宝拍卖')
    @allure.story('增价拍创建活动失败,不输入起拍价和加价规则')
    @pytest.mark.run(order=8)
    def test_pat_fail(self, go_auction_page):
        """
        1. 进入增价拍页面
        2.选择宝贝,输入数据
        3.点击'上架预展'
        4.判断是否出现'确定上架预展'按钮
        :return:
        """
        price_empty = AuctionPage().price_is_empty()
        # 断言:
        assert price_empty is False
