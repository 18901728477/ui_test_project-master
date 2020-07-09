from poco.proxy import UIObjectProxy
from time import sleep
from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import BasePage, poco, init_element, locate_by_anchor, get_text_of_view, randomize


class EvaluationOperationPage(BasePage):
    evaluate_now_button_locator = ('and', (('attr=', ('text', '立即评价')),))  # 立即评价按钮
    insert_phrase_button_locator = ('and', (('attr=', ('text', '插入快捷短语')),))  # 插入短语按钮
    phrase_locator = ('and', (('attr=', ('name', 'android:id/text1')),))
    phrase_text_box_locator = ('and', (('attr=', ('name', 'android.widget.EditText')),))

    # 选择好评
    def choose_good(self):
        insert = init_element(self.insert_phrase_button_locator)
        good = locate_by_anchor(insert, parent_lv=5, child_lv='v1l0l0')
        good.click()
        if get_text_of_view(good) == '\ue69d':
            return True
        else:
            return False

    def choose_good_batch(self):
        insert = init_element(self.insert_phrase_button_locator)
        good = locate_by_anchor(insert, parent_lv=5, child_lv='v0l0l0')
        good.click()
        if get_text_of_view(good) == '\ue69d':
            return True
        else:
            return False

    # 选择中评
    def choose_mid(self):
        insert = init_element(self.insert_phrase_button_locator)
        good = locate_by_anchor(insert, parent_lv=5, child_lv='v1l1l0')
        good.click()
        if get_text_of_view(good) == '\ue69d':
            return True
        else:
            return False

    def choose_mid_batch(self):
        insert = init_element(self.insert_phrase_button_locator)
        good = locate_by_anchor(insert, parent_lv=5, child_lv='v0l1l0')
        good.click()
        if get_text_of_view(good) == '\ue69d':
            return True
        else:
            return False

    # 选择差评
    def choose_bad(self):
        insert = init_element(self.insert_phrase_button_locator)
        good = locate_by_anchor(insert, parent_lv=5, child_lv='v1l2l0')
        good.click()
        if get_text_of_view(good) == '\ue69d':
            return True
        else:
            return False

    def choose_bad_batch(self):
        insert = init_element(self.insert_phrase_button_locator)
        good = locate_by_anchor(insert, parent_lv=5, child_lv='v0l2l0')
        good.click()
        if get_text_of_view(good) == '\ue69d':
            return True
        else:
            return False

    # 随机插入评价短语
    def insert_phrase(self):
        insert = init_element(self.insert_phrase_button_locator)
        insert.click()
        phrase_temp = init_element(self.phrase_locator)
        phrase = randomize(phrase_temp)
        expect_text = get_text_of_view(phrase)
        phrase.click()
        phrase_text_box = init_element(self.phrase_text_box_locator)
        actual_text = phrase_text_box.get_text()
        if expect_text == actual_text:
            return True, actual_text
        else:
            return False, actual_text

    # 点击立即评价
    def evaluate_now(self):
        evaluate_now_button = init_element(self.evaluate_now_button_locator)
        evaluate_now_button.click()

    # 自定义填充
    def insert_phrase_by_custom(self):
        phrase_temp = init_element(self.insert_phrase_button_locator)
        phrase_temp_edit = locate_by_anchor(phrase_temp, parent_lv=4, child_lv='v1')
        phrase_temp_edit_text = phrase_temp_edit.offspring('android.widget.EditText')
        phrase_temp_edit_text.set_text('自动化操作评价')
        phrase_temp_edit_text.click()
        phrase_temp_edit_text.invalidate()
        phrase_temp_news = phrase_temp_edit_text.get_text()
        if phrase_temp_news == '自动化操作评价':
            return True
        else:
            return False


if __name__ == '__main__':
    print(EvaluationOperationPage().insert_phrase_by_custom())

