# -*- encoding=utf8 -*-
__author__ = 'xiaoxuan'

# import json
# import re
# import time
# import allure
# from base64 import b64decode
# import jsonpath
import pytest
from mobile.mitem_ui_test.mitem_ui_test.item_info import *
from airtest.core.android.adb import ADB

# 添加报错截图到allure报告里
# import requests
# from airtest.core.api import stop_app, start_app, auto_setup, device
# from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from mobile.mitem_ui_test.mitem_ui_test.pages.first_page import *
from mobile.mitem_ui_test.mitem_ui_test.pages.mdetail_page import *
from mobile.mitem_ui_test.mitem_ui_test.pages.mdetail_item_list import *
from mobile.mitem_ui_test.mitem_ui_test.pages.detail_page import *
from mobile.mitem_ui_test.mitem_ui_test.pages.title_improve_list_page import *
from mobile.mitem_ui_test.mitem_ui_test.pages.title_improve_detail_page import *

poco = AndroidUiautomationPoco(device=device(), screenshot_each_action=False)


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
    # we only look at actual failing test calls, not setup/teardown
    if rep.when == "call" and rep.failed:
        with allure.step('添加失败页面截图...'):
            b64img, fmt = poco.snapshot(width=720)
            open('screen.{}'.format(fmt), 'wb').write(b64decode(b64img))
            file = open('screen.jpg', 'rb').read()
            allure.attach(file, "失败页面截图", allure.attachment_type.JPG)


# @pytest.fixture(scope='session', autouse=True) # 所有.py文件，执行之前调用一次
# def check_session():
#     try:
#         # BasePage().edit_viptime() # 避免出现授权弹窗，提高用例效率
#         wakeup()
#         restart_app()
#         time.sleep(3)
#         try:
#             poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').wait_for_appearance(5)  # 第一次进入授权，5秒显示等待
#             poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').click()
#         except Exception:
#             pass
#         poco(text='出售中').parent().offspring(textMatches='\d*').wait_for_appearance(5)  # 进入首页，5秒显示等待
#         # 首页如果有公告将其关闭
#         BasePage().close_notice()
#         BasePage().refresh_backhome()
#         # 列表页如果有公告将其关闭
#         FirstPage().go_item_list(0)
#         BasePage().close_notice()
#         BasePage().refresh_backhome()
#         # 详情页如果有公告将其关闭
#         FirstPage().go_item_list(0)
#         ItemList().go_detail_page()
#         BasePage().close_notice()
#         BasePage().refresh_backhome()
#     except Exception:
#         print('出现异常')
def wakeup_item():
    ADB(SERIALNO).keyevent('224')
    ADB(SERIALNO).swipe((300, 1000), (300, 500))
    # try:
    #
    #     #ADB(SERIALNO).push(r'C:\uitest\mobile\webtool\static\trade\test.png', '/sdcard/Pictures')#测试电脑
    #     #顾超电脑
    #     # ADB(SERIALNO).push(r'C:\Users\Guchao\Desktop\pr\uitest_project\ui_test_project\mobile\webtool\static\trade', '/sdcard/Pictures')
    #     # ADB(SERIALNO).shell('am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/Pictures/test.txt.png')
    #     # 陈羽的电脑
    #     ADB(SERIALNO).push(r' D:\ui_test\ui_test_project - master\mobile\webtool\static\trade', '/sdcard/Pictures')
    #     ADB(SERIALNO).shell('am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/Pictures/test.txt.png')
    # except Exception as e:
    #     print(e)
    #     return False


@pytest.fixture(scope='class')  # 所有class，执行之前调用一次
def init_app_item():
    try:
        wakeup_item()
        restart_app()
        time.sleep(3)
        try:
            poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').wait_for_appearance(
                5)  # 第一次进入授权，5秒显示等待
            poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').click()
        except Exception:
            pass
        poco(text='出售中').parent().offspring(textMatches='\d*').wait_for_appearance(10)  # 进入首页，5秒显示等待
    except Exception:
        print('出现异常')
    return FirstPage()


@pytest.fixture(scope='class')  # 所有class，执行之前调用一次
def init_app_scan():
    try:
        # wakeup()
        restart_app_by_scan()
        time.sleep(3)
        try:
            poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').wait_for_appearance(
                5)  # 第一次进入授权，5秒显示等待
            poco(textMatches='.*授权.*', name='com.taobao.qianniu:id/open_auth_btn_grant').click()
        except Exception:
            pass
        poco(text='出售中').parent().offspring(textMatches='\d*').wait_for_appearance(10)  # 进入首页，5秒显示等待
    except Exception:
        print('出现异常')
    return FirstPage()


@pytest.fixture()
# 进入首页
def go_firstpage(init_app_item):
    yield FirstPage()
    BasePage().refresh_backhome()


@pytest.fixture()
# 进入手机详情首页
def go_mdetail(init_app_item):
    try:
        first_page = init_app_item
        BasePage().page_swipe_buttom()
        first_page.go_mdetail()
    except Exception:
        print('出现异常')
    yield MdetailPage()
    BasePage().refresh_backhome()


@pytest.fixture()
# 进入出售中的宝贝详情页
def go_detail_page_onsale(init_app_item):
    try:
        first_page = init_app_item
        item_list = first_page.go_item_list(0)
        item_list.search_by_keyword(ITEM_ONSALE_TITLE, poco(text=ITEM_ONSALE_TITLE))
        item_list.go_detail_page()
    except Exception:
        print('出现异常')
    yield ItemDetail()
    BasePage().refresh_backhome()


@pytest.fixture()
# 进入出售中的宝贝详情页,改标题
def go_detail_page_onsale_title(init_app_item):
    try:
        first_page = init_app_item
        item_list = first_page.go_item_list(0)
        item_list.search_by_keyword(ITEM_EDIT_TITLE_ONSELA_TITLE, poco(text=ITEM_EDIT_TITLE_ONSELA_TITLE))
        item_list.go_detail_page()
    except Exception:
        print('出现异常')
    yield ItemDetail()
    BasePage().refresh_backhome()


@pytest.fixture()
# 进入仓库中的宝贝详情页
def go_detail_page_inventory(init_app_item):
    try:
        first_page = init_app_item
        item_list = first_page.go_item_list(1)
        item_list.search_by_keyword(ITEM_INVENTORY_TITLE, poco(text=ITEM_INVENTORY_TITLE))
        item_list.go_detail_page()
    except Exception:
        print('出现异常')
    yield ItemDetail()
    BasePage().refresh_backhome()


@pytest.fixture()
# 进入已售完的宝贝详情页
def go_detail_page_soldout(init_app_item):
    try:
        first_page = init_app_item
        item_list = first_page.go_item_list(2)
        item_list.search_by_keyword(ITEM_SOLDOUT_TITLE, poco(text=ITEM_SOLDOUT_TITLE))
        item_list.go_detail_page()
    except Exception:
        print('出现异常')
    yield ItemDetail()
    BasePage().refresh_backhome()


@pytest.fixture()
# 进入属性有格式要求的宝贝详情页
def go_detail_page_format_props(init_app_item):
    try:
        first_page = init_app_item
        item_list = first_page.go_item_list(0)
        item_list.search_by_keyword(ITEM_PROPERTY_FORMAT_TITLE, poco(text=ITEM_PROPERTY_FORMAT_TITLE))
        item_list.go_detail_page()
    except Exception:
        print('出现异常')
    yield ItemDetail()
    BasePage().refresh_backhome()


@pytest.fixture()
# 进入标题优化列表页
def go_title_improve_list(init_app_item):
    try:
        first_page = init_app_item
        BasePage().page_swipe_buttom()
        first_page.go_title_improve()
    except Exception:
        print('出现异常')
    yield TitleImproveList()
    BasePage().refresh_backhome()


@pytest.fixture()
# 进入标题优化详情页
def go_title_improve_detail(init_app_item):
    try:
        first_page = init_app_item
        BasePage().page_swipe_buttom()
        title_improve_list_page = first_page.go_title_improve()
        title_improve_list_page.search_by_keyword(ITEM_TITLE_IMPROVE_TITLE, poco(text='上次优化时间：'))
        title_improve_list_page.go_title_improve_detail_page(ITEM_TITLE_IMPROVE_TITLE)
    except Exception:
        print('出现异常')
    yield TitleImproveDetail()
    BasePage().refresh_backhome()


@pytest.fixture()
def first_page_wait(init_app_item):
    try:
        first_page = init_app_item
    except Exception:
        print('出现异常')
    sleep(2)
    yield FirstPage()
    BasePage().refresh_backhome()


@pytest.fixture()
# 进入出售中列表
def go_onsale_list(init_app_item):
    try:
        first_page = init_app_item
        first_page.go_item_list(0)
    except Exception:
        print('出现异常')
    yield ItemList()
    BasePage().refresh_backhome()


@pytest.fixture()
# 进入仓库中列表
def go_inventory_list(init_app_item):
    try:
        first_page = init_app_item
        first_page.go_item_list(1)
    except Exception:
        print('出现异常')
    yield ItemList()
    BasePage().refresh_backhome()


@pytest.fixture()
# 进入已售完列表
def go_soldout_list(init_app_item):
    try:
        first_page = init_app_item
        first_page.go_item_list(2)
    except Exception:
        print('出现异常')
    yield ItemList()
    BasePage().refresh_backhome()


# 进入违规词检测页面
@pytest.fixture()
def go_badword_detect_page(init_app_item):
    try:
        first_page = init_app_item
        BasePage().page_swipe_buttom()
        first_page.go_badword_detect()
    except Exception:
        print('出现异常')
    yield BadwordDetect()
    BasePage().refresh_backhome()


@pytest.fixture()
# 进入首页
def go_firstpage_scan(init_app_scan):
    yield FirstPage()
    BasePage().refresh_backhome()


@pytest.fixture()
# 进入手机详情首页
def go_mdetail_scan(init_app_scan):
    try:
        first_page = init_app_scan
        first_page.go_mdetail()
    except Exception:
        print('出现异常')
    yield MdetailPage()
    BasePage().refresh_backhome()


@pytest.fixture()
# 进入出售中的宝贝详情页
def go_detail_page_onsale_scan(init_app_scan):
    try:
        first_page = init_app_scan
        item_list = first_page.go_item_list(0)
        item_list.search_by_keyword(ITEM_ONSALE_TITLE, poco(text=ITEM_ONSALE_TITLE))
        item_list.go_detail_page()
    except Exception:
        print('出现异常')
    yield ItemDetail()
    BasePage().refresh_backhome()


@pytest.fixture()
# 进入出售中的宝贝详情页,改标题
def go_detail_page_onsale_title_scan(init_app_scan):
    try:
        first_page = init_app_scan
        item_list = first_page.go_item_list(0)
        item_list.search_by_keyword(ITEM_EDIT_TITLE_ONSELA_TITLE, poco(text=ITEM_EDIT_TITLE_ONSELA_TITLE))
        item_list.go_detail_page()
    except Exception:
        print('出现异常')
    yield ItemDetail()
    BasePage().refresh_backhome()


@pytest.fixture()
# 进入仓库中的宝贝详情页
def go_detail_page_inventory_scan(init_app_scan):
    try:
        first_page = init_app_scan
        item_list = first_page.go_item_list(1)
        item_list.search_by_keyword(ITEM_INVENTORY_TITLE, poco(text=ITEM_INVENTORY_TITLE))
        item_list.go_detail_page()
    except Exception:
        print('出现异常')
    yield ItemDetail()
    BasePage().refresh_backhome()


@pytest.fixture()
# 进入已售完的宝贝详情页
def go_detail_page_soldout_scan(init_app_scan):
    try:
        first_page = init_app_scan
        item_list = first_page.go_item_list(2)
        item_list.search_by_keyword(ITEM_SOLDOUT_TITLE, poco(text=ITEM_SOLDOUT_TITLE))
        item_list.go_detail_page()
    except Exception:
        print('出现异常')
    yield ItemDetail()
    BasePage().refresh_backhome()


@pytest.fixture()
# 进入属性有格式要求的宝贝详情页
def go_detail_page_format_props_scan(init_app_scan):
    try:
        first_page = init_app_scan
        item_list = first_page.go_item_list(0)
        item_list.search_by_keyword(ITEM_PROPERTY_FORMAT_TITLE, poco(text=ITEM_PROPERTY_FORMAT_TITLE))
        item_list.go_detail_page()
    except Exception:
        print('出现异常')
    yield ItemDetail()
    BasePage().refresh_backhome()


@pytest.fixture()
# 进入标题优化列表页
def go_title_improve_list_scan(init_app_scan):
    try:
        first_page = init_app_scan
        first_page.go_title_improve()
    except Exception:
        print('出现异常')
    yield TitleImproveList()
    BasePage().refresh_backhome()


@pytest.fixture()
# 进入标题优化详情页
def go_title_improve_detail_scan(init_app_scan):
    try:
        first_page = init_app_scan
        title_improve_list_page = first_page.go_title_improve()
        title_improve_list_page.search_by_keyword(ITEM_TITLE_IMPROVE_TITLE, poco(text='上次优化时间：'))
        title_improve_list_page.go_title_improve_detail_page(ITEM_TITLE_IMPROVE_TITLE)
    except Exception:
        print('出现异常')
    yield TitleImproveDetail()
    BasePage().refresh_backhome()


@pytest.fixture()
def first_page_wait_scan(init_app_scan):
    try:
        init_app_scan
    except Exception:
        print('出现异常')
    sleep(2)
    yield FirstPage()
    BasePage().refresh_backhome()


@pytest.fixture()
# 进入出售中列表
def go_onsale_list_scan(init_app_scan):
    try:
        first_page = init_app_scan
        first_page.go_item_list(0)
    except Exception:
        print('出现异常')
    yield ItemList()
    BasePage().refresh_backhome()


@pytest.fixture()
# 进入仓库中列表
def go_inventory_list_scan(init_app_scan):
    try:
        first_page = init_app_scan
        first_page.go_item_list(1)
    except Exception:
        print('出现异常')
    yield ItemList()
    BasePage().refresh_backhome()


@pytest.fixture()
# 进入已售完列表
def go_soldout_list_scan(init_app_scan):
    try:
        first_page = init_app_scan
        first_page.go_item_list(2)
    except Exception:
        print('出现异常')
    yield ItemList()
    BasePage().refresh_backhome()


# 进入违规词检测页面
@pytest.fixture()
def go_badword_detect_page_scan(init_app_scan):
    try:
        first_page = init_app_scan
        first_page.go_badword_detect()
    except Exception:
        print('出现异常')
    yield BadwordDetect()
    BasePage().refresh_backhome()


# 进入发布宝贝页面
@pytest.fixture()
def go_release_page(init_app_item):
    try:
        first_page = init_app_item
        BasePage().page_swipe_buttom()
        first_page.go_release_detect()
    except Exception:
        print('出现异常')
    yield ReleasePage()
    BasePage().refresh_backhome()
    # 点击返回,确定
    poco(name="com.taobao.qianniu:id/qn_widmill_nav_bar_back_btn").click()
    poco(name='退出').click()


# 启动千牛
def restart_app():
    try:
        stop_app("com.taobao.qianniu")  # 如果应用存在后台，先停止，保证能够进入千牛工作台首页
    finally:
        start_app('com.taobao.qianniu')  # 启动千牛工作台

    # 线上
    try:
        poco(text='商品').click()
        poco('商品管理').click()
    except PocoNoSuchNodeException:
        restart_app()

    # 调试
    # try:
    #     poco('com.taobao.qianniu:id/workbench_title_scan').click()
    #     poco('com.taobao.qianniu:id/btn_album').click()
    #     poco(name='显示根目录').click()
    #     poco(text='图片', name='android:id/title').click()
    #     sleep(1.5)
    #     poco(name='com.android.documentsui:id/icon_thumb').click()
    #     sleep(1.5)
    #     poco(name='com.android.documentsui:id/icon_thumb').click()
    # except PocoNoSuchNodeException:
    #     restart_app()

    # 千牛跳转bug
    try:
        poco(text='1688淘货源').wait_for_appearance(2)
        print('进入1688淘货源')
        restart_app()
    except PocoTargetTimeout:
        print('成功进入商品首页')


def wakeup_item():
    ADB(SERIALNO).keyevent('224')
    ADB(SERIALNO).swipe((300, 1000), (300, 500))
    try:
        # ADB(SERIALNO).push(r'C:\uitest\mobile\webtool\static\item\test.png', ADB_PIC_URL)#测试电脑路径
        # ADB(SERIALNO).push(
        #     r'C:\Users\Guchao\Desktop\pr\uitest_project\ui_test_project\mobile\webtool\static\item\test.png',
        #     ADB_PIC_URL)  # 顾超电脑路径
        # 陈羽的电脑
        ADB(SERIALNO).push(r' D:\ui_test\ui_test_project - master\mobile\webtool\static\trade', '/sdcard/Pictures')
        ADB(SERIALNO).shell(ADB_SCAN_FILE)
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
        poco(text='图片').click()
        poco('com.android.gallery3d:id/iv_thumbnail').click()
        poco(desc='确定').click()
    except PocoNoSuchNodeException:
        restart_app_by_scan()

    # # 高志轩测试机
    # try:
    #     stop_app("com.taobao.qianniu")  # 如果应用存在后台，先停止，保证能够进入千牛工作台首页
    # finally:
    #     start_app('com.taobao.qianniu')  # 启动千牛工作台
    # try:
    #     poco('com.taobao.qianniu:id/workbench_title_scan').click()
    #     poco('com.taobao.qianniu:id/btn_album').click()
    #     poco(name='显示根目录').click()
    #     poco(text='图片', name='android:id/title').click()
    #     sleep(1.5)
    #     poco(name='com.android.documentsui:id/icon_thumb').click()
    #     sleep(1.5)
    #     poco(name='com.android.documentsui:id/icon_thumb').click()
    #
    # except PocoNoSuchNodeException:
    #     restart_app_by_scan()


if __name__ == '__main__':
    go_release_page()
