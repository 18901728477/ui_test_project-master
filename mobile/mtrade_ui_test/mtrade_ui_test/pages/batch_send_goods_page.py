import time

from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import BasePage, poco, init_element, locate_by_anchor, get_wait_send_goods_number, ay_exists, \
    ay_click


# from conftest import refresh


class BatchSendGoodsPage(BasePage):
    batch_send_goods_button_locator = (
        'and', (('attr=', ('name', 'android.widget.Button')), ('attr=', ('text', '批量发货'))))  # 页面批量发货按钮
    choose_express_locator = ('and', (('attr=', ('text', '选择快递')),))  # 选择快递
    confirm_button_locator = ('and', (('attr=', ('text', '确定')),))  # 确定按钮
    all_deliver_button_locator = ('and', (('attr=', ('text', '全部发货')),))  # 全部发货
    change_mode_locator = ('and', (('attr=', ('text', '更改发货方式')),))  # 更改发货方式
    offline_delivery_button_locator = ('and', (('attr=', ('text', '自己联系')),))  # 自己联系
    offline_delivery_info_locator = ('and', (('attr=', ('text', '当前为自己联系')),))  # 当前为自己联系
    online_delivery_button_locator = ('and', (('attr=', ('text', '在线下单')),))  # 在线下单
    online_delivery_info_locator = ('and', (('attr=', ('text', '当前为在线下单')),))  # 当前为在线下单
    dummy_delivery_button_locator = ('and', (('attr=', ('text', '无需物流')),))  # 无需物流
    dummy_delivery_info_locator = ('and', (('attr=', ('text', '当前为无需物流')),))  # 当前为无需物流
    delay_locator = ('and', (('attr=', ('text', '稍后处理')),))  # 稍后处理
    addressee_locator = ('and', (('attr=', ('text', '收件人')),))  # 收件人

    def self_check(self):
        check = init_element(self.addressee_locator)
        check.wait_for_appearance(10)

    # 跳转批量发货二级页面
    def go_batch_send_goods_page2(self):
        batch_send_goods_button = init_element(self.batch_send_goods_button_locator)
        batch_send_goods_button.click()
        time.sleep(3)
        try:
            poco(text="确定").wait_for_appearance(10)
            poco(text="确定").click()
        except Exception:
            pass
        delay = init_element(self.delay_locator)
        delay.wait_for_appearance(10)
        return ay_exists(self.all_deliver_button_locator)

    # 选择自己联系发货
    def choose_offline_delivery(self):
        poco.click([0.27, 0.95])
        ay_click(self.offline_delivery_button_locator)
        return ay_exists(self.offline_delivery_info_locator)

    # 选择在线下单发货
    def choose_online_delivery(self):
        poco.click([0.27, 0.95])
        ay_click(self.online_delivery_button_locator)
        return ay_exists(self.online_delivery_info_locator)

    # 选择无需物流发货
    def choose_dummy_delivery(self):
        poco.click([0.27, 0.95])
        ay_click(self.dummy_delivery_button_locator)
        return ay_exists(self.dummy_delivery_info_locator)

    # 稍后处理
    def pending_handle(self):
        ay_click(self.delay_locator)
        if ay_exists(self.delay_locator):
            return False
        else:
            return True

    # 选择单笔订单
    def choose_single_order(self):
        try:
            poco(text="备注").wait_for_appearance(10)
            batch_send_goods_button = init_element(self.batch_send_goods_button_locator)
            locate_by_anchor(batch_send_goods_button, 1, 'l0l0').click()  # 点击全选按钮
            receiver_name = poco(text="收件人")
            locate_by_anchor(receiver_name, 3, "v0l0l0").click()  # 选中第一笔订单
        except Exception as e:
            print(e)

    # 选择快递公司
    def choose_deliver_company(self):
        self.choose_offline_delivery()
        choose_express = init_element(self.choose_express_locator)
        if poco(text="顺丰速运").exists():
            return poco(text="顺丰速运").exists()
        else:
            locate_by_anchor(choose_express, 1, 'l1l1').click()
            result = poco(text="确定").exists()
            if result:
                poco(text="确定").click()
                poco(text="顺丰速运").wait()
                poco(text="顺丰速运").click()
            else:
                poco(text="顺丰速运").wait()
                poco(text="顺丰速运").click()
            return poco(text="顺丰速运").exists()

    # 输入快递单号
    @staticmethod
    def edit_express_number(self, express_number: str):
        poco(name='android.widget.EditText').set_text(gen_express_number())

    # 全部发货
    @staticmethod
    def all_deliver(self):
        BatchSendGoodsPage().choose_offline_delivery()
        BatchSendGoodsPage().choose_deliver_company()
        BatchSendGoodsPage().edit_express_number(gen_express_number())
        poco.click([0.76, 0.88])  # 全部发货按钮
        poco(text="确定").click()
        return get_wait_send_goods_number()


if __name__ == '__main__':
    for i in range(5):
        poco(text='批量发货', name='android.widget.Button').click()
        poco(text='确定').wait(3).click()
        t =  poco(text='全部发货').attr('pos')
        print(t)
        BasePage().back()
    # try:
    #     change_mode = init_element(t.change_mode_locator)
    #     change_mode.wait_for_appearance(10)
    #     print(change_mode.attr('pos'))
    #     ay_click(t.change_mode_locator)
    #     ay_click(t.offline_delivery_button_locator)
    # except Exception as e:
    #     print(e)
    #     print(json.dumps(poco.agent.hierarchy.dump()))
