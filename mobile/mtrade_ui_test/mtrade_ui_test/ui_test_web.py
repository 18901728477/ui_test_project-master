import os
import re
import time
from concurrent.futures.thread import ThreadPoolExecutor

import git
from git import *
import flask
from flask import render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms\
     .validators import DataRequired

from mobile.mtrade_ui_test.mtrade_ui_test.conftest import wakeup, restart_app, restart_app_by_scan
from mobile.mtrade_ui_test.mtrade_ui_test.dingding_talk import DingDingTalk
from mobile.mtrade_ui_test.mtrade_ui_test.pages.first_page import FirstPage
from mobile.mtrade_ui_test.mtrade_ui_test.run import case_daily, case_dev, case_temp, run_with_report

root_path = os.path.dirname(os.path.abspath(__file__))

server = flask.Flask(__name__)
server.config["SECRET_KEY"] = '123456'

executor = ThreadPoolExecutor(1, 1)

task = None

ALLOWED_EXTENSIONS = {'png', 'jpg', 'JPG', 'PNG', 'bmp'}

version = ''  # 全局变量，自检时获取，并且用来生成测试报告文件夹

token = 'https://oapi.dingtalk.com/robot/send?access_token=55fbf24d632f546fc23024ef12b3640c144530b5aa9881035aae2a9929e42094'
# 'https://oapi.dingtalk.com/robot/send?access_token=55fbf24d632f546fc23024ef12b3640c144530b5aa9881035aae2a9929e42094' 交易环境
#  https://oapi.dingtalk.com/robot/send?access_token=a81c8b7b727f4511aa9ca5f60bec2d0b6949edaa00104a03d4c7bfbb616daf0f 中台环境
# 'https://oapi.dingtalk.com/robot/send?access_token=67c876fd99b898c9de1cf7f0c0fd302c328008bba4f1cd7a5e6dc54292cdb868' debug
dd = DingDingTalk(token)


class DataForm(FlaskForm):
    WAIT_BUYER_PAY_ORDER = StringField('待付款订单号', validators=[DataRequired()])
    WAIT_BUYER_PAY_ORDER_CART = StringField('待付款购物车订单号', validators=[DataRequired()])
    submit = SubmitField('提交')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def run():
    """
    处理日常回归测试
    执行测试用例并产生报告
    推送测试结果到钉钉机器人
    :return:
    """
    dd.push_start_info(_case_dir=case_daily,
                       _version=version)
    report_dir = os.path.join(root_path, 'report_v_' + version)
    run_with_report(_case_dir=case_daily,
                    _report_dir=report_dir)
    dd.push_test_results(_report_dir=report_dir)


def run_dev():
    """
    用于开发自测
    :return:
    """
    dd.push_start_info(_case_dir=case_dev,
                       _version=version)
    report_dir = os.path.join(root_path, 'report_v_' + version)
    run_with_report(_case_dir=case_dev,
                    _report_dir=report_dir)
    dd.push_test_results(_report_dir=report_dir)


def run_debug():
    """
    用于调试
    :return:
    """
    dd.push_start_info(_case_dir=case_temp,
                       _version=version)
    report_dir = os.path.join(root_path, 'report_v_' + version)
    run_with_report(_case_dir=case_temp,
                    _report_dir=report_dir)
    dd.push_test_results(_report_dir=report_dir)


@server.route('/run', methods=['get', 'post'])
def run_test_normal():
    global task
    if not task or task.done():
        health_check()  # 通过自检可以确定获取version信息
        task = executor.submit(run)
        return '已提交测试，完成后会推送消息到钉钉，请勿重复提交'
    else:
        dd.push_error_info(_error_info='当前已有测试任务，请在收到测试结果消息推送后重试')
        return '当前已有测试任务，请在收到测试结果消息推送后重试'


@server.route('/run_dev', methods=['get', 'post'])
def run_test_dev():
    global task
    if not task or task.done():
        res1 = health_check(dev_flag=True)[0]
        res2 = health_check(dev_flag=True)[1]
        if res1:
            task = executor.submit(run_dev)
        else:
            dd.push_error_info(res2)
            return False
        return '已提交测试，完成后会推送消息到钉钉，请勿重复提交'
    else:
        dd.push_error_info('当前已有测试任务，请在收到测试结果消息推送后重试')
        return '当前已有测试任务，请在收到测试结果消息推送后重试'


@server.route('/run_debug', methods=['get', 'post'])
def run_test_debug():
    global task
    if not task or task.done():
        health_check()
        task = executor.submit(run_debug)
        return '已提交测试，完成后会推送消息到钉钉，请勿重复提交'
    else:
        dd.push_error_info('当前已有测试任务，请在收到测试结果消息推送后重试')
        return '当前已有测试任务，请在收到测试结果消息推送后重试'


@server.route('/stop', methods=['get', 'post'])
def stop_test():
    global executor
    executor.shutdown()
    dd.push_error_info('人为触发终止')
    return '测试已终止'


@server.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']

        if not (f and allowed_file(f.filename)):
            return flask.jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        user_input = request.form.get("name")

        basepath = os.path.dirname(__file__)  # 当前文件所在路径

        upload_path = os.path.join(basepath, 'static/item_images', 'test.txt.png')  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)

        return render_template('upload_ok.html', userinput=user_input, val1=time.time())

    return render_template('upload.html')


@server.route('/data', methods=['POST', 'GET'])  # 添加路由
def change_data():
    form = DataForm()
    if form.validate_on_submit():
        wait_buyer_pay = form.WAIT_BUYER_PAY_ORDER.data
        wait_buyer_pay_cart = form.WAIT_BUYER_PAY_ORDER_CART.data
        f_path = root_path + r'\data.py'
        f = open(f_path, 'r+', encoding='utf-8')
        con = f.read()
        c1 = re.compile(r'WAIT_BUYER_PAY_ORDER = .*\n')
        c2 = re.compile(r'WAIT_BUYER_PAY_ORDER_CART = .*\n')
        con1 = c1.sub('WAIT_BUYER_PAY_ORDER = \'{}\'\n'.format(wait_buyer_pay), con)
        con2 = c2.sub('WAIT_BUYER_PAY_ORDER_CART = \'{}\'\n'.format(wait_buyer_pay_cart), con1)
        f.close()
        with open(f_path, 'w', encoding='utf-8') as f1:
            f1.write(con2)
        return '订单数据已成功更新'
    return render_template('change_data.html', title='Change Order Data', form=form)


@server.route('/')
@server.route('/index')
def index():
    return render_template('index_for_trade.html', title='Home')


def health_check(dev_flag: bool = False):
    """
    todo:检查是否存在有效订单
    :return:
    """
    global version
    msg = ''
    wakeup()
    if dev_flag:
        try:
            open(r'C:\mtrade_ui_test\mtrade_ui_test\static\images\test.png', 'r')
        except Exception:
            msg = '二维码图片不存在'
            return False, msg
        restart_app_by_scan()
    else:
        restart_app()
    FirstPage().self_check()
    m = FirstPage().go_my_page()
    version = m.get_version()
    return version, msg

if __name__ == '__main__':
    server.run(port=9002, debug=True, host='0.0.0.0')
