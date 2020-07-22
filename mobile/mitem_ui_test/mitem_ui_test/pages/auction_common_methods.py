from poco.proxy import UIObjectProxy

from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import BasePage, init_element, locate_by_anchor, poco, sleep, \
    element_click, element_sendtext
from mobile.mitem_ui_test.mitem_ui_test.pages.common_list_page import CommonList


class AuctionCommonMethods(BasePage):
    sign_up_immediately_locator = ('and', (('attr=', ('text', '立即报名')),))
    pat_increase_locator = ('and', (('attr=', ('text', '增价拍')),))
    arbitrary_drop_locator = ('and', (('attr=', ('text', '任意降')),))
    choose_products_locator = ('and', (('attr=', ('text', '选择活动的宝贝')),))
    copy_baby_button = ('and', (('attr=', ('text', '复制宝贝')),))
    number_locator = ('and', (('attr=', ('name', 'android.widget.EditText')),))
    on_preview_locator = ('and', (('attr=', ('text', '上架预展')),))
    confirm_shelf_locator = ('and', (('attr=', ('text', '确定上架预展')),))
    price_cycle_button = ('and', (('attr=', ('text', '计算降价周期')),))
    starting_time_locator = ('and', (('attr=', ('text', '开始时间')),))
    end_time_locator = ('and', (('attr=', ('text', '结束时间')),))
    # 进入九块九页面
    def nine_page(self):
        init_element(self.sign_up_immediately_locator).click()

    # 进入任意降页面
    def arbitrary_drop_page(self):
        locate_by_anchor(poco(text='任意降'), 2, 'v3v1').click()

    # 进入增价拍页面
    def pat_increase_page(self):
        locate_by_anchor(poco(text='增价拍'), 2, 'v3v1').click()

    # 选择宝贝
    def choose_products(self):
        # 点击'+'
        locate_by_anchor(init_element(self.choose_products_locator), 1, 'v0').click()
        # 搜索宝贝,点击'复制宝贝'
        CommonList().search_by_keyword('测试宝贝不发货', poco(text='测试宝贝不发货不发货'))
        poco(text='测试宝贝不发货不发货').click()
        init_element(self.copy_baby_button).click()

    # 输入拍卖数量
    def auction_number(self, number):
        init_element(self.number_locator).set_text(number)

    # 修改活动时间(九块九)
    def activity_time(self):
        poco(text="09:00-12:00").click()
        poco(text="9:00-12:00").click()

    # 点击上架预展
    def click_on_preview_button(self):
        init_element(self.on_preview_locator).click()
        init_element(self.confirm_shelf_locator).click()

    # 授权
    def impower(self):
        poco(name="android:id/button2").click()
        poco(name='com.taobao.qianniu:id/open_auth_btn_grant').click()

    # 输入拍卖数量,起拍价,保底价
    def number_and_price(self, number2, starting_price, base_price):
        # 输入拍卖数量
        poco(name='android.widget.EditText').set_text(number2)
        # 起拍价
        poco(name='android.widget.EditText')[1].set_text(starting_price)
        # 保底价
        poco(name='android.widget.EditText')[2].set_text(base_price)

    # 输入降价幅度和保证金
    def reduction_and_margin(self, price_cut, earnest_money):
        # 上滑
        poco("android.widget.FrameLayout").swipe([0, -0.2])
        # 降价幅度
        poco(name='android.widget.EditText')[3].set_text(price_cut)
        # 保证金
        poco(name='android.widget.EditText')[4].set_text(earnest_money)
        # 点击'计算降价周期'按钮
        init_element(self.price_cycle_button).click()













if __name__ == '__main__':
    # AuctionCommonMethods().choose_products()
    AuctionCommonMethods().activity_time()
