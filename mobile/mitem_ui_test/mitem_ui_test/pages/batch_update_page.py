from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import *
from mobile.mitem_ui_test.mitem_ui_test.pages.batch_update_itemlist_page import *
import random
import requests
import json
import re


class BatchUpdate(BasePage):
    baby_title_locator = ('and', (('attr=', ('text', '宝贝标题')),))
    baby_price_locator = ('and', (('attr=', ('text', '宝贝价格')),))
    baby_news_locator = ('and', (('attr=', ('text', '宝贝详情')),))
    baby_inventory_locator = ('and', (('attr=', ('text', '宝贝库存')),))
    baby_putaway_locator = ('and', (('attr=', ('text', '上架')),))
    baby_unshelve_locator = ('and', (('attr=', ('text', '下架')),))
    baby_state_locator = ('and', (('attr=', ('text', '宝贝状态:')),))
    baby_choice_locator = ('and', (('attr=', ('text', '选择宝贝:')),))
    delete_keyword_locator = ('and', (('attr=', ('text', '删除关键字')),))
    delete_keyword_box_locator = ('and', (('attr=', ('text', '请输入需要删除的关键字')),))
    replace_keyword_locator = ('and', (('attr=', ('text', '替换关键字')),))
    replace_keyword_box_old_locator = ('and', (('attr=', ('text', '请输入原文关键字')),))
    replace_keyword_box_new_locator = ('and', (('attr=', ('text', '请输入替换的关键字')),))
    add_baby_news_locator = ('and', (('attr=', ('text', '添加名称前后缀')),))
    add_baby_news_box_front_locator = ('and', (('attr=', ('text', '请输入前缀文字')),))
    add_baby_news_box_behind_locator = ('and', (('attr=', ('text', '请输入后缀文字')),))
    search_baby_locator = ('and', (('attr=', ('text', '搜索...')),))
    all_choice_locator = ('and', (('attr=', ('text', '全选')),))
    sure_button_locator = ('and', (('attr=', ('text', '确定')),))
    start_change_button_locator = ('and', (('attr=', ('text', '开始修改')),))
    sure_change_button_locator = ('and', (('attr=', ('text', '确认修改')),))
    please_choice_baby_locator = ('and', (('attr=', ('text', '请选择需要修改的宝贝')),))
    please_enter_titlekey_locator = ('and', (('attr=', ('text', '请输入标题关键词搜索')),))
    change_baby_price_bymath_locator = ('and', (('attr=', ('text', '按公式修改')),))
    change_baby_price_byint_locator = ('and', (('attr=', ('text', '价格统一修改为')),))
    change_baby_price_byfloat_locator = ('and', (('attr=', ('text', '价格的小数部分统一修改')),))
    unified_inventory_locator = ('and', (('attr=', ('text', '统一每个宝贝的sku库存')),))
    increase_inventory_locator = ('and', (('attr=', ('text', '增加每个宝贝的sku库存')),))
    reduce_inventory_locator = ('and', (('attr=', ('text', '减少每个宝贝的sku库存')),))
    inventory_box_locator = ('and', (('attr=', ('text', '件')),))

    # 批量修改宝贝标题(替换)
    def change_baby_title_replace(self):
        baby_title = init_element(self.baby_title_locator)
        baby_title.click()
        please_choice_baby = init_element(self.please_choice_baby_locator)
        please_choice_baby.click()
        search_box = init_element(self.search_baby_locator)
        search_box.wait_for_appearance(5)
        search_box.click()
        please_enter_titlekey = init_element(self.please_enter_titlekey_locator)
        self.super_add(locate_by_anchor(please_enter_titlekey, parent_lv=1), '修改标题标题修改专用宝贝修改标题')
        poco(text='搜索').click()
        poco(text='修改标题标题修改专用宝贝修改标题').wait_for_appearance(10)
        locate_by_anchor(poco(text='修改标题标题修改专用宝贝修改标题'), parent_lv=3, child_lv='l0').click()
        sure_button = init_element(self.sure_button_locator)
        sure_button.click()
        replace_keyword = init_element(self.replace_keyword_locator)
        locate_by_anchor(replace_keyword, parent_lv=1, child_lv='l0').click()
        replace_keyword_box_old = init_element(self.replace_keyword_box_old_locator)
        self.super_add(locate_by_anchor(replace_keyword_box_old, parent_lv=1), '修改标题')
        replace_keyword_box_new = init_element(self.replace_keyword_box_new_locator)
        self.super_add(locate_by_anchor(replace_keyword_box_new, parent_lv=1), '替换标题')
        start_change = init_element(self.start_change_button_locator)
        start_change.click()
        sure_change_button = init_element(self.sure_change_button_locator)
        sure_change_button.click()
        poco(name='com.taobao.qianniu:id/center_panel').child(text='批量修改').wait_for_appearance(20)
        return self.check_task_detail_title()

    # 批量修改宝贝标题(删除)
    def change_baby_title_delete(self):
        baby_title = init_element(self.baby_title_locator)
        baby_title.click()
        please_choice_baby = init_element(self.please_choice_baby_locator)
        please_choice_baby.click()
        search_box = init_element(self.search_baby_locator)
        search_box.wait_for_appearance(5)
        search_box.click()
        please_enter_titlekey = init_element(self.please_enter_titlekey_locator)
        self.super_add(locate_by_anchor(please_enter_titlekey, parent_lv=1), '替换标题标题修改专用宝贝替换标题')
        poco(text='搜索').click()
        poco(text='替换标题标题修改专用宝贝替换标题').wait_for_appearance(10)
        locate_by_anchor(poco(text='替换标题标题修改专用宝贝替换标题'), parent_lv=3, child_lv='l0').click()
        sure_button = init_element(self.sure_button_locator)
        sure_button.click()
        delete_keyword = init_element(self.delete_keyword_locator)
        locate_by_anchor(delete_keyword, parent_lv=1, child_lv='l0').click()
        delete_keyword_box = init_element(self.delete_keyword_box_locator)
        self.super_add(locate_by_anchor(delete_keyword_box, parent_lv=1), '替换标题')
        start_change = init_element(self.start_change_button_locator)
        start_change.click()
        sure_change_button = init_element(self.sure_change_button_locator)
        sure_change_button.click()
        poco(name='com.taobao.qianniu:id/center_panel').child(text='批量修改').wait_for_appearance(20)
        return self.check_task_detail_title()

    # 批量修改宝贝标题(添加)
    def change_baby_title_add(self):
        baby_title = init_element(self.baby_title_locator)
        baby_title.click()
        please_choice_baby = init_element(self.please_choice_baby_locator)
        please_choice_baby.click()
        search_box = init_element(self.search_baby_locator)
        search_box.wait_for_appearance(5)
        search_box.click()
        please_enter_titlekey = init_element(self.please_enter_titlekey_locator)
        self.super_add(locate_by_anchor(please_enter_titlekey, parent_lv=1), '标题修改专用宝贝')
        poco(text='搜索').click()
        poco(text='标题修改专用宝贝').wait_for_appearance(10)
        locate_by_anchor(poco(text='标题修改专用宝贝'), parent_lv=3, child_lv='l0').click()
        sure_button = init_element(self.sure_button_locator)
        sure_button.click()
        add_baby_news = init_element(self.add_baby_news_locator)
        locate_by_anchor(add_baby_news, parent_lv=1, child_lv='l0').click()
        add_baby_news_box_front = init_element(self.add_baby_news_box_front_locator)
        add_baby_news_box_behind = init_element(self.add_baby_news_box_behind_locator)
        self.super_add(locate_by_anchor(add_baby_news_box_front, parent_lv=1), '修改标题')
        self.super_add(locate_by_anchor(add_baby_news_box_behind, parent_lv=1), '修改标题')
        start_change = init_element(self.start_change_button_locator)
        start_change.click()
        sure_change_button = init_element(self.sure_change_button_locator)
        sure_change_button.click()
        poco(name='com.taobao.qianniu:id/center_panel').child(text='批量修改').wait_for_appearance(20)
        return self.check_task_detail_title()

    # 选择需要修改的测试宝贝
    def choose_baby(self):
        please_choice_baby = init_element(self.please_choice_baby_locator)
        please_choice_baby.click()
        search_box = init_element(self.search_baby_locator)
        search_box.wait_for_appearance(5)
        search_box.click()
        please_enter_titlekey = init_element(self.please_enter_titlekey_locator)
        self.super_add(locate_by_anchor(please_enter_titlekey, parent_lv=1), '批量修改test自动化宝贝批量修改')
        poco(text='搜索').click()
        poco(text='批量修改test自动化宝贝批量修改').wait_for_appearance(10)
        locate_by_anchor(poco(text='批量修改test自动化宝贝批量修改'), parent_lv=3, child_lv='l0').click()
        all_choice = init_element(self.all_choice_locator)
        locate_by_anchor(all_choice, parent_lv=1, child_lv='l0').click()
        sure_button = init_element(self.sure_button_locator)
        sure_button.click()

    # 批量修改宝贝价格
    def change_baby_price(self, method):
        baby_price = init_element(self.baby_price_locator)
        baby_price.click()
        self.choose_baby()
        methods = {
            'bymath': self.change_baby_price_bymath,
            'byint': self.change_baby_price_byint,
            'byfloat': self.change_baby_price_byfloat
        }
        run_method = methods.get(method)
        return run_method()

    # 批量修改宝贝价格(按公式修改)
    def change_baby_price_bymath(self):
        change_baby_price_bymath = init_element(self.change_baby_price_bymath_locator)
        locate_by_anchor(change_baby_price_bymath, parent_lv=1, child_lv='l0').click()
        choice_box = locate_by_anchor(poco(text='修改公式'), parent_lv=1, child_lv='v1')
        choose_button = random.choice(choice_box.children())
        choose_button.click()
        locate_by_anchor(choose_button, parent_lv=0, child_lv='l2').offspring('android.widget.EditText').set_text(
            '1.1')
        float_dispose = locate_by_anchor(poco(text='小数部分的处理'), parent_lv=1, child_lv='v3')
        float_choose_button = random.choice(float_dispose.children())
        float_choose_button.click()
        start_change_button = init_element(self.start_change_button_locator)
        start_change_button.click()
        poco(text='确定').click()
        sleep(2)
        if poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').exists():
            poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').click()
        else:
            pass
        poco(name='com.taobao.qianniu:id/center_panel').child(text='批量修改').wait_for_appearance(20)
        return self.check_task_detail_price()

    # 批量修改宝贝价格(价格统一修改)
    def change_baby_price_byint(self):
        change_baby_price_byint = init_element(self.change_baby_price_byint_locator)
        locate_by_anchor(change_baby_price_byint, parent_lv=1, child_lv='l0').click()
        byint_box = locate_by_anchor(change_baby_price_byint, parent_lv=1, child_lv='l2')
        byint_box.offspring('android.widget.EditText').set_text(2)
        start_change_button = init_element(self.start_change_button_locator)
        start_change_button.click()
        poco(text='确定').click()
        sleep(2)
        if poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').exists():
            poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').click()
        else:
            pass
        poco(name='com.taobao.qianniu:id/center_panel').child(text='批量修改').wait_for_appearance(20)
        return self.check_task_detail_price()

    def change_baby_price_byfloat(self):
        change_baby_price_byfloat = init_element(self.change_baby_price_byfloat_locator)
        locate_by_anchor(change_baby_price_byfloat, parent_lv=1, child_lv='l0').click()
        byfloat_box = locate_by_anchor(change_baby_price_byfloat, parent_lv=1, child_lv='l2')
        byfloat_box.offspring('android.widget.EditText').set_text(99)
        start_change_button = init_element(self.start_change_button_locator)
        start_change_button.click()
        poco(text='确定').click()
        sleep(2)
        if poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').exists():
            poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').click()
        else:
            pass
        poco(name='com.taobao.qianniu:id/center_panel').child(text='批量修改').wait_for_appearance(20)
        return self.check_task_detail_price()

    # 修改库存
    def change_baby_num(self, method):
        baby_inventory = init_element(self.baby_inventory_locator)
        baby_inventory.click()
        self.choose_baby()
        methods = {
            'unified': self.unified_inventory,
            'increase': self.increase_inventory,
            'reduce': self.reduce_inventory
        }
        run_method = methods.get(method)
        return run_method()

    # 统一库存
    def unified_inventory(self):
        unified_inventory_button = init_element(self.unified_inventory_locator)
        unified_inventory_button.click()
        inventory_box = init_element(self.inventory_box_locator)
        inventory_box = locate_by_anchor(inventory_box, parent_lv=1, child_lv='l1').offspring(
            'android.widget.EditText')
        inventory_box.set_text('5')
        start_change_button = init_element(self.start_change_button_locator)
        start_change_button.click()
        poco(text='确定').click()
        sleep(2)
        if poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').exists():
            poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').click()
        else:
            pass
        poco(name='com.taobao.qianniu:id/center_panel').child(text='批量修改').wait_for_appearance(20)
        return self.check_task_detail_store()

    # 增加库存
    def increase_inventory(self):
        increase_inventory = init_element(self.increase_inventory_locator)
        increase_inventory.click()
        inventory_box = init_element(self.inventory_box_locator)
        inventory_box = locate_by_anchor(inventory_box, parent_lv=1, child_lv='l1').offspring(
            'android.widget.EditText')
        inventory_box.set_text('100')
        start_change_button = init_element(self.start_change_button_locator)
        start_change_button.click()
        poco(text='确定').click()
        sleep(2)
        if poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').exists():
            poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').click()
        else:
            pass
        poco(name='com.taobao.qianniu:id/center_panel').child(text='批量修改').wait_for_appearance(20)
        return self.check_task_detail_store()

    # 减少库存
    def reduce_inventory(self):
        reduce_inventory = init_element(self.reduce_inventory_locator)
        reduce_inventory.click()
        inventory_box = init_element(self.inventory_box_locator)
        inventory_box = locate_by_anchor(inventory_box, parent_lv=1, child_lv='l1').offspring(
            'android.widget.EditText')
        inventory_box.set_text('99')
        start_change_button = init_element(self.start_change_button_locator)
        start_change_button.click()
        poco(text='确定').click()
        sleep(2)
        if poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').exists():
            poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').click()
        else:
            pass
        poco(name='com.taobao.qianniu:id/center_panel').child(text='批量修改').wait_for_appearance(20)
        return self.check_task_detail_store()

    # 点击上、下架
    def go_list(self, index: int):
        """

        :param index:
        0：上架
        1：下架
        :return:
        """
        info_dict = {
            0: self.baby_putaway_locator,
            1: self.baby_unshelve_locator
        }
        element_click(info_dict.get(index))
        return BatchUpdateItemList()

    # 修改详情-添加文字
    def go_update_detail_add_word(self, my_add: str):
        element_click(self.baby_news_locator)
        poco(name='android.widget.EditText').set_text(my_add)
        poco(text='开始修改').click()
        return BatchUpdateItemList()

    # 修改详情-添加图片
    def go_update_detail_add_picture(self):
        element_click(self.baby_news_locator)
        poco(text='文字').click()
        poco(text='图片').click()
        poco(text='上传图片').click()
        poco(text='\ue6ba').click()
        poco(text='选择图片').click()
        poco(text='开始修改').click()
        return BatchUpdateItemList()

    # 修改详情-替换描述
    def go_update_detail_replace(self, old_content: str, new_content: str):
        element_click(self.baby_news_locator)
        poco(text='替换描述').click()
        poco(text='请输入替换的关键字，如多个请用换行符分隔').parent().offspring(name='android.widget.EditText').set_text(old_content)
        poco(text='请输入替换的内容').parent().offspring(name='android.widget.EditText').set_text(new_content)
        poco(text='开始修改').click()
        return BatchUpdateItemList()

    # 修改详情-删除描述
    def go_update_detail_delete(self, my_delete: str):
        element_click(self.baby_news_locator)
        poco(text='删除描述').click()
        poco(name='android.widget.EditText').set_text(my_delete)
        poco(text='开始修改').click()
        return BatchUpdateItemList()

    # 方法，调用api获取一个宝贝的pc详情
    def tb_api_get_item_desc(self, numid: str) -> str:
        """

        :param numid:
        :return:
        宝贝详情
        """
        req_url = 'http://crm.aiyongbao.com/testtools/getOfficialApi'
        params = {
            'nick': '赵东昊的测试店铺',
            'method': 'taobao.item.seller.get',
            'param[fields]': 'desc',
            'param[num_iid]': numid
        }
        cookies = {'PHPSESSID': self.get_sessionId()}
        r = requests.post(req_url, params=params, cookies=cookies)
        return json.loads(r.content).get('item_seller_get_response').get('item').get('desc')

    # 方法：发起还原价格任务
    def restore_price(self):
        poco(text='还原价格').click()
        poco(text='还原').click()
        sleep(2)
        if poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').exists():
            poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').click()
        else:
            pass
        sleep(10)

    # 方法：检查价格是否修改成功
    def check_task_detail_price(self) -> bool:
        """

        :return:
        如果任务日志，修改前后的价格、库存不相等，返回true，否则返回false
        """
        sleep(3)
        poco(text='详情').click()
        poco(textMatches='价格 : .*').wait_for_appearance(3)
        price_list = re.findall(r'\d\.*\d*', poco(textMatches='价格 : .*').get_text())
        self.turn_back()
        if price_list[0] != price_list[1]:
            return True
        elif price_list[0] == price_list[1]:
            return False

    # 方法：检查库存是否修改成功
    def check_task_detail_store(self) -> bool:
        """

        :return:
        如果任务日志，修改前后的价格、库存不相等，返回true，否则返回false
        """
        sleep(3)
        poco(text='详情').click()
        poco(textMatches='库存 : .*').wait_for_appearance(3)
        price_list = re.findall(r'\d+', poco(textMatches='库存 : .*').get_text())
        self.turn_back()
        if price_list[0] != price_list[1]:
            return True
        elif price_list[0] == price_list[1]:
            return False

    # 方法：检查标题是否修改
    def check_task_detail_title(self) -> bool:
        """
         如果任务日志，修改前后的标题不相等，返回true，否则返回false
        :return:
        """
        sleep(3)
        poco(text='详情').click()
        poco(text='修改前:').wait_for_appearance(3)
        ele_anchor = poco(text='修改前:')
        old_title = locate_by_anchor(ele_anchor, 2, 'l1v0').get_text()
        new_title = locate_by_anchor(ele_anchor, 2, 'l1v1').get_text()
        self.turn_back()
        if old_title != new_title:
            return True
        else:
            self.turn_back()
            return False


if __name__ == '__main__':
    x = BatchUpdate()
    y = x.check_task_detail_store()
    print(y)
