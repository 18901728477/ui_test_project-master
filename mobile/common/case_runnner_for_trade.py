import os
import time
import pytest
from mobile.common.utils import mkdir
from mobile.config.path_config import ITEM_REPORT, ITEM_ROOT, TRADE_ROOT, TRADE_REPORT
from mobile.mtrade_ui_test.mtrade_ui_test.conftest import wakeup, restart_app_by_scan, restart_app
from mobile.mtrade_ui_test.mtrade_ui_test.pages.first_page import FirstPage


def get_version(mode='dev'):
    wakeup()
    if mode == 'dev':
        restart_app_by_scan()
    else:
        restart_app()
    FirstPage().self_check()
    m = FirstPage().go_my_page()
    version = m.get_version()
    return version


class TradeRunner:
    def __init__(self, mode='dev'):
        self.version = get_version(mode)
        report_with_verison = "report_v" + self.version
        self.report_dir = TRADE_REPORT / report_with_verison
        if mode == 'dev':
            self.case_dir = TRADE_ROOT / "testsuite/test_temp"
        else:
            self.case_dir = TRADE_ROOT / "testsuite/test_daily_regress"
        mkdir(str(self.report_dir))

    def gen_report_url(self):  # trade报告端口是9003
        command = r'allure serve {}\xml -p 9003'.format(self.report_dir)
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

    def get_test_summary(self):
        d = {}
        target = self.report_dir /"html/export/prometheusData.txt"
        with open(target, 'r') as f:
            for lines in f:
                launch_name = lines.strip('\n').split(' ')[0]
                num = lines.strip('\n').split(' ')[1]
                d.update({launch_name: num})
        return d

    def run(self):
        try:
            pytest.main([str(self.case_dir), '-vv', #'--reruns=2', '--reruns-delay=2',
                         '--alluredir={}/xml'.format(str(self.report_dir))])
            os.system(r'allure generate {}/xml -o {}/html --clean'.format(str(self.report_dir), str(self.report_dir)))
            time.sleep(5)
            self.gen_report_url()
        except Exception as e:
            print(e)
            print(str(self.report_dir))
            raise


if __name__ == '__main__':
    r = TradeRunner(mode='dev')
    t = r.get_test_summary()
    print(t)


