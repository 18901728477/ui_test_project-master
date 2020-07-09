
from mobile.mitem_ui_test.mitem_ui_test.pages.common_list_page import *
from mobile.mitem_ui_test.mitem_ui_test.pages.title_improve_detail_page import *
from mobile.mitem_ui_test.mitem_ui_test.item_info import *
from mobile.mitem_ui_test.mitem_ui_test.pages.shop_test_page import *

class ItemList(CommonList):

    go_detail_locator = ('and', (('attr.*=', ('text', '销量: \d*件')),))
    on_shelf_button_locator = ('and', (('attr=', ('text', '上架')),))
    off_shelf_button_locator = ('and', (('attr=', ('text', '下架')),))
    promotion_button_locator = ('and', (('attr=', ('text', '促销推广')),))
    title_optimization_button_locator = ('and', (('attr.*=', ('text', '标题.*')),))
    mobile_detail_button_locator = ('and', (('attr=', ('text', '手机详情')),))
    copy_link_button_locator = ('and', (('attr=', ('text', '复制链接')),))
    two_dimensional_code_button_locator = ('and', (('attr=', ('text', '二维码')),))
    choose_button_locator = ('and', (('attr=', ('text', '筛选')),))
    long_click_two_dimensional_code_locator = ('and', (('attr=', ('text', '长按识别二维码')),))
    more_function_locator = ('and', (('attr=', ('text', '···')),))
    tab_onsale_locator = ('and', (('attr.*=', ('text', '出售中.*')),))
    tab_inventory_locator = ('and', (('attr.*=', ('text', '仓库中.*')),))
    tab_soldout_locator = ('and', (('attr.*=', ('text', '已售完.*')),))

    calendar_anchor = ('and', (('attr.*=', ('text', '立即.*')),))

    # 方法，滑动弹窗
    def swipe_618(self):
        poco(name='android.widget.Image').swipe([0, 1])

    # 方法：进入宝贝详情页
    def go_detail_page(self):
        element_click(self.go_detail_locator)
        try:
            poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').wait_for_appearance(
                5)  # 第一次进入授权，5秒显示等待
            poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').click()
        except Exception:
            pass
        poco(text='编辑图片').wait_for_appearance(6) # 跳转详情页，3秒显示等待
        poco(text='查看宝贝').click()
        self.turn_back()
        # self.swipe_618()


    # 获取出售中数量
    def get_onsale_number(self):
        onsale_number = poco(name='tab0')
        onsale_number_text = get_text_of_view(onsale_number)
        num = re.findall('\d+', onsale_number_text)
        return int(num[0])

    # 获取仓库中数量
    def get_inventory_number(self):
        inventory_number = poco(name='tab1')
        inventory_number_text = get_text_of_view(inventory_number)
        num = re.findall('\d+', inventory_number_text)
        return int(num[0])

    # 获取已售完数量
    def get_soldout_number(self):
        soldout_number = poco(name='tab2')
        soldout_number_text = get_text_of_view(soldout_number)
        num = re.findall('\d+', soldout_number_text)
        return int(num[0])

    # 获取第一个宝贝库存数量
    def get_stock_number(self):
        stock_text = poco(textMatches='库存.*').get_text()
        num = re.findall('\d+', stock_text)
        return int(num[0])

    # 获取第一个宝贝销量数量
    def get_sold_number(self):
        sold_text = poco(textMatches='销量.*').get_text()
        num = re.findall('\d+', sold_text)
        return int(num[0])

    # 上架第一个宝贝
    def on_shelf_list(self):
        if not init_element(self.on_shelf_button_locator).exists():
            self.element_click_async(self.more_function_locator)
        else:
            pass
        self.element_click_async(self.on_shelf_button_locator)
        poco(text='确定').click()

    #下架
    def off_shelf_list(self):
        if not init_element(self.off_shelf_button_locator).exists():
            self.element_click_async(self.more_function_locator)
        else:
            pass
        self.element_click_async(self.off_shelf_button_locator)
        poco(text='确定').click()

    #促销推广
    def promotion_list(self) -> bool:
        self.element_click_async(self.promotion_button_locator)
        poco(text='满减优惠').click()
        self.check_QN_auth()
        self.check_AYitem_auth()
        # 立刻创建1个满减优惠活动，判断是否成功
        self.quick_create()
        # 返回，进入促销打折页面，立刻创建1个促销打折活动，判断是否成功
        sleep(3)
        self.turn_back()
        poco(text='促销打折').click()
        self.check_QN_auth()
        self.check_AYitem_auth()
        self.quick_create()
        # 结束创建成功的促销打折活动，避免影响店铺体检跳转ump
        poco(name=' 知道了 ').click()
        poco(name='android.support.v7.widget.RecyclerView').swipe([0, 1])
        sleep(2)
        poco(name='结束活动').click()
        poco(text='确定').click()
        sleep(1)
        self.turn_back()
        return True

    # 快速创建ump活动
    def quick_create(self) -> bool:
        """

        :return:
        如果创建失败，返回False
        """
        try:
            poco(name=' 创建活动 ').wait_for_appearance(5)  # 跳转ump页面，5秒显示等待
        except PocoTargetTimeout:
            return False
        poco(name=' 创建活动 ').click()
        poco(name='确定提交').click()
        try:
            poco(name='活动已创建成功!').wait_for_appearance(5)
        except PocoTargetTimeout:
            return False

    #标题优化
    def title_optimization_list(self) -> bool:
        self.element_click_async(self.title_optimization_button_locator)
        poco(text=ITEM_INVENTORY_TITLE).wait_for_appearance(10)  # 跳转标题优化详情页，10秒显示等待
        TitleImproveDetail().edit_title('标题')
        title_before_improve = TitleImproveDetail().get_title()
        TitleImproveDetail().one_click_improve()
        sleep(3)  # 一键优化，3秒sleep
        title_after_improve = TitleImproveDetail().get_title()
        return title_after_improve != title_before_improve

    #手机详情
    def mobile_detail_list(self) -> bool:
        self.element_click_async(self.mobile_detail_button_locator)
        try:
            poco(textMatches='.*生成.*').wait_for_appearance(5)  # 跳转手机详情，3秒显示等待
        except PocoTargetTimeout:
            return False
        poco(textMatches='.*生成.*').click()
        try:
            poco(text='预计剩余时间').wait_for_appearance(3)
        except PocoTargetTimeout:
            return False
        self.turn_back()
        return True

    #复制链接
    def copy_link_list(self):
        if not init_element(self.copy_link_button_locator).exists():
            self.element_click_async(self.more_function_locator)
        else:
            pass
        #淘宝链接
        copy_link_button = init_element(self.copy_link_button_locator)
        assert self.search_by_keyword('测试多sku属性宝贝',copy_link_button), '宝贝不存在'
        copy_link_button.click()
        poco(text = '取消').wait_for_appearance(5)
        poco(text = '淘宝链接').click()
        choose_button = init_element(self.choose_button_locator)
        search_close_button = locate_by_anchor(choose_button,3,'l0l0l1')
        search_close_button.click()
        element_click(self.search1_locator)
        poco(name='android.widget.EditText').long_click()
        poco(text = '粘贴').click()
        text1 = poco(name='android.widget.EditText').get_text()
        self.turn_back()
        #防微信屏蔽链接
        assert self.search_by_keyword(ITEM_COPY_LINK_TITLE, copy_link_button), '宝贝不存在'
        copy_link_button.click()
        poco(text='取消').wait_for_appearance(5)
        poco(text='防微信屏蔽链接').click()
        choose_button = init_element(self.choose_button_locator)
        search_close_button = locate_by_anchor(choose_button, 3, 'l0l0l1')
        search_close_button.click()
        element_click(self.search1_locator)
        poco(name='android.widget.EditText').long_click()
        poco(text='粘贴').click()
        text2 = poco(name='android.widget.EditText').get_text()
        self.turn_back()

        return text1,text2

    # 查看详情
    def view_detail_list(self, my_title: str):
        if not init_element(self.two_dimensional_code_button_locator).exists():
            self.element_click_async(self.more_function_locator)
        else:
            pass
        view_detail_ele = locate_by_anchor(init_element(self.two_dimensional_code_button_locator), 2, 'l3')
        view_detail_ele.click()
        try:
            poco(text=my_title).wait_for_appearance(10)
            self.turn_back()
            return True
        except PocoTargetTimeout:
            self.turn_back()
            return False


    # 二维码
    def two_dimensional_code_list(self):
        if not init_element(self.two_dimensional_code_button_locator).exists():
            self.element_click_async(self.more_function_locator)
        else:
            pass
        self.element_click_async(self.two_dimensional_code_button_locator)
        poco(text='下载图片').click()
        try:
            poco(text='图片下载失败').wait_for_appearance(8)  # 等待文件保存到本地，8秒显示等待
            poco(text='确认').click()
            return False
        except PocoTargetTimeout:
            return True

    # 切换顶部tab
    def switch_tab(self, index: int):
        """

        :param index:
        0:出售中
        1:仓库中
        2:已售完
        :return:
        """
        tab_dict = {
            0: self.tab_onsale_locator,
            1: self.tab_inventory_locator,
            2: self.tab_soldout_locator
        }
        init_element(tab_dict.get(index)).invalidate()
        element_click(tab_dict.get(index))

    # 点击列表活动日历，跳转功能
    def activity_calendar_shop_test_enter(self) -> bool:
        # 如果日历下线，跳转店铺体检
        sleep(3)
        if not init_element(self.calendar_anchor).exists():
            print('日历已下线，跳转店铺体检')
            BasePage().close_auto_list()
            poco(text='查看详情').click()
            poco(text='一键优化').wait_for_appearance(60)
            ShopTest().click_one_touch_optimize()
            advertising_num = ShopTest().get_advertising_testing_num()
            baby_time_num = ShopTest().get_baby_up_and_down_num()
            hand_weights_num = ShopTest().get_hand_weights_num()
            if advertising_num != '0':
                return False
            if baby_time_num != '0':
                return False
            if hand_weights_num != '0':
                return False
            return True

        # 如果日历没下线，跳转活动日历
        else:
            my_function = locate_by_anchor(init_element(self.calendar_anchor), 2, 'l1').get_text()
            function1 = '设置营销折扣，吸引买家下单'  # 促销打折话术
            function2 = '优化标题，增加宝贝曝光率'  # 标题优化话术
            function3 = '多买多减优惠，提高客单价'  # 满减优惠话术
            function4 = '投放活动海报，增强活动气氛'  # 促销海报话术
            function5 = '添加活动水印，提示宝贝点击率'  # 促销水印话术
            element_click(self.calendar_anchor)
            self.check_QN_auth()
            self.check_AYitem_auth()
            if my_function == function1:
                try:
                    poco(name=' 创建活动 ').wait_for_appearance(5)
                    self.turn_back()
                    return True
                except PocoTargetTimeout:
                    self.turn_back()
                    return False
            elif my_function == function2:
                try:
                    poco(text='上次优化时间：').wait_for_appearance(5)
                    self.turn_back()
                    return True
                except PocoTargetTimeout:
                    self.turn_back()
                    return False
            elif my_function == function3:
                try:
                    poco(name=' 创建活动 ').wait_for_appearance(5)
                    self.turn_back()
                    return True
                except PocoTargetTimeout:
                    self.turn_back()
                    return False
            elif my_function == function4:
                try:
                    poco(text='促销海报').wait_for_appearance(5)
                    self.turn_back()
                    return True
                except PocoTargetTimeout:
                    self.turn_back()
                    return False
            elif my_function == function5:
                try:
                    sleep(2)
                    poco(textMatches='.*水印').wait_for_appearance(5)
                    self.turn_back()
                    return True
                except PocoTargetTimeout:
                    self.turn_back()
                    return False


if __name__ == '__main__':
    x = ItemList()

    