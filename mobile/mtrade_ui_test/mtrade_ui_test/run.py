import datetime
import os
import shutil
import time

import pytest

root_path = os.path.dirname(os.path.abspath(__file__))  # __file__表示当前文件自身，观察下run.py所在路径，可以知道root_path
testsuite_dir = os.path.join(root_path, 'testsuite')
case_daily = os.path.join(testsuite_dir, 'test_daily_regress')
case_dev = os.path.join(testsuite_dir, 'test_for_developer')
case_temp = os.path.join(root_path, 'test_temp')
jenkins_report_dir = os.path.join(root_path, 'report_for_jenkins')  # 拼接字符串，使得每次能够能到不同的测试报告，防止测试结果数据冲突
img_dir = root_path + r'\static\images'
test_case_map = {
    'test_auto_evaluate.py': '首页->自动评价设置',
    'test_batch_send_goods.py': '首页->批量发货',
    'test_differential_interception.py': '差评拦截设置',
    'test_evaluation_management.py': '首页->评价管理',
    'test_first_page.py': '首页->其他页面跳转',
    'test_my_page.py': '我的',
    'test_wait_buyer_pay.py': '订单列表_待付款订单',
}

test_case_conf_dict = {
    '首页->自动评价设置': True,
    '首页->批量发货': True,
    '首页->差评拦截设置': False,
    '首页->评价管理': True,
    '首页->其他页面跳转': True,
    '我的': False,
    '订单列表_待付款订单': True,
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
            case_name_zh = test_case_map.get(_name)
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
    # -n=auto,需要安装pytest-xdist，自动根据电脑配置启用多线程执行测试用例，要求测试用例之间不能有依赖性，对设计要求较高，更多适用于API测试提高执行效率,如果是UI测试则需多态设备
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


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    # 判断结果
    if isExists:
        shutil.rmtree(path)
    os.makedirs(path)


def gen_report_url(_report_dir):
    command = r'allure serve {}\xml -p 9003'.format(_report_dir)
    try:
        taskinfo = os.popen('netstat -ano | findstr 9003')
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
        taskinfo = os.popen('netstat -ano | findstr 9003')
        line = taskinfo.readline()
        aList = line.split()
        taskinfo.close()
        pid = aList[4]
        os.popen('taskkill /pid %s /f' % pid)
    except Exception:
        pass


def read_case_title():
    pass


def millisecond2minute(t: int):
    m = t // 1000 // 60
    s = t // 1000 % 60
    return '{}分{}秒'.format(m, s)


def get_test_summary(_report_dir):
    d = {}
    target = _report_dir + r'\html\export\prometheusData.txt'
    with open(target, 'r') as f:
        for lines in f:
            # lines.strip('\n').replace(' ', '').replace('、', '/').replace('?', '').split(' ')
            for c in lines:
                launch_name = lines.strip('\n').split(' ')[0]
                num = lines.strip('\n').split(' ')[1]
                d.update({launch_name: num})
        f.close()
    return d


def choose_test_case_by_name(case_list):
    """
    根据用例中文名称筛选用例到指定的测试目录下
    :param case_list:
    :return:
    """
    temp = os.path.join(root_path, 'test_temp')
    mkdir(temp)
    temp_dict = invert_dict(test_case_map)
    for case in case_list:
        case_file = temp_dict.get(case)
        src = os.path.join(testsuite_dir, case_file)
        desc = os.path.join(temp, case_file)
        shutil.copy(src, desc)


if __name__ == '__main__':
    gen_report_url(r'C:\mtrade_ui_test\mtrade_ui_test\report_v_0.0.90')
