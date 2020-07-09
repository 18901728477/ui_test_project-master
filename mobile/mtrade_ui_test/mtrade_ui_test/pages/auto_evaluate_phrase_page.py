from time import sleep

from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import *
import requests
import json


class PhraseFromAutoEvalaute(BasePage):
    new_button_locator = ('and', (('attr=', ('text', '新建')), ('attr=', ('name', 'android.widget.Button'))))  # 新建按钮
    text_box_locator = ('index', (('>', (
        ('and', (('attr=', ('name', '__react-content')),)),
        ('and', (('attr=', ('name', 'android.widget.EditText')),)))),
                                  0))  # 自动评价短语文本框
    save_button_locator = (
        'and', (('attr=', ('text', '保存')), ('attr=', ('name', 'android.widget.Button'))))  # 自动评价短语保存按钮
    latest_phrase_edit_locator = ('index', (('/', (('index', (('/', (('/', (
        ('index', (('/', (('/', (('and', (('attr=', ('name', '__react-content')),)), ('and', ()))), ('and', ()))), 5)),
        ('and', ()))), ('and', ()))), 1)), ('and', ()))), 0))  # 最新的自定义短语编辑按钮
    delete_button_locator = ('and', (('attr=', ('text', '删除')), ('attr=', ('name', 'android.view.View'))))  # 删除自定义短语按钮
    confirm_delete_button_locator = (
        'and', (('attr=', ('text', '确定')), ('attr=', ('name', 'android:id/button2'))))  # 确认删除按钮
    cancel_delete_button_locator = (
        'and', (('attr=', ('text', '取消')), ('attr=', ('name', 'android:id/button1'))))  # 取消删除按钮

    def self_check(self):
        check = init_element(self.new_button_locator)
        check.wait_for_appearance(5)

    # 方法：获取当前短语总条数
    def get_phrase_amount(self):
        amount_phrase = len(poco("__react-content").child().children()) - 1
        return (amount_phrase)

    # 方法：获取最近一条的短语内容
    def get_latest_phrase(self):
        return ay_get_text(self.latest_phrase_edit_locator)

    # 方法：新增一条自定义短语
    def create_phrase(self, my_text):
        ay_click(self.new_button_locator)
        ay_set_text(self.text_box_locator, my_text)
        ay_click(self.save_button_locator)
        save = init_element(self.save_button_locator)
        save.wait_for_disappearance(5)
        return poco(text=my_text).wait(5)

    # 方法：编辑最新的一条自定义短语
    def edit_phrase(self, my_edit_text):
        ay_click(self.latest_phrase_edit_locator)
        sleep(2)
        ay_set_text(self.text_box_locator, my_edit_text)
        sleep(1)
        ay_click(self.save_button_locator)
        sleep(2)

    # 方法：删除最新的一条自定义短语
    def delete_phrase(self, phrase):
        phrase_locator = ('and', (('attr=', ('text', phrase)),))
        ay_click(phrase_locator)
        ay_click(self.delete_button_locator)
        ay_click(self.confirm_delete_button_locator)

    # 方法：返回api获取到的所有短语
    @staticmethod
    def api_all_auto_evaluate_phrase():
        res = api_auto_evaluate_phrase()
        text_list = json.loads(res)['ratetexts']
        all_phrase = []
        for x in text_list:
            all_phrase.append(x['content'])
        return all_phrase

    # 方法：返回api获取到的最新的一条短语
    @staticmethod
    def api_latest_auto_evaluate_phrase():
        res = api_auto_evaluate_phrase()
        return json.loads(res)['ratetexts'][0]['content']


if __name__ == "__main__":
    x = PhraseFromAutoEvalaute()
    print(x.api_auto_evaluate_phrase())
    print(x.api_latest_auto_evaluate_phrase())
    print(x.api_all_auto_evaluate_phrase())
