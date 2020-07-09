from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import *
from mobile.mtrade_ui_test.mtrade_ui_test.pages.blacklist_page import *
from mobile.mtrade_ui_test.mtrade_ui_test.pages.auto_evaluate_phrase_page import *
from mobile.mtrade_ui_test.mtrade_ui_test.pages.evaluate_record_page import *
from mobile.mtrade_ui_test.mtrade_ui_test.pages.order_list_page import OrderListPage


class AutoEvaluatePage(OrderListPage):
    main_switch_locator = (
        'index', (('/', (('^', (('and', (('attr=', ('text', '开启自动评价')),)), ('and', ()))), ('and', ()))), 1))  # 总开关
    evaluate_methods_locator = ('index', (
        ('/', (('^', (('^', (('and', (('attr=', ('text', '开启自动评价')),)), ('and', ()))), ('and', ()))), ('and', ()))),
        1))  # 自动评价-选择评价方式
    evaluate_methods_immediatly_locator = ('and', (('attr=', ('text', '立即评价')),))  # 自动评价-评价方式改成立即评价
    evaluate_methods_after_locator = ('and', (('attr=', ('text', '评价后回评')),))  # 自动评价-评价方式改成评价后回评
    evaluate_methods_sometime_locator = ('and', (('attr=', ('text', '定时评价')),))  # 自动评价-评价方式改成定时评价
    evaluate_methods_cancel_locator = ('and', (('attr=', ('text', '取消')),))  # 自动评价-评价方式取消更改
    blacklist_management_locator = ('and', (('attr=', ('text', '黑名单管理')),))  # 黑名单管理
    add_blacklist_switch_locator = ('index', (
        ('/', (('^', (('and', (('attr=', ('text', '中差评买家自动加入黑名单')),)), ('and', ()))), ('and', ()))), 1))  # 中差评自动加入黑名单开关
    blacklist_switch_locator = (
        'index',
        (('/', (('^', (('and', (('attr=', ('text', '黑名单用户不自动评价')),)), ('and', ()))), ('and', ()))), 1))  # 黑名单不评价开关
    cloud_blacklist_switch_locator = ('index', (
        ('/', (('^', (('and', (('attr=', ('text', '云黑名单中的买家不评价')),)), ('and', ()))), ('and', ()))), 1))  # 云黑名单不评价开关
    evalute_remind_switch_locator = ('/', (('index', (
        ('/', (('^', (('^', (('and', (('attr=', ('text', '中差评提醒')),)), ('and', ()))), ('and', ()))), ('and', ()))), 1)),
                                           ('and', ())))  # 中差评提醒开关
    edit_phone_locator = ('and', (('attr=', ('text', '接收手机号')),))  # 接收手机号
    evaluate_phrase_locator = ('and', (('attr=', ('text', '评价短语')),))  # 评价短语
    evaluate_record_locator = ('and', (('attr=', ('text', '评价记录')),))  # 评价记录
    edit_phone_number_locator = ('and', (('attr=', ('text', '请正确填写手机号')),))  # 编辑手机号
    phonenum_confirm_locator = ('and', (('attr=', ('text', '确定')),))  # 确定编辑
    phonenum_cancel_locator = ('and', (('attr=', ('text', '取消')),))  # 取消编辑
    methods_locator = ('index', (('/', (('index', (('/', (('index', (
        ('/', (('^', (('^', (('and', (('attr=', ('text', '开启自动评价')),)), ('and', ()))), ('and', ()))), ('and', ()))),
        1)),
                                                          ('and', ()))), 0)), ('and', ()))), 0))  # 自动评价方式

    def self_check(self):
        check = init_element(self.evaluate_record_locator)
        check.wait_for_appearance(5)

    # 方法：切换自动评价总开关
    def turn_main_switch(self):
        ay_click(self.main_switch_locator)

    # 方法：更改评价方式
    def change_evaluate_methods(self, evaluate_methods):
        ay_click(self.evaluate_methods_locator)
        ay_click(evaluate_methods)

    # 方法：返回页面上显示的评价方式
    def get_evaluate_methods(self):
        return ay_get_text(self.methods_locator)

    # 方法：取消评价方式修改
    def evaluate_methods_cancel(self):
        ay_click(self.evaluate_methods_locator)
        ay_click(self.evaluate_methods_cancel_locator)

    # 方法：切换中差评自动加入黑名单开关
    def turn_add_blacklist_switch(self):
        ay_click(self.add_blacklist_switch_locator)

    # 方法：切换黑名单不评价开关
    def turn_blacklist_switch(self):
        ay_click(self.blacklist_switch_locator)

    # 方法：切换云黑名单不评价开关
    def turn_cloud_blacklist(self):
        ay_click(self.cloud_blacklist_switch_locator)

    # 方法：切换中差评提醒开关
    def turn_evaluate_remind_switch(self):
        ay_click(self.evalute_remind_switch_locator)

    # 方法：编辑手机号并确认编辑
    def edit_phonenum(self, my_phonenum):
        ay_click(self.edit_phone_locator)
        ay_set_text(self.edit_phone_number_locator, my_phonenum)
        ay_click(self.phonenum_confirm_locator)

    # 方法：四个子开关，状态全部切换
    def turn_four_switch(self):
        self.turn_add_blacklist_switch()
        self.turn_blacklist_switch()
        self.turn_cloud_blacklist()
        self.turn_evaluate_remind_switch()

    # # 方法：四个子开关，状态恢复默认，全部开启
    # def recover_four_swtich(self):
    #     try:
    #         loop_find(Template(r"pic_data/tpl1582189593236.png", record_pos=(-0.001, -0.261), resolution=(1080, 2340),
    #                            threshold=0.95))
    #     except:
    #         self.turn_add_blacklist_switch()
    #     try:
    #         loop_find(Template(r"pic_data/tpl1582189599964.png", record_pos=(-0.003, -0.143), resolution=(1080, 2340),
    #                            threshold=0.95))
    #     except:
    #         self.turn_blacklist_switch()
    #     try:
    #         loop_find(Template(r"pic_data/tpl1582189608210.png", record_pos=(0.003, -0.025), resolution=(1080, 2340),
    #                            threshold=0.95))
    #     except:
    #         self.turn_cloud_blacklist()
    #     try:
    #         loop_find(Template(r"pic_data/tpl1582189614156.png", record_pos=(-0.003, 0.134), resolution=(1080, 2340),
    #                            threshold=0.95))
    #     except:
    #         self.turn_evaluate_remind_switch()

    # 方法：进入自动评价-黑名单管理页面
    def go_blacklist_page(self):
        ay_click(self.blacklist_management_locator)
        res = BlacklistPage()
        return res

    # 方法：进入自动评价-评价短语页面
    def go_evalaute_phrase(self):
        ay_click(self.evaluate_phrase_locator)
        res = PhraseFromAutoEvalaute()
        res.self_check()
        return res

    # 方法：进入自动评价-评价记录页面
    def go_evaluate_record(self):
        ay_click(self.evaluate_record_locator)
        return EvaluateRecordPage()
