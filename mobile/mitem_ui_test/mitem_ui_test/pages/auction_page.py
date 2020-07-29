from mobile.mitem_ui_test.mitem_ui_test.pages.auction_common_methods import AuctionCommonMethods
from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import BasePage, init_element, locate_by_anchor, poco, sleep


class AuctionPage(BasePage):
    impower_locator = ('and', (('attr=', ('text', '去授权')),))
    on_preview_locator = ('and', (('attr=', ('text', '上架预展')),))

    auction_common = AuctionCommonMethods()

    # 九块九--创建活动成功
    def nine_activities_successful(self):
        # 进入九块九页面
        self.auction_common.nine_page()
        # 选择宝贝
        self.auction_common.choose_products()
        # 输入拍卖数量
        self.auction_common.auction_number(1)
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

    # 九块九--创建活动--拍卖数量大于库存,创建失败
    def nine_activities_fail(self):
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
        # 进入任意降页面
        self.auction_common.arbitrary_drop_page()
        # 输入拍卖数量,起拍价,保底价
        self.auction_common.number_and_price(1, 100, 88)
        # 设置时间
        self.auction_common.set_time()
        # 输入降价幅度和保证金,点击'计算降价周期'按钮
        self.auction_common.reduction_and_margin(5, 999)
        # 选择宝贝
        self.auction_common.choose_products()
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

    # 任意降--创建活动--点击'放入仓库中'成功
    def any_drop_warehouse(self):
        # 进入任意降页面
        self.auction_common.arbitrary_drop_page()
        # 输入拍卖数量,起拍价,保底价
        self.auction_common.number_and_price(1, 100, 88)
        # 设置时间
        self.auction_common.set_time()
        # 输入降价幅度和保证金,点击'计算降价周期'按钮
        self.auction_common.reduction_and_margin(5, 999)
        # 选择宝贝
        self.auction_common.choose_products()
        # 点击放入仓库中
        self.auction_common.in_warehouse()
        # 放入仓库中之前判断是否需要授权
        if init_element(self.impower_locator).exists():
            self.auction_common.impower()
            # 点击放入仓库中
            self.auction_common.in_warehouse()
        sleep(5)
        # 返回拍卖主页
        poco(name="com.taobao.qianniu:id/qn_widmill_nav_bar_back_btn").click()

    # 任意降--创建活动失败--计算降价周期小于等于1
    def any_drop_fail(self):
        # 进入任意降页面
        self.auction_common.arbitrary_drop_page()
        # 输入拍卖数量,起拍价,保底价
        self.auction_common.number_and_price(1, 8888, 88888)
        # 设置时间
        self.auction_common.set_time()
        # 输入降价幅度和保证金,点击'计算降价周期'按钮
        self.auction_common.reduction_and_margin(888, 999)
        # 选择宝贝
        self.auction_common.choose_products()
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

    # 增价拍--创建活动成功--上架预展
    def pat_increase_successful(self):
        # 进入增价拍页面
        self.auction_common.pat_increase_page()
        # 选择宝贝
        self.auction_common.choose_products()
        # 输入起拍价,加价规则
        self.auction_common.rules_for_starting_price(123456, 321)
        # 输入重复上架,封顶价
        self.auction_common.repetition_and_top_price(0, 0)
        # 设置时间
        self.auction_common.set_time()
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

    # 增价拍--创建活动成功--放入仓库中
    def pat_increase_warehouse(self):
        # 进入增价拍页面
        self.auction_common.pat_increase_page()
        # 选择宝贝
        self.auction_common.choose_products()
        # 输入起拍价,加价规则
        self.auction_common.rules_for_starting_price(123456, 321)
        # 输入重复上架,封顶价
        self.auction_common.repetition_and_top_price(0, 0)
        # 设置时间
        self.auction_common.set_time()
        # 点击放入仓库中
        self.auction_common.in_warehouse()
        # 放入仓库中之前判断是否需要授权
        if init_element(self.impower_locator).exists():
            self.auction_common.impower()
            # 点击放入仓库中
            self.auction_common.in_warehouse()
        sleep(5)
        # 返回拍卖主页
        poco(name="com.taobao.qianniu:id/qn_widmill_nav_bar_back_btn").click()

    # 增价拍--创建活动失败--不输入起拍价和加价规则
    def price_is_empty(self):
        # 进入增价拍页面
        self.auction_common.pat_increase_page()
        # 选择宝贝
        self.auction_common.choose_products()
        # 输入重复上架,封顶价
        self.auction_common.repetition_and_top_price(9, 999999)
        # 设置时间
        self.auction_common.set_time()
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


if __name__ == '__main__':
    AuctionPage().pat_increase_successful()
