# -*- encoding=utf8 -*-
__author__ = 'xiaoxuan'

from base64 import b64decode
import allure
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.proxy import UIObjectProxy
import requests
import re
import json
from poco.exceptions import *

poco = AndroidUiautomationPoco(device=device(), screenshot_each_action=False)


def init_element(my_locator: tuple) -> UIObjectProxy:
    element = UIObjectProxy(poco)
    element.query = my_locator
    return element


# 方法：获取元素文本值
def get_text_of_view(element: UIObjectProxy):
    while len(element.offspring('android.view.View')) and not element.attr('text'):
        element = element.offspring('android.view.View')
    return element.get_text()


# 方法：点击特定元素
def element_click(my_locator: tuple):
    element = UIObjectProxy(poco)
    element.query = my_locator
    element.click()


# 方法：textbox输入内容
def element_sendtext(my_locator: tuple, my_text):
    element = UIObjectProxy(poco)
    element.query = my_locator
    element.set_text(my_text)


# 方法：特定元素是否存在
def does_element_exists(my_locator: tuple):
    element = UIObjectProxy(poco)
    element.query = my_locator
    return element.exists()


def get_screen(self):
    with allure.step('用例通过，最后步骤截图...'):
        b64img, fmt = self.poco.snapshot(width=720)
        open('success.{}'.format(fmt), 'wb').write(b64decode(b64img))
        file = open('success.jpg', 'rb').read()
        allure.attach(file, "成功用例截图", allure.attachment_type.JPG)


def locate_by_anchor(element: UIObjectProxy, parent_lv: int = 0, child_lv: str = ''):
    """
    通过锚元素相对定位元素
    :param element: 锚元素
    :param parent_lv: 父节点层级，默认为0表示锚元素自身
    :param child_lv: 子节点层级，默认为空表示锚元素自身
    :return:
    """
    if not parent_lv:
        element_p = element
    else:
        element_p = get_parent_by_level(element, parent_lv)
    if not child_lv:
        element_c = element_p
    else:
        child_path_list = trans_child_level(child_lv)
        element_c = get_offspring_by_index(element_p, child_path_list)
    return element_c


def trans_child_level(child_lv: str):
    i = 0
    temp2 = []
    temp3 = []
    try:
        while i < len(child_lv):
            temp2.append(child_lv[i:i + 2])
            i += 2
        for j in temp2:
            temp3.append((j[0], int(j[1])))
        return temp3
    except Exception:
        print('传入参数不合法')


def get_offspring_by_index(element_p, path_list=None):  # ''
    if path_list is None:
        path_list = []
    length = len(path_list)
    result = get_child_by_index(element_p, path_list[0][0], path_list[0][1])
    if length == 1:
        return result
    else:
        return get_offspring_by_index(result, path_list[1:length])


def get_child_by_index(element_p, structure, index) -> UIObjectProxy:
    """
    根据可见的位置关系选择子元素
    :param element_p: 父节点
    :param structure: l表示左右结构，v表示上下结构，
    :param index: 序号，按从左往右，从上往下顺序取
    :return:
    """
    temp_list = []
    element_list = []
    for element_c in element_p.child():  # 遍历子节点
        temp_list.append({'element': element_c, 'pos': element_c.attr('pos')})  # 将元素以及其位置POS属性构造成字典以后再存入列表
    if structure == 'l':  # 左右结构
        temp_list.sort(key=lambda e: e['pos'][0], reverse=False)  # 调用列表sort排序方法，排序的key是字典的POS键值的下标为0的值，即横坐标
    elif structure == 'v':  # 上下结构
        temp_list.sort(key=lambda e: e['pos'][1], reverse=False)
    for element in temp_list:
        element_list.append(element['element'])
    return element_list[index]


def get_parent_by_level(element: UIObjectProxy, level=1):
    if level <= 1:
        return element.parent()
    else:
        return get_parent_by_level(element.parent(), level - 1)


def super_click(element: UIObjectProxy):
    element.invalidate()
    element.click()


class BasePage():

    # 方法：页面翻滚至底部
    def page_swipe_buttom(self):
        poco("__react-content").swipe([0, -1])
        sleep(3)

    # 方法：发布宝贝页面翻滚至底部
    def page_swipe_buttom02(self):
        poco("android.widget.ScrollView").swipe([0, -1])
        sleep(3)

    # 方法：页面翻滚至顶部
    def page_swipe_top(self):
        poco("__react-content").swipe([0, 1])
        sleep(3)

    # 方法: 发布宝贝页面翻滚至顶部
    def page_swipe_top_release(self):
        poco("android.widget.ScrollView").swipe([0, 1])
        sleep(3)

    # 方法：返回
    def turn_back(self):
        poco(name='com.taobao.qianniu:id/qn_widmill_nav_bar_back_btn').click()
        sleep(0.5)

    # 方法：刷新回到首页
    def refresh_backhome(self):
        try:
            poco(name='com.taobao.qianniu:id/qn_nav_menu_more_btn').click()
            anchor = poco(name='com.taobao.qianniu:id/menu_popup_container')
            locator = locate_by_anchor(element=anchor, parent_lv=0, child_lv='v1l0')
            locator.click()
            poco(textMatches='\d{2}').wait_for_appearance(10)  # 重新加载首页，10秒显示等待
        except PocoNoSuchNodeException:
            print('千牛刷新元素定位异常')
        except PocoTargetTimeout:
            print('刷新后没有正常返回首页')

    def get_sessionId(self):
        session_url = 'http://mitem.aiyongbao.com/tc/entry?appkey=21085832&appsecretb=MjM%3D&category=shangpinguanli&deviceuuid=9cfc46d073b3adea5c59922dd64b8497&from=qianniupc&nick=%E8%B5%B5%E4%B8%9C%E6%98%8A%E7%9A%84%E6%B5%8B%E8%AF%95%E5%BA%97%E9%93%BA:%E6%B5%8B%E8%AF%951&sdkversion=107005&seller_id=3936370796&sessionkey=50008101825uziqd0PEWgfQfPU0jhlQL4hwUl1440d8d0C4FRwEuoXywOmdefbVgg&sign=417845CC9E2F7832359351803FD27900&slot=qianniu×tamp=1585881161280&user_id=3936370796&version=7.17.03N'
        result = requests.get(session_url)
        phpsessid = re.findall(r"PHPSESSID=(.+?);", result.headers['Set-Cookie'])[0]
        return phpsessid

    # 获取手机详情全店任务执行的宝贝总数
    def get_mdetail_full_shop_total_num(self):
        url = 'https://mitem.aiyongbao.com//newmitem/getNewOneTouch'
        headers = {
            'User-Agent': 'python'
        }
        params = {
            "id": self.get_mdetail_full_shop_taskid()
        }
        cookies = {'PHPSESSID': self.get_sessionId()}
        r = requests.get(url, params=params, headers=headers, cookies=cookies)
        res = json.loads(r.content)
        return res[0].get('itemcount_total')

    # 获取手机详情全店任务的id
    def get_mdetail_full_shop_taskid(self):
        url = 'https://item.aiyongbao.com/wireless/selectUserLastTime'
        headers = {
            'User-Agent': 'python'
        }
        params = {
            "trade_source": "TAO"
        }
        cookies = {'PHPSESSID': self.get_sessionId()}
        r = requests.post(url, params=params, headers=headers, cookies=cookies)
        res = json.loads(r.content)
        return res[-1].get('id')

    # 同级快捷填充
    def super_add(self, element, text):
        text_edit = element
        text_edit.offspring('android.widget.EditText').set_text(text)

    # 方法：关闭自动上下架
    def close_auto_list(self):
        url = "https://item.aiyongbao.com/Autoadjust/waresSW"
        headers = {
            'User-Agent': 'python'
        }
        params = {
            'sel': 'off',
            'trade_source': 'TAO'
        }
        cookies = {'PHPSESSID': self.get_sessionId()}
        requests.get(url, params=params, headers=headers, cookies=cookies)

    # 方法：跳转qap页面，检查千牛是否授权
    def check_QN_auth(self):
        try:
            poco(text='立即授权').wait_for_appearance(2)
            poco(text='立即授权').click()
        except PocoTargetTimeout:
            pass

    # 方法：跳转qap页面，检查商品是否需要重新授权
    def check_AYitem_auth(self):
        try:
            poco(text='联系主账号授权').wait_for_appearance(5)
            poco(text='取消').click()
        except PocoTargetTimeout:
            pass

    # 方法：增加账号到期时间
    def edit_viptime(self):
        url = "http://crm.aiyongbao.com/testtools/changeAccountTime"
        headers = {
            'User-Agent': 'python'
        }
        params = {
            'nick': '赵东昊的测试店铺',
            'app': 'item',
            'time': '100'
        }
        cookies = {'PHPSESSID': self.get_sessionId()}
        requests.get(url, params=params, headers=headers, cookies=cookies)

    # 方法：关闭公告
    def close_notice(self):
        try:
            poco(text='公告').wait_for_appearance(3)
            # 关闭公告
            locate_by_anchor(poco(text='公告'), 2, 'l2').click()
        except PocoTargetTimeout:
            pass

    # 方法：异步加载时，点击特定元素
    def element_click_async(self, my_locator: tuple):
        element = UIObjectProxy(poco)
        element.query = my_locator
        self.page_swipe_top()
        element.invalidate()
        element.click()


if __name__ == '__main__':
    def print_demo(parm_demo='xxx'):
        print(parm_demo)


    print_demo(123)
