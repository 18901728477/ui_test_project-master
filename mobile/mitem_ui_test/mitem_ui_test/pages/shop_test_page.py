
from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import *
import re

class ShopTest(BasePage):
    advertising_testing_locator = ('and', (('attr=', ('text', '广告法违规检测')),))
    free_search_locator = ('and', (('attr=', ('text', '免费搜索流量权重检测')),))
    baby_up_and_down_locator = ('and', (('attr=', ('text', '宝贝上下架时间检测')),))
    hand_weights_locator = ('and', (('attr=', ('text', '手淘权重检测')),))
    baby_click_rate_locator = ('and', (('attr=', ('text', '宝贝点击率检测')),))
    marketing_ability_locator = ('and', (('attr=', ('text', '营销能力检测')),))
    advertising_testing_button_locator = ('and', (('attr=', ('text', '删除违规词')),))
    free_search_button_locator = ('and', (('attr=', ('text', '优化标题')),))
    baby_up_and_down_button_locator = ('and', (('attr=', ('text', '开启调整')),))
    hand_weights_button_locator = ('and', (('attr=', ('text', '增加权重')),))
    baby_click_rate_button_locator = ('and', (('attr=', ('text', '提高点击率')),))
    marketing_ability_button_locator = ('and', (('attr=', ('text', '设置营销活动')),))
    one_touch_optimize_locator = ('and', (('attr=', ('text', '一键优化')),))

    # 获取广告法违规宝贝数
    def get_advertising_testing_num(self):
        ad_test_demo = init_element(self.advertising_testing_locator)
        try:
            ad_test = locate_by_anchor(ad_test_demo, parent_lv=2, child_lv='v1v0l1')
            ad_test_num = get_text_of_view(ad_test)
            return ad_test_num
        except PocoNoSuchNodeException:
            ad_test = locate_by_anchor(ad_test_demo, parent_lv=2, child_lv='v1v0')
            ad_test_num = get_text_of_view(ad_test)
            return re.findall(r'\d+', ad_test_num)[0]

    # 获取需要标题优化的宝贝数
    def get_free_search_num(self):
        free_search_demo = init_element(self.free_search_locator)
        free_search = locate_by_anchor(free_search_demo, parent_lv=2, child_lv='v1v0l1')
        free_search_num = get_text_of_view(free_search)
        return free_search_num

    # 获取低谷期宝贝数量
    def get_baby_up_and_down_num(self):
        baby_up_and_down_demo = init_element(self.baby_up_and_down_locator)
        if poco(text='建议开启自动调整，提高宝贝展现机会').exists():
            return 1
        else:
            baby_up_and_down = locate_by_anchor(baby_up_and_down_demo, parent_lv=2, child_lv='v1v0')
            baby_up_and_down_num = get_text_of_view(baby_up_and_down)
            return re.findall(r'\d+', baby_up_and_down_num)[0]

    # 获取无手机详情宝贝数
    def get_hand_weights_num(self):
        hand_weights_demo = init_element(self.hand_weights_locator)
        try:
            hand_weights = locate_by_anchor(hand_weights_demo, parent_lv=2, child_lv='v1v0l1')
            hand_weights_num = get_text_of_view(hand_weights)
            return hand_weights_num
        except PocoNoSuchNodeException:
            hand_weights = locate_by_anchor(hand_weights_demo, parent_lv=2, child_lv='v1v0')
            hand_weights_num = get_text_of_view(hand_weights)
            return re.findall(r'\d+', hand_weights_num)[0]

    # 获取无促销水印宝贝数
    def get_baby_click_rate_num(self):
        baby_click_rate_demo = init_element(self.baby_click_rate_locator)
        baby_click_rate = locate_by_anchor(baby_click_rate_demo, parent_lv=2, child_lv='v1v0l1')
        baby_click_rate_num = get_text_of_view(baby_click_rate)
        return baby_click_rate_num

    # 获取未参加活动宝贝数
    def get_marketing_ability_num(self):
        marketing_ability_demo = init_element(self.marketing_ability_locator)
        BasePage().page_swipe_buttom()
        marketing_ability = locate_by_anchor(marketing_ability_demo, parent_lv=2, child_lv='v1v0l1')
        marketing_ability_num = get_text_of_view(marketing_ability)
        return marketing_ability_num

    # 删除宝贝违规项
    def to_advertising_testing(self):
        advertising_testing_button = init_element(self.advertising_testing_button_locator)
        advertising_testing_button.click()

    # 优化标题
    def to_free_search(self):
        ree_search_button = init_element(self.free_search_button_locator)
        ree_search_button.click()

    # 开启宝贝自动上下架
    def to_baby_up_and_down(self):
        baby_up_and_down = init_element(self.baby_up_and_down_button_locator)
        baby_up_and_down.click()

    # 生成手机详情
    def to_hand_weights(self):
        hand_weights = init_element(self.hand_weights_button_locator)
        hand_weights.click()

    # 添加水印
    def to_baby_click_rate(self):
        baby_click_rate = init_element(self.baby_click_rate_button_locator)
        baby_click_rate.click()

    # 创建活动
    def to_marketing_ability(self):
        marketing_ability = init_element(self.marketing_ability_button_locator)
        marketing_ability.click()

    # 一键优化
    def click_one_touch_optimize(self):
        one_touch_optimize = init_element(self.one_touch_optimize_locator)
        one_touch_optimize.click()
        poco(text='由于标题没有参加一键优化，需要手动优化标题，是否立即去优化？').wait_for_appearance(15)
        poco(text='取消').click()
        return True

    # 宝贝违规检测跳转
    @staticmethod
    def check_advertising_testing():
        #if poco(textMatches='\d+个宝贝').exists():
        if poco(text = '违规词检测').exists():
            return True
        else:
            return False

    # 标题优化跳转
    @staticmethod
    def check_free_search():
        poco(textMatches='差.*').wait_for_appearance(10)
        if poco(textMatches='.*上次检测时间：.*').exists():
            return True
        else:
            return False

    # 跳转自动上下架
    @staticmethod
    def check_baby_up_and_down():
        poco(nameMatches='.*仅高峰期分布.*').wait_for_appearance(10)
        if poco(nameMatches='.*开启自动上下架.*').exists():
            return True
        else:
            return False

    # 跳转手机详情
    @staticmethod
    def check_hand_weights():
        poco(textMatches='.*生成.*').wait_for_appearance(10)
        if poco(textMatches='.*生成.*').exists():
            return True
        else:
            return False

    # 跳转促销水印
    @staticmethod
    def check_baby_click_rate():
        try:
            poco(name='按主题筛选').wait_for_appearance(8)
            return True
        except PocoTargetTimeout:
            try:
                poco(nameMatches='.*添加水印活动.*').wait_for_appearance(8)
                return True
            except PocoTargetTimeout:
                return False

    # 跳转活动创建
    @staticmethod
    def check_marketing_ability():
        poco(nameMatches='.*优惠方式.*').wait_for_appearance(10)
        if poco(nameMatches='.*创建活动.*').exists():
            return True
        else:
            return False

    @staticmethod
    def is_need_auth():
        if poco(text='立即授权').exists():
            poco(text='立即授权').click()
        else:
            return 'Element not found'


if __name__ == '__main__':
    x = ShopTest()
    print(x.get_advertising_testing_num())
    print(x.get_hand_weights_num())