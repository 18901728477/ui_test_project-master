import allure
import pytest
from airtest.core.api import *

from mobile.mtrade_ui_test.mtrade_ui_test.data import WAIT_SELLER_SEND_GOODS_COMBINE, WAIT_BUYER_CONFIRM_GOODS
from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import ay_exists, get_order_detail
from mobile.mtrade_ui_test.mtrade_ui_test.pages.first_page import *


# 需要数据 WAIT_SELLER_SEND_GOODS/WAIT_SELLER_SEND_GOODS_WITH_PRINT_HISTORY/WAIT_SELLER_SEND_GOODS_COMBINE
class TestWaitSellerSendGoods(BasePage):

    @allure.feature('待发货订单列表')
    @allure.story('有绑定单号的订单，列表显示打印记录')
    def test_check_order_with_print_history(self, wait_seller_send_goods_with_print_history):
        """
        pass
        1.进入列表页，搜索出一笔有打印记录的订单
        2.校验是否存在打印信息一栏
        :param wait_seller_send_goods_with_print_history: fixture
        """
        res = wait_seller_send_goods_with_print_history.check_order_print_history()
        assert res, '订单有历史打印记录，但页面上没有显示'

    @allure.feature('待发货订单列表')
    @allure.story('没有绑定单号的订单，列表不显示打印记录一项')
    def test_check_order_without_print_history(self, wait_seller_send_goods):
        """
        1.进入列表页，搜索出一笔无打印记录的订单
        2.无打印记录时，页面不显示打印记录相关信息
        :param wait_seller_send_goods: fixture
        """
        res = wait_seller_send_goods.check_order_print_history()
        assert not res, '订单无历史打印记录，列表页不应该显示历史打印的相关信息'

    @allure.feature('待发货订单列表')
    @allure.story('合单订单，显示的订单状态应为待发货合单,并且存在取消合单按钮')
    def test_combining_order_status(self, wait_seller_send_goods_combine):
        """
        1.进入列表页，搜索出一笔合单
        2.校验列表页的合单，订单状态是否为 待发货合单
        :param wait_seller_send_goods_combine:
        :return:
        """
        res = wait_seller_send_goods_combine.is_combine()
        assert res[0] == '待发货合单', '预期状态：待发货合单，实际状态：{}'.format(res[0])
        assert res[1], '页面上没有显示取消合单按钮'
        assert res[2], '页面上没有显示参与合单的订单数量'

    @allure.feature('发货页面')
    @allure.story('普通订单,发货页面的订单信息正确')
    # @pytest.mark.skip(reason='发货页没设计完成')
    def test_check_order_detail_deliver_normal_order(self, wait_seller_send_goods):
        """
        1.进入列表页，搜索出一笔普通订单
        2.点击发货按钮，进入发货页面面
        3.校验发货页面面的订单信息
        :param wait_seller_send_goods: fixture
        """
        res = wait_seller_send_goods.check_order_info()
        assert res[0], '发货页面，普通订单信息有误{}'.format(res[1])

    @allure.feature('发货页面')
    @allure.story('购物车订单,发货页面的订单信息正确')
    @pytest.mark.skip(reason='发货页没设计完成')
    def test_check_order_detail_deliver_shopping_cart_order(self, wait_seller_send_goods_cart):
        """
        1.进入列表页，搜索出一笔购物车订单
        2.点击发货按钮，进入发货页面面
        3.校验发货页面面的订单信息
        :param wait_seller_send_goods_cart: fixture
        """
        res = wait_seller_send_goods_cart.check_order_info_cart()
        assert res[0], '发货页面，购物车订单信息有误{}'.format(res[1])

    @allure.feature('发货页面')
    @allure.story('合单订单,发货页面的订单信息正确')
    @pytest.mark.skip(reason='发货页没设计完成')
    def test_check_order_detail_deliver_combining_order(self, send_goods_combine):
        """
        1.进入列表页，搜索出一笔合并订单
        2.点击发货按钮，进入发货页面面
        3.校验发货页面面的订单信息
        :param send_goods_combine: fixture
        """
        deliver_page = send_goods_combine
        res1 = deliver_page.check_order_detail_deliver(WAIT_SELLER_SEND_GOODS_COMBINE[0])
        res2 = deliver_page.check_order_detail_deliver(WAIT_SELLER_SEND_GOODS_COMBINE[1])
        assert res1[0] and res2[0], '发货页面，合单订单信息有误！第一笔订单校验结果：{},第二笔订单校验结果：{}'.format(res1[1], res2[1])

    @allure.feature('发货页面')
    @allure.story('发货页面，有历史打印记录的订单，快递公司、物流单号的默认绑定正确')
    def test_deliver_page_check_order_with_print_history(self, send_goods_with_print_history):
        """
        1.进入列表页，搜索出一笔有历史打印记录的订单
        2.点击发货按钮，进入发货页面面
        3.校验发货页面面的快递公司、物流单号的默认绑定
        :return:
        """
        res = send_goods_with_print_history.check_order_print_history()
        assert res[0], '发货页面,有历史打印记录的订单，快递公司、物流单号的默认绑定异常，快递公司预期：{}，实际：{}；物流单号预期：{}，实际：{}'.format(res[1], res[2],
                                                                                                 res[3], res[4])

    @allure.feature('发货页面')
    @allure.story('发货页面，无历史打印的订单，物流单号默认为空')
    def test_deliver_page_check_order_without_print_history(self, send_goods_without_print_history):
        """
        1.进入列表页，搜索出一笔无历史打印记录的订单
        2.点击发货按钮，进入发货页面面
        3.校验发货页面面的物流单号默认为空
        :return:
        """
        res = send_goods_without_print_history.check_order_print_history()
        assert res[0] and res[4] == '', '发货页面，无历史打印的订单，物流单号默认值异常，应该为空,实际是{}！'.format(res[3])

    @allure.feature('发货页面')
    @allure.story('无需物流，可以正常发货')
    # @pytest.mark.skip(reason="避免消耗所有订单数据")
    def test_send_goods_without_logsitics(self, send_goods):
        """
        1.进入列表页，搜索出一笔订单
        2.点击发货按钮，进入发货页面面
        3.选择无需物流
        4.点击立即发货按钮，成功返回列表页
        :return:
        """
        send_goods.without_contact()
        deliver_page.push_deliver_button()
        assert ay_exists(my_list.order_status_anchor), '点击立即发货后，没有发货成功！'

    @allure.feature('修改地址页')
    @allure.story('清空地址后，一键填充地址')
    def test_one_click_enter_address(self, wait_seller_send_goods):
        """
        1.进入列表页，搜索出一笔订单
        2.点击修改地址按钮，进入修改地址页面
        3.清空地址
        4.一键填入新地址后，点击确定保存
        5.接口获取地址校验
        6.复原地址
        """
        ORIGINAL_ADDRESS = '顾超，18621729133，上海，上海市，宝山区， 高境镇 新二路55号皇冠，201900'
        ORIGINAL_ADDRESS_FROM_API = get_order_detail(WAIT_BUYER_CONFIRM_GOODS_ORDER)
        MODIFY_ADDRESS = '小高，13001356923，上海，上海市，杨浦区， 长白新村56号皇冠，201112'
        my_list = wait_seller_send_goods
        modify_address = my_list.go_to_modify_address()
        modify_address.clear_address()
        modify_address.one_click_fill_address(MODIFY_ADDRESS)
        MODIFY_ADDRESS_FROM_API = get_order_detail(WAIT_BUYER_CONFIRM_GOODS_ORDER)
        flag = True
        for x in ['收件人姓名', '收件人手机', '收件地址']:
            if ORIGINAL_ADDRESS_FROM_API[x] == MODIFY_ADDRESS_FROM_API[x]:
                flag = False
        # 地址复原
        my_list.go_to_modify_address()
        modify_address.clear_address()
        modify_address.one_click_fill_address(ORIGINAL_ADDRESS)
        assert flag

    @allure.feature('订单详情页')
    @allure.story('详情页，核对地址短语正确')
    def test_detail_page_check_address_phrase(self, wait_seller_send_goods):
        """
        1.进入列表页，搜索出一笔订单，点击宝贝主图进入详情页
        2.点击核对地址按钮，进入旺旺
        3.校验核对地址短语
        :return:
        """
        my_list = wait_seller_send_goods
        res = my_list.check_detail_page_send_check_address_phrase(WAIT_BUYER_CONFIRM_GOODS_ORDER)
        assert res[0], '核对地址短语有误，实际：{}，预期：{}'.format(res[1], res[2])

    @allure.feature('订单详情页')
    @allure.story('详情页进入修改地址页，修改地址，清空地址后，一键填充地址正常')
    def test_detail_page_one_click_enter_address(self, wait_seller_send_goods):
        """
        1.进入列表页，搜索出一笔订单，点击宝贝主图进入详情页
        2.点击修改地址按钮，进入修改地址页面
        3.清空地址
        4.一键填入新地址后，点击确定保存
        5.接口获取地址校验
        6.复原地址
        """
        ORIGINAL_ADDRESS = '顾超，18621729133，上海，上海市，宝山区， 高境镇 新二路55号皇冠，201900'
        ORIGINAL_ADDRESS_FROM_API = get_order_detail(WAIT_BUYER_CONFIRM_GOODS_ORDER)
        MODIFY_ADDRESS = '小高，13001356923，上海，上海市，杨浦区， 长白新村56号皇冠，201112'
        my_list = wait_seller_send_goods
        modify_address = my_list.detail_go_to_modify_address()
        modify_address.clear_address()
        modify_address.one_click_fill_address(MODIFY_ADDRESS)
        MODIFY_ADDRESS_FROM_API = get_order_detail(WAIT_BUYER_CONFIRM_GOODS_ORDER)
        # 地址复原
        sleep(3)
        poco(text='修改地址').click()
        modify_address.clear_address()
        modify_address.one_click_fill_address(ORIGINAL_ADDRESS)
        flag = True
        for x in ['收件人姓名', '收件人手机', '收件地址']:
            if ORIGINAL_ADDRESS_FROM_API[x] == MODIFY_ADDRESS_FROM_API[x]:
                flag = False
        assert flag

    @allure.feature('订单详情页')
    @allure.story('详情页进入发货页面，可以正常扫码发货')
    @pytest.mark.skip(reason="避免消耗所有订单数据")
    def test_detail_page_scan_to_deliver_contact_myself(self, wait_seller_send_goods):
        """
        1.进入列表页，搜索出一笔订单，点击宝贝主图进入详情页
        2.点击扫码发货按钮，选择相册中的第一张二维码
        3.进入发货页面，选择自己联系
        4.输入快递公司
        5.点击立即发货按钮，成功返回列表页
        :return:`
        """
        my_list = wait_seller_send_goods
        deliver_page = my_list.detail_scan_to_deliver()
        deliver_page.contact_myself()
        deliver_page.choose_logistics_company_contact_myself('芝麻开门')
        deliver_page.push_deliver_button()
        assert ay_exists(my_list.detail_delivery_locator), '点击立即发货后，没有发货成功！'

    @allure.feature('订单详情页')
    @allure.story('详情页进入发货页面，无需物流，可以正常发货')
    @pytest.mark.skip(reason="避免消耗所有订单数据")
    def test_without_logsitics(self, wait_seller_send_goods):
        """
        1.进入列表页，搜索出一笔订单，点击宝贝主图进入详情页
        2.点击立即发货按钮，进入发货页面面
        3.选择无需物流
        4.点击立即发货按钮，成功返回列表页
        :return:
        """
        my_list = wait_seller_send_goods
        deliver_page = my_list.detail_go_to_deliver()
        deliver_page.without_contact()
        deliver_page.push_deliver_button()
        assert ay_exists(my_list.detail_delivery_locator), '点击立即发货后，没有发货成功！'

    @allure.feature('订单详情页')
    @allure.story('核对订单的短语正确')
    @pytest.mark.skip(reason="error")
    def test_detail_check_order(self, wait_seller_send_goods_combine):
        my_list = wait_seller_send_goods_combine
        my_list.go_detail_page()
        wangwang_check_order_info = my_list.send_check_order_phrase()
        api_check_order_list1 = get_order_detail(WAIT_SELLER_SEND_GOODS_COMBINE[0])
        api_check_order_list2 = get_order_detail(WAIT_SELLER_SEND_GOODS_COMBINE[1])
        flag = True
        # 接口获取的信息里，排除不需要的信息，手机号需要额外处理
        for x in [api_check_order_list1, api_check_order_list2]:
            del x['买家昵称']
            del x['备注']
            x['收件人手机'] = x['收件人手机'].replace('-', '')
            # 接口信息和旺旺短语对比，sku、地址需要额外处理
            for y in x.keys():
                if y == '商品属性':
                    # sku列表每个属性校验
                    for z in x[y]:
                        if z in wangwang_check_order_info:
                            pass
                        else:
                            print('有误的sku：', z)
                            flag = False
                elif y == '收件地址':
                    if x[y].replace(' ', '').replace('，', '') in wangwang_check_order_info.replace(' ', '').replace(',',
                                                                                                                    ''):
                        pass
                    else:
                        print('有误的地址信息：', x[y].replace(' ', ''))
                        flag = False
                else:
                    if x[y] in wangwang_check_order_info:
                        pass
                    else:
                        print('有误的其他信息：', x[y])
                        flag = False
        assert flag, '详情页核对订单生成的旺旺话术有误，生成的话术：{}，接口返回值：{}'.format(wangwang_check_order_info,
                                                                 [api_check_order_list1, api_check_order_list2])

    @allure.feature('订单详情页')
    @allure.story('单sku规格宝贝，能正常修改属性')
    @pytest.mark.skip(reason="bug")
    def test_detail_modify_property_single_sku(self, wait_seller_send_goods):
        my_list = wait_seller_send_goods
        my_list.detail_go_to_modify_property()
        touch(Template(r"pic_data/tpl1583741040856.png", record_pos=(0.215, 0.97), resolution=(1080, 2340)))
        sleep(3)
        poco(text='浅灰色').click()
        sleep(3)
        # 点击重置
        touch(Template(r"pic_data/tpl1583738253423.png", record_pos=(-0.267, 0.993), resolution=(1080, 2340)))
        sleep(3)
        order_info = get_order_detail(WAIT_BUYER_CONFIRM_GOODS)
        # 还原属性
        poco("__react-content").child().child().child().child()[1].child()[1].click()
        sleep(3)
        poco(text='乳白色').click()
        sleep(3)
        # 点击立即修改
        touch(Template(r"pic_data/tpl1583738260013.png", record_pos=(0.215, 0.97), resolution=(1080, 2340)))
        assert order_info['商品属性'][0] == '浅灰色', '详情页无法正常修改属性'

    @allure.feature('设置页')
    @allure.story('设置页，核对地址短语可以正常设置')
    @pytest.mark.skip(reason="error")
    def test_settings_check_address_phrase(self, go_mine):
        """
        1.进入设置页，选择第三种核对地址短语
        2.进入列表页，搜索出一笔订单，获取核对地址短语
        3.从接口获取sku信息，校验短语中是否包含sku信息
        :return:
        """
        first_page = FirstPage()
        mine_page = first_page.go_my_page()
        mine_page.change_phrase()
        my_list = first_page.search_order_by_No(WAIT_BUYER_CONFIRM_GOODS_ORDER)
        wangwang_info = my_list.get_list_check_address_phrase2()
        sku_list = get_order_detail(WAIT_BUYER_CONFIRM_GOODS_ORDER)['商品属性']
        flag = True
        for x in sku_list:
            if x in wangwang_info:
                pass
            else:
                flag = False
        first_page.go_my_page()
        mine_page.recover_phrase()
        mine_page.refresh()
        assert flag, '设置中核对地址短语更换后，实际发送的核对地址短语有误'

    @allure.feature('设置页')
    @allure.story('设置页，自动合并订单开关有效')
    @pytest.mark.skip(reason="error")
    def test_settings_auto_combine(self, go_mine):
        """
        1.进入设置页,关闭自动合单开关
        2.进入列表页，搜索订单
        3.搜索结果，订单状态不显示“合单”
        :return:
        """
        mine_page = go_mine
        mine_page.close_auto_combine()
        first_page = FirstPage()
        list_page = first_page.go_order_list_page()
        list_page.search_order_by_No(WAIT_SELLER_SEND_GOODS_COMBINE[0])
        flag = True
        order_status = list_page.get_order_status()
        first_page.go_my_page()
        mine_page.open_auto_combine()
        if '合单' in order_status:
            flag = False
        else:
            pass
        assert flag, '自动合单开关关闭后，列表还显示合单！'

    @allure.feature('设置页')
    @allure.story('设置页，常用物流可以正常更改')
    @pytest.mark.skip(reason="error")
    def test_settings_change_default_logistic(self, go_mine):
        """
        1.进入设置页,自己联系和在线下单物流，勾选安能物流”，保存
        2.比较保存前后，物流接口返回的信息里，有无“安能物流”
        :param :
        :return:
        """
        mine_page = go_mine
        logistic_before_change = mine_page.get_default_logistic()
        mine_page.change_default_logistic()
        logistic_after_change = mine_page.get_default_logistic()
        mine_page.change_default_logistic()
        flag = True
        if '安能物流' in ''.join(logistic_before_change.values()):
            flag = False
        if '安能物流' not in logistic_after_change['自己联系默认物流'] and '安能物流' not in logistic_after_change['在线下单默认物流']:
            flag = False
        assert flag, '常用物流新增安能物流后，实际没有修改成功'
