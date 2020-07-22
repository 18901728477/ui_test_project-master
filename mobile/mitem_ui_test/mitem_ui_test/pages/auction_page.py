from mobile.mitem_ui_test.mitem_ui_test.pages.auction_common_methods import AuctionCommonMethods
from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import BasePage, init_element, locate_by_anchor, poco, sleep


class AuctionPage(BasePage):
    in_preview_locator = ('and', (('attr=', ('text', '预展中')),))
    impower_locator = ('and', (('attr=', ('text', '去授权')),))
    on_preview_locator = ('and', (('attr=', ('text', '上架预展')),))
    in_shooting_locator = ('and', (('attr=', ('text', '开拍中')),))
    in_warehouse_locator = ('and', (('attr=', ('text', '仓库中')),))
    auction_common = AuctionCommonMethods()

    # 九块九--创建活动成功
    def nine_activities_successful(self):
        # 创建活动前获取预展中的数量
        pre_creation_quantity = locate_by_anchor(init_element(self.in_preview_locator), 1, 'v0').get_text()
        print(pre_creation_quantity)
        # 进入九块九页面
        self.auction_common.nine_page()
        # 选择宝贝
        self.auction_common.choose_products()
        # 输入拍卖数量
        self.auction_common.auction_number(88)
        # 修改活动时间
        self.auction_common.activity_time()
        # 点击上架预展
        self.auction_common.click_on_preview_button()
        # 上架预展前判断是否需要授权
        if init_element(self.impower_locator).exists():
            self.auction_common.impower()
            # 点击上架预展
            self.auction_common.click_on_preview_button()
        sleep(5)
        # 返回拍卖主页
        poco(name="com.taobao.qianniu:id/qn_widmill_nav_bar_back_btn").click()
        amount_created = locate_by_anchor(init_element(self.in_preview_locator), 1, 'v0').get_text()
        print(amount_created)
        # 断言: 预展中数量是否+1
        assert pre_creation_quantity != amount_created

    # 九块九--创建活动--拍卖数量大于库存,创建失败
    def nine_activities_fail(self):
        # 创建活动前获取预展中的数量
        pre_creation_quantity2 = locate_by_anchor(init_element(self.in_preview_locator), 1, 'v0').get_text()
        print(pre_creation_quantity2)
        # 进入九块九页面
        self.auction_common.nine_page()
        # 选择宝贝
        self.auction_common.choose_products()
        # 输入拍卖数量
        self.auction_common.auction_number(999)
        # 点击上架预展
        init_element(self.on_preview_locator).click()
        # 上架预展前判断是否需要授权
        if init_element(self.impower_locator).exists():
            self.auction_common.impower()
            # 点击上架预展
            init_element(self.on_preview_locator).click()
        # 断言
        try:
            # 确定上架预展是否存在
            poco(text='确定上架预展').exists()
            poco(text='确定上架预展').click()
        except Exception:
            return False

    # 任意降--创建活动成功(使用默认时间,进入开拍中)
    def any_drop_successful(self):
        # 创建活动前获取开拍中的数量
        in_shooting_quantity1 = locate_by_anchor(init_element(self.in_shooting_locator), 1, 'v0').get_text()
        print('创建活动之前开拍中的数量', in_shooting_quantity1)
        # 进入任意降页面
        self.auction_common.arbitrary_drop_page()
        # 选择宝贝
        self.auction_common.choose_products()
        # 输入拍卖数量,起拍价,保底价
        self.auction_common.number_and_price(20, 100, 88)
        # 输入降价幅度和保证金,点击'计算降价周期'按钮
        self.auction_common.reduction_and_margin(5, 999)
        # 点击上架预展
        self.auction_common.click_on_preview_button()
        # 上架预展前判断是否需要授权
        if init_element(self.impower_locator).exists():
            self.auction_common.impower()
            # 点击上架预展
            self.auction_common.click_on_preview_button()
        sleep(5)
        # 返回拍卖主页
        poco(name="com.taobao.qianniu:id/qn_widmill_nav_bar_back_btn").click()
        in_shooting_quantity2 = locate_by_anchor(init_element(self.in_shooting_locator), 1, 'v0').get_text()
        print('创建活动之后开拍中的数量', in_shooting_quantity2)
        # 断言: 开拍中数量是否+1
        assert in_shooting_quantity1 != in_shooting_quantity2

    # 任意降--创建活动--放入仓库中成功
    def any_drop_warehouse(self):
        # 创建活动前获取仓库中的数量
        in_warehouse_quantity1 = locate_by_anchor(init_element(self.in_warehouse_locator), 1, 'v0').get_text()
        print('创建活动之前仓库中的数量', in_warehouse_quantity1)
        # 进入任意降页面
        self.auction_common.arbitrary_drop_page()
        # 选择宝贝
        self.auction_common.choose_products()
        # 输入拍卖数量,起拍价,保底价
        self.auction_common.number_and_price(20, 100, 88)
        # 输入降价幅度和保证金,点击'计算降价周期'按钮
        self.auction_common.reduction_and_margin(5, 999)
        # 点击放入仓库中
        # 放入仓库中之前判断是否需要授权
        if init_element(self.impower_locator).exists():
            self.auction_common.impower()
            # 点击放入仓库中










if __name__ == '__main__':
    AuctionPage().nine_activities_fail()
