from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import element_click, init_element, locate_by_anchor, BasePage, \
    poco, element_sendtext, get_text_of_view, get_child_by_index, touch, Template, text, PocoNoSuchNodeException, \
    PocoTargetTimeout, super_click
from mobile.mitem_ui_test.mitem_ui_test.pages.common_list_page import CommonList
from mobile.mitem_ui_test.mitem_ui_test.pages.release_common_methods import ReleaseCommonMethods


class ReleasePage(ReleaseCommonMethods):
    baby_title = ('and', (('attr=', ('name', '宝贝标题:')),))
    baby_category = ('and', (('attr=', ('name', '宝贝类目:')),))
    details_description = ('and', (('attr=', ('name', '详情描述')),))
    add_text = ('and', (('attr=', ('name', '添加文字')),))
    input = ('and', (('attr=', ('text', '请输入宝贝标题')),))
    num = ('and', (('attr=', ('name', '数量:')),))
    input_character = ('and', (('attr=', ('text', '请输入文字')),))
    ISBN = ('and', (('attr=', ('name', 'ISBN编号:')),))
    fixed_price = ('and', (('attr=', ('name', '价格:')),))
    now_release = ('and', (('attr=', ('name', '立即发布')),))
    merchandise = ('and', (('attr=', ('name', '商品')),))

    # 方法：发布宝贝成功--填写必填信息
    def release_baby_success(self):
        # 添加主图
        self.add_main_pictures()
        # 编辑宝贝标题
        self.edit_baby_title()
        # 选择宝贝类目
        self.choose_baby_category()
        # 添加年份季节
        self.add_year_season()
        # 一口价和数量
        self.price_and_quantity()
        # BasePage().page_swipe_buttom02()
        # # 运费
        # self.release_common.choose_freight_template()
        # # 详情描述
        # self.release_common.add_details_description()
        # # 采购地和店铺分类
        # self.release_common.place_and_store_category()
        # 立即发布
        self.immediately_release()
        # 断言发布成功
        return self.release_success()

    # 发布宝贝--放入仓库成功
    def in_warehouse_success(self):
        # 添加主图
        self.add_main_pictures()
        # 编辑宝贝标题
        self.edit_baby_title()
        # 选择宝贝类目
        self.choose_baby_category()
        # 添加年份季节
        self.add_year_season()
        # 一口价和数量
        self.price_and_quantity()
        # BasePage().page_swipe_buttom02()
        # # 运费
        # self.choose_freight_template()
        # # 详情描述
        # self.add_details_description()
        # # 采购地和店铺分类
        # self.release_common.place_and_store_category()
        # 放入仓库
        self.in_the_warehouse()
        # 断言发布成功
        return self.in_warehouse_success()

    # 发布宝贝--定时发布成功
    def time_interval_success(self):
        # 添加主图
        self.add_main_pictures()
        # 编辑宝贝标题
        self.edit_baby_title()
        # 选择宝贝类目
        self.choose_baby_category()
        # 添加年份季节
        self.add_year_season()
        # 一口价和数量
        self.price_and_quantity()
        # BasePage().page_swipe_buttom02()
        # # 运费
        # self.choose_freight_template()
        # # 详情描述
        # self.add_details_description()
        # # 采购地和店铺分类
        # self.place_and_store_category()
        # 定时发布
        self.time_interval()
        return self.in_warehouse_success()

    # 发布宝贝--无sku宝贝发布成功
    def no_sku_success(self):
        # 添加主图
        self.add_main_pictures()
        # 编辑宝贝标题
        self.edit_baby_title()
        # 选择宝贝类目
        self.choose_baby_category()
        # 添加年份季节
        self.add_year_season()
        # 一口价和数量

        # BasePage().page_swipe_buttom02()
        # 运费
        # self.choose_freight_template()
        # # 详情描述
        # self.add_details_description()
        # 采购地和店铺分类
        # self.place_and_store_category()
        # 立即发布
        self.immediately_release()
        # 断言发布成功
        return self.release_success()

    # 方法: 发布宝贝--不添加主图(必填信息)
    def no_pictures(self):
        # 编辑宝贝标题
        self.edit_baby_title()
        # 选择宝贝类目
        self.choose_baby_category()
        # 滑至底部
        BasePage().page_swipe_buttom02()
        # 一口价和数量
        self.price_and_quantity()
        confirm_button = poco(name='确定')
        confirm_button.click()
        # 运费
        self.choose_freight_template()
        # 上滑至顶部
        self.page_swipe_top_release()
        # 详情描述
        self.add_details_description()
        # 立即发布
        self.immediately_release()

        try:
            poco(name='成功发布到出售中').wait_for_appearance(5)
            print(poco(name='成功发布到出售中'))
        except PocoTargetTimeout:
            return False

    # 方法：发布宝贝失败--价格和库存不填--失败
    def no_price_num(self):
        # 添加主图
        self.add_main_pictures()
        # 编辑宝贝标题
        self.edit_baby_title()
        # 选择宝贝类目
        self.choose_baby_category()
        # 添加年份季节
        self.add_year_season()
        # 滑至底部
        BasePage().page_swipe_buttom02()
        # 运费
        self.choose_freight_template()
        # 店铺分类

        # 上滑至顶部
        self.page_swipe_top_release()
        # 详情描述
        self.add_details_description()
        # 立即发布
        self.immediately_release()

        try:
            poco(name='成功发布到出售中').wait_for_appearance(5)
            print(poco(name='成功发布到出售中 '))
        except PocoTargetTimeout:
            return False



if __name__ == '__main__':
    ReleasePage().release_baby_success()
