from time import sleep

from mobile.mtrade_ui_test.mtrade_ui_test.pages.auto_evaluate_page import AutoEvaluatePage
from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import BasePage, init_element, ay_click, poco, locate_by_anchor
from mobile.mtrade_ui_test.mtrade_ui_test.pages.batch_send_goods_page import BatchSendGoodsPage
from mobile.mtrade_ui_test.mtrade_ui_test.pages.batch_evaluation_page import BatchEvaluationPage
from mobile.mtrade_ui_test.mtrade_ui_test.pages.negative_comment_interception_page import NegativeCommentInterception
from mobile.mtrade_ui_test.mtrade_ui_test.pages.evaluation_management_page import EvalutionManagementPage
from mobile.mtrade_ui_test.mtrade_ui_test.pages.my_page import MyPage
from mobile.mtrade_ui_test.mtrade_ui_test.pages.order_list_page import OrderListPage
from mobile.mtrade_ui_test.mtrade_ui_test.pages.wait_buyer_confirm_goods_page import WaitBuyerConfirmGoods


class FirstPage(BasePage):
    evalution_management_button_locator = ('and', (('attr=', ('text', '评价管理')),))
    batch_send_goods_button_locator = ('and', (('attr=', ('text', '批量发货')),))
    search_box_locator = ('and', (('attr=', ('text', '订单号/昵称/宝贝关键词/手机号/运单号...')),))  # 搜索框
    search_text_box_locator = ('and', (('attr=', ('name', 'android.widget.EditText')),))  # 搜索文本框
    order_number_label_locator = ('and', (('attr=', ('text', '订单号')),))  # 订单号标签
    release_taobao_button_locator = ('and', (('attr=', ('text', '发微淘')),))
    taobao_workbench_title_locator = ('and', (('attr=', ('text', '微淘工作台')),))
    taobao_broadcast_button_locator = ('and', (('attr=', ('text', '淘大直播')),))
    watch_broadcast_text_locator = ('and', (('attr=', ('text', '立即观看直播>')),))
    violation_words_check_button_locator = ('and', (('attr=', ('text', '违规词检测')),))
    item_on_sale_text_locator = ('and', (('attr=', ('text', '出售中')),))
    confirm_auth_button_locator = ('and', (('attr=', ('text', '确认授权')),))
    wait_buyer_pay_locator = ('and', (('attr=', ('text', '待付款')),))
    buttom_anchor = ('and', (('attr=', ('name', 'com.taobao.qianniu:id/tab_container')),))
    automatic_evaluation_locator = ('and', (('attr=', ('text', '自动评价')),))  # 自动评价
    negative_comment_interception_locator = ('and', (('attr=', ('text', '差评拦截')),))  # 差评拦截
    batch_evaluation_locator = ('and', (('attr=', ('text', '批量评价')),))  # 批量评价
    seller_tools_locator = ('and', (('attr=', ('text', '卖家工具')),))  # 卖家工具

    def self_check(self):
        check = init_element(self.seller_tools_locator)
        check.wait_for_appearance(10)

    # 首页进入我的页面
    @staticmethod
    def  go_my_page():
        p = poco("android:id/content").offspring("android.widget.LinearLayout")
        my = locate_by_anchor(p, 0, 'l2')
        my.click()
        return MyPage()

    # 首页进待付款列表页面
    def go_wait_buyer_pay_page(self):
        ay_click(self.wait_buyer_pay_locator)
        return OrderListPage()

    # 进入评价管理页面
    def go_evalution_management(self):
        ay_click(self.evalution_management_button_locator)
        return EvalutionManagementPage()

    # 进入批量发货列表
    def go_batch_send_goods_page(self):
        ay_click(self.batch_send_goods_button_locator)
        batch_send_goods_page = BatchSendGoodsPage()
        batch_send_goods_page.self_check()
        return batch_send_goods_page

    # 根据订单号搜索
    def search_order_by_No(self, order_no):
        ay_click(self.search_box_locator)
        search_text_box = init_element(self.search_text_box_locator)
        order_number_label = init_element(self.order_number_label_locator)
        search_text_box.wait()
        search_text_box.set_text(order_no)
        order_number_label.click()
        return OrderListPage()

    # 进入发微淘页面
    def go_release_taobao_page(self):
        release_taobao_button = init_element(self.release_taobao_button_locator)
        release_taobao_button.wait_for_appearance()
        release_taobao_button.click()
        taobao_workbench_title = init_element(self.taobao_workbench_title_locator)
        taobao_workbench_title.wait_for_appearance()
        return poco(text='微淘工作台').exists()

    # 进入淘大直播页面
    def go_taobao_broadcast_page(self):
        taobao_broadcast_button = init_element(self.taobao_broadcast_button_locator)
        taobao_broadcast_button.wait_for_appearance()
        taobao_broadcast_button.click()
        watch_broadcast_text = init_element(self.watch_broadcast_text_locator)
        watch_broadcast_text.wait_for_appearance()
        return poco(text='立即观看直播>').exists()

    # 进入违规词检测页面
    def go_violation_words_check_page(self):
        violation_words_check_button = init_element(self.violation_words_check_button_locator)
        violation_words_check_button.click()
        if poco(text='立即授权').exists():
            confirm_auth_button = init_element(self.confirm_auth_button_locator)
            confirm_auth_button.click()
        BasePage().refresh()

        return poco(text='违规词检测').exists()

    # 首页进入订单列表页面
    def go_order_list_page(self):
        order_list_element = locate_by_anchor(init_element(self.buttom_anchor), 0, 'l0l0l1')
        order_list_element.click()
        return WaitBuyerConfirmGoods()

    # 首页进入自动评价页面
    def go_auto_evaluate_page(self):
        ay_click(self.automatic_evaluation_locator)
        res = AutoEvaluatePage()
        res.self_check()
        return res

    # 首页进入批量评价页面
    def go_batch_evaluation_page(self):
        batch_evaluation = init_element(self.batch_evaluation_locator)
        batch_evaluation.click()
        return BatchEvaluationPage()

    # 首页进入差评拦截页面
    def go_negative_comment_interception_page(self):
        negative_comment_interception_page = init_element(self.negative_comment_interception_locator)
        negative_comment_interception_page.click()
        return NegativeCommentInterception()


if __name__ == '__main__':
    f = FirstPage()
    f.go_my_page()
