import time

from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import element_click, init_element, locate_by_anchor, BasePage, \
    poco, element_sendtext, get_text_of_view, get_child_by_index, touch, Template, text, PocoNoSuchNodeException, \
    PocoTargetTimeout
from mobile.mitem_ui_test.mitem_ui_test.pages.common_list_page import CommonList
from mobile.mitem_ui_test.mitem_ui_test.pages.element_page import ElementPage
from mobile.mitem_ui_test.mitem_ui_test.pages.release_common_methods import ReleaseCommonMethods


class ReleasePage(BasePage):
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
    release_common = ReleaseCommonMethods()

    # 方法：普通发布--发布宝贝成功--只填写必填信息(bug)
    def release_baby_success(self):
        # 普通发布
        self.release_common.release_baby_edit(1)
        # 添加主图
        self.release_common.add_main_pictures()
        # 编辑宝贝标题
        self.release_common.edit_baby_title()
        # 选择宝贝类目
        self.release_common.choose_baby_category()
        # 滑至底部
        BasePage().page_swipe_buttom02()
        # 一口价和数量
        self.release_common.price_and_quantity()
        poco(name='确定').click()  # (bug,点击确定按钮,提示错误)
        # 运费
        self.release_common.choose_freight_template()
        # 上滑至顶部
        self.page_swipe_top_release()
        # 详情描述
        self.release_common.add_details_description()
        # 立即发布
        self.release_common.immediately_release()
        # 断言发布成功
        return self.release_common.release_success()

    # 方法: 普通发布--发布宝贝失败--商家无该类目权限
    # def no_pictures(self):
    #     # 进入普通发布
    #     self.releasecommon.release_baby_edit(1)
    #     # 编辑宝贝标题
    #     init_element(self.baby_title).click()
    #     element_sendtext(self.input, '矿泉水')
    #     poco(name=' 确定 ').click()
    #     # 方法: 选择宝贝类目
    #     init_element(self.baby_category).click()
    #     poco(name='盒马>>水饮料>>水>>矿泉水').click()
    #     poco(name='盒马>>水饮料>>水>>矿泉水').wait_for_appearance(5)
    #     # 类目必填属性
    #     poco(name='包装:').click()
    #     poco(name='*').click()
    #     poco(name='瓶装').click()
    #     poco(name='是否含气:').click()
    #     poco(name='否').click()
    #     poco(name='确定').click()
    #     # 滑至底部
    #     BasePage().page_swipe_buttom02()
    #     poco().click([0.1675925925925926, 0.29010416666666666])
    #     # 定位有问题...
    #     ElementPage().find_price().set_text('9')
    #     ElementPage().find_num().set_text('10')
    #     # 点击确定按钮
    #     poco(name='确定').click()
    #     poco(name='运费:').click()
    #     poco(name='不包邮北京19091610073374492').click()
    #     # 上滑至顶部
    #     self.page_swipe_top_release()
    #     init_element(self.details_description).click()
    #     init_element(self.add_text).click()
    #     element_sendtext(self.input_character, '健康好喝...')
    #     poco(name=' 确定 ').click()
    #     init_element(self.now_release).click()
    #     try:
    #         poco(name='成功发布到出售中!').wait_for_appearance(5)
    #         print(poco(name='成功发布到出售中!'))
    #     except PocoTargetTimeout:
    #         return False

    # 方法：发布宝贝失败--价格和库存不填--失败
    def no_price_num(self):
        # 普通发布
        self.release_common.release_baby_edit(1)
        # 添加主图
        self.release_common.add_main_pictures()
        # 编辑宝贝标题
        self.release_common.edit_baby_title()
        # 选择宝贝类目
        self.release_common.choose_baby_category()
        # 滑至底部
        BasePage().page_swipe_buttom02()
        # 运费
        self.release_common.choose_freight_template()
        # 上滑至顶部
        self.page_swipe_top_release()
        # 详情描述
        self.release_common.add_details_description()
        # 立即发布
        self.release_common.immediately_release()
        try:
            poco(name='成功发布到出售中！').wait_for_appearance(5)
            print(poco(name='成功发布到出售中！'))
        except PocoTargetTimeout:
            return False

    # 极速发布宝贝--添加主图--成功
    def speed_post_success(self):
        # 进入极速发布
        self.release_common.release_baby_edit(0)
        # 添加主图
        self.release_common.add_main_pictures()
        # 立即发布
        self.release_common.immediately_release()
        release_text = self.release_common.release_success()
        return release_text

    # 极速发布--定时发布宝贝
    def time_release_baby(self):
        # 进入极速发布
        self.release_common.release_baby_edit(0)
        # 添加主图
        self.release_common.add_main_pictures()
        # 定时发布
        self.release_common.time_interval()
        # 断言发布成功
        return self.release_common.release_success()

    # 极速发布--宝贝放入仓库
    def baby_in_warehouse(self):
        # 进入极速发布
        self.release_common.release_baby_edit(0)
        # 添加主图
        self.release_common.add_main_pictures()
        # 放入仓库
        self.release_common.in_the_warehouse()
        # 断言成功发布到仓库
        return self.release_common.in_warehouse_success()


if __name__ == '__main__':
    ReleasePage().baby_in_warehouse()
