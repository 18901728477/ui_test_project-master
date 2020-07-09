from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import *
from mobile.mitem_ui_test.mitem_ui_test.pages.edit_pic_page import *
from mobile.mitem_ui_test.mitem_ui_test.pages.detail_porperty_page import *
import re
from mobile.mitem_ui_test.mitem_ui_test.pages.title_improve_detail_page import TitleImproveDetail
from mobile.mitem_ui_test.mitem_ui_test.pages.shop_test_page import *


class ItemDetail(BasePage):
    item_top_info_anchor = ('and', (('attr.*=', ('text', '库存: .*件')),))

    pic_video_tab_locator = ('and', (('attr=', ('text', '主图/视频')),))
    edit_pic_locator = ('and', (('attr=', ('text', '编辑图片')),))
    create_shortvideo_locator = ('and', (('attr.*=', ('text', '.*生成视频')),))
    long_pic_locator = ('and', (('attr=', ('text', '长图图片')),))

    basic_info_tab_locator = ('and', (('attr=', ('text', '基本信息')),))
    class_checkbox = '\ue6ba'  # 分类的选择框
    show_second_class = '\ue911'  # 展开二级分类
    item_status_anchor = ('and', (('attr=', ('text', '宝贝状态')),))
    list_locator = ('and', (('attr.*=', ('text', '.架')),))
    delist_time_anchor = ('and', (('attr=', ('text', '下架时间')),))
    item_code_anchor = ('and', (('attr=', ('text', '商品编码')),))
    bar_code_anchor = ('and', (('attr=', ('text', '条形码')),))
    item_property_anchor = ('and', (('attr=', ('text', '宝贝属性')),))
    shop_cat_anchor = ('and', (('attr=', ('text', '店铺分类')),))
    deliver_tempalte_anchor = ('and', (('attr=', ('text', '运费模版')),))
    guarantee_anchor = ('and', (('attr=', ('text', '保修')),))
    invoice_anchor = ('and', (('attr=', ('text', '发票')),))
    store_calculate_anchor = ('and', (('attr=', ('text', '库存计数')),))

    sale_info_tab_locator = ('and', (('attr=', ('text', '销售规格')),))
    edit_price_locator = ('and', (('attr=', ('text', '编辑')),))
    fixed_price_anchor = ('and', (('attr=', ('text', '一口价')),))

    mdetail_tab_locator = ('and', (('attr=', ('text', '手机详情')),))
    create_locator = ('and', (('attr=', ('text', '重新生成')),))

    calendar_anchor = ('and', (('attr.*=', ('text', '立即.*')),))

    watermark_anchor = ('and', (('attr=', ('text', '热门水印')),))
    watermark_restore_pic_locator = ('and', (('attr=', ('text', '恢复至原主图')),))
    watermark_delete_locator = ('and', (('attr=', ('text', '手动恢复至该主图')),))

    # 方法：切换tab
    def switch_tab(self, tab_index: int):
        """

        :param tab_index:
        0:主图/视频，1：基本信息，2：销售规格，3：手机详情
        :return:
        """

        tab_dict = {
            0: self.pic_video_tab_locator,
            1: self.basic_info_tab_locator,
            2: self.sale_info_tab_locator,
            3: self.mdetail_tab_locator
        }
        ele = init_element(tab_dict.get(tab_index))
        poco(text='查看宝贝').click()
        self.turn_back()
        ele.invalidate()
        ele.click()
        # 如果进入的是主图/视频tab
        if tab_index == 0:
            try:
                poco(text='编辑图片').wait_for_appearance(3)
            except PocoTargetTimeout:
                # 第一次没点到，点击第二次，滑动触发invalidate
                self.does_enter_wrong_page()
                BasePage().page_swipe_buttom()
                ele.invalidate()
                ele.click()
        # 如果进入的是基本信息tab
        elif tab_index == 1:
            try:
                poco(text='宝贝状态').wait_for_appearance(3)
            except PocoTargetTimeout:
                # 第一次没点到，点击第二次，滑动触发invalidate
                self.does_enter_wrong_page()
                BasePage().page_swipe_buttom()
                ele.invalidate()
                ele.click()
        # 如果进入的是销售规格tab
        elif tab_index == 2:
            try:
                poco(text='编辑').wait_for_appearance(3)
            except PocoTargetTimeout:
                # 第一次没点到，点击第二次，滑动触发invalidate
                self.does_enter_wrong_page()
                BasePage().page_swipe_buttom()
                ele.invalidate()
                ele.click()
        # 如果进入的是手机详情tab
        elif tab_index == 3:
            try:
                poco(text='重新生成').wait_for_appearance(3)
            except PocoTargetTimeout:
                # 第一次没点到，点击第二次，滑动触发invalidate
                self.does_enter_wrong_page()
                BasePage().page_swipe_buttom()
                ele.invalidate()
                ele.click()

    # 方法：详情页切换tab如果进错页面
    def does_enter_wrong_page(self):
        if poco(text='编辑图片').exists():
            pass
        else:
            self.turn_back()

    # 方法：编辑标题
    def edit_title(self, new_title: str):
        """
        编辑后的标题
        :param new_title:
        :return:
        """
        title_element = locate_by_anchor(init_element(self.item_top_info_anchor), 2, 'v0l1')
        title_element.click()
        poco(name='android.widget.EditText').set_text(new_title)
        poco(text='确定').click()

    # 方法：获取显示的标题
    def get_title(self) -> str:
        """

        :return:
        页面显示的标题
        """
        title_element = locate_by_anchor(init_element(self.item_top_info_anchor), 2, 'v0l0')
        return get_text_of_view(title_element)

    # 方法：进入标题优化页面
    def go_title_improve_page(self) -> TitleImproveDetail():
        locate_by_anchor(init_element(self.item_top_info_anchor), 2, 'v1l0').click()
        poco(text='标题优化').wait_for_appearance(10)
        return TitleImproveDetail()

    # 方法：获取显示的一口价
    def get_fixed_price(self) -> str:
        """

        :return:
        获得的一口价,去掉第一个特殊字符
        """
        fixed_price_element = locate_by_anchor(init_element(self.item_top_info_anchor), 2, 'v2')
        fixed_price = get_text_of_view(fixed_price_element)
        return fixed_price[1:]

    # 方法：获取显示的库存
    def get_store(self) -> str:
        """

        :return:
        返回库存
        """
        store_element = locate_by_anchor(init_element(self.item_top_info_anchor), 2, 'v3l1')
        store = get_text_of_view(store_element)
        return re.findall(r"\d+\.?\d*", store)[0]

    # 方法：进入图片编辑页面
    def go_edit_pic_page(self):
        element_click(self.edit_pic_locator)
        return EditPic()

    # 方法：生成主图视频
    def create_shortvideo(self) -> bool:
        """

        :return:
        有视频还正在生成中，返回false；否则返回true
        """
        enable_create = True
        if poco(text='视频正在审核中...').exists():
            poco(text='刷新').click()
        if poco(textMatches='.视频正在生成中').exists():
            enable_create = False
        elif not poco(textMatches='.视频正在生成中').exists():
            element_click(self.create_shortvideo_locator)
            poco(text='使用模板')[7].click()
        return enable_create

    # 方法：上下架宝贝
    def list_delist_item(self):
        element_click(self.list_locator)
        poco(text='确定').click()

    # 方法：获取宝贝状态
    def get_item_status(self) -> str:
        """

        :return:
        返回出售中或仓库中
        """
        status_ele = init_element(self.item_status_anchor).parent().parent().offspring(textMatches='.*中')
        return get_text_of_view(status_ele)

    # 方法：获取下架时间
    def get_delist_time(self) -> str:
        """

        :return:
        返回下架时间
        """
        delist_time_element = locate_by_anchor(init_element(self.delist_time_anchor), 2, 'l1')
        return get_text_of_view(delist_time_element)

    # 方法：编辑商品编码
    def edit_item_code(self, my_code: str):
        """

        :param my_code:
        输入的编码
        :return:
        """
        item_code_element = locate_by_anchor(init_element(self.item_code_anchor), 2, 'l1')
        item_code_element.click()
        poco(name='android.widget.EditText').set_text(my_code)
        poco(text='确认').click()

    # 方法：获取商品编码
    def get_item_code(self) -> str:
        code_ele = locate_by_anchor(init_element(self.item_code_anchor), 2, 'l1l0l0')
        return get_text_of_view(code_ele)

    # 方法：编辑条形码
    def edit_bar_code(self, my_code: str):
        """

        :param my_code:
        输入的条形码
        :return:
        """
        bar_code_element = locate_by_anchor(init_element(self.bar_code_anchor), 2, 'l1')
        bar_code_element.click()
        poco(name='android.widget.EditText').set_text(my_code)
        poco(text='确认').click()

    # 方法：获取条形码
    def get_bar_code(self) -> str:
        code_ele = locate_by_anchor(init_element(self.item_code_anchor), 2, 'l1l0l0')
        return get_text_of_view(code_ele)

    # 方法：进入宝贝属性页面
    def go_item_property_page(self):
        """

        :return:
        返回宝贝属性页面
        """
        item_property_element = locate_by_anchor(init_element(self.item_property_anchor), 2, 'l1')
        item_property_element.click()
        poco(text='保存').wait_for_appearance(10)  # 进入属性页面，10s显示等待
        return DetailProperty()

    # 方法：清空所有店铺分类
    def recover_shop_class(self):
        shop_cat_element = locate_by_anchor(init_element(self.shop_cat_anchor), 2, 'l1')
        shop_cat_element.click()
        all_choose_anchor = poco(text='全选')
        all_choose_ele = locate_by_anchor(all_choose_anchor, 1, 'l0')
        # 如果属性已经全选
        if get_text_of_view(all_choose_ele) == '\ue618':
            pass
        # 如果没有全选，全选
        elif get_text_of_view(all_choose_ele) != '\ue618':
            all_choose_ele.click()
        all_choose_ele.click()  # 再次点击全选，取消全选
        poco(text='保存').click()

    # 方法：选择店铺分类
    def choose_shop_class(self, class_level: int, class_dict: dict):
        """

           :param class_level:
           0：一级分类
           1：二级分类
           :param class_dict:
           class_level=0,{'一级分类'：'xxx'}
           class_level=1,{'一级分类':'xxx','二级分类':'yyy'}
           :return:
        """
        shop_cat_element = locate_by_anchor(init_element(self.shop_cat_anchor), 2, 'l1')
        shop_cat_element.click()
        class_level_dict = {0: '一级分类', 1: '二级分类'}
        class_text = class_dict.get('一级分类')
        if class_level_dict.get(class_level) == '一级分类':
            poco(text=class_text).parent().parent().offspring(text=self.class_checkbox).click()
        elif class_level_dict.get(class_level) == '二级分类':
            poco(text=class_text).parent().parent().offspring(text=self.show_second_class).click()
            poco(text=class_dict.get('二级分类')).click()
        poco(text='保存').click()

    # 方法：获取店铺分类
    def get_shop_cat(self) -> str:
        shop_cat_ele = locate_by_anchor(init_element(self.shop_cat_anchor), 2, 'l1l0l0')
        return get_text_of_view(shop_cat_ele)

    # 方法：选择运费模板
    def change_delivery_template(self, my_deliver: str):
        """

        :param my_deliver:
        要选择的运费模板名字
        :return:
        """
        delivery_template_ele = locate_by_anchor(init_element(self.deliver_tempalte_anchor), 2, 'l1')
        delivery_template_ele.click()
        poco(text=my_deliver).click()
        poco(text='确认').click()

    # 方法：编辑其他信息
    def edit_other_info(self, guarantee: int, invoice: int, store_cal: int):
        """

        :param guarantee:
        保修，0：无，1：有
        :param invoice:
        发票，0：无，1：有
        :param store_cal:
        库存计数，0:拍下减库存，1：付款减库存
        :return:
        """
        guarantee_dict = {0: '无', 1: '有'}
        invoice_dict = {0: '无', 1: '有'}
        store_cal_dict = {0: '拍下减库存', 1: '付款减库存'}
        locate_by_anchor(init_element(self.guarantee_anchor), 2, 'l1').click()
        poco(text=guarantee_dict.get(guarantee)).click()
        locate_by_anchor(init_element(self.invoice_anchor), 2, 'l1').click()
        poco(text=invoice_dict.get(invoice)).click()
        locate_by_anchor(init_element(self.store_calculate_anchor), 2, 'l1').click()
        poco(text=store_cal_dict.get(store_cal)).click()

    # 方法：返回其他信息
    def get_other_info(self) -> dict:
        """

        :return:
        {0:'无', 1:'有' , 2:'不参与会员打折'}
        """
        other_info_dict = {
            0: get_text_of_view(locate_by_anchor(init_element(self.guarantee_anchor), 2, 'l1l0l0')),
            1: get_text_of_view(locate_by_anchor(init_element(self.invoice_anchor), 2, 'l1l0l0')),
            2: get_text_of_view(locate_by_anchor(init_element(self.store_calculate_anchor), 2, 'l1l0l0'))
        }
        return other_info_dict

    # 方法：更换一口价
    def change_fixed_price(self, my_price: str):
        """

        :param my_price:
        输入一口价：1234.00，要带上小数点
        :return:
        """
        locate_by_anchor(init_element(self.fixed_price_anchor), 1, 'l1l1').click()
        poco(text='确定').parent().parent().offspring(text=my_price).click()
        poco(text='确定').click()
        # 如果需要授权
        try:
            poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').wait_for_appearance(3)
            print('出现授权弹窗！')
            print(poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').attr('pos'))
            poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').click()
            poco(text='确定').click()
        except PocoTargetTimeout:
            pass

    # 方法：编辑第n个规格的价格、库存
    def edit_price_store(self, index: int, my_price: str, my_store: str):
        """

        :param index:
        如果是无sku宝贝，index=0
        如果是sku宝贝，
        index=0，编辑第一个sku价格库存
        index=1，编辑第二个sku价格库存
        :param my_price:
        价格
        :param my_store:
        库存
        :return:
        """
        poco(text='编辑')[index].click()
        poco(name='android.widget.EditText')[0].set_text(my_price)
        poco(name='android.widget.EditText')[1].set_text(my_store)
        poco(text='确定').click()
        # 如果需要授权
        try:
            poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').wait_for_appearance(3)
            print('出现授权弹窗！')
            print(poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').attr('pos'))
            poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').click()
            poco(text='确定').click()
        except PocoTargetTimeout:
            pass
        # 如果编辑后一口价发生变化
        if poco(textMatches='该sku的价格已设为一口价.*').exists():
            locate_by_anchor(poco(text='取消'), 1, 'l1').click()

    # 方法：生成手机详情
    def create_mdetail(self):
        if poco(text='重新生成').exists():
            poco(text='重新生成').click()
        if poco(text='一键生成手机详情').exists():
            poco(text='一键生成手机详情').click()
        poco(textMatches='.*生成.*').click()
        BasePage().turn_back()

    # 方法：获取底部全部吸底按钮的文本
    def get_buttom_button(self) -> list:
        """

        :return:
        包含了所有吸底按钮，文本值的列表
        """
        base_ele = poco(text='查看宝贝')
        buttom_list = []
        for buttom in base_ele.parent().children():
            buttom_list.append(buttom.get_text())
        return buttom_list

    # 方法：检查查看宝贝按钮是否可点击
    def check_watch_item(self, item_title: str) -> bool:
        """

        :param item_title:
        要查看的宝贝标题
        :return:
        跳转后，如果标题显示返回true，否则返回false
        """
        poco(text='查看宝贝').click()
        sleep(1)
        try:
            poco(text=item_title).wait_for_appearance(5)
            self.turn_back()
            return True
        except PocoTargetTimeout:
            self.turn_back()
            return False

    # 方法：增删规格，跳转后删除、增加一个sku规格
    def check_add_delete_sku_prop(self, item_title: str):
        try:
            poco(text='增删规格').click()
            self.check_QN_auth()
            self.check_AYitem_auth()
            poco(name='颜色分类').wait_for_appearance(15)  # 跳转qap增删规格页面，15秒显示等待

            # qap小键盘问题
            # locate_by_anchor(poco(name='颜色分类'), 1, 'v1v1l4').click()
            # locate_by_anchor(poco(text='选择或输入颜色'), 4, 'l2').click()
            # poco(name='白色系').click()
            # poco(name='乳白色').click()
            # poco(name='确定').click()
            # poco("android:id/content").swipe([0, -1])
            # sleep(3)
            # locate_by_anchor(poco(name='价格：'), 4, 'v0v1l0').offspring(name='android.widget.EditText').set_text(767)
            # locate_by_anchor(poco(name='价格：'), 4, 'v0v1l1').offspring(name='android.widget.EditText').set_text(50)
            # locate_by_anchor(poco(name='价格：'), 4, 'v1v1l0').offspring(name='android.widget.EditText').set_text(766)
            # locate_by_anchor(poco(name='价格：'), 4, 'v1v1l1').offspring(name='android.widget.EditText').set_text(50)
            # locate_by_anchor(poco(name='价格：'), 4, 'v2v1l0').offspring(name='android.widget.EditText').set_text(765)
            # locate_by_anchor(poco(name='价格：'), 4, 'v2v1l1').offspring(name='android.widget.EditText').set_text(50)

            poco(name='确定').click()
            poco(name=item_title).wait_for_appearance(10)
            self.turn_back()
            return True
        except Exception as e_msg:
            print(e_msg)
            return False

    # 方法：检查复制链接是否可用
    def check_copy_link(self):
        poco(text='复制链接').click()
        poco(text='防微信屏蔽链接').click()
        sleep(1)
        if not poco(text='防微信屏蔽链接').exists():
            return True
        else:
            return False

    # 点击列表活动日历，跳转功能
    def activity_calendar_shop_test_enter(self):
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
        # 如果日历没下线
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
                    poco(name=' 创建活动 ').wait_for_appearance(3)
                    self.turn_back()
                    return True
                except PocoTargetTimeout:
                    print('第一次没点到')
                    poco(text='查看宝贝').click()
                    self.turn_back()
                    init_element(self.calendar_anchor).invalidate()
                    element_click(self.calendar_anchor)
                    self.check_QN_auth()
                    self.check_AYitem_auth()
                    poco(name=' 创建活动 ').wait_for_appearance(3)
                    self.turn_back()
                    return True
            elif my_function == function2:
                try:
                    poco(text='上次优化时间：').wait_for_appearance(5)
                    self.turn_back()
                    return True
                except PocoTargetTimeout:
                    print('第一次没点到')
                    poco(text='查看宝贝').click()
                    self.turn_back()
                    init_element(self.calendar_anchor).invalidate()
                    element_click(self.calendar_anchor)
                    poco(name='上次优化时间：').wait_for_appearance(5)
                    self.turn_back()
                    return True
            elif my_function == function3:
                try:
                    poco(name=' 创建活动 ').wait_for_appearance(3)
                    self.turn_back()
                    return True
                except PocoTargetTimeout:
                    print('第一次没点到')
                    poco(text='查看宝贝').click()
                    self.turn_back()
                    init_element(self.calendar_anchor).invalidate()
                    element_click(self.calendar_anchor)
                    self.check_QN_auth()
                    self.check_AYitem_auth()
                    poco(name=' 创建活动 ').wait_for_appearance(3)
                    self.turn_back()
                    return True
            elif my_function == function4:
                try:
                    poco(text='促销海报').wait_for_appearance(3)
                    self.turn_back()
                    return True
                except PocoTargetTimeout:
                    print('第一次没点到')
                    poco(text='查看宝贝').click()
                    self.turn_back()
                    init_element(self.calendar_anchor).invalidate()
                    element_click(self.calendar_anchor)
                    self.check_QN_auth()
                    self.check_AYitem_auth()
                    poco(name='促销海报').wait_for_appearance(3)
                    self.turn_back()
                    return True
            elif my_function == function5:
                try:
                    sleep(2)
                    poco(textMatches='.*水印').wait_for_appearance(3)
                    self.turn_back()
                    return True
                except PocoTargetTimeout:
                    print('第一次没点到')
                    poco(text='查看宝贝').click()
                    self.turn_back()
                    init_element(self.calendar_anchor).invalidate()
                    element_click(self.calendar_anchor)
                    sleep(2)
                    self.check_QN_auth()
                    self.check_AYitem_auth()
                    poco(textMatches='.*水印').wait_for_appearance(3)
                    self.turn_back()
                    return True

    # 方法：详情页添加、删除水印
    def add_delete_watermark(self) -> bool:
        # 如果宝贝打过水印，先删
        if init_element(self.watermark_restore_pic_locator).exists():
            element_click(self.watermark_restore_pic_locator)
            element_click(self.watermark_delete_locator)
            poco(text='确认').click()
            sleep(3)
        else:
            pass
        # 点击第一个热门水印，快速添加
        locate_by_anchor(init_element(self.watermark_anchor), parent_lv=2, child_lv='v2l0').click()
        self.check_QN_auth()
        self.check_AYitem_auth()
        poco(name='直接打水印').wait_for_appearance(10)
        poco(name='直接打水印').click()
        try:
            poco(name='主图/视频').wait_for_appearance(5)
        except PocoTargetTimeout:
            self.turn_back()
            return False
        self.turn_back()
        # 返回小程序详情页后，判断水印是否添加成功
        try:
            init_element(self.watermark_restore_pic_locator).wait_for_appearance(15)
        except PocoTargetTimeout:
            return False
        # 删除水印，判断水印是否删除成功
        element_click(self.watermark_restore_pic_locator)
        element_click(self.watermark_delete_locator)
        poco(text='确认').click()
        sleep(3)
        if poco(text='查看更多').exists():
            return True
        else:
            return False

    # 方法：手机详情tab，编辑手机详情,增加文字
    def edit_mdetail_add_word(self, my_text: str):
        poco(text='编辑').click()
        BasePage().page_swipe_buttom()
        try:
            poco(text='添加文字').click()
        except PocoNoSuchNodeException:
            print('请调整测试的宝贝的手机详情，只能有1段文字')
        poco(text='后面加文字').click()
        poco(text='请输入文字').parent().offspring(name='android.widget.EditText').set_text(my_text)
        poco(text='确定').click()
        poco(text='确定修改').click()
        poco(text='确定').click()

    # 方法：手机详情tab，编辑手机详情,增加图片
    def edit_mdetail_add_pic(self):
        poco(text='编辑').click()
        try:
            poco(text='前加图片').click()
        except PocoNoSuchNodeException:
            print('请调整测试的宝贝的手机详情，只能有1段文字')
        poco(text='图片空间').click()
        PicRoom().enter_dict('商品自动化目录')
        PicRoom().choose_pic('长图.jpg')
        PicRoom().submit_pic()
        poco(text='确定修改').click()
        poco(text='确定').click()

    # 还原手机详情，清除添加的文字和图片
    def restore_mdetail(self):
        poco(text='编辑').click()
        poco(text='后加图片').parent().parent().parent().offspring(name='android.widget.Image').click()
        # poco(text='删除')[1].click()
        poco(text='确定修改').click()
        poco(text='确定').click()

    # 方法，调用api获取一个宝贝的手机详情
    def tb_api_get_item_mdetail(self, numid: str) -> str:
        """

        :param numid:
        :return:
        宝贝详情
        """
        req_url = 'http://crm.aiyongbao.com/testtools/getOfficialApi'
        params = {
            'nick': '赵东昊的测试店铺',
            'method': 'taobao.item.seller.get',
            'param[fields]': 'wireless_desc',
            'param[num_iid]': numid
        }
        cookies = {'PHPSESSID': self.get_sessionId()}
        r = requests.post(req_url, params=params, cookies=cookies)
        return json.loads(r.content).get('item_seller_get_response').get('item').get('wireless_desc')


if __name__ == '__main__':
    x = ItemDetail()
    watermark_anchor = ('and', (('attr=', ('text', '热门水印')),))
    locate_by_anchor(init_element(watermark_anchor), parent_lv=2, child_lv='v2l0').click()
