import json
import urllib3
import socket

from mobile.common.utils import get_ip
from mobile.mtrade_ui_test.mtrade_ui_test.run import get_test_summary, test_case_map, read_case_module

# 单例模式
# def Singleton(cls):
#     _instance = {}
#
#     def _singleton(*args, **kargs):
#         if cls not in _instance:
#             _instance[cls] = cls(*args, **kargs)
#         return _instance[cls]
#
#     return _singleton


# @Singleton
class DingDingTalk:
    #  测试结果通过get_test_resuls获取，包括用例总数、通过数量、不通过数量、执行耗时，可扩充
    #  job_name, job_url, report_url报告路径从jenkins中取
    #  https://oapi.dingtalk.com/robot/send?access_token=55fbf24d632f546fc23024ef12b3640c144530b5aa9881035aae2a9929e42094 爱用交易
    #  https://oapi.dingtalk.com/robot/send?access_token=a81c8b7b727f4511aa9ca5f60bec2d0b6949edaa00104a03d4c7bfbb616daf0f 中台
    # https://oapi.dingtalk.com/robot/send?access_token=67c876fd99b898c9de1cf7f0c0fd302c328008bba4f1cd7a5e6dc54292cdb868 个人

    def __init__(self, my_hook):
        self.hook = my_hook

    def gen_report_address(self, _catetory):
        if _catetory == 'trade':
            report_report = '9003'
        else:
            report_report = '9004'
        addr_ip = get_ip()
        addr_url = 'http://' + str(addr_ip) + ':{}/index.html'.format(report_report)
        return addr_url

    def push_test_results(self,_category, summary):
        """
        推送测试结果
        :param _category:
        :param summary:
        :return:
        """
        total = int(summary.get('launch_retries_run')) - int(summary.get('launch_status_skipped'))
        e = int(summary.get('launch_status_broken'))
        con = {"msgtype": "text",
               "text": {
                   "content": "m{} UI自动化测试脚本执行完成。\n测试概述:\n运行总数:".format(_category) + summary.get(
                       'launch_retries_run') + "\n通过数量:" + summary.get(
                       'launch_status_passed') + "\n失败数量:" + summary.get(
                       'launch_status_failed') + "\n阻塞数量:" + summary.get(
                       'launch_status_broken') + "\n略过数量:" + summary.get(
                       'launch_status_skipped') + "\n异常失败率:{}".format(
                       round(e / total, 2)) + "\n测试报告地址:" + self.gen_report_address(_category)},
               "at": {
                   "atMobiles": [
                       "18621729133"
                   ],
                   "isAtAll": False
               }
               }
        urllib3.disable_warnings()
        http = urllib3.PoolManager()
        jd = json.dumps(con)
        jd = bytes(jd, 'utf-8')
        http.request('POST', self.hook, body=jd, headers={'Content-Type': 'application/json'})

    def push_start_info(self, _category, _version):
        """
        推送测试启动信息
        :param _case_dir:
        :param _version:
        :return:
        """
        con = {"msgtype": "text",
               "text": {
                   "content": "m{} UI自动化测试脚本开始执行，在推送测试报告信息前，请勿重复提交测试申请！\n此轮测试对应版本号为:{}".format(_category, _version)},
               "at": {
                   "atMobiles": [
                       #  "18621729133"
                   ],
                   "isAtAll": False
               }
               }
        urllib3.disable_warnings()
        http = urllib3.PoolManager()
        jd = json.dumps(con)
        jd = bytes(jd, 'utf-8')
        http.request('POST', self.hook, body=jd, headers={'Content-Type': 'application/json'})

    def push_error_info(self, _error_info):
        """
        推送错误信息
        :param _error_info:
        :return:
        """
        con = {"msgtype": "text",
               "text": {
                   "content": "自动化测试异常终止，可能的原因是:\n***{}***".format(_error_info)},
               }
        urllib3.disable_warnings()
        http = urllib3.PoolManager()
        jd = json.dumps(con)
        jd = bytes(jd, 'utf-8')
        http.request('POST', self.hook, body=jd, headers={'Content-Type': 'application/json'})


if __name__ == '__main__':
    dd = DingDingTalk('67c876fd99b898c9de1cf7f0c0fd302c328008bba4f1cd7a5e6dc54292cdb868')
    t = dd.gen_report_address()
    print(t)



