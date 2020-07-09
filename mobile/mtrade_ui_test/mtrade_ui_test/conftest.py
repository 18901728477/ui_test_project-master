# 写在conftest.py

# 测试理念：测试页面中不允许操作任何测试数据，同样的就没有任何断言
# 测试数据与用例分离
# 测试用例里不允许直接操作任何元素
import allure
from base64 import b64decode
import pytest
from airtest.core.android.adb import ADB
from poco.exceptions import PocoNoSuchNodeException

from mobile.mitem_ui_test.mitem_ui_test.conftest import restart_app, wakeup_item
from mobile.mtrade_ui_test.mtrade_ui_test.data import *
from mobile.mtrade_ui_test.mtrade_ui_test.pages.mine_page import MinePage, device
from airtest.core.api import stop_app, start_app
from mobile.mtrade_ui_test.mtrade_ui_test.pages.first_page import FirstPage
from mobile.mtrade_ui_test.mtrade_ui_test.pages.send_goods_page import *
from mobile.mtrade_ui_test.mtrade_ui_test.pages.auto_evaluate_page import *
from mobile.mtrade_ui_test.mtrade_ui_test.pages.wait_buyer_confirm_goods_page import WaitBuyerConfirmGoods
poco = AndroidUiautomationPoco(device=device(),screenshot_each_action=False)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)  # 当测试步骤执行失败时，在allure测试报告中添加测试截图
def pytest_runtest_makereport(item, call):
    """
    hook pytest失败
    :param item:
    :param call:
    :return:
    """
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    # we only look at actual failing test.txt calls, not setup/teardown
    if rep.when == "call" and rep.failed:
        with allure.step('失败页面截图...'):
            b64img, fmt = poco.snapshot(width=720)
            open('screen.{}'.format(fmt), 'wb').write(b64decode(b64img))
            file = open('screen.jpg', 'rb').read()
            allure.attach(file, "失败页面截图", allure.attachment_type.JPG)


@pytest.fixture(scope='class')  # 每个测试类执行之前调用一次
def init_app():
    wakeup_trade()
    restart_app()
    first = FirstPage()
    first.self_check()
    return first


@pytest.fixture(scope='class')  # 每个测试类执行之前调用一次
def init_app_by_scan():
    wakeup_item()
    restart_app_by_scan()
    first = FirstPage()
    first.self_check()
    return first


@pytest.fixture(scope='function')
def first(init_app):
    yield FirstPage()
    try:
        FirstPage().refresh()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture(scope='function')
def first_by_scan(init_app_by_scan):
    yield FirstPage()
    try:
        FirstPage().refresh()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页

#
# def restart_app():
#     try:
#         stop_app("com.taobao.qianniu")  # 如果应用存在后台，先停止，保证能够进入千牛工作台首页
#     finally:
#         start_app('com.taobao.qianniu')  # 启动千牛工作台
#     try:
#         poco(text='订单').click()
#         poco('订单管理').click()
#     except PocoNoSuchNodeException:
#         restart_app()




def wakeup_trade():
    ADB(SERIALNO).keyevent('224')
    ADB(SERIALNO).swipe((300, 1000), (300, 500))
    try:

        #ADB(SERIALNO).push(r'C:\uitest\mobile\webtool\static\trade\test.png', '/sdcard/Pictures')#测试电脑
        #顾超电脑
        # ADB(SERIALNO).push(r'C:\Users\Guchao\Desktop\pr\uitest_project\ui_test_project\mobile\webtool\static\trade', '/sdcard/Pictures')
        # ADB(SERIALNO).shell('am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/Pictures/test.txt.png')
        # 陈羽的电脑
        ADB(SERIALNO).push(r' D:\ui_test\ui_test_project - master\mobile\webtool\static\trade', '/sdcard/Pictures')
        ADB(SERIALNO).shell('am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/Pictures/test.txt.png')
    except Exception as e:
        print(e)
        return False


def restart_app_by_scan():
    try:
        stop_app("com.taobao.qianniu")  # 如果应用存在后台，先停止，保证能够进入千牛工作台首页
    finally:
        start_app('com.taobao.qianniu')  # 启动千牛工作台
    try:
        poco('com.taobao.qianniu:id/workbench_title_scan').click()
        poco('com.taobao.qianniu:id/btn_album').click()
        poco(name='显示根目录').click()
        poco(text='图库').click()
        poco(text='trade').click()
        poco('com.android.gallery3d:id/iv_thumbnail').click()
        poco(desc='确定').click()
    except PocoNoSuchNodeException:
        restart_app_by_scan()


# 待付款列表
@pytest.fixture(scope='function')
def wait_buyer_pay(init_app):
    first_page = init_app
    wait_buyer_pay_page = first_page.search_order_by_No(WAIT_BUYER_PAY_ORDER)
    wait_buyer_pay_page.self_check()
    yield wait_buyer_pay_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 待付款列表
@pytest.fixture(scope='function')
def wait_buyer_pay_by_scan(init_app_by_scan):
    first_page = init_app_by_scan
    wait_buyer_pay_page = first_page.search_order_by_No(WAIT_BUYER_PAY_ORDER)
    wait_buyer_pay_page.self_check()
    yield wait_buyer_pay_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 待付款列表, 购物车订单
@pytest.fixture(scope='function')
def wait_buyer_pay_cart(init_app):
    first_page = init_app
    wait_buyer_pay_page = first_page.search_order_by_No(WAIT_BUYER_PAY_ORDER_CART)
    wait_buyer_pay_page.self_check()
    yield wait_buyer_pay_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture()
# 待发货列表，普通订单
def wait_seller_send_goods(init_app):
    first_page = init_app  # 进入首页
    wait_seller_send_goods_page = first_page.search_order_by_No(WAIT_SELLER_SEND_GOODS)  # 输入订单号，搜索
    yield wait_seller_send_goods_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture()
# 待发货列表，没有打印信息记录的订单
def wait_seller_send_goods(init_app):
    first_page = init_app  # 进入首页
    wait_seller_send_goods_page = first_page.search_order_by_No(
        WAIT_SELLER_SEND_GOODS_WITHOUT_PRINT_HISTORY)  # 输入订单号，搜索
    yield wait_seller_send_goods_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture()
# 待发货列表，有打印历史记录的订单
def wait_seller_send_goods_with_print_history(init_app):
    first_page = init_app  # 进入首页
    wait_seller_send_goods_page = first_page.search_order_by_No(WAIT_SELLER_SEND_GOODS_WITH_PRINT_HISTORY)  # 输入订单号，搜索
    yield wait_seller_send_goods_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture()
# 待发货列表，购物车订单
def wait_seller_send_goods_cart(init_app):
    first_page = init_app  # 进入首页
    wait_seller_send_goods_page = first_page.search_order_by_No(WAIT_SELLER_SEND_GOODS_CART)  # 输入订单号，搜索
    yield wait_seller_send_goods_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture()
# 待发货列表，合并订单
def wait_seller_send_goods_combine(init_app):
    first_page = init_app  # 进入首页
    wait_seller_send_goods_page = first_page.search_order_by_No(WAIT_SELLER_SEND_GOODS_COMBINE[0])  # 输入订单号，搜索
    yield wait_seller_send_goods_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture()
# 普通订单，发货页
def send_goods(init_app):
    first_page = init_app  # 进入首页
    wait_seller_send_goods_page = first_page.search_order_by_No(WAIT_BUYER_CONFIRM_GOODS)  # 输入订单号，搜索
    wait_seller_send_goods_page.go_to_deliver()
    yield SendGoodsPage()
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture()
# 购物车订单，发货页
def send_goods_cart(init_app):
    first_page = init_app  # 进入首页
    wait_seller_send_goods_page = first_page.search_order_by_No(WAIT_SELLER_SEND_GOODS_CART)  # 输入订单号，搜索
    wait_seller_send_goods_page.go_to_deliver()
    yield SendGoodsPage()
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture()
# 合并订单，发货页
def send_goods_combine(init_app):
    first_page = init_app  # 进入首页
    wait_seller_send_goods_page = first_page.search_order_by_No(WAIT_SELLER_SEND_GOODS_COMBINE[0])  # 输入订单号，搜索
    wait_seller_send_goods_page.go_to_deliver()
    yield SendGoodsPage()
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture()
# 有打印记录的订单，进入发货页
def send_goods_with_print_history(init_app):
    first_page = init_app  # 进入首页
    wait_seller_send_goods_page = first_page.search_order_by_No(WAIT_SELLER_SEND_GOODS_WITH_PRINT_HISTORY)  # 输入订单号，搜索
    wait_seller_send_goods_page.go_to_deliver()
    yield SendGoodsPage()
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture()
# 无打印记录的订单，进入发货页
def send_goods_without_print_history(init_app):
    first_page = init_app  # 进入首页
    wait_seller_send_goods_page = first_page.search_order_by_No(
        WAIT_SELLER_SEND_GOODS_WITHOUT_PRINT_HISTORY)  # 输入订单号，搜索
    wait_seller_send_goods_page.go_to_deliver()
    yield SendGoodsPage()
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture()
# 进入自动评价首页
def auto_evaluate(init_app):
    first_page = init_app  # 进入首页
    first_page.go_auto_evaluate_page()
    yield AutoEvaluatePage()
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture(scope='function')
def to_be_shipped_orderlist(init_app):
    first_page = init_app  # 进入首页
    to_be_shipped_order_list_page = first_page.go_order_list_page()  # 点击订单列表
    to_be_shipped_order_list_page.search_order_by_No(WAIT_SELLER_SEND_GOODS)  # 根据订单号搜索订单，大写字符标识常量
    to_be_shipped_order_list_page.init_page(WAIT_SELLER_SEND_GOODS)  # 调用init_page方法，获取动态属性的定位字符串
    yield to_be_shipped_order_list_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 待付款购物车
@pytest.fixture(scope='function')
def shopping_cart_wait_buyer_pay_order_list(init_app):
    first_page = init_app
    wait_buyer_pay_shopping_cart_order_list_page = first_page.search_order_by_No(
        WAIT_BUYER_PAY_ORDER_CART)  # 搜索待付款订单
    wait_buyer_pay_shopping_cart_order_list_page.self_check()
    poco("__react-content").child().child()[5].child()[1].swipe([0, -1])
    time.sleep(1)
    yield wait_buyer_pay_shopping_cart_order_list_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 退款中列表
@pytest.fixture(scope='function')
def wait_refund_order_list(init_app):
    first_page = init_app
    wait_refund_order_list_page = first_page.search_order_by_No(WAIT_REFUND_ORDER)  # 搜索退款中订单
    wait_refund_order_list_page.init_page(WAIT_REFUND_ORDER)
    wait_refund_order_list_page.self_check()
    yield wait_refund_order_list_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 批量评价
@pytest.fixture(scope='function')
def evalution_management_list(init_app):
    first_page = init_app
    evalution_management_list = first_page.go_evalution_management()
    yield evalution_management_list
    try:
        first_page.refresh()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 批量发货列表
@pytest.fixture(scope='function')
def batch_send_goods_list(init_app):
    first_page = init_app
    batch_send_goods_list = first_page.go_batch_send_goods_page()
    yield batch_send_goods_list
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 批量发货列表操作
@pytest.fixture(scope='function')
def batch_send_goods_list(init_app):
    first_page = init_app
    batch_send_goods_list_page = first_page.go_batch_send_goods_page()
    yield batch_send_goods_list_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 批量发货页面
@pytest.fixture(scope='function')
def batch_send_goods_page(init_app):
    first_page = init_app
    batch_send_goods_page = first_page.go_batch_send_goods_page()
    batch_send_goods_page.self_check()
    yield batch_send_goods_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 批量发货单笔订单操作
@pytest.fixture(scope='function')
def batch_send_goods_single_order_handle(init_app):
    first_page = init_app
    batch_send_goods_list = first_page.go_batch_send_goods_page()
    batch_send_goods_page = batch_send_goods_list.choose_single_order()
    yield batch_send_goods_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 评价管理页面
@pytest.fixture(scope='function')
def evalution_management_page(init_app):
    first_page = init_app
    evalution_management_page = first_page.go_evalution_management()
    yield evalution_management_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 搜索已发货订单
@pytest.fixture(scope='function')
def wait_buyer_confirm_goods(init_app):
    first_page = init_app  # 进入首页
    wait_buyer_confirm_goods_page = first_page.search_order_by_No(WAIT_BUYER_CONFIRM_GOODS)  # 根据订单号搜索订单，大写字符标识常量
    yield wait_buyer_confirm_goods_page, WAIT_BUYER_CONFIRM_GOODS
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 搜索需要评价订单
@pytest.fixture(scope='function')
def need_seller_rate(init_app):
    first_page = init_app  # 进入首页
    # need_seller_rate_page = first_page.go_order_list_page()  # 点击订单列表
    first_page.search_order_by_No(NEED_RATE)  # 根据订单号搜索订单，大写字符标识常量
    yield first_page, NEED_RATE  # 返回元组（页面，页面校验结果），其中页面校验结果仍然为元组（是否正确，详细比对结果）
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture(scope='function')
def need_seller_rate_list(init_app):
    first_page = init_app  # 进入首页
    need_seller_rate_list_page = first_page.go_order_list_page()  # 点击订单列表
    poco("android:id/content").offspring("com.taobao.qianniu:id/fragment_container").child(
        "android.widget.RelativeLayout").offspring("__react-content").child("android.view.View").offspring(
        "tabNEED_RATE").child("android.view.View").click()  # 点击需要评价列表
    yield need_seller_rate_list_page  # 返回元组（页面，页面校验结果），其中页面校验结果仍然为元组（是否正确，详细比对结果）
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 搜索待发货订单
@pytest.fixture(scope='function')
def to_be_shipped_orderlist(init_app):
    first_page = init_app  # 进入首页
    to_be_shipped_order_list_page = first_page.go_order_list_page()  # 点击订单列表
    to_be_shipped_order_list_page.search_order_by_No(WAIT_SELLER_SEND_GOODS)  # 根据订单号搜索订单，大写字符标识常量
    to_be_shipped_order_list_page.init_page(WAIT_SELLER_SEND_GOODS)  # 调用init_page方法，获取动态属性的定位字符串
    yield to_be_shipped_order_list_page  # , check_order_info(
    #  WAIT_SELLER_SEND_GOODS)  # 返回元组（页面，页面校验结果），其中页面校验结果仍然为元组（是否正确，详细比对结果）
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 去我的页面
@pytest.fixture(scope='function')
def go_to_my_page(init_app):
    first_page = init_app  # 进入首页
    my_page = first_page.go_my_page()  # 点击我的
    yield my_page  # 返回我的页面
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 去首页批量评价页面
@pytest.fixture(scope='function')
def go_to_firstbatch_evaluation_page(init_app):
    first_page = init_app  # 进入首页
    batch_evaluation_page = first_page.go_batch_evaluation_page()  # 点击批量评价
    yield batch_evaluation_page  # 返回批量评价页面
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 前往首页差评拦截页面
@pytest.fixture(scope='function')
def go_to_negative_comment_interception_page(init_app_by_scan):
    first_page = init_app_by_scan  # 进入首页
    negative_comment_interception_page = first_page.go_negative_comment_interception_page()  # 点击差评拦截
    yield negative_comment_interception_page  # 返回差评拦截页面
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture()
# 进入我的页面
def go_mine(init_app):
    first_page = init_app  # 进入首页
    first_page.go_my_page()
    yield MinePage()
    first_page.refresh()


# 待付款列表, 购物车订单
@pytest.fixture(scope='function')
def wait_buyer_pay_cart_by_scan(init_app_by_scan):
    first_page = init_app_by_scan
    wait_buyer_pay_page = first_page.search_order_by_No(WAIT_BUYER_PAY_ORDER_CART)
    wait_buyer_pay_page.self_check()
    yield wait_buyer_pay_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture()
# 待发货列表，普通订单
def wait_seller_send_goods_by_scan(init_app_by_scan):
    first_page = init_app_by_scan  # 进入首页
    wait_seller_send_goods_page = first_page.search_order_by_No(WAIT_SELLER_SEND_GOODS)  # 输入订单号，搜索
    yield wait_seller_send_goods_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture()
# 待发货列表，没有打印信息记录的订单
def wait_seller_send_goods_by_scan(init_app_by_scan):
    first_page = init_app_by_scan  # 进入首页
    wait_seller_send_goods_page = first_page.search_order_by_No(
        WAIT_SELLER_SEND_GOODS_WITHOUT_PRINT_HISTORY)  # 输入订单号，搜索
    yield wait_seller_send_goods_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture()
# 待发货列表，有打印历史记录的订单
def wait_seller_send_goods_with_print_history_by_scan(init_app_by_scan):
    first_page = init_app_by_scan  # 进入首页
    wait_seller_send_goods_page = first_page.search_order_by_No(WAIT_SELLER_SEND_GOODS_WITH_PRINT_HISTORY)  # 输入订单号，搜索
    yield wait_seller_send_goods_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture()
# 待发货列表，购物车订单
def wait_seller_send_goods_cart_by_scan(init_app_by_scan):
    first_page = init_app_by_scan  # 进入首页
    wait_seller_send_goods_page = first_page.search_order_by_No(WAIT_SELLER_SEND_GOODS_CART)  # 输入订单号，搜索
    yield wait_seller_send_goods_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture()
# 待发货列表，合并订单
def wait_seller_send_goods_combine_by_scan(init_app_by_scan):
    first_page = init_app_by_scan  # 进入首页
    wait_seller_send_goods_page = first_page.search_order_by_No(WAIT_SELLER_SEND_GOODS_COMBINE[0])  # 输入订单号，搜索
    yield wait_seller_send_goods_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture()
# 普通订单，发货页
def send_goods_by_scan(init_app_by_scan):
    first_page = init_app_by_scan  # 进入首页
    wait_seller_send_goods_page = first_page.search_order_by_No(WAIT_BUYER_CONFIRM_GOODS)  # 输入订单号，搜索
    wait_seller_send_goods_page.go_to_deliver()
    yield SendGoodsPage()
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture()
# 购物车订单，发货页
def send_goods_cart_by_scan(init_app_by_scan):
    first_page = init_app_by_scan  # 进入首页
    wait_seller_send_goods_page = first_page.search_order_by_No(WAIT_SELLER_SEND_GOODS_CART)  # 输入订单号，搜索
    wait_seller_send_goods_page.go_to_deliver()
    yield SendGoodsPage()
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture()
# 合并订单，发货页
def send_goods_combine_by_scan(init_app_by_scan):
    first_page = init_app_by_scan  # 进入首页
    wait_seller_send_goods_page = first_page.search_order_by_No(WAIT_SELLER_SEND_GOODS_COMBINE[0])  # 输入订单号，搜索
    wait_seller_send_goods_page.go_to_deliver()
    yield SendGoodsPage()
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture()
# 有打印记录的订单，进入发货页
def send_goods_with_print_history_by_scan(init_app_by_scan):
    first_page = init_app_by_scan  # 进入首页
    wait_seller_send_goods_page = first_page.search_order_by_No(WAIT_SELLER_SEND_GOODS_WITH_PRINT_HISTORY)  # 输入订单号，搜索
    wait_seller_send_goods_page.go_to_deliver()
    yield SendGoodsPage()
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture()
# 无打印记录的订单，进入发货页
def send_goods_without_print_history_by_scan(init_app_by_scan):
    first_page = init_app_by_scan  # 进入首页
    wait_seller_send_goods_page = first_page.search_order_by_No(
        WAIT_SELLER_SEND_GOODS_WITHOUT_PRINT_HISTORY)  # 输入订单号，搜索
    wait_seller_send_goods_page.go_to_deliver()
    yield SendGoodsPage()
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture()
# 进入自动评价首页
def auto_evaluate_by_scan(init_app_by_scan):
    first_page = init_app_by_scan  # 进入首页
    first_page.go_auto_evaluate_page()
    yield AutoEvaluatePage()
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture(scope='function')
def to_be_shipped_orderlist_by_scan(init_app_by_scan):
    first_page = init_app_by_scan  # 进入首页
    to_be_shipped_order_list_page = first_page.go_order_list_page()  # 点击订单列表
    to_be_shipped_order_list_page.search_order_by_No(WAIT_SELLER_SEND_GOODS)  # 根据订单号搜索订单，大写字符标识常量
    to_be_shipped_order_list_page.init_page(WAIT_SELLER_SEND_GOODS)  # 调用init_page方法，获取动态属性的定位字符串
    yield to_be_shipped_order_list_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 待付款购物车
@pytest.fixture(scope='function')
def shopping_cart_wait_buyer_pay_order_list_by_scan(init_app_by_scan):
    first_page = init_app_by_scan
    wait_buyer_pay_shopping_cart_order_list_page = first_page.search_order_by_No(
        WAIT_BUYER_PAY_ORDER_CART)  # 搜索待付款订单
    wait_buyer_pay_shopping_cart_order_list_page.self_check()
    poco("__react-content").child().child()[5].child()[1].swipe([0, -1])
    time.sleep(1)
    yield wait_buyer_pay_shopping_cart_order_list_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 退款中列表
@pytest.fixture(scope='function')
def wait_refund_order_list_by_scan(init_app_by_scan):
    first_page = init_app_by_scan
    wait_refund_order_list_page = first_page.search_order_by_No(WAIT_REFUND_ORDER)  # 搜索退款中订单
    wait_refund_order_list_page.init_page(WAIT_REFUND_ORDER)
    wait_refund_order_list_page.self_check()
    yield wait_refund_order_list_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 批量评价
@pytest.fixture(scope='function')
def evalution_management_list_by_scan(init_app_by_scan):
    first_page = init_app_by_scan
    evalution_management_list = first_page.go_evalution_management()
    yield evalution_management_list
    try:
        first_page.refresh()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 批量发货页面
@pytest.fixture(scope='function')
def batch_send_goods_page_by_scan(init_app_by_scan):
    first_page = init_app_by_scan
    batch_send_goods_page = first_page.go_batch_send_goods_page()
    batch_send_goods_page.self_check()
    yield batch_send_goods_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 批量发货单笔订单操作
@pytest.fixture(scope='function')
def batch_send_goods_single_order_handle_by_scan(init_app_by_scan):
    first_page = init_app_by_scan
    batch_send_goods_list = first_page.go_batch_send_goods_page()
    batch_send_goods_page = batch_send_goods_list.choose_single_order()
    yield batch_send_goods_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 评价管理页面
@pytest.fixture(scope='function')
def evalution_management_page_by_scan(init_app_by_scan):
    first_page = init_app_by_scan
    evalution_management_page = first_page.go_evalution_management()
    yield evalution_management_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 搜索已发货订单
@pytest.fixture(scope='function')
def wait_buyer_confirm_goods_by_scan(init_app_by_scan):
    first_page = init_app_by_scan  # 进入首页
    wait_buyer_confirm_goods_page = first_page.search_order_by_No(WAIT_BUYER_CONFIRM_GOODS)  # 根据订单号搜索订单，大写字符标识常量
    yield wait_buyer_confirm_goods_page
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 搜索需要评价订单
@pytest.fixture(scope='function')
def need_seller_rate_by_scan(init_app_by_scan):
    first_page = init_app_by_scan  # 进入首页
    # need_seller_rate_page = first_page.go_order_list_page()  # 点击订单列表
    first_page.search_order_by_No(NEED_RATE)  # 根据订单号搜索订单，大写字符标识常量
    yield first_page, NEED_RATE  # 返回元组（页面，页面校验结果），其中页面校验结果仍然为元组（是否正确，详细比对结果）
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture(scope='function')
def need_seller_rate_list_by_scan(init_app_by_scan):
    first_page = init_app_by_scan  # 进入首页
    need_seller_rate_list_page = first_page.go_order_list_page()  # 点击订单列表
    poco("android:id/content").offspring("com.taobao.qianniu:id/fragment_container").child(
        "android.widget.RelativeLayout").offspring("__react-content").child("android.view.View").offspring(
        "tabNEED_RATE").child("android.view.View").click()  # 点击需要评价列表
    yield need_seller_rate_list_page  # 返回元组（页面，页面校验结果），其中页面校验结果仍然为元组（是否正确，详细比对结果）
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 搜索待发货订单
@pytest.fixture(scope='function')
def to_be_shipped_orderlist_by_scan(init_app_by_scan):
    first_page = init_app_by_scan  # 进入首页
    to_be_shipped_order_list_page = first_page.go_order_list_page()  # 点击订单列表
    to_be_shipped_order_list_page.search_order_by_No(WAIT_SELLER_SEND_GOODS)  # 根据订单号搜索订单，大写字符标识常量
    to_be_shipped_order_list_page.init_page(WAIT_SELLER_SEND_GOODS)  # 调用init_page方法，获取动态属性的定位字符串
    yield to_be_shipped_order_list_page  # , check_order_info(
    #  WAIT_SELLER_SEND_GOODS)  # 返回元组（页面，页面校验结果），其中页面校验结果仍然为元组（是否正确，详细比对结果）
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 去我的页面
@pytest.fixture(scope='function')
def go_to_my_page_by_scan(init_app_by_scan):
    first_page = init_app_by_scan  # 进入首页
    my_page = first_page.go_my_page()  # 点击我的
    yield my_page  # 返回我的页面
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 去首页批量评价页面
@pytest.fixture(scope='function')
def go_to_firstbatch_evaluation_page_by_scan(init_app_by_scan):
    first_page = init_app_by_scan  # 进入首页
    batch_evaluation_page = first_page.go_batch_evaluation_page()  # 点击批量评价
    yield batch_evaluation_page  # 返回批量评价页面
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


# 前往首页差评拦截页面
@pytest.fixture(scope='function')
def go_to_negative_comment_interception_page_by_scan(init_app_by_scan):
    first_page = init_app_by_scan  # 进入首页
    negative_comment_interception_page = first_page.go_negative_comment_interception_page()  # 点击差评拦截
    yield negative_comment_interception_page  # 返回差评拦截页面
    try:
        first_page.refresh()
        first_page.self_check()
    except Exception as e:
        print(e)
        restart_app()  # 如果失败，则重新初始化，得到首页


@pytest.fixture()
# 进入我的页面
def go_mine_by_scan(init_app_by_scan):
    first_page = init_app_by_scan  # 进入首页
    first_page.go_my_page()
    yield MinePage()
    first_page.refresh()


if __name__ == '__main__':
    wakeup()
    restart_app()
