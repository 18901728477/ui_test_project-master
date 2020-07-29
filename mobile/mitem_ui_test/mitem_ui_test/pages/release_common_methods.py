from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import BasePage, poco, init_element, element_sendtext, sleep, \
    element_click, locate_by_anchor, does_element_exists
from mobile.mitem_ui_test.mitem_ui_test.pages.common_list_page import CommonList, UIObjectProxy


class ReleaseCommonMethods(BasePage):
    upload_pictures_locator = ('and', (('attr=', ('text', '上传图片')),))
    local_album_locator = ('and', (('attr=', ('text', '本地相册')),))
    baby_title_locator = ('and', (('attr=', ('text', '宝贝标题')),))
    baby_category_locator = ('and', (('attr=', ('text', '宝贝类目')),))
    now_release_locator = ('and', (('attr=', ('text', '立即发布')),))
    time_release_locator = ('and', (('attr=', ('text', '定时发布')),))
    details_description_locator = ('and', (('attr=', ('text', '详情描述')),))
    add_text_locator = ('and', (('attr=', ('text', '添加文字')),))
    input_character_locator = ('and', (('attr=', ('text', '请输入文字')),))
    in_warehouse_locator = ('and', (('attr=', ('text', '放入仓库')),))
    search01_locator = ('and', (('attr=', ('text', '请输入搜索关键词')),))
    search02_locator = ('and', (('attr=', ('text', '搜索')),))
    picture_locator = ('and', (('attr=', ('name', 'com.taobao.qianniu:id/media_check')),))
    sure_locator = ('and', (('attr=', ('name', 'com.taobao.qianniu:id/ensure')),))
    year_season_locator = ('and', (('attr=', ('text', '年份季节')),))
    baby_attribute_locator = ('and', (('attr=', ('text', '宝贝属性')),))
    save_locator = ('and', (('attr=', ('text', '保存')),))
    fixed_price_locator = ('and', (('attr=', ('text', '一口价')),))
    choose_color_locator = ('and', (('attr=', ('text', '选择颜色')),))
    sure2_locator = ('and', (('attr=', ('text', '确定')),))
    article_number_locator = ('and', (('attr=', ('text', '货号')),))
    choose_size_locator = ('and', (('attr=', ('text', '选择尺码')),))
    freight_locator = ('and', (('attr=', ('text', '运费模板')),))
    basic_information_locator = ('and', (('attr=', ('text', '基本信息')),))
    place_locator = ('and', (('attr=', ('text', '采购地')),))
    store_category_locator = ('and', (('attr=', ('text', '店铺分类')),))

    # 方法: 添加主图
    def add_main_pictures(self):
        # 从本地相册添加5张图片
        init_element(self.upload_pictures_locator).click()
        init_element(self.local_album_locator).click()
        init_element(self.picture_locator)[0].click()
        init_element(self.picture_locator)[1].click()
        init_element(self.picture_locator)[2].click()
        init_element(self.picture_locator)[3].click()
        init_element(self.picture_locator)[4].click()
        init_element(self.sure_locator).click()

    # 方法: 编辑宝贝标题
    def edit_baby_title(self):
        locate_by_anchor(init_element(self.baby_title_locator), 2, 'v1v0v0v0v0').set_text('女装,发布宝贝测试用')

    # 方法: 选择宝贝类目(存在sku)
    def choose_baby_category(self):
        # 输入关键词搜索,选中女装类目
        init_element(self.baby_category_locator).click()
        sleep(5)
        ReleaseCommonMethods().search_keyword('女装/女士精品>>连衣裙', poco(text="女装/女士精品>>连衣裙"))
        locate_by_anchor(poco(text="保证金1000/订单险/账期保障"), 1, 'l0').click()

    # 添加年份季节(宝贝类目存在必填属性,自定义属性)
    def add_year_season(self):
        init_element(self.year_season_locator).wait_for_appearance(8)
        init_element(self.year_season_locator).click()
        # 显性等待跳转到宝贝属性页面
        init_element(self.baby_attribute_locator).wait_for_appearance(8)
        init_element(self.year_season_locator).click()
        poco(text="2016年冬季").click()
        init_element(self.article_number_locator).wait_for_appearance(8)
        locate_by_anchor(init_element(self.article_number_locator), 2, 'l1l0l0').set_text('00123')
        init_element(self.save_locator).click()

    # 方法: 输入sku
    def price_and_quantity(self):
        poco('android.widget.RelativeLayout').swipe('down')
        # BasePage().page_swipe_buttom02()
        init_element(self.fixed_price_locator).click()
        poco(text='设置规格').wait_for_appearance(8)
        # 选择尺码
        init_element(self.choose_size_locator).click()
        poco(text="145/52A").click()
        poco(text="155/60A").click()
        poco(text='确定').click()
        init_element(self.choose_size_locator).invalidate()
        # 选择颜色
        sleep(3)
        init_element(self.choose_color_locator).click()
        poco(text="乳白色").click()
        poco(text="米白色").click()
        init_element(self.sure2_locator).click()
        # 批量填充价格和库存
        poco(text="批量填充").invalidate()
        poco(text="批量填充").click()
        locate_by_anchor(poco(text='价格'), 1, 'l1l0l0').set_text('10000000')
        locate_by_anchor(poco(text='库存'), 1, 'l1l0l0').set_text('999')
        poco(text="确认").click()
        poco(text="确定").click()

    # 方法: 选择运费和模板
    def choose_freight_template(self):

        init_element(self.freight_locator).click()
        poco(text="我的模板1").click()
        poco(text="确认").click()

    # 方法: 添加详情描述
    def add_details_description(self):
        init_element(self.details_description_locator).click()
        init_element(self.add_text_locator).click()
        locate_by_anchor(poco(text='取消'), 2, 'v0v0v0v0').set_text('发布宝贝测试,不发货不发货不发货不发货不发货......')
        poco(text="确定").click()

    # 设置采购地和店铺分类
    def place_and_store_category(self):
        # 切换回基本信息
        init_element(self.basic_information_locator).click()
        BasePage().page_swipe_buttom()
        # init_element(self.place_locator).click()
        init_element(self.store_category_locator).click()
        locate_by_anchor(poco(text="一级分类00"), 2, 'l0l0').click()
        poco(text="确定").click()

    # 方法: 立即发布
    def immediately_release(self):
        init_element(self.now_release_locator).click()

    # 方法: 放入仓库
    def in_the_warehouse(self):
        init_element(self.in_warehouse_locator).click()

    # 方法: 定时发布
    def time_interval(self):
        init_element(self.time_release_locator).click()

    # 方法: 发布成功断言
    def release_success(self):
        return poco(text='成功发布到出售').exists()

    # 方法: 发布放入仓库中断言
    def in_warehouse_success(self):
        return poco(text='成功发布到仓库中').exists()

    # 下架宝贝
    # def sold_out(self, keyword, element_for_wait):
    #     # poco(name='com.taobao.qianniu:id/triver_tab_image').click()
    #     CommonList().search_by_keyword(keyword, element_for_wait)

    # 关键词搜索(搜索类目)
    def search_keyword(self, keyword, element):
        does_item_search = True
        # 输入搜索的关键字后，点击搜索
        poco(name='android.widget.EditText').set_text(keyword)
        element_click(self.search02_locator)
        try:
            sleep(3)  # 3秒sleep，搜索完成前，页面上存在的元素使显示等待无实际作用
            element.wait_for_appearance(10)  # 列表搜索，10秒显示等待
        except:
            does_item_search = False
        return does_item_search


if __name__ == '__main__':
    ReleaseCommonMethods().price_and_quantity()
