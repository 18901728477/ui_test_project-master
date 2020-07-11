from mobile.mitem_ui_test.mitem_ui_test.item_info import picture
from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import BasePage, poco, init_element, element_sendtext, sleep, \
    element_click
from mobile.mitem_ui_test.mitem_ui_test.pages.common_list_page import CommonList, UIObjectProxy
from mobile.mitem_ui_test.mitem_ui_test.pages.element_page import ElementPage


class ReleaseCommonMethods(BasePage):
    general_release = ('and', (('attr=', ('name', '普通发布')),))
    use_baby_as_template = ('and', (('attr=', ('name', '西遇女鞋2020新款夏季时尚粗花呢一字带搭扣珍珠平底凉鞋...')),))
    upload_pictures = ('and', (('attr=', ('name', 'android.widget.ImageView')),))
    image_space = ('and', (('attr=', ('name', '图片空间')),))
    baby_title = ('and', (('attr=', ('name', '宝贝标题:')),))
    input = ('and', (('attr=', ('text', '请输入宝贝标题')),))
    baby_category = ('and', (('attr=', ('name', '宝贝类目:')),))
    now_release = ('and', (('attr=', ('name', '立即发布')),))
    time_release = ('and', (('attr=', ('name', '定时发布')),))
    details_description = ('and', (('attr=', ('name', '详情描述')),))
    add_text = ('and', (('attr=', ('name', '添加文字')),))
    input_character = ('and', (('attr=', ('text', '请输入文字')),))
    in_warehouse_button = ('and', (('attr=', ('name', '放入仓库')),))
    back_homepage = ('and', (('attr=', ('name', '放入仓库')),))
    search01_locator = ('and', (('attr=', ('text', '搜索...')),))
    search02_locator = ('and', (('attr=', ('text', '搜索')),))
    restore_search_locator = ('and', (('attr=', ('text', '\ue917')),))
    search_by_keyword_locator = ('and', (('attr=', ('text', '关键词')),))
    search03_input_keyword = ('and', (('attr=', ('text', '请输入标题关键词搜索')),))

    # 方法: 进入发布宝贝编辑主页(判断是极速发布还是普通发布)
    def release_baby_edit(self, mode='fast'):
        poco(name='发布宝贝').wait_for_appearance(10)
        if mode == 'fast':
            poco(name='极速发布').click()
            init_element(self.use_baby_as_template).click()
        else:
            init_element(self.general_release).click()

    # 方法: 添加主图
    def add_main_pictures(self):
        init_element(self.upload_pictures).click()
        init_element(self.image_space).click()
        poco(name=picture).click()
        poco(name='完成').click()

    # 方法: 编辑宝贝标题
    def edit_baby_title(self):
        # 编辑宝贝标题
        init_element(self.baby_title).click()
        element_sendtext(self.input, '杯子')
        poco(name=' 确定 ').click()

    # 方法: 选择宝贝类目
    def choose_baby_category(self):
        init_element(self.baby_category).click()
        poco(name='家居饰品>>创意饰品>>搞怪杯子').click()
        poco(name='家居饰品>>创意饰品>>搞怪杯子').wait_for_appearance(5)

    # 方法: 输入一口价和数量
    def price_and_quantity(self):
        poco().click([0.1675925925925926, 0.29010416666666666])
        # 定位有问题...
        ElementPage().find_price().set_text('9')
        ElementPage().find_num().set_text('10')

    # 方法: 选择运费和模板
    def choose_freight_template(self):
        poco(name='运费:').click()
        poco(name='淘宝二手默认运费模板_上海').click()

    # 方法: 添加详情描述
    def add_details_description(self):
        init_element(self.details_description).click()
        init_element(self.add_text).click()
        element_sendtext(self.input_character, '纯手工制作')
        poco(name=' 确定 ').click()

    # 方法: 立即发布
    def immediately_release(self):
        init_element(self.now_release).click()

    # 方法: 放入仓库
    def in_the_warehouse(self):
        init_element(self.in_warehouse_button).click()

    # 方法: 定时发布
    def time_interval(self):
        init_element(self.time_release).click()
        # 设置时间
        poco(name='com.taobao.qianniu:id/wv_hour').swipe('up')
        poco(text='确认').click()

    # 方法: 发布成功断言
    def release_success(self):
        return poco(name='成功发布到仓库中！').exists()

    # 方法: 发布放入仓库中断言
    def in_warehouse_success(self):
        return poco(name='成功发布到仓库中！').exists()

    # 发布成功后下架
    def sold_out(self, keyword, element_for_wait: UIObjectProxy):
        does_item_search = True
        # init_element(self.back_homepage).click()
        poco(text='商品').click()
        if init_element(self.search01_locator).exists():
            init_element(self.search01_locator).click()
        else:
            init_element(self.restore_search_locator).click()
            init_element(self.search01_locator).click()
        sleep(1)
        # 输入搜索的关键字后，点击搜索
        poco(name='android.widget.EditText').set_text(keyword)
        element_click(self.search02_locator)
        try:
            sleep(3)  # 3秒sleep，搜索完成前，页面上存在的元素使显示等待无实际作用
            element_for_wait.wait_for_appearance(10)  # 列表搜索，10秒显示等待
        except:
            does_item_search = False
        return does_item_search


if __name__ == '__main__':
    ReleaseCommonMethods().sold_out(keyword='西遇女鞋', element_for_wait=poco(name='杯子'))
