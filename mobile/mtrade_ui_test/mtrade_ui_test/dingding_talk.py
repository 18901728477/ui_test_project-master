import json
import urllib3
import socket

from mobile.mtrade_ui_test.mtrade_ui_test.run import get_test_summary, test_case_map, read_case_module


def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@Singleton
class DingDingTalk:
    #  测试结果通过get_test_resuls获取，包括用例总数、通过数量、不通过数量、执行耗时，可扩充
    #  job_name, job_url, report_url报告路径从jenkins中取
    #  todo 1、解决jenkins相关的网络问题
    #  todo 2、设计钉钉机器人的交互，包括功能，一键执行日常回归、开发人员自定义测试（模块级别）
    #  https://oapi.dingtalk.com/robot/send?access_token=55fbf24d632f546fc23024ef12b3640c144530b5aa9881035aae2a9929e42094 爱用交易
    #  https://oapi.dingtalk.com/robot/send?access_token=a81c8b7b727f4511aa9ca5f60bec2d0b6949edaa00104a03d4c7bfbb616daf0f 中台
    # https://oapi.dingtalk.com/robot/send?access_token=67c876fd99b898c9de1cf7f0c0fd302c328008bba4f1cd7a5e6dc54292cdb868 个人

    def __init__(self, _url):
        self.url = _url
    def get_ip(self):
        # 获取本机电脑名
        myname = socket.getfqdn(socket.gethostname())
        # 获取本机ip
        myaddr = socket.gethostbyname(myname)
        print(myname)
        print(myaddr)
        add = 'http://' + str(myaddr) + ':9003/index_for_trade.html'
        return str(add.strip())

    def push_test_results(self, _report_dir):
        """
        推送测试结果
        :param _report_dir:
        :return:
        """
        add_ip = self.get_ip()
        summary = get_test_summary(_report_dir)
        total = int(summary.get('launch_retries_run')) - int(summary.get('launch_status_skipped'))
        e = int(summary.get('launch_status_broken'))
        con = {"msgtype": "text",
               "text": {
                   "content": "mtrade UI自动化测试脚本执行完成。\n测试概述:\n运行总数:" + summary.get(
                       'launch_retries_run') + "\n通过数量:" + summary.get(
                       'launch_status_passed') + "\n失败数量:" + summary.get(
                       'launch_status_failed') + "\n阻塞数量:" + summary.get(
                       'launch_status_broken') + "\n略过数量:" + summary.get(
                       'launch_status_skipped') + "\n异常失败率:{}".format(
                       round(e / total, 2)) + "\n测试报告地址:" + add_ip},
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
        http.request('POST', self.url, body=jd, headers={'Content-Type': 'application/json'})

    def push_start_info(self, _case_dir, _version):
        """
        推送测试启动信息
        :param _case_dir:
        :param _version:
        :return:
        """
        case_list = read_case_module(_case_dir)
        con = {"msgtype": "text",
               "text": {
                   "content": "mtrade UI自动化测试脚本开始执行，在推送测试报告信息前，请勿重复提交测试申请！\n此轮测试对应版本号为:{}\n测试范围包括:\n{}".format(_version,
                                                                                                               ' ,'.join(
                                                                                                                   case_list))},
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
        http.request('POST', self.url, body=jd, headers={'Content-Type': 'application/json'})

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
        http.request('POST', self.url, body=jd, headers={'Content-Type': 'application/json'})


if __name__ == '__main__':
    # # dd = DingDingTalk(_url='https://oapi.dingtalk.com/robot/send?access_token=67c876fd99b898c9de1cf7f0c0fd302c328008bba4f1cd7a5e6dc54292cdb868')
    # # dd.push_error_info('当前已有测试运行，请稍后重试')
    # 获取本机电脑名
    myname = socket.getfqdn(socket.gethostname())
    # 获取本机ip
    myaddr = socket.gethostbyname(myname)
    print(myname)
    print(myaddr)
    add =  'http://' +str(myaddr)+':9003/index_for_trade.html'
    print(add.strip())


