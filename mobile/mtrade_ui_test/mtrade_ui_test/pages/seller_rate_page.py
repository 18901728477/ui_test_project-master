from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import BasePage, init_element, locate_by_anchor, get_text_of_view, randomize


class SellerRatePage(BasePage):
    rate_now_locator = ('and', (('attr=', ('text', '立即评价')),))  # 立即评价
    insert_locator = ('and', (('attr=', ('text', '插入快捷短语')),))  # 插入快捷短语
    phrase_text_box_locator = ('and', (('attr=', ('name', 'android.widget.EditText')),))  # 快捷短语文本框
    phrase_locator = ('and', (('attr=', ('name', 'android:id/text1')),))  # 快捷短语

    def choose_good(self):
        insert = init_element(self.insert_locator)
        good = locate_by_anchor(insert, parent_lv=5, child_lv='v1l0l0')
        good.click()
        if get_text_of_view(good) == b'\\ue69d':
            return True
        else:
            return False

    def choose_medium(self):
        insert = init_element(self.insert_locator)
        medium = locate_by_anchor(insert, parent_lv=5, child_lv='v1l1l0')
        medium.click()
        if get_text_of_view(medium) == b'\\ue69d':
            return True
        else:
            return False

    def choose_bad(self):
        insert = init_element(self.insert_locator)
        bad = locate_by_anchor(insert, parent_lv=5, child_lv='v1l2l0')
        bad.click()
        if get_text_of_view(bad) == b'\\ue69d':
            return True
        else:
            return False

    def insert_phrase(self):
        insert = init_element(self.insert_locator)
        insert.click()
        phrase_temp = init_element(self.phrase_locator)
        phrase = randomize(phrase_temp)
        expect_text = phrase.get_text()
        phrase.click()
        phrase_text_box = init_element(self.phrase_text_box_locator)
        actual_text = phrase_text_box.get_text()
        if expect_text == actual_text:
            return True
        else:
            return False

    def input_phrase(self):
        pass

    def rate_now_method(self):
        pass
