import os
import shutil
import time

import pytest

from mobile.config.path_config import ITEM_ROOT, TRADE_ROOT

item_case_daily = ITEM_ROOT / "testsuite" / "test_daily_regress"
item_case_dev = ITEM_ROOT / "testsuite" / "test_for_developer"
item_case_temp =ITEM_ROOT / "testsuite" / "test_temp"

trade_case_daily = TRADE_ROOT / "testsuite" / "test_daily_regress"
trade_case_dev = TRADE_ROOT / "testsuite" / "test_for_developer"
trade_case_temp =TRADE_ROOT / "testsuite" / "test_temp"

# jenkins_report_dir = os.path.join(root_path, 'report_for_jenkins')  # 拼接字符串，使得每次能够能到不同的测试报告，防止测试结果数据冲突
item_img_dir = ITEM_ROOT / "static" / "images"
trade_img_dir = TRADE_ROOT / "static" / "images"

item_test_case_map = {
    'test_badword_detect.py': '违规词检测',
    'test_batch_update.py': '批量修改',
    'test_detail_page.py': '详情页',
    'test_item_list.py': '列表页',
    'test_mdetail.py': '手机详情',
    'test_shop_medical.py': '店铺体检',
    'test_title_improve.py': '标题优化'
}

item_test_case_conf_dict = {
    '违规词检测': True,
    '批量修改': True,
    '详情页': True,
    '列表页': True,
    '手机详情': True,
    '店铺体检': True,
    '标题优化': True,
}


def read_case_module(_case_dir):
    """
    读取所有可用的测试模块
    :return:
    """
    name = os.listdir(_case_dir)
    case_list = []
    for _name in name:
        if _name.startswith('test.txt') and _name.endswith('py'):
            case_name_zh = item_test_case_map.get(_name)
            if case_name_zh:
                case_list.append(case_name_zh)
    return case_list


#  allure generate report/xml -o report/html --clean
def run_with_report(_case_dir: str, _report_dir: str) -> None:
    """
    执行测试用例，并得到allure report
    :param _case_dir: 测试用例目录，应当是test开头的文件夹
    :param _report_dir: 测试报告目录
    :return:
    """
    mkdir(_report_dir)
    pytest.main([_case_dir, '-vv', '--reruns=2', '--reruns-delay=2',
                 '--alluredir={}/xml'.format(_report_dir)])
    # 常用参数说明:
    # -n=auto,需要安装pytest-xdist，自动根据电脑配置启用多线程执行测试用例，要求测试用例之间不能有依赖性，对设计要求较高，更多适用于API测试提高执行效率,如果是UI测试则需多设备
    # --reruns,--reruns-delay,需要安装pytest-rerunfailures，表示用例执行失败时自动重试的次数，以及两次重试之间的间隔
    # --alluredir 指定测试结果文件存在路径
    # --vv 显示详细结果
    # -q 显示简易测试结果
    # -s 显示用例中的print语句输出结果
    # 其他使用的pytest插件可以参考链接 https://www.cnblogs.com/peng-lan/p/11511569.html
    # pytest 推荐教程 https://www.jianshu.com/p/4ee3a0dd37c5
    os.system(r'allure generate {}/xml -o {}/html --clean'.format(_report_dir, _report_dir))
    time.sleep(5)
    gen_report_url(_report_dir)


def invert_dict(d):
    return dict(zip(d.values(), d.keys()))





def gen_report_url(_report_dir):
    command = r'allure serve {}\xml -p 9004'.format(_report_dir)
    try:
        taskinfo = os.popen('netstat -ano | findstr 9004')
        line = taskinfo.readline()
        aList = line.split()
        taskinfo.close()
        pid = aList[4]
        os.popen('taskkill /pid %s /f' % pid)
    except Exception:
        pass
    finally:
        os.popen(command)


def kill_report_process():
    try:
        taskinfo = os.popen('netstat -ano | findstr 9004')
        line = taskinfo.readline()
        aList = line.split()
        taskinfo.close()
        pid = aList[4]
        os.popen('taskkill /pid %s /f' % pid)
    except Exception:
        pass


def read_case_title():
    pass


def get_test_summary(_report_dir):
    d = {}
    target = _report_dir + r'\html\export\prometheusData.txt'
    with open(target, 'r') as f:
        for lines in f:
            launch_name = lines.strip('\n').split(' ')[0]
            num = lines.strip('\n').split(' ')[1]
            d.update({launch_name: num})
    return d


# def choose_test_case_by_name(case_list):
#     """
#     根据用例中文名称筛选用例到指定的测试目录下
#     需要支持开发同学选择用例时再开放
#     :param case_list:
#     :return:
#     """
#     temp = os.path.join(root_path, 'test_temp')
#     mkdir(temp)
#     temp_dict = invert_dict(item_test_case_map)
#     for case in case_list:
#         case_file = temp_dict.get(case)
#         src = os.path.join(testsuite_dir, case_file)
#         desc = os.path.join(temp, case_file)
#         shutil.copy(src, desc)


if __name__ == '__main__':
    gen_report_url(r'C:\mtrade_ui_test\mtrade_ui_test\report_v_0.0.90')
