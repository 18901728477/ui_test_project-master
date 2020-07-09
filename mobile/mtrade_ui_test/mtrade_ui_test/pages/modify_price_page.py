from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import *


class ModifyPricePage(BasePage):
    one_click_modify_locator = ('and', (('attr=', ('text', '一键改价')),))  # 一键改价按钮
    confirm1_locator = ('and', (('attr=', ('name', 'com.taobao.qianniu:id/changeprice_ok_btn')),))  # 改价页面的确定按钮
    price_text_box_locator = ('and', (('attr=', ('name', 'com.taobao.qianniu:id/price_input_text')),))  # 价格编辑文本框
    confirm2_locator = ('and', (('attr=', ('name', 'com.taobao.qianniu:id/btn_ok')),))  # 价格编辑页面的确定按钮

    # 修改单笔订单价格
    def modify_price(self, my_price: str):
        one_click_modify = init_element(self.one_click_modify_locator)
        one_click_modify.click()
        ay_set_text(self.price_text_box_locator, my_price)
        ay_click(self.confirm2_locator)
        ay_click(self.confirm1_locator)
        one_click_modify.invalidate()
        one_click_modify.wait_for_disappearance(10)


if __name__ == '__main__':
    for i in range(5):
        poco(text='修改价格').click()
        m = ModifyPricePage()
        m.modify_price('0.02')
