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
    in_warehouse_locator = ('and', (('attr=', ('text', '放入仓库中')),))
    sure_in_warehouse_locator = ('and', (('attr=', ('text', '确定放入仓库')),))
    bottom_price_locator = ('and', (('attr=', ('name', 'android.widget.EditText')),))
    in_preview_locator = ('and', (('attr=', ('text', '预展中')),))
    in_shooting_locator = ('and', (('attr=', ('text', '开拍中')),))
    in_warehouse_locator2 = ('and', (('attr=', ('text', '仓库中')),))
    input_pattern = ('and', (('attr=', ('name', 'android:id/toggle_mode')),))
    minute_locator = ('and', (('attr=', ('name', 'android:id/input_minute')),))
    hour_locator = ('and', (('attr=', ('name', 'android:id/input_hour')),))

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
        # 等待页面跳转成功
        init_element(self.choose_products_locator).wait_for_appearance(10)
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
        # 降价幅度
        poco(name='android.widget.EditText')[3].set_text(price_cut)
        # 保证金
        poco(name='android.widget.EditText')[4].set_text(earnest_money)
        # 点击'计算降价周期'按钮
        init_element(self.price_cycle_button).click()

    # 点击'放入仓库中'
    def in_warehouse(self):
        init_element(self.in_warehouse_locator).click()
        init_element(self.sure_in_warehouse_locator).click()

    # 输入起拍价和加价规则
    def rules_for_starting_price(self, starting_price, rules):
        init_element(self.bottom_price_locator).set_text(starting_price)
        init_element(self.bottom_price_locator)[1].set_text(rules)

    # 输入重复上架和封顶价
    def repetition_and_top_price(self, repetition, top_price):
        init_element(self.bottom_price_locator)[2].set_text(repetition)
        init_element(self.bottom_price_locator)[3].set_text(top_price)

    #  获取预展中的数量
    def get_amount_in_preview(self):
        pre_creation_quantity = locate_by_anchor(init_element(self.in_preview_locator), 1, 'v0').get_text()
        print('创建活动预展中的数量:', pre_creation_quantity)
        return pre_creation_quantity

    # 获取开拍中的数量
    def get_amount_in_shots(self):
        in_shooting_quantity = locate_by_anchor(init_element(self.in_shooting_locator), 1, 'v0').get_text()
        print('创建活动开拍中的数量:', in_shooting_quantity)
        return in_shooting_quantity

    # 获取仓库中的数量
    def get_amount_in_warehouse(self):
        in_warehouse_quantity = locate_by_anchor(init_element(self.in_warehouse_locator2), 1, 'v0').get_text()
        print('创建活动仓库中的数量:', in_warehouse_quantity)
        return in_warehouse_quantity

    # 日历插件: 设置时间
    def set_time(self):
        # 打开日历
        locate_by_anchor(init_element(self.starting_time_locator), 1, 'l1l1').click()
        # 点击确定
        poco(text="确定").click()
        # 切换到输入模式,获取分钟的文本信息,基础上加2分钟,如果到58时,则获取小时的文本,基础上加1小时
        init_element(self.input_pattern).click()
        minute1 = init_element(self.minute_locator).get_text()
        if int(minute1) == 58:
            hour1 = init_element(self.hour_locator).get_text()
            hour2 = int(hour1) + 1
            element_sendtext(self.hour_locator, hour2)
            # 点击确定
            poco(name="android:id/button1").click()
        else:
            minute2 = int(minute1) + 2
            element_sendtext(self.minute_locator, minute2)
            # 点击确定
            poco(name="android:id/button1").click()


if __name__ == '__main__':
    AuctionCommonMethods().nine_page()
    AuctionCommonMethods().choose_products()
