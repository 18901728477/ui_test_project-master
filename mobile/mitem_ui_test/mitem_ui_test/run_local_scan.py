import datetime
import os
import pytest
from tkinter import messagebox

#  allure generate report/xml -o report/html --clean
def run_with_report(test_case_dir: str, test_report_dir: str) -> None:
    """
    执行测试用例，并得到allure report
    :param test_case_dir: 测试用例目录，应当是test开头的文件夹
    :param test_report_dir: 测试报告目录
    :return:
    """
    pytest.main([test_case_dir, '-vv', '--alluredir={}/xml'.format(test_report_dir)])
    #pytest.main([test_case_dir, '-vv','--alluredir={}/xml'.format(test_report_dir),'--reruns=3','--reruns-delay=5'])
    # 常用参数说明:
    # -n=auto,需要安装pytest-xdist，自动根据电脑配置启用多线程执行测试用例，要求测试用例之间不能有依赖性，对设计要求较高，更多适用于API测试提高执行效率,如果是UI测试则需多态设备
    # --reruns,--reruns-delay,需要安装pytest-rerunfailures，表示用例执行失败时自动重试的次数，以及两次重试之间的间隔
    # --alluredir 指定测试结果文件存在路径
    # --vv 显示详细结果
    # -q 显示简易测试结果
    # -s 显示用例中的print语句输出结果
    # 其他使用的pytest插件可以参考链接 https://www.cnblogs.com/peng-lan/p/11511569.html
    # pytest 推荐教程 https://www.jianshu.com/p/4ee3a0dd37c5
    os.system(r'allure generate {}/xml -o {}/html --clean'.format(report_dir, report_dir))

if __name__ == '__main__':
    root_path = os.path.dirname(os.path.abspath(__file__))  # __file__表示当前文件自身，观察下run.py所在路径，可以知道root_path
    # 表示项目根目录，即test_by_poco/
    test_dir = os.path.join(root_path, 'testsuite/test_for_developer')  # 找到测试脚本所在目录,root_path/testsuite/test_for_developer
    now_time = datetime.datetime.now()
    time_suffix = now_time.strftime('%Y%m%d_%H%M%S')  # 固定语法获取时间戳
    report_dir = os.path.join(root_path+'\\report\\', 'report_' + time_suffix)  # 拼接字符串，使得每次能够能到不同的测试报告，防止测试结果数据冲突
    run_with_report(test_dir, report_dir)
