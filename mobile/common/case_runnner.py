import os
import time
import pytest
from mobile.common.utils import mkdir
from mobile.config.path_config import ITEM_REPORT, ITEM_ROOT, TRADE_ROOT, TRADE_REPORT
from mobile.mitem_ui_test.mitem_ui_test.conftest import wakeup as wakeup_item, restart_app_by_scan as restart_app_by_scan_item, restart_app as restart_app_item
from mobile.mtrade_ui_test.mtrade_ui_test.conftest import wakeup as wakeup_trade, restart_app_by_scan as restart_app_by_scan_trade, restart_app as restart_app_trade
from mobile.mtrade_ui_test.mtrade_ui_test.pages.first_page import FirstPage as firstpage_trade
from mobile.mitem_ui_test.mitem_ui_test.pages.first_page import FirstPage as firstpage_item




class Runner:
    def __init__(self, category, mode):
        self.category = category
        self.mode = mode
        self.version = self.get_version()
        report_with_verison = "report_v" + self.version
        if category == 'trade':
            if mode == 'dev':
                self.case_dir = TRADE_ROOT / "testsuite/test_for_developer"
            else:
                self.case_dir = TRADE_ROOT / "testsuite/test_daily_regress"
            self.report_dir = TRADE_REPORT / report_with_verison
        else:
            if mode == 'dev':
                self.case_dir = ITEM_ROOT / "testsuite/test_for_developer"
            else:
                self.case_dir = ITEM_ROOT / "testsuite/test_daily_regress"
            self.report_dir = ITEM_REPORT / report_with_verison
        mkdir(str(self.report_dir))

    def get_version(self):
        if self.category == 'trade':
            wakeup_trade()
            if self.mode == 'dev':
                restart_app_by_scan_trade()
            else:
                restart_app_trade()
            firstpage_trade().self_check()
            m = firstpage_trade().go_my_page()
            return  m.get_version()
        else:
            wakeup_item()
            if self.mode == 'dev':
                restart_app_by_scan_item()
            else:
                restart_app_item()
            firstpage_item().self_check()
            m = firstpage_item().go_my_page()
            return  m.get_version()

    def gen_report_url(self):  # item报告端口9004
        if self.category == 'trade':
            report_port = '9003'
        else:
            report_port = '9004'
        command = r'allure serve {}\xml -p {}'.format(self.report_dir, report_port)
        try:
            taskinfo = os.popen('netstat -ano | findstr {}'.format(report_port))
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
            pytest.main([str(self.case_dir), '-vv', '--reruns=1', '--reruns-delay=2',
                         '--alluredir={}/xml'.format(str(self.report_dir))])
            os.system(r'allure generate {}/xml -o {}/html --clean'.format(str(self.report_dir), str(self.report_dir)))
            time.sleep(5)
            self.gen_report_url()
        except Exception as e:
            print(e)
            print(str(self.report_dir))
            raise

    def run_p1(self):
        try:
            pytest.main([str(self.case_dir), '-vv', '-m=p1', '--reruns=1', '--reruns-delay=2',
                         '--alluredir={}/xml'.format(str(self.report_dir))])
            os.system(r'allure generate {}/xml -o {}/html --clean'.format(str(self.report_dir), str(self.report_dir)))
            time.sleep(5)
            self.gen_report_url()
        except Exception as e:
            print(e)
            print(str(self.report_dir))
            raise

    def run_p2(self):
        try:
            pytest.main([str(self.case_dir), '-vv', '-m=p2', '--reruns=1', '--reruns-delay=2',
                         '--alluredir={}/xml'.format(str(self.report_dir))])
            os.system(r'allure generate {}/xml -o {}/html --clean'.format(str(self.report_dir), str(self.report_dir)))
            time.sleep(5)
            self.gen_report_url()
        except Exception as e:
            print(e)
            print(str(self.report_dir))
            raise


if __name__ == '__main__':
    r = Runner(category='trade', mode='dev')
    r.run()

