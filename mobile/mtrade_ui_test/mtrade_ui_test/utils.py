import datetime
import json
import logging
import os
import random
import string

root_path = os.path.dirname(os.path.abspath(__file__))


def format_mobile_number(phone: str) -> str:
    return phone[0:3] + '-' + phone[3:7] + '-' + phone[7:11]


def unformat_mobile_number(phone: str) -> str:
    return phone.replace('-', '')


def get_random_number(m: int) -> int:
    """
    获取随机正整数值
    :param m: 限制随机整数范围
    :return: 最小值0，最大值m-1
    """
    return random.randint(0, m - 1)


# 获取2天前时间
# beforeOfDay=2
def getdate_2():
    today = datetime.datetime.now()
    # 计算偏移量
    offset = datetime.timedelta(days=-2)
    # 获取想要的日期的时间
    re_date = (today + offset).strftime('%Y-%m-%d %H:%M:%S')
    return re_date


def get_current_time():
    now_time = datetime.datetime.now()
    return now_time.strftime('%Y%m%d_%H%M%S')  # 固定语法获取时间戳


# 生成随机8位快递单号
def gen_express_number():
    seeds = string.digits
    random_str = []
    for j in range(8):
        random_str.append(random.choice(seeds))
    return "".join(random_str)


date_2 = getdate_2()

if __name__ == '__main__':
    for i in range(15):
        print(get_random_number(5))
