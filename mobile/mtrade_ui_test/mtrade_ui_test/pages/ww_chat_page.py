from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import BasePage, ay_click, poco, ay_get_text, ay_set_text, init_element


class WwChatPage(BasePage):
    return_locator = ('index', (('and', (('attr=', ('name', 'android.widget.ImageView')),)), 0))  # 返回按钮
    send_locator = ('and', (('attr=', ('name', '发送')),))  # 发送按钮
    input_box_locator = ('and', (('attr=', ('name', 'com.taobao.qianniu:id/msgcenter_panel_input_edit')),))  # 聊天输入框

    def self_check(self):
        input_box = init_element(self.input_box_locator)
        input_box.wait_for_appearance(5)

    def get_chat_text_and_return(self):
        res = ay_get_text(self.input_box_locator)
        self.send_chat()
        self.return_qiannniu()
        return res

    def send_chat(self):
        ay_click(self.send_locator)
        if poco(text='离线提示').exists():
            poco(text='登录').click()
            ay_click(self.send_locator)

    def return_qiannniu(self):
        ay_click(self.return_locator)

    # 重置旺旺聊天窗
    def clear_ww_chat_box(self):
        ay_set_text(self.input_box_locator, '')

if __name__ == '__main__':
    WwChatPage().get_chat_text_and_return()
