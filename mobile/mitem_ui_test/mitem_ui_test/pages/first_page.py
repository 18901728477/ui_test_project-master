# -*- encoding=utf8 -*-
__author__ = 'xiaoxuan'

from mobile.mitem_ui_test.mitem_ui_test.pages.auction_page import AuctionPage
from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import *
from mobile.mitem_ui_test.mitem_ui_test.pages.release_baby_page import ReleasePage
from mobile.mitem_ui_test.mitem_ui_test.pages.mdetail_page import MdetailPage
from mobile.mitem_ui_test.mitem_ui_test.pages.badword_detect_page import BadwordDetect
from mobile.mitem_ui_test.mitem_ui_test.pages.batch_update_page import BatchUpdate
from mobile.mitem_ui_test.mitem_ui_test.pages.item_list_page import ItemList
from mobile.mitem_ui_test.mitem_ui_test.pages.shop_test_page import ShopTest
from mobile.mitem_ui_test.mitem_ui_test.pages.shortvideo_page import ShortVideo
from mobile.mitem_ui_test.mitem_ui_test.pages.title_improve_list_page import TitleImproveList
from mobile.mitem_ui_test.mitem_ui_test.pages.mine_page import MinePage
from mobile.mitem_ui_test.mitem_ui_test.item_info import ACTIVITY_NAME


class FirstPage(BasePage):
    shop_test_locator = ('and', (('attr=', ('text', '店铺体检')),))
    shop_test_top_area_locator1 = ('and', (('attr=', ('text', '查看详情')),))
    shop_test_top_area_locator2 = ('and', (('attr=', ('text', '重新检测')),))
    shop_test_score_locator = ('and', (('attr.*=', ('text', '\\d{1,4}')),))
    onsale_item_anchor = ('and', (('attr=', ('text', '出售中')),))
    inventory_item_anchor = ('and', (('attr=', ('text', '仓库中')),))
    soldout_item_anchor = ('and', (('attr=', ('text', '已售完')),))
    mdetail_locator = ('and', (('attr=', ('text', '手机详情')),))
    shortvideo_locator = ('and', (('attr=', ('text', '主图视频')),))
    badword_detect_locator = ('and', (('attr=', ('text', '违规词检测')),))
    batch_update_locator = ('and', (('attr=', ('text', '批量修改')),))
    title_improve_locator = ('and', (('attr=', ('text', '标题优化')),))

    first_page_locator = ('and', (('attr=', ('text', '首页')),))
    list_page_locator = ('and', (('attr=', ('text', '商品')),))
    release_btn = ('and', (('attr=', ('text', '发布宝贝')),))
    auction_button_locator = ('and', (('attr=', ('text', '淘宝拍卖')),))

    activity_calendar_anchor = ('and', (('attr=', ('text', ACTIVITY_NAME)),))

    def go_my_page(self):
        poco(name='android.support.v7.app.ActionBar$Tab')[2].click()
        return MinePage()

    def self_check(self):
        poco(text='出售中').parent().offspring(textMatches='\d*').wait_for_appearance(5)  # 进入首页，5秒显示等待

    # 方法：首页-店铺体检区域，点击“查看详情”或“重新检测”，跳转“店铺体检”页面
    def go_shop_test_top_area(self):
        shop_test_top_area_locator1 = init_element(self.shop_test_top_area_locator1)
        shop_test_top_area_locator2 = init_element(self.shop_test_top_area_locator2)
        poco(text='分').parent().offspring(textMatches='\d+').wait_for_appearance(10)
        if shop_test_top_area_locator1.exists():
            shop_test_top_area_locator1.click()
        else:
            shop_test_top_area_locator2.click()
        # 检测完需要时间，60秒显示等待
        poco(text='一键优化').wait_for_appearance(60)
        return ShopTest()

    # 方法：首页，点击“店铺体检”图标，跳转“店铺体检”页面
    def go_shop_test(self):
        BasePage().page_swipe_buttom()
        element_click(self.shop_test_locator)
        poco(text='一键优化').wait_for_appearance(60)  # 检测完需要时间，60秒显示等待
        return ShopTest()

    # 方法：首页，获取店铺体检分数
    def get_shop_test_score(self) -> str:
        BasePage().page_swipe_top()
        return get_text_of_view(init_element(self.shop_test_score_locator))

    # 方法：获取各状态的宝贝总数
    def get_item_num(self, status: int) -> str:
        """
        status:
        0：出售中
        1：仓库中
        2：已售完
        :param status:
        :return:
        """
        amout_dict = {0: locate_by_anchor(init_element(self.onsale_item_anchor), 1, 'v0'),
                      1: locate_by_anchor(init_element(self.inventory_item_anchor), 1, 'v0'),
                      2: locate_by_anchor(init_element(self.soldout_item_anchor), 1, 'v0')}
        return get_text_of_view(amout_dict.get(status))

    # 方法：进入各状态列表
    def go_item_list(self, status: int):
        """
        status:
        0：出售中
        1：仓库中
        2：已售完
        :param status:
        :return:
        """
        dict = {0: self.onsale_item_anchor, 1: self.inventory_item_anchor, 2: self.soldout_item_anchor}
        element_click(dict.get(status))
        poco(textMatches='编码: .*').wait_for_appearance(5)  # 列表加载，5秒显示等待
        return ItemList()

    # 方法：进入手机详情页面
    def go_mdetail(self):
        element_click(self.mdetail_locator)

        # 如果终止过全店任务
        task_delete_locator = ('and', (('attr=', ('text', '删除任务')),))
        if does_element_exists(task_delete_locator):
            element_click(task_delete_locator)

        # 如果有全店任务执行完
        watch_record_locator = ('and', (('attr=', ('text', '查看详情')),))
        if does_element_exists(watch_record_locator):
            element_click(watch_record_locator)
            BasePage().turn_back()

        poco(textMatches='\d{1,4}').wait_for_appearance(20)  # 页面跳转，20秒显示等待
        return MdetailPage()

    # 方法：进入主图视频页面
    def go_shortvideo(self):
        element_click(self.shortvideo_locator)
        poco(textMatches='..生成').wait_for_appearance(5)  # 页面跳转，5秒显示等待
        return ShortVideo()

        # 方法：进入违规词检测页面

    def go_badword_detect(self):
        BasePage().page_swipe_buttom()
        badword_detect_button = init_element(self.badword_detect_locator)
        badword_detect_button.click()
        try:
            poco(text='开始检测').wait_for_appearance(5)  # 页面跳转，5秒显示等待
        except PocoTargetTimeout:
            print('第一次没点到')
            super_click(badword_detect_button)
        poco(text='开始检测').wait_for_appearance(5)
        return BadwordDetect()

    # 方法：进入发布宝贝页面
    def go_release_detect(self):

        release_button = init_element(self.release_btn)
        release_button.click()

        try:
            poco(text='发布宝贝').wait_for_appearance(5)  # 页面跳转，5秒显示等待
            text_release = poco(text='发布宝贝').exists()
        except PocoTargetTimeout:
            print('没有进入发布宝贝页面')
            # 刷新页面
            self.refresh_backhome()
            super_click(release_button)
        poco(text='发布宝贝').wait_for_appearance(5)
        return ReleasePage(), text_release

    # 进入淘宝拍卖页面
    def go_auction_detect(self):
        auction_button = init_element(self.auction_button_locator)
        auction_button.click()
        try:
            poco(text='淘宝拍卖').wait_for_appearance(5)  # 页面跳转，5秒显示等待
            text_auction = poco(text='淘宝拍卖').exists()
        except PocoTargetTimeout:
            print('没有进入淘宝拍卖页面')
            # 刷新页面
            self.refresh_backhome()
            super_click(auction_button)
        poco(text='淘宝拍卖').wait_for_appearance(5)
        return AuctionPage(), text_auction




# 方法：进入批量修改页面
def go_batch_update(self):
    self.page_swipe_buttom()
    element_click(self.batch_update_locator)
    poco(text='详情').wait_for_appearance(5)  # 页面跳转，5秒显示等待
    return BatchUpdate()


# 方法：进入标题优化列表页
def go_title_improve(self):
    element_click(self.title_improve_locator)
    poco(text='重新检测').wait_for_appearance(10)  # 页面跳转，10秒显示等待
    return TitleImproveList()


# 方法：首页活动日历跳转营销折扣
def test_calendar_01(self):
    locate_by_anchor(init_element(self.activity_calendar_anchor), 2, 'v1l0').click()
    self.check_QN_auth()
    self.check_AYitem_auth()
    try:
        poco(name=' 创建活动 ').wait_for_appearance(5)
        self.turn_back()
        return True
    except PocoTargetTimeout:
        self.turn_back()
        return False


# 方法：首页活动日历跳转促销水印
def test_calendar_02(self):
    locate_by_anchor(init_element(self.activity_calendar_anchor), 2, 'v1l1').click()
    self.check_QN_auth()
    self.check_AYitem_auth()
    try:
        sleep(2)
        poco(textMatches='.*水印').wait_for_appearance(5)
        self.turn_back()
        return True
    except PocoTargetTimeout:
        self.turn_back()
        return False


# 方法：首页活动日历跳转标题优化
def test_calendar_03(self):
    locate_by_anchor(init_element(self.activity_calendar_anchor), 2, 'v1').swipe([-0.5, 0])
    sleep(1.5)
    locate_by_anchor(init_element(self.activity_calendar_anchor), 2, 'v1l2').click()
    try:
        poco(text='上次优化时间：').wait_for_appearance(5)
        self.turn_back()
        return True
    except PocoTargetTimeout:
        self.turn_back()
        return False


# 方法：首页活动日历跳转促销海报
def test_calendar_04(self):
    locate_by_anchor(init_element(self.activity_calendar_anchor), 2, 'v1').swipe([-1, 0])
    sleep(1.5)
    locate_by_anchor(init_element(self.activity_calendar_anchor), 2, 'v1l3').click()
    self.check_QN_auth()
    self.check_AYitem_auth()
    try:
        poco(text='促销海报').wait_for_appearance(5)
        self.turn_back()
        return True
    except PocoTargetTimeout:
        self.turn_back()
        return False


# 方法：首页活动日历跳转满减优惠
def test_calendar_05(self):
    locate_by_anchor(init_element(self.activity_calendar_anchor), 2, 'v1').swipe([-1, 0])
    sleep(1.5)
    locate_by_anchor(init_element(self.activity_calendar_anchor), 2, 'v1l4').click()
    self.check_QN_auth()
    self.check_AYitem_auth()
    try:
        poco(name=' 创建活动 ').wait_for_appearance(5)
        self.turn_back()
        return True
    except PocoTargetTimeout:
        self.turn_back()
        return False


# 方法：首页存在活动日历时，检查跳转；不存在活动日历时，用例直接pass
def test_activity_calendar_first_page(self):
    # 如果不存在活动日历，直接返回true
    if not init_element(self.activity_calendar_anchor).exists():
        print('活动日历已自动下线')
        return True
    # 如果活动日历存在，检查5项跳转
    else:
        result_list = [self.test_calendar_01(), self.test_calendar_02(), self.test_calendar_03(),
                       self.test_calendar_04(), self.test_calendar_05()]
        final_result = True
        for each_result in result_list:
            if not each_result:
                final_result = False
                break
        return final_result


if __name__ == '__main__':
    FirstPage().go_release_detect()
