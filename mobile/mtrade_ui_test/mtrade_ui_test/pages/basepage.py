import json
import re
import time
import jsonpath
import requests
import random
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.proxy import UIObjectProxy
from mobile.mitem_ui_test.mitem_ui_test.utils import *

options = {'pre_action_wait_for_appearance': 6, 'action_interval': 0.8, 'poll_interval': 1.44}  # 默认值分别为6, 0.8, 1.44
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False, **options)


def init_element(locator: tuple) -> UIObjectProxy:
    """
    逻辑
    :param locator: 参数
    :return:
    """
    element = UIObjectProxy(poco)
    element.query = locator
    return element


def ay_swipe(my_loc: tuple, direction: str, sleep_time: int = 2) -> None:
    """
    :param sleep_time: 滑动操作容易导致点错元素，封装默认等待时间2秒
    :param my_loc:定位字符串
    :param direction:滑动方向
    :return:
    """
    element = init_element(my_loc)
    if direction not in ['left', 'right', 'up', 'down']:
        print('方向参数设置错误，只能是left,right其中之一')
        return None
    if direction == 'left':
        element.swipe([-1, 0])
    elif direction == 'right':
        element.swipe([1, 0])
    elif direction == 'up':
        element.swipe([0, -1])
    elif direction == 'down':
        element.swipe(([0, 1]))
    time.sleep(sleep_time)

def swipe_to_element(my_loc: tuple, target_loc: tuple, sleep_time: int = 2) -> None:
    """
    :param sleep_time: 滑动操作容易导致点错元素，封装默认等待时间2秒
    :param my_loc:滑动元素定位字符串
    :param target_loc:目标元素定位字符串
    滑动后的效果为初始定位元素的位置显示期望被滑动的位置
    :return:
    """
    element = init_element(my_loc)
    element_pos = element.attr('pos')
    target_element = init_element(target_loc)
    target_element_pos = target_element.attr('pos')
    element.swipe([element_pos[0] - target_element_pos[0], 0])
    element.swipe([0, element_pos[1] - target_element_pos[1]])

    time.sleep(sleep_time)


# 方法：点击特定元素
def ay_click(my_loc):
    element = init_element(my_loc)
    element.click()


# 方法：特定元素输入内容
def ay_set_text(my_loc, my_text):
    element = init_element(my_loc)
    element.set_text(my_text)


# 方法：特定元素是否存在
def ay_exists(my_loc):
    element = init_element(my_loc)
    return element.exists()


# 方法：获取特定元素的文本内容
def ay_get_text(my_loc):
    element = init_element(my_loc)
    return element.get_text()


def get_text_of_view(element: UIObjectProxy):
    while len(element.offspring('android.view.View')) and not element.attr('text'):
        element = element.offspring('android.view.View')
    return element.get_text()

def get_random_number(m:int):
    return random.randint(0,m-1)


def randomize(element) -> UIObjectProxy:
    length = len(element)
    index = get_random_number(length)
    return element[index]


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


def get_offspring_by_index(element_p, path_list=None):  # ''
    if path_list is None:
        path_list = []
    length = len(path_list)
    result = get_child_by_index(element_p, path_list[0][0], path_list[0][1])
    if length == 1:
        return result
    else:
        return get_offspring_by_index(result, path_list[1:length])


def trans_child_level(child_lv: str):
    i = 0
    temp2 = []
    temp3 = []
    try:
        while i < len(child_lv):
            temp2.append(child_lv[i:i + 2])  # 将字符串进行两个一组的拆分并放入temp2中，如v0l1l2拆成['v0','l1','l2']
            i += 2
        for j in temp2:
            temp3.append((j[0], int(j[1])))  # 遍历temp2,将字符串拆成单一的字符后再构造成元组，存入temp3中，得到[(v,0),(l,1),(l,2)]
        return temp3
    except Exception:
        print('传入参数不合法')


def get_parent_by_level(element: UIObjectProxy, level=1):
    if level <= 1:
        return element.parent()
    else:
        return get_parent_by_level(element.parent(), level - 1)


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


def get_sessionId() -> str:
    """
    通用方法，获取phpsessionId
    :return: str
    """
    session_url = 'http://mtrade.aiyongbao.com/tc/entry?appkey=21085840&appsecretb=YTg%3D&category=jiaoyiguanli' \
                  '&deviceuuid=7a6077f7ba9c6fcda1ce91dbaad3bd3e&from=qianniupc&nick=%E8%B5%B5%E4%B8%9C%E6%98%8A%E7%9A' \
                  '%84%E6%B5%8B%E8%AF%95%E5%BA%97%E9%93%BA:guchao&sdkversion=107005&seller_id=3936370796&sessionkey' \
                  '=80008600403w1of10024fe6hvQlyDiAwxqqEdZmvdqpBuSHXgdTAPUVlKDuGvkz9HJg2lzWRs&sign' \
                  '=D3242C38B4247A1A63B7B12A8812B5AB&slot=qianniu&timestamp=1571644334340&user_id=3941710226&version' \
                  '=7.12.02N '
    result = requests.get(session_url)
    phpsessid = re.findall(r"PHPSESSID=(.+?);", result.headers['Set-Cookie'])[0]

    return phpsessid

#获取待评价数量
def get_rate_num():
    url = 'https://trade.aiyongbao.com/aiyongTrade/base.list.get'
    headers = {
        'User-Agent': 'python'
    }
    params = {
        "fields": 'promise_service,collect_time,delivery_time,dispatch_time,sign_time,cutoff_minutes,es_date,es_range,os_date,os_range,timing_promise,num,buyer_alipay_no,step,modified,timeout_action_time,end_time,pay_time,consign_time,rate_status,seller_nick,shipping_type,cod_status,orders.oid,orders.oid_str,orders.outer_iid,orders.outer_sku_id,orders.consign_time,tid,tid_str,status,end_time,buyer_nick,trade_from,credit_card_fee,buyer_rate,seller_rate,created,num,payment,pic_path,has_buyer_message,receiver_country,receiver_state,receiver_city,receiver_district,receiver_town,receiver_address,receiver_zip,receiver_name,receiver_mobile,receiver_phone,orders.timeout_action_time,orders.end_time,orders.title,orders.status,orders.price,orders.payment,orders.sku_properties_name,orders.num_iid,orders.refund_id,orders.pic_path,orders.refund_status,orders.num,orders.logistics_company,orders.invoice_no,orders.adjust_fee,seller_flag,type,post_fee,has_yfx,yfx_fee,buyer_message,buyer_flag,buyer_memo,seller_memo,orders.seller_rate,adjust_fee,invoice_name,invoice_type,invoice_kind,promotion_details,alipay_no,buyerTaxNO,pbly,orders,total_fee,orders.cid,service_orders.tmser_spu_code,step_trade_status,step_paid_fee,send_time',
        "type": 'fixed,auction,guarantee_trade,step,independent_simple_trade,independent_shop_trade,auto_delivery,ec,cod,game_equipment,shopex_trade,netcn_trade,external_trade,instant_trade,b2c_cod,hotel_trade,super_market_trade,super_market_cod_trade,taohua,waimai,nopaid,eticket,tmall_i18n,o2o_offlinetrade',
        "pageSize": "20",
        "pageNo": "1",
        "status": "TRADE_FINISHED",
        "rate_status": "RATE_UNSELLER",
        "trade_source": "TAO"
    }
    cookies = {'PHPSESSID': get_sessionId()}
    r = requests.post(url, params=params, headers=headers, cookies=cookies)
    res = json.loads(r.content)
    return jsonpath.jsonpath(res, '$..total_results')[0]


def get_multiple_packages_logistics_fromTAO(tid):
    logistics_detail = {}
    for sub_tid in get_order_detail(tid)['子订单号']:
        url = "http://crm.aiyongbao.com/testtools/getOfficialApi"
        headers = {
            'User-Agent': 'python'
        }
        params = {
            'nick': '赵东昊的测试店铺',
            'method': 'taobao.logistics.trace.search',
            'param[tid]': tid,
            'param[is_split]': '1',
            'param[sub_tid]': sub_tid,
        }
        cookies = {'PHPSESSID': get_sessionId()}
        r = requests.post(url, params=params, headers=headers, cookies=cookies)

        res = json.loads(r.content)
        logistics_news = [jsonpath.jsonpath(res, '$..company_name'), jsonpath.jsonpath(res, '$..out_sid'),
                          jsonpath.jsonpath(res, '$..status_desc')[-1]]
        if logistics_news in logistics_detail.values():
            continue
        else:
            logistics_detail[sub_tid] = logistics_news

    return logistics_detail


# 获取物流信息
def get_logistics_from_tao(tid):
    url = "http://crm.aiyongbao.com/testtools/getOfficialApi"
    headers = {
        'User-Agent': 'python'
    }
    params = {
        'nick': '赵东昊的测试店铺',
        'method': 'taobao.logistics.trace.search',
        'param[tid]': tid
    }
    cookies = {'PHPSESSID': get_sessionId()}
    r = requests.post(url, params=params, headers=headers, cookies=cookies)
    logistics_detail = {}
    res = json.loads(r.content)

    try:
        logistics_detail['物流公司'] = jsonpath.jsonpath(res, '$..company_name')[0]
    except Exception as e:
        print(e)
    logistics_detail['运单号'] = jsonpath.jsonpath(res, '$..out_sid')[0]
    logistics_detail['物流消息'] = jsonpath.jsonpath(res, '$..status_desc')[0]
    logistics_detail['最新物流消息'] = jsonpath.jsonpath(res, '$..status_desc')[-1]
    return logistics_detail


def get_logistics_choose(tid):
    # len(get_order_detail(tid)['子订单号'])  处理合单订单使用
    if len(list(get_order_detail(tid)['运单号'])) > 1 and get_order_detail(tid)['订单状态'] == 'WAIT_BUYER_CONFIRM_GOODS':
        return get_multiple_packages_logistics_fromTAO(tid)
    else:
        return get_logistics_from_tao(tid)


# 获取卖家地址库地址
def get_seller_address():
    url = "http://crm.aiyongbao.com/testtools/getOfficialApi"
    headers = {
        'User-Agent': 'python'
    }
    params = {
        'nick': '赵东昊的测试店铺',
        'method': 'taobao.logistics.address.search',
        'param[rdef]': '',
    }
    cookies = {'PHPSESSID': get_sessionId()}
    r = requests.post(url, params=params, headers=headers, cookies=cookies)

    res = json.loads(r.content)
    address_result = jsonpath.jsonpath(res, '$..address_result')[0]
    # print(address_result)
    name_list = []
    mobile_phone_list = []
    addr_news_list = []
    if len(address_result) == 1:
        name = address_result[0]['contact_name']
        province = address_result[0]['province']
        city = address_result[0]['city']
        country = address_result[0]['country']
        address = address_result[0]['addr']
        mobile_phone = address_result[0]['mobile_phone']
        addr_news = province + ' ' + city + ' ' + country + ' ' + address
        return name, mobile_phone, addr_news
    else:
        for i in range(len(address_result)):
            name = address_result[i]['contact_name']
            province = address_result[i]['province']
            city = address_result[i]['city']
            country = address_result[i]['country']
            address = address_result[i]['addr']
            mobile_phone = address_result[i]['mobile_phone']
            addr_news = province + ' ' + city + ' ' + country + ' ' + address
            name_list.append(name)
            mobile_phone_list.append(mobile_phone)
            addr_news_list.append(addr_news)
        return name_list, mobile_phone_list, addr_news_list


def get_order_check_send():
    url = "https://trade.aiyongbao.com/set/updateDetectSet"
    headers = {
        'User-Agent': 'python'
    }
    params = {
        'type': 'get',
        'trade_source': 'TAO',
    }
    cookies = {'PHPSESSID': get_sessionId()}
    r = requests.post(url, params=params, headers=headers, cookies=cookies)

    res = json.loads(r.content)
    addrKeyWord = jsonpath.jsonpath(res, '$..addrKeyWord')
    buyerToMeBad = jsonpath.jsonpath(res, '$..buyerToMeBad')
    dangerTrade = jsonpath.jsonpath(res, '$..dangerTrade')
    moreBad = jsonpath.jsonpath(res, '$..moreBad')
    results = {'中差评': buyerToMeBad, '留言信息': dangerTrade, '收货地址': addrKeyWord, '5次差评': moreBad}
    return results


# 获取差评拦截开关状态
def get_interception_status():
    url = "https://trade.aiyongbao.com/defence/getsummary"
    headers = {
        'User-Agent': 'python'
    }
    params = {
        'type': 'get',
        'trade_source': 'TAO',
    }
    cookies = {'PHPSESSID': get_sessionId()}
    r = requests.post(url, params=params, headers=headers, cookies=cookies)
    res = json.loads(r.content)
    results = {
        #'addbiew': True if 'on' in res['addbiew'] else False,
        'addblack': True if 'on' in res['addblack'] else False,
        'areaon': True if 'on' in res['areaon'] else False,
        'babynum': True if 'on' in res['babynum'] else False,
        'babynumless': True if 'on' in res['babynumless'] else False,
        'babyon': True if 'on' in res['babyon'] else False,
        'bigmoney': True if 'on' in res['bigmoney'] else False,
        'carnum': True if 'on' in res['carnum'] else False,
        'carnumless': True if 'on' in res['carnumless'] else False,
        'conditions': True if 'on' in res['conditions'] else False,
        'conon': True if 'on' in res['conon'] else False,
        #'credit': True if 'on' in res['credit'] else False,
        'denfenon': True if 'on' in res['denfenon'] else False,
        # goodrate
        #'goodrate': True if 'on' in res['goodrate'] else False,
        'handon': True if 'on' in res['handon'] else False,
        'neutralon': True if 'on' in res['neutralon'] else False,
        'noalipay': True if 'on' in res['noalipay'] else False,
        # 'optime': res['optime'],
        # 'phone':  res['phone'],
        #'publicon': True if 'on' in res['publicon'] else False,
        # regdays
        #'regdays': True if 'on' in res['regdays'] else False,
        # 'sellernote': res['sellernote'],
        #'sendsms': True if 'on' in res['sendsms'] else False,
        'smallmoney': True if 'on' in res['smallmoney'] else False,
        'whiteon': True if 'on' in res['whiteon'] else False,
        'wwon': True if 'on' in res['wwon'] else False
    }
    sum_results = True
    for k in results:
        sum_results = sum_results and results[k]
    return sum_results,results


# 获取拦截记录
def get_interception_news():
    url = "https://trade.aiyongbao.com/Iytrade2/getblacklist"
    headers = {
        'User-Agent': 'python'
    }
    params = {
        'page_no': '1',
        'trade_source': 'TAO',
    }
    cookies = {'PHPSESSID': get_sessionId()}
    r = requests.post(url, params=params, headers=headers, cookies=cookies)

    res = json.loads(r.content)
    tid_list = jsonpath.jsonpath(res, '$..tid')
    return tid_list[0:5]


def get_full_order_detail(order_no: str) -> dict:
    """
    根据订单号获取完整的订单信息
    :param order_no: 订单号
    :return: dict
    https://trade.aiyongbao.com/aiyongTrade/base.list.get
    """
    url = 'https://trade.aiyongbao.com/aiyongTrade/detail.info.get'
    headers = {
        'User-Agent': 'python'
    }
    params = {
        "fields": 'promise_service,collect_time,delivery_time,dispatch_time,sign_time,cutoff_minutes,es_date,'
                  'es_range,os_date,os_range,timing_promise,num,buyer_alipay_no,step,modified,timeout_action_time,'
                  'end_time,pay_time,consign_time,rate_status,seller_nick,shipping_type,cod_status,orders.oid,'
                  'orders.oid_str,orders.outer_iid,orders.outer_sku_id,orders.consign_time,tid,tid_str,status,'
                  'end_time,buyer_nick,trade_from,credit_card_fee,buyer_rate,seller_rate,created,num,payment,'
                  'pic_path,has_buyer_message,receiver_country,receiver_state,receiver_city,receiver_district,'
                  'receiver_town,receiver_address,receiver_zip,receiver_name,receiver_mobile,receiver_phone,'
                  'orders.timeout_action_time,orders.end_time,orders.title,orders.status,orders.price,orders.payment,'
                  'orders.sku_properties_name,orders.num_iid,orders.refund_id,orders.pic_path,orders.refund_status,'
                  'orders.num,orders.logistics_company,orders.invoice_no,orders.adjust_fee,seller_flag,type,post_fee,'
                  'has_yfx,yfx_fee,buyer_message,buyer_flag,buyer_memo,seller_memo,orders.seller_rate,adjust_fee,'
                  'invoice_name,invoice_type,invoice_kind,promotion_details,alipay_no,buyerTaxNO,pbly,orders,'
                  'total_fee,orders.cid,service_orders.tms er_spu_code,step_trade_status,step_paid_fee,send_time,'
                  'promise_service,timing_promise',
        "taoTid": order_no,
        "corpId": "3936370796",
        "sellerId": "3936370796",
        "userId": "3936370796",
        "nick": "赵东昊的测试店铺",
        "isVip": 1,
        "trade_source": "TAO"
    }
    cookies = {'PHPSESSID': get_sessionId()}
    r = requests.post(url, params=params, headers=headers, cookies=cookies)
    return r.text


# 方法：获取自己联系、在线下单的默认物流
def get_default_logistic():
    url = 'https://trade.aiyongbao.com/iytrade2/getSend'
    headers = {
        'User-Agent': 'python'
    }
    params = {
        'trade_source': 'TAO',
    }
    cookies = {'PHPSESSID': get_sessionId()}
    r = requests.get(url, params=params, headers=headers, cookies=cookies)
    default_logistic = {'自己联系默认物流': jsonpath.jsonpath(r.json(), '$..name')[0],
                        '在线下单默认物流': jsonpath.jsonpath(r.json(), '$..name')[1]}
    return default_logistic


# 方法：调用ratebalckname接口，获取自动评价黑名单信息
def api_blacklist_info_auto_evaluate():
    url = 'https://trade.aiyongbao.com/iytrade2/ratebalckname?'
    headers = {
        'User-Agent': 'python'
    }
    parmas = {
        'page': 1,
        'trade_source': 'TAO'
    }
    cookies = {
        'PHPSESSID': get_sessionId()
    }
    resp = requests.get(url, headers=headers, params=parmas, cookies=cookies)
    return resp.text


# 方法：调用showzdrate接口，获取自动评价短语信息
def api_auto_evaluate_phrase():
    url = 'https://trade.aiyongbao.com/iytrade2/showzdrate?trade_source=TAO'
    headers = {
        'User-Agent': 'python'
    }
    parmas = {
        'trade_source': 'TAO'
    }
    cookies = {
        'PHPSESSID': get_sessionId()
    }
    resp = requests.get(url, params=parmas, headers=headers, cookies=cookies)
    return resp.text


def get_order_detail(order_no: str) -> dict:
    """
    根据需要组装需要的订单信息字段，可自由扩充
    :param order_no: 订单号
    :return: dict
    """
    order_detail = {}
    res = json.loads(get_full_order_detail(order_no))
    # 先列出显示在页面上的属性
    if jsonpath.jsonpath(res, '$..receiver_mobile'):
        order_detail['收件人手机'] = jsonpath.jsonpath(res, '$..receiver_mobile')[0]  # 手机号一定存在
        order_detail['收件人手机f'] = (jsonpath.jsonpath(res, '$..receiver_mobile')[0])  # 使用-连接符格式化后的手机号
    if jsonpath.jsonpath(res, '$..buyer_nick'):
        order_detail['买家昵称'] = jsonpath.jsonpath(res, '$..buyer_nick')[0]  # 买家昵称一定存在
    if jsonpath.jsonpath(res, '$..title'):
        order_detail['商品标题'] = jsonpath.jsonpath(res, '$..title')[0]  # 商品标题一定存在
    full_address = gen_full_address(**res)  # 调用gen_full_address方法拼接地址
    order_detail['收件地址'] = full_address  # 收件地址一定存在
    if jsonpath.jsonpath(res, '$..receiver_name'):
        order_detail['收件人姓名'] = jsonpath.jsonpath(res, '$..receiver_name')[0]  # 收件人姓名一定存在
    sku_properties_name_list = gen_sku_properties_name(**res)  # 调用gen_sku_properties_name，构造完整的商品属性列表，可能不存在
    order_detail['商品属性'] = sku_properties_name_list
    status_dict = {'WAIT_SELLER_SEND_GOODS': '待发货', 'TRADE_FINISHED': '已成功', 'TRADE_CLOSED': '已关闭',
                   'TRADE_CLOSED_BY_TAOBAO': '已关闭', 'WAIT_BUYER_CONFIRM_GOODS': '已发货'}  # 不完整，暂不使用，后续优化
    if jsonpath.jsonpath(res, '$..status'):
        order_detail['订单状态'] = jsonpath.jsonpath(res, '$..status')[0]  # 订单状态一定存在
    if jsonpath.jsonpath(res, '$..created'):
        order_detail['拍下时间'] = jsonpath.jsonpath(res, '$..created')[0]  # 拍下时间，订单创建时间，一定存在
    if jsonpath.jsonpath(res, '$..seller_memo'):
        order_detail['备注'] = jsonpath.jsonpath(res, '$..seller_memo')[0]  # 备注，一定存在，可能为空值
    if jsonpath.jsonpath(res, '$..outer_sku_id'):
        order_detail['商品编码'] = '商家编码：' + jsonpath.jsonpath(res, '$..outer_sku_id')[0]  # 商家编码：编码01，可能不存在
    if jsonpath.jsonpath(res, '$..has_buyer_message'):
        order_detail['有留言'] = jsonpath.jsonpath(res, '$..has_buyer_message')[0]  # 判断是否由留言，一定存在
    if jsonpath.jsonpath(res, '$..pay_time'):
        order_detail['付款时间'] = jsonpath.jsonpath(res, '$..pay_time')[0]  # 付款时间，可能不存在
    if jsonpath.jsonpath(res, '$..consign_time'):
        order_detail['发货时间'] = jsonpath.jsonpath(res, '$..consign_time')[0]  # 发货时间，可能不存在
    if jsonpath.jsonpath(res, '$..seller_flag'):
        order_detail['flag'] = jsonpath.jsonpath(res, '$..seller_flag')[0]  # 备注小旗 0-5对应灰红黄绿蓝紫
    if jsonpath.jsonpath(res, '$..refund_status'):
        order_detail['退款状态'] = jsonpath.jsonpath(res, '$..refund_status')[0]  # 退款状态
    if jsonpath.jsonpath(res, '$..tid'):
        order_detail['订单号'] = jsonpath.jsonpath(res, '$..tid')[0]
    if jsonpath.jsonpath(res, '$..consign_time'):
        order_detail['收货时间'] = jsonpath.jsonpath(res, '$..consign_time')[0]
    if jsonpath.jsonpath(res, '$..timeout_action_time'):
        order_detail['预计结束时间'] = jsonpath.jsonpath(res, '$..timeout_action_time')[0]  # 可能不存在该字段
    if jsonpath.jsonpath(res, '$..seller_rate'):
        order_detail['评价状态'] = jsonpath.jsonpath(res, '$..seller_rate')[0]
    if jsonpath.jsonpath(res, '$..oid'):
        order_detail['子订单号'] = jsonpath.jsonpath(res, '$..oid')[0]
    if jsonpath.jsonpath(res, '$..invoice_no'):
        order_detail['运单号'] = set(jsonpath.jsonpath(res, '$..invoice_no'))
    if jsonpath.jsonpath(res, '$..buyer_message'):
        order_detail['留言'] = jsonpath.jsonpath(res, '$..buyer_message')[0]
    return order_detail


def get_order_print_history(order_no):
    url = 'https://trade.aiyongbao.com/print/getPrintWeightHistory'
    headers = {
        'User-Agent': 'python'
    }
    params = {
        "tid[0]": order_no,
        "wayTid[0]": order_no,
        "aiyongSend[0]": order_no,
        "msg_tid[0]": order_no,
        "redis_tid[0]": order_no,
        "wwcf_tid[0]": order_no,
        "trade_source": "TAO"
    }
    cookies = {'PHPSESSID': get_sessionId()}
    print_history_info = {}
    r = requests.post(url, params=params, headers=headers, cookies=cookies)
    res = json.loads(r.content)
    print_history_info['绑定的单号'] = jsonpath.jsonpath(res, '$..voice')
    print_history_info['绑定的物流公司'] = jsonpath.jsonpath(res, '$..Delivercompany')
    return print_history_info


# 获取待处理差评
def get_pending_bad_evalution_number(strdate):
    url = 'http://crm.aiyongbao.com/testtools/getOfficialApi'
    headers = {
        'User-Agent': 'python'
    }
    params = {
        "nick": '赵东昊的测试店铺',
        "method": 'taobao.traderates.get',
        "param[fields]": 'tid,oid,role,nick,result,created,rated_nick,item_title,item_price,content,reply,num_iid',
        "param[rate_type]": 'get',
        "param[role]": 'buyer',
        "param[result]": 'bad',
        "param[start_date]": strdate
    }
    cookies = {'PHPSESSID': get_sessionId()}
    r = requests.get(url, params=params, headers=headers, cookies=cookies)
    pending_bad_evalution_number = {}
    res = json.loads(r.content)
    pending_bad_evalution_number['总数'] = jsonpath.jsonpath(res, '$..total_results')[0]
    return str(pending_bad_evalution_number['总数'])


def gen_full_address(**order_detail: dict) -> str:
    """
    拼接字符串形成完整的收货地址
    :param order_detail: 由接口返回订单信息，接口中的receiver_district字段放弃使用
    :return: 收货地址字符串
    """
    full_address_temp = []
    if jsonpath.jsonpath(order_detail, '$..receiver_state'):
        full_address_temp.append(jsonpath.jsonpath(order_detail, '$..receiver_state')[0])  # 省
    if jsonpath.jsonpath(order_detail, '$..receiver_city'):
        full_address_temp.append(jsonpath.jsonpath(order_detail, '$..receiver_city')[0])
    if jsonpath.jsonpath(order_detail, '$..receiver_district'):
        full_address_temp.append(jsonpath.jsonpath(order_detail, '$..receiver_district')[0])
    if jsonpath.jsonpath(order_detail, '$..receiver_address'):
        full_address_temp.append(jsonpath.jsonpath(order_detail, '$..receiver_address')[0])
    if jsonpath.jsonpath(order_detail, '$..receiver_zip'):
        if jsonpath.jsonpath(order_detail, '$..receiver_zip')[0] != '000000':
            full_address_temp.append(jsonpath.jsonpath(order_detail, '$..receiver_zip')[0])
    full_address = '，'.join(full_address_temp)  # 使用中文逗号拼接成完整地址
    return full_address


def gen_sku_properties_name(**order_detail: dict) -> list or None:
    """
    拼接用户界面上显示的商品属性
    :param order_detail: 订单信息dict
    :return: list or None
    """
    if jsonpath.jsonpath(order_detail, '$..sku_properties_name'):
        sku_properties_name_list_temp = jsonpath.jsonpath(order_detail, '$..sku_properties_name')[0].split(';')
        sku_properties_name_list = []
        for sku_properties_name in sku_properties_name_list_temp:
            sku_properties_name_list.append(sku_properties_name.split(':')[
                                                -1])  # 商品属性可能为多个，构造列表存放 原始数据示例："sku_properties_name":
            # "尺寸:50X50cm;颜色分类:宝蓝色;材质:泰麂绒"
        return sku_properties_name_list


# 获取待发货数量
def get_wait_send_goods_number():
    url = 'http://crm.aiyongbao.com/testtools/getOfficialApi'
    headers = {
        'User-Agent': 'python'
    }
    params = {
        "nick": '赵东昊的测试店铺',
        "method": 'taobao.trades.sold.get',
        "param[fields]": 'promise_service,collect_time,delivery_time,dispatch_time,sign_time,cutoff_minutes,es_date,es_range,os_date,os_range,timing_promise,num,buyer_alipay_no,step,modified,timeout_action_time,end_time,pay_time,consign_time,rate_status,seller_nick,shipping_type,cod_status,orders.oid,orders.oid_str,orders.outer_iid,orders.outer_sku_id,orders.consign_time,tid,tid_str,status,end_time,buyer_nick,trade_from,credit_card_fee,buyer_rate,seller_rate,created,num,payment,pic_path,has_buyer_message,receiver_country,receiver_state,receiver_city,receiver_district,receiver_town,receiver_address,receiver_zip,receiver_name,receiver_mobile,receiver_phone,orders.timeout_action_time,orders.end_time,orders.title,orders.status,orders.price,orders.payment,orders.sku_properties_name,orders.num_iid,orders.refund_id,orders.pic_path,orders.refund_status,orders.num,orders.logistics_company,orders.invoice_no,orders.adjust_fee,seller_flag,type,post_fee,has_yfx,yfx_fee,buyer_message,buyer_flag,buyer_memo,seller_memo,orders.seller_rate,adjust_fee,invoice_name,invoice_type,invoice_kind,promotion_details,alipay_no,buyerTaxNO,pbly,orders,total_fee,orders.cid,service_orders.tmser_spu_code,step_trade_status,step_paid_fee,send_time',
        "param[status]": 'WAIT_SELLER_SEND_GOODS'
    }
    cookies = {'PHPSESSID': get_sessionId()}
    r = requests.get(url, params=params, headers=headers, cookies=cookies)
    wait_send_goods_number = {}
    res = json.loads(r.content)
    wait_send_goods_number['总数'] = jsonpath.jsonpath(res, '$..total_results')[0]
    wait_send_goods_number['订单号'] = jsonpath.jsonpath(res, '$..tid')
    return str(wait_send_goods_number['总数'])


# 获取待处理中评
def get_pending_interim_evalution_number(strdate):
    url = 'http://crm.aiyongbao.com/testtools/getOfficialApi'
    headers = {
        'User-Agent': 'python'
    }
    params = {
        "nick": '赵东昊的测试店铺',
        "method": 'taobao.traderates.get',
        "param[fields]": 'tid,oid,role,nick,result,created,rated_nick,item_title,item_price,content,reply,num_iid',
        "param[rate_type]": 'get',
        "param[role]": 'buyer',
        "param[result]": 'neutral',
        "param[start_date]": strdate
    }
    cookies = {'PHPSESSID': get_sessionId()}
    r = requests.get(url, params=params, headers=headers, cookies=cookies)
    pending_interim_evalution_number = {}
    res = json.loads(r.content)
    pending_interim_evalution_number['总数'] = jsonpath.jsonpath(res, '$..total_results')[0]
    return str(pending_interim_evalution_number['总数'])


# 获取待评价
def get_to_be_evaluated_number():
    url = 'https://trade.aiyongbao.com/aiyongTrade/base.list.get'
    headers = {
        'User-Agent': 'python'
    }
    params = {

        "fields": 'promise_service,collect_time,delivery_time,dispatch_time,sign_time,cutoff_minutes,es_date,es_range,os_date,os_range,timing_promise,num,buyer_alipay_no,step,modified,timeout_action_time,end_time,pay_time,consign_time,rate_status,seller_nick,shipping_type,cod_status,orders.oid,orders.oid_str,orders.outer_iid,orders.outer_sku_id,orders.consign_time,tid,tid_str,status,end_time,buyer_nick,trade_from,credit_card_fee,buyer_rate,seller_rate,created,num,payment,pic_path,has_buyer_message,receiver_country,receiver_state,receiver_city,receiver_district,receiver_town,receiver_address,receiver_zip,receiver_name,receiver_mobile,receiver_phone,orders.timeout_action_time,orders.end_time,orders.title,orders.status,orders.price,orders.payment,orders.sku_properties_name,orders.num_iid,orders.refund_id,orders.pic_path,orders.refund_status,orders.num,orders.logistics_company,orders.invoice_no,orders.adjust_fee,seller_flag,type,post_fee,has_yfx,yfx_fee,buyer_message,buyer_flag,buyer_memo,seller_memo,orders.seller_rate,adjust_fee,invoice_name,invoice_type,invoice_kind,promotion_details,alipay_no,buyerTaxNO,pbly,orders,total_fee,orders.cid,service_orders.tmser_spu_code,step_trade_status,step_paid_fee,send_time',
        "type": 'fixed,auction,guarantee_trade,step,independent_simple_trade,independent_shop_trade,auto_delivery,ec,cod,game_equipment,shopex_trade,netcn_trade,external_trade,instant_trade,b2c_cod,hotel_trade,super_market_trade,super_market_cod_trade,taohua,waimai,nopaid,eticket,tmall_i18n,o2o_offlinetrade',
        "status": 'TRADE_FINISHED',
        "isVip": 1,
        "trade_source": 'TAO',
        "rate_status": 'RATE_UNSELLER'
    }
    cookies = {'PHPSESSID': get_sessionId()}
    r = requests.get(url, params=params, headers=headers, cookies=cookies)
    pending_interim_evalution_number = {}
    res = json.loads(r.content)
    pending_interim_evalution_number['总数'] = jsonpath.jsonpath(res, '$..total_results')[0]
    return str(pending_interim_evalution_number['总数'])


# 获取90天前时间
# def getdate(date_inter: num) 获取指定天数间隔后的日期
def getdate(day:int):
    """
    :return:
    """
    today = datetime.datetime.now()
    # 计算偏移量
    offset = datetime.timedelta(days=-day)
    # 获取想要的日期的时间
    re_date = (today + offset).strftime('%Y-%m-%d %H:%M:%S')
    return re_date


date_90 = getdate(90)
date_2 = getdate(2)

# 获取近90天漏评数量
def get_missing_evalution_number(strdate):
    url = 'http://crm.aiyongbao.com/testtools/getOfficialApi'
    headers = {
        'User-Agent': 'python'
    }
    params = {
        "nick": '赵东昊的测试店铺',
        "method": 'taobao.trades.sold.get',
        "param[fields]": 'promise_service,collect_time,delivery_time,dispatch_time,sign_time,cutoff_minutes,es_date,es_range,os_date,os_range,timing_promise,num,buyer_alipay_no,step,modified,timeout_action_time,end_time,pay_time,consign_time,rate_status,seller_nick,shipping_type,cod_status,orders.oid,orders.oid_str,orders.outer_iid,orders.outer_sku_id,orders.consign_time,tid,tid_str,status,end_time,buyer_nick,trade_from,credit_card_fee,buyer_rate,seller_rate,created,num,payment,pic_path,has_buyer_message,receiver_country,receiver_state,receiver_city,receiver_district,receiver_town,receiver_address,receiver_zip,receiver_name,receiver_mobile,receiver_phone,orders.timeout_action_time,orders.end_time,orders.title,orders.status,orders.price,orders.payment,orders.sku_properties_name,orders.num_iid,orders.refund_id,orders.pic_path,orders.refund_status,orders.num,orders.logistics_company,orders.invoice_no,orders.adjust_fee,seller_flag,type,post_fee,has_yfx,yfx_fee,buyer_message,buyer_flag,buyer_memo,seller_memo,orders.seller_rate,adjust_fee,invoice_name,invoice_type,invoice_kind,promotion_details,alipay_no,buyerTaxNO,pbly,orders,total_fee,orders.cid,service_orders.tmser_spu_code,step_trade_status,step_paid_fee,send_time',
        "param[rate_status]": 'RATE_UNSELLER',
        "param[status]": 'TRADE_FINISHED',
        "param[start_created]": strdate
    }
    cookies = {'PHPSESSID': get_sessionId()}
    r = requests.get(url, params=params, headers=headers, cookies=cookies)
    pending_interim_evalution_number = {}
    res = json.loads(r.content)
    pending_interim_evalution_number['总数'] = jsonpath.jsonpath(res, '$..total_results')[0]
    pending_interim_evalution_number['订单号'] = jsonpath.jsonpath(res, '$..tid')
    return str(pending_interim_evalution_number['总数'])


# 获取中评
def get_interim_evaluation_number():
    url = 'http://crm.aiyongbao.com/testtools/getOfficialApi'
    headers = {
        'User-Agent': 'python'
    }
    params = {
        "nick": '赵东昊的测试店铺',
        "method": 'taobao.traderates.get',
        "param[fields]": 'tid,oid,role,nick,result,created,rated_nick,item_title,item_price,content,reply,num_iid',
        "param[rate_type]": 'get',
        "param[role]": 'buyer',
        "param[result]": 'neutral'
    }
    cookies = {'PHPSESSID': get_sessionId()}
    r = requests.get(url, params=params, headers=headers, cookies=cookies)
    interim_evaluation_number = {}
    res = json.loads(r.content)
    interim_evaluation_number['总数'] = jsonpath.jsonpath(res, '$..total_results')[0]
    return str(interim_evaluation_number['总数'])


# 获取好评
def get_good_evaluation_number():
    url = 'http://crm.aiyongbao.com/testtools/getOfficialApi'
    headers = {
        'User-Agent': 'python'
    }
    params = {
        "nick": '赵东昊的测试店铺',
        "method": 'taobao.traderates.get',
        "param[fields]": 'tid,oid,role,nick,result,created,rated_nick,item_title,item_price,content,reply,num_iid',
        "param[rate_type]": 'get',
        "param[role]": 'buyer',
        "param[result]": 'good'
    }
    cookies = {'PHPSESSID': get_sessionId()}
    r = requests.get(url, params=params, headers=headers, cookies=cookies)
    good_evaluation_number = {}
    res = json.loads(r.content)
    good_evaluation_number['总数'] = jsonpath.jsonpath(res, '$..total_results')[0]
    return str(good_evaluation_number['总数'])


# 获取给他人评价数量
def get_to_others_evaluation_number():
    url = 'http://crm.aiyongbao.com/testtools/getOfficialApi'
    headers = {
        'User-Agent': 'python'
    }
    params = {
        "nick": '赵东昊的测试店铺',
        "method": 'taobao.traderates.get',
        "param[fields]": 'tid,oid,role,nick,result,created,rated_nick,item_title,item_price,content,reply,num_iid',
        "param[rate_type]": 'give',
        "param[role]": 'seller',
        # "param[result]" :'good'
    }
    cookies = {'PHPSESSID': get_sessionId()}
    r = requests.get(url, params=params, headers=headers, cookies=cookies)
    others_evaluation_number = {}
    res = json.loads(r.content)
    others_evaluation_number['总数'] = jsonpath.jsonpath(res, '$..total_results')[0]
    return str(others_evaluation_number['总数'])


# 获取差评
def get_bad_evaluation_number():
    url = 'http://crm.aiyongbao.com/testtools/getOfficialApi'
    headers = {
        'User-Agent': 'python'
    }
    params = {
        "nick": '赵东昊的测试店铺',
        "method": 'taobao.traderates.get',
        "param[fields]": 'tid,oid,role,nick,result,created,rated_nick,item_title,item_price,content,reply,num_iid',
        "param[rate_type]": 'get',
        "param[role]": 'buyer',
        "param[result]": 'bad'
    }
    cookies = {'PHPSESSID': get_sessionId()}
    r = requests.get(url, params=params, headers=headers, cookies=cookies)
    bad_evaluation_number = {}
    res = json.loads(r.content)
    bad_evaluation_number['总数'] = jsonpath.jsonpath(res, '$..total_results')[0]
    return str(bad_evaluation_number['总数'])

#超级点击
def super_click(element: UIObjectProxy):
    element.invalidate()
    element.click()

def time_calculation(start_time,end_time):
    date1 = datetime.datetime.strptime(start_time[0:10], "%Y-%m-%d")
    date2 = datetime.datetime.strptime(end_time[0:10], "%Y-%m-%d")
    num = (date2 - date1).days
    return num



class BasePage:
    # 刷新按钮
    refresh_locator = ('and', (('attr=', ('text', '刷新')),))
    # 返回按钮
    back_locator = ('and', (('attr=', ('name', 'com.taobao.qianniu:id/qn_widmill_nav_bar_back_btn')),))
    # 更多按钮
    more_locator = ('and', (('attr=', ('name', 'com.taobao.qianniu:id/qn_nav_menu_more_btn')),))
    # 关闭按钮
    close_locator = ('and', (('attr=', ('name', 'com.taobao.qianniu:id/qn_nav_menu_close_btn')),))

    def refresh(self):
        try:
            more_element = init_element(self.more_locator)
            refresh_element = init_element(self.refresh_locator)
            more_element.click()
            refresh_element.click()
            if poco(text='网页无法打开').exists():
                self.refresh()
        except Exception:
            return False

    def back(self):
        try:
            back_element = init_element(self.back_locator)
            back_element.click()
        except Exception:
            return False

    def close(self):
        try:
            close_element = init_element(self.close_locator)
            close_element.click()
        except Exception:
            return False

    @staticmethod
    def page_swipe():
        poco('android:id/content').swipe([0, -1])

    @staticmethod
    def page_swipe_for_custom(pos):
        poco('android:id/content').swipe([0, pos])
        time.sleep(3)

    def ensure_copy_info(self, copy_info):
        """
        验证剪贴版中文本是否与预期一致
        :param copy_info:
        :return:
        """
        self.refresh()  # 刷新进入首页
        poco(textMatches='订单号.*').click()  # 点击搜索栏
        poco('android.widget.EditText').long_click()  # 长按搜索栏文本框
        poco('android.widget.EditText').long_click()
        poco(text='粘贴').click()  # 选择粘贴
        poco('android.widget.EditText').invalidate()  # 重新定位搜索栏文本框，获得更新后的text属性
        actual = poco('android.widget.EditText').get_text()  # 保留文本框中的内容
        return copy_info == actual, actual  # 返回校验结果以及实际结果


if __name__ == '__main__':
    # s = get_sessionId()
    # print(s)
    # t = get_full_order_detail('919152672772620411')
    # print(t)
    #BasePage().page_swipe_for_custom(-0.7)
    # e = ('and', (('attr=', ('text', '关闭差评拦截开关')),))
    # t = ('and', (('attr=', ('text', '订单信息拦截')),))
    # t2 = ('and', (('attr=', ('text', '买家信息拦截')),))
    # swipe_to_element(e, t, 2)
    # swipe_to_element(t, t2, 2)
    a = '2020-06-03 23:44:44'
    b = '2020-06-04 23:44:44'
    print(time_calculation(a,b))