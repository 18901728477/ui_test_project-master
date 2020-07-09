from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import *
import allure
import pytest

class TestShopMedical(BasePage):

    @allure.feature('店铺体检')
    @allure.story('体检项单独跳转')
    @pytest.mark.p1
    def test_single_break(self, first_page_wait_scan):
        first_page_wait_scan.close_auto_list()
        shop_test_page = first_page_wait_scan.go_shop_test_top_area()
        shop_test_page.page_swipe_buttom()
        advertising_num = shop_test_page.get_advertising_testing_num()
        title_num = shop_test_page.get_free_search_num()
        baby_time_num = shop_test_page.get_baby_up_and_down_num()
        hand_weights_num = shop_test_page.get_hand_weights_num()
        baby_click_num = shop_test_page.get_baby_click_rate_num()
        marketing_ability_num = shop_test_page.get_marketing_ability_num()
        shop_test_page.page_swipe_top()
        # 违规词跳转检测
        if int(advertising_num)>0:
            shop_test_page.to_advertising_testing()
            shop_test_page.is_need_auth()
            advertising_is_break = shop_test_page.check_advertising_testing()
            time.sleep(5)
            shop_test_page.turn_back()
        else:
            advertising_is_break = False
        # 标题优化跳转
        print(title_num)
        if int(title_num)>0:
            shop_test_page.to_free_search()
            shop_test_page.is_need_auth()
            free_search_is_break = shop_test_page.check_free_search()
            time.sleep(5)
            shop_test_page.turn_back()
        else:
            free_search_is_break = False
        # 自动上下架跳转
        if int(baby_time_num)>0:
            shop_test_page.to_baby_up_and_down()
            shop_test_page.is_need_auth()
            shop_test_page.check_AYitem_auth()
            shop_test_page.check_AYitem_auth()
            baby_up_and_down_is_break = shop_test_page.check_baby_up_and_down()
            time.sleep(5)
            shop_test_page.turn_back()
        else:
            baby_up_and_down_is_break = False
        # 生成手机详情跳转
        if int(hand_weights_num)>0:
            shop_test_page.to_hand_weights()
            shop_test_page.is_need_auth()
            hand_weights_is_break = shop_test_page.check_hand_weights()
            time.sleep(5)
            shop_test_page.turn_back()
        else:
            hand_weights_is_break = False
        # 添加水印跳转
        if int(baby_click_num)>0:
            shop_test_page.to_baby_click_rate()
            shop_test_page.is_need_auth()
            shop_test_page.check_AYitem_auth()
            baby_click_rate_is_break = shop_test_page.check_baby_click_rate()
            time.sleep(5)
            shop_test_page.turn_back()
        else:
            baby_click_rate_is_break = False
        shop_test_page.page_swipe_buttom()
        # 添加活动跳转
        if int(marketing_ability_num)>0:
            shop_test_page.to_marketing_ability()
            shop_test_page.is_need_auth()
            shop_test_page.check_AYitem_auth()
            marketing_ability_is_break = shop_test_page.check_marketing_ability()
            time.sleep(5)
            shop_test_page.turn_back()
        else:
            marketing_ability_is_break = False

        assert advertising_is_break,'Jump failed,advertising_is_break'
        assert free_search_is_break,'Jump failed,free_search_is_break'
        assert baby_up_and_down_is_break,'Jump failed,baby_up_and_down_is_break'
        assert hand_weights_is_break,'Jump failed,hand_weights_is_break'
        assert baby_click_rate_is_break,'Jump failed,baby_click_rate_is_break'
        assert marketing_ability_is_break,'Jump failed,marketing_ability_is_break'



    @allure.feature('店铺体检')
    @allure.story('一键优化是否可用')
    @pytest.mark.p1
    def test_one_touch_optimize(self, first_page_wait_scan):
        shop_test_page = first_page_wait_scan.go_shop_test_top_area()
        shop_test_page.click_one_touch_optimize()
        advertising_num = shop_test_page.get_advertising_testing_num()
        baby_time_num = shop_test_page.get_baby_up_and_down_num()
        hand_weights_num = shop_test_page.get_hand_weights_num()
        assert advertising_num == '0', '一键优化异常'
        assert baby_time_num == '0', '一键优化异常'
        assert hand_weights_num == '0', '一键优化异常'


