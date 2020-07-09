from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import *


class ModifyAddressPage(BasePage):
    name_phone_address_anchor = ('and', (('attr=', ('text', '收件人')),))
    clear_address_button_locator = ('and', (('attr=', ('text', '清空地址')),))
    one_click_fill_address_button_locator = ('and', (('attr=', ('text', '一键填充')),))
    cancel_button_locator = ('and', (('attr=', ('text', '取消')),))
    other_info_anchor = ('and', (('attr=', ('text', '收货人姓名')),))
    confirm_button_locator = ('and', (('attr=', ('text', '确定')),))
    check_locator = ('and', (('attr=', ('text', '阻止Ta拍单')),))
    modify_address_locator = ('and', (('attr=', ('text', '修改地址')),))

    # 方法：清空地址
    def clear_address(self):
        ay_click(self.clear_address_button_locator)

    # 方法：获取地址信息
    def get_address_info(self):
        buyer_name_element = locate_by_anchor(init_element(self.other_info_anchor), 2, 'l1v0l0')
        contact_information_element = locate_by_anchor(init_element(self.other_info_anchor), 2, 'l1v0l1')
        buyer_address_element = locate_by_anchor(init_element(self.other_info_anchor), 2, 'l1v1')
        address_info = {'收件人姓名': get_text_of_view(buyer_name_element),
                        '收件人手机': get_text_of_view(contact_information_element),
                        '收件地址': get_text_of_view(buyer_address_element)[:-7],
                        '邮政编码': get_text_of_view(buyer_address_element)[-6:]}
        return address_info

    # 方法：输入地址后一键填充,保存修改
    def one_click_fill_address(self, my_input_address):
        auto_fill_address_text_box_element = locate_by_anchor(init_element(self.name_phone_address_anchor), 4,
                                                              'v1v0v0l0')
        auto_fill_address_text_box_element.set_text(my_input_address)
        ay_click(self.one_click_fill_address_button_locator)
        ay_click(self.confirm_button_locator)
        check = init_element(self.check_locator)
        check.wait_for_appearance(5)

    # 方法：编辑地址后，保存修改
    def modify_address(self, buyer_name, buyer_mobphone, buyer_telphone, buyer_province, buyer_city, buyer_area,
                       stress_address, zip_code):
        buyer_name_text_box_element = locate_by_anchor(init_element(self.other_info_anchor), 3, 'v0').offspring(
            'android.widget.EditText')
        buyer_phone_number_text_box_element = locate_by_anchor(init_element(self.other_info_anchor), 3,
                                                               'v1v0l0').offspring('android.widget.EditText')
        telphone_text_box_element = locate_by_anchor(init_element(self.other_info_anchor), 3, 'v1v0l1').offspring(
            'android.widget.EditText')
        street_address_text_box_element = locate_by_anchor(init_element(self.other_info_anchor), 3, 'v3').offspring(
            'android.widget.EditText')
        zip_code_text_box_element = locate_by_anchor(init_element(self.other_info_anchor), 3, 'v4').offspring(
            'android.widget.EditText')
        province_element = locate_by_anchor(init_element(self.other_info_anchor), 3, 'v2v0l0v1l1')
        buyer_name_text_box_element.set_text(buyer_name)
        buyer_phone_number_text_box_element.set_text(buyer_mobphone)
        telphone_text_box_element.set_text(buyer_telphone)
        street_address_text_box_element.set_text(stress_address)
        zip_code_text_box_element.set_text(zip_code)
        province_element.click()
        poco(name='android:id/text1', text=buyer_province).click()
        poco(name='android:id/text1', text=buyer_city).click()
        poco(name='android:id/text1', text=buyer_area).click()
        ay_click(self.confirm_button_locator)
