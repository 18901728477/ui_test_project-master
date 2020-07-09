# -*- encoding=utf8 -*-
__author__ = 'xiaoxuan'

import pytest
from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import *
from mobile.mitem_ui_test.mitem_ui_test.conftest import *
from mobile.mitem_ui_test.mitem_ui_test.item_info import *
from mobile .mitem_ui_test.mitem_ui_test.pages.edit_pic_page import *
from mobile.mitem_ui_test.mitem_ui_test.pages.detail_page import *
from datetime import datetime
from mobile.mitem_ui_test.mitem_ui_test.utils import *


class TestDetailPage(BasePage):

    @allure.feature('详情页')
    @allure.story('详情页，可以正常编辑标题')
    @pytest.mark.p1
    def test_edit_title(self, go_detail_page_onsale_title_scan):
        """
        1.进入详情页
        2.编辑标题
        3.判断页面时显示的标题是否一致
        4.还原标题
        """
        detail_page = go_detail_page_onsale_title_scan
        new_title = '编辑后的标题'
        detail_page.edit_title(new_title)
        actual_title = detail_page.get_title()
        detail_page.edit_title(ITEM_EDIT_TITLE_ONSELA_TITLE)
        assert actual_title == new_title

    @allure.feature('详情页')
    @allure.story('详情页，可以正常跳转标题优化页面')
    @pytest.mark.p2
    @pytest.mark.skip(reason='bug:类目热搜词过多页面卡顿')
    def test_title_improve(self, go_detail_page_onsale_title_scan):
        """
         1.进入详情页
         2.点击标题检测图片，进入标题优化页
         3.一键优化标题并更新到淘宝
         4.返回详情页，还原标题
         5.判断标题是否实际更新
        :param go_detail_page_onsale_title_scan:
        :return:
        """
        detail_page = go_detail_page_onsale_title_scan
        title_improve_detail_page = detail_page.go_title_improve_page()
        title_improve_detail_page.one_click_improve()
        title_improve_detail_page.update_title_after_improve()
        BasePage().turn_back()
        actual_title = detail_page.get_title()
        detail_page.edit_title(ITEM_EDIT_TITLE_ONSELA_TITLE)
        assert actual_title != ITEM_EDIT_TITLE_ONSELA_TITLE, '跳转标题优化页面后，不能正常一键优化标题'

    @allure.feature('详情页')
    @allure.story('详情页，可以正常编辑图片')
    @pytest.mark.p2
    def test_edit_pic(self, go_detail_page_onsale_scan):
        """
        1.进入详情页
        2.进入编辑图片页面
        3.删除所有图片
        4.上传主图和长图后更新
        5.判断是否返回详情页
        :param go_detail_page_onsale_scan:
        :return:
        """
        detail_page = go_detail_page_onsale_scan
        edit_pic_page = detail_page.go_edit_pic_page()
        edit_pic_page.delete_all_pic()
        edit_pic_page.choose_pic_position(0)
        pic_zoom = edit_pic_page.go_pic_zoom()
        assert pic_zoom.enter_dict('商品自动化目录'), '有沙雕清过图片空间了'
        pic_zoom.choose_pic('我的图片4.jpg')
        pic_zoom.submit_pic()
        edit_pic_page.choose_pic_position(5)
        edit_pic_page.go_pic_zoom()
        pic_zoom.enter_dict('商品自动化目录')
        pic_zoom.choose_pic('长图.jpg')
        pic_zoom.submit_pic()
        edit_pic_page.update_pic()
        assert poco(text='基本信息').exists(), '主图、长图更新失败'

    @allure.feature('详情页')
    @allure.story('详情页，可以正常提交主图视频任务')
    @pytest.mark.p2
    def test_create_short_video(self, go_detail_page_onsale_scan):
        """
            1.进入详情页
            2.提交任务
            3.判断任务是否提交成功
        """
        detail_page = go_detail_page_onsale_scan
        assert detail_page.create_shortvideo(), '该宝贝的主图视频任务还在生成中，无法继续生成'
        does_task_start = True
        try:
            poco(textMatches='.视频正在生成中...').wait_for_appearance(5)  # 提交任务后返回详情页，5s显示等待
        except PocoTargetTimeout:
            does_task_start = False
        assert does_task_start, '详情页无法提交主图视频任务'

    @allure.feature('详情页')
    @allure.story('详情页，宝贝可以正常上下架，显示的下架时间也正确')
    @pytest.mark.p1
    def test_list_delist(self, go_detail_page_onsale_scan):
        """
        1.进入详情页,切换基本信息tab
        2.下架宝贝，判断是否下架成功，记录下架时间
        3.上架宝贝，判断是否上架成功 ，记录虚拟下架时间
        4.判断两次时间的时间差是否为7天
        :param go_detail_page_onsale_scan:
        :return:
        """
        detail_page = go_detail_page_onsale_scan
        detail_page.switch_tab(1)
        detail_page.list_delist_item()
        assert detail_page.get_item_status() == '仓库中', '宝贝下架失败'
        date1 = detail_page.get_delist_time()
        detail_page.list_delist_item()
        assert detail_page.get_item_status() == '出售中', '宝贝上架失败'
        date2 = detail_page.get_delist_time()
        date1_time = datetime.datetime.strptime(date1, '%Y-%m-%d %X')
        date2_time = datetime.datetime.strptime(date2, '%Y-%m-%d %X')
        assert (date2_time - date1_time).days == 7, '下架时间计算有误'

    @allure.feature('详情页')
    @allure.story('详情页，已售完宝贝，显示的状态正确')
    @pytest.mark.p2
    def test_soldout_status(self, go_detail_page_soldout_scan):
        """
        1.进入详情页,切换基本信息tab
        2.判断宝贝状态一栏，显示的按钮是否为"已售完"
        3.判断点击按钮没有反应
        :param go_detail_page_soldout_scan:
        :return:
        """
        detail_page = go_detail_page_soldout_scan
        detail_page.switch_tab(1)
        flag = True
        try:
            poco(text='已售完').wait_for_appearance(3)  # 已售完信息获取，3秒显示等待
        except PocoTargetTimeout:
            flag = False
        assert flag, '已售完状态显示异常'

        poco(text='已售完').click()
        try:
            poco(text='确定').wait_for_appearance(1)
            flag = False
        except PocoTargetTimeout:
            pass
        assert flag, '已售完按钮点击后，出现弹窗'

    @allure.feature('详情页')
    @allure.story('详情页，商家编码可以正常编辑')
    @pytest.mark.p2
    def test_edit_code(self, go_detail_page_onsale_scan):
        """
        1.进入详情页
        2.切换基本信息tab
        3.编辑商家编码
        4.判断编辑是否成功
        :param go_detail_page_onsale_scan:
        :return:
        """
        detail_page = go_detail_page_onsale_scan
        detail_page.switch_tab(1)
        item_code = get_current_time()  # 当前时间戳
        detail_page.edit_item_code(item_code)
        assert detail_page.get_item_code() == item_code, '商家编码，不能正常编辑'

    @allure.feature('详情页')
    @allure.story('详情页，属性页，“品牌”属性、多选属性、可选不可填属性，可以正常编辑')
    @pytest.mark.p2
    def test_edit_props_1(self, go_detail_page_onsale_scan):
        """
        1.进入详情页
        2.切换基本信息tab
        3.进入属性页面
        4.编辑“品牌”属性
        5.编辑“流行元素/工艺”多选属性
        6.编辑“面料”可选不可填属性
        7.点击保存返回
        8.再次进入属性页面，判断编辑是否生效
        :param go_detail_page_onsale_scan:
        :return:
        """
        detail_page = go_detail_page_onsale_scan
        detail_page.switch_tab(1)
        props_page = detail_page.go_item_property_page()
        poco(text='货号').wait_for_appearance(10)  # 跳转10秒显示等待
        # 编辑品牌属性
        except_props1 = props_page.edit_props_enum('品牌', {0: '004', 1: '007', 2: '0127'})
        # 编辑多选属性
        BasePage().page_swipe_buttom()
        props_page.edit_props_multi('流行元素/工艺', {0: '蝴蝶结', 1: '肩章', 2: '亮丝'})
        # 编辑可选不可填属性
        BasePage().page_swipe_buttom()
        except_props3 = props_page.edit_props_enum('面料', {0: '雪纺', 1: '羊皮', 2: '猪皮'})
        poco(text='保存').click()
        detail_page.go_item_property_page()
        BasePage().page_swipe_buttom()
        actual_props1 = props_page.get_props_value('品牌')
        actual_props2 = props_page.get_props_value('流行元素/工艺')
        actual_props3 = props_page.get_props_value('面料')
        assert actual_props1 == except_props1 and actual_props2 == '蝴蝶结,肩章,亮丝' and \
               actual_props3 == except_props3, '“品牌”属性、多选属性、可选不可填属性，无法正常编辑'

    @allure.feature('详情页')
    @allure.story('详情页，属性页，可填不可选属性、有格式要求的属性，可以正常编辑')
    @pytest.mark.p2
    @pytest.mark.skip(reason="bug：多个可编辑属性无法正常编辑")
    def test_edit_props_2(self, go_detail_page_format_props_scan):
        """
        1.进入详情页
        2.切换基本信息tab
        3.进入属性页面
        4.编辑“宽度”有格式要求的属性
        5.编辑“货号”可填不可选属性
        6.点击保存返回
        7.再次进入属性页面，判断编辑是否生效
        :param go_detail_page_format_props_scan:
        :return:
        """
        detail_page = go_detail_page_format_props_scan
        detail_page.switch_tab(1)
        props_page = detail_page.go_item_property_page()
        poco(text='宽度').wait_for_appearance(10)  # 跳转10秒显示等待
        # 编辑宽度属性
        except_props1 = props_page.edit_props_input('宽度', {0: '10.0cm', 1: '11.0cm', 2: '12.2cm'})
        # 编辑货号属性
        BasePage().page_swipe_buttom()
        except_props2 = props_page.edit_props_input('货号', {0: '货号001', 1: '货号002', 2: '货号003'})
        poco(text='保存').click()
        detail_page.go_item_property_page()
        actual_props1 = props_page.get_props_value('宽度')
        BasePage().page_swipe_buttom()
        actual_props2 = props_page.get_props_value('货号')
        assert actual_props1 == except_props1 and actual_props2 == except_props2, \
            '可填不可选属性、有格式要求的属性，无法正常编辑'

    @allure.feature('详情页')
    @allure.story('详情页，店铺分类，可以正常选择')
    @pytest.mark.p2
    def test_edit_shop_cat(self, go_detail_page_onsale_scan):
        """
        1.进入详情页
        2.切换基本信息tab
        3.点击店铺分类，清空所有选中项，保存
        4.判断分类是否正常取消
        5.再次点击店铺分类，勾选1个一级分类和1个二级分类，保存
        5.判断分类是否正常保存
        :param go_detail_page_onsale_scan:
        :return:
        """
        detail_page = go_detail_page_onsale_scan
        detail_page.switch_tab(1)
        detail_page.recover_shop_class()
        assert detail_page.get_shop_cat() == '未分类', '店铺分类不能正常取消全选'
        detail_page.choose_shop_class(class_level=0, class_dict={'一级分类': '一级分类00'})
        detail_page.choose_shop_class(class_level=1, class_dict={'一级分类': '一级分类01', '二级分类': '二级分类01'})
        assert detail_page.get_shop_cat() == '一级分类00/二级分类01', '店铺分类不能正常选择'

    @allure.feature('详情页')
    @allure.story('详情页，运费模板可以正常编辑')
    @pytest.mark.p2
    def test_edit_delivery(self, go_detail_page_onsale_scan):
        """
        1.进入详情页
        2.切换基本信息tab
        3.点击运费模板，选择国内模板
        4.判断运费模板、宝贝所在地是否更新成功
        5.再次点击运费模板，选择海外模板
        6.判断接口是否报错
        :param go_detail_page_onsale_scan:
        :return:
        """
        detail_page = go_detail_page_onsale_scan
        detail_page.switch_tab(1)
        detail_page.change_delivery_template('我的模板1')
        does_api_fail = True
        if poco(text='确定').exists():
            poco(text='确定').click()
            does_api_fail = False
        assert does_api_fail, '更换运费模板时接口报错'
        assert poco(text='我的模板1').exists() and poco(text='上海上海杨浦').exists(), '编辑运费模板后，信息没有更新成功'
        detail_page.change_delivery_template('海外模板')
        assert poco(textMatches='.*【发货地】为【国内】时.*').exists(), '选择海外模板时，没有报错'
        poco(text='确定').click()

    @allure.feature('详情页')
    @allure.story('详情页，其他信息可以正常编辑')
    @pytest.mark.p2
    def test_edit_other_info(self, go_detail_page_onsale_scan):
        """
        1.进入详情页
        2.切换基本信息tab
        3.编辑其他信息
        4.判断是否编辑成功
        :param go_detail_page_onsale:
        :return:
        """
        detail_page = go_detail_page_onsale_scan
        detail_page.switch_tab(1)
        BasePage().page_swipe_buttom()
        detail_page.edit_other_info(guarantee=1, invoice=0, store_cal=1)
        assert detail_page.get_other_info().get(0) == '有' and detail_page.get_other_info().get(1) == '无' and \
               detail_page.get_other_info().get(2) == '付款减库存', '其他信息无法正常编辑'

    @allure.feature('详情页')
    @allure.story('详情页，可以正常提交手机详情任务')
    @pytest.mark.p1
    def test_submit_mdetail_task(self, go_detail_page_inventory_scan):
        """
        1.进入详情页
        2.切换手机详情tab
        3.提交任务
        4.判断任务是否提交成功
        :param go_detail_page_inventory_scan:
        :return:
        """
        detail_page = go_detail_page_inventory_scan
        detail_page.switch_tab(3)
        detail_page.create_mdetail()
        assert poco(textMatches='.*生成中.*').exists(), '手机详情任务提交成功'

    @allure.feature('详情页')
    @allure.story('详情页，出售中宝贝，底部吸底按钮显示正常，并能正常跳转')
    @pytest.mark.p2
    def test_onsale_buttom_button(self, go_detail_page_onsale_scan):
        """
        1.进入出售中sku宝贝的详情页
        2.判断主图/视频tab下的按钮显示正常
        3.判断按钮可以正常点击
        4.切换销售规格tab，判断按钮是否显示正常
        5.判断按钮可以正常点击，增删规格可以正常跳转使用
        :return:
        """
        detail_page = go_detail_page_onsale_scan
        button_list = detail_page.get_buttom_button()
        assert button_list == ['查看宝贝', '分享推广', '复制链接'], '出售中宝贝，底部吸底按钮数量异常'
        assert detail_page.check_watch_item(ITEM_ONSALE_TITLE), '出售中宝贝，查看宝贝无法正常跳转'
        assert detail_page.check_copy_link(), '出售中宝贝，宝贝链接无法正常复制'
        detail_page.switch_tab(2)
        button_list = detail_page.get_buttom_button()
        assert button_list == ['查看宝贝', '增删规格', '复制链接'], '出售中sku宝贝，销售规格tab，底部吸底按钮数量异常'
        assert detail_page.check_watch_item(ITEM_ONSALE_TITLE), '出售中sku宝贝，销售规格tab，查看宝贝无法正常跳转'
        assert detail_page.check_add_delete_sku_prop(ITEM_ONSALE_TITLE), '出售中sku宝贝，销售规格tab，增删规格无法正常跳转'

    @allure.feature('详情页')
    @allure.story('详情页，仓库中宝贝，底部吸底按钮显示正常')
    @pytest.mark.p2
    def test_inventory_buttom_button(self, go_detail_page_inventory_scan):
        """
        1.进入仓库中无sku宝贝的详情页
        2.判断主图/视频tab下的按钮显示正常
        3.判断按钮可以正常点击
        4.切换销售规格tab，判断按钮是否显示正常
        5.切换基本信息tab，判断按钮是否显示正常
        :return:
        """
        detail_page = go_detail_page_inventory_scan
        button_list = detail_page.get_buttom_button()
        assert button_list == ['查看宝贝', '删除宝贝', '复制链接'], '仓库中宝贝，底部吸底按钮数量异常'
        assert detail_page.check_watch_item(ITEM_INVENTORY_TITLE), '仓库中宝贝，查看宝贝无法正常跳转'
        assert detail_page.check_copy_link(), '仓库中宝贝，宝贝链接无法正常复制'
        detail_page.switch_tab(2)
        button_list = detail_page.get_buttom_button()
        assert button_list == ['查看宝贝', '复制链接'], '出售中sku宝贝，销售规格tab，底部吸底按钮数量异常'
        assert detail_page.check_watch_item(ITEM_INVENTORY_TITLE), '出售中sku宝贝，销售规格tab，查看宝贝无法正常跳转'

    @allure.feature('详情页')
    @allure.story('详情页，活动日历、店铺体检跳转')
    @pytest.mark.p1
    def test_activity_calendar(self, go_detail_page_inventory_scan):
        assert go_detail_page_inventory_scan.activity_calendar_shop_test_enter()

    @allure.feature('详情页')
    @allure.story('详情页，添加、删除水印')
    @pytest.mark.p1
    @pytest.mark.skip(reason='bug：促销水印，第一个热门水印无法正常跳转')
    def test_add_delete_watermark(self, go_detail_page_onsale_scan):
        assert go_detail_page_onsale_scan.add_delete_watermark(), '水印任务没有成功发起，或者任务耗时异常，请检查后端水印队列'

    @allure.feature('详情页')
    @allure.story('详情页，有sku宝贝，sku价格库存可以正常编辑')
    @pytest.mark.p1
    def test_edit_sku(self, go_detail_page_onsale_scan):
        """
        1.进入详情页
        2.切换销售规格tab
        3.编辑sku
        4.判断一口价、总库存是否更新
        :param go_detail_page_onsale:
        :return:
        """
        detail_page = go_detail_page_onsale_scan
        detail_page.switch_tab(2)
        BasePage().page_swipe_buttom()
        origin_price = detail_page.get_fixed_price()
        origin_store = detail_page.get_store()
        detail_page.edit_price_store(index=0, my_price=str(int(float(origin_price)) + 3),
                                     my_store=str(int(int(origin_store) / 3 + 1)))
        detail_page.edit_price_store(index=1, my_price=str(int(float(origin_price)) + 2),
                                     my_store=str(int(int(origin_store) / 3 + 1)))
        detail_page.edit_price_store(index=2, my_price=str(int(float(origin_price)) + 1),
                                     my_store=str(int(int(origin_store) / 3 + 1)))
        assert detail_page.get_fixed_price() != origin_price and detail_page.get_store() != origin_store, \
            'sku更新实际失败'

    @allure.feature('详情页')
    @allure.story('详情页，有sku宝贝，一口价可以正常选择')
    @pytest.mark.p2
    def test_edit_fixed_price_with_sku(self, go_detail_page_onsale_scan):
        """
        1.进入详情页
        2.切换销售规格tab
        3.获取第一个sku的价格
        4.一口价更换成第一个sku的价格
        5.判断一口价是否更换成功
        6.还原一口价
        :param go_detail_page_onsale:
        :return:
        """
        detail_page = go_detail_page_onsale_scan
        detail_page.switch_tab(2)
        origin_price = detail_page.get_fixed_price()
        first_price = get_text_of_view(locate_by_anchor(poco(text='价格：'), 1, 'l1'))
        print(first_price)
        detail_page.change_fixed_price(first_price)
        assert detail_page.get_fixed_price() == first_price
        detail_page.change_fixed_price(origin_price)

    @allure.feature('详情页')
    @allure.story('详情页，无sku宝贝，一口价、库存可以正常编辑')
    @pytest.mark.p1
    def test_edit_fixed_price_without_sku(self, go_detail_page_inventory_scan):
        """
        1.进入详情页
        2.切换销售规格tab
        3.编辑一口价、库存
        4.判断编辑是否生效
        :param go_detail_page_inventory_scan:
        :return:
        """
        detail_page = go_detail_page_inventory_scan
        detail_page.switch_tab(2)
        edit_price = str(int(float(detail_page.get_fixed_price())) + 1)
        edit_store = str(int(detail_page.get_store()) + 1)
        detail_page.edit_price_store(index=0, my_price=edit_price, my_store=edit_store)
        assert detail_page.get_fixed_price() == edit_price and detail_page.get_store() == edit_store, \
            '无sku宝贝一口价库存无法正常编辑'

    @allure.feature('详情页')
    @allure.story('详情页，可以正常编辑手机详情')
    @pytest.mark.p1
    def test_edit_mdetail(self, go_detail_page_onsale_scan):
        """
        1.进入出售中宝贝详情页
        2.切换手机详情tab
        3.进入编辑模式
        4.插入时间戳文本、图片后提交编辑
        5.调用api获取最新详情后，还原编辑
        6.判断编辑是否生效
        :param go_detail_page_onsale_scan:
        :return:
        """
        detail_page = go_detail_page_onsale_scan
        detail_page.switch_tab(3)
        insert_word = get_current_time()
        detail_page.edit_mdetail_add_word(insert_word)
        detail_page.edit_mdetail_add_pic()
        new_mdetail_from_api = detail_page.tb_api_get_item_mdetail('615055673244')
        detail_page.restore_mdetail()
        assert insert_word in new_mdetail_from_api and '<img>' in new_mdetail_from_api, '文字和图片的编辑实际没有生效！'
