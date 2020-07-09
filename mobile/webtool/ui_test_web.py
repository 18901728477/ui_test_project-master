import os
import re
import time
from concurrent.futures.thread import ThreadPoolExecutor
import flask
from flask import render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from mobile.common.case_runnner import Runner
from mobile.common.dingding_talk import DingDingTalk
from mobile.config.path_config import TRADE_ROOT

root_path = os.path.dirname(os.path.abspath(__file__))
server = flask.Flask(__name__)
server.config["SECRET_KEY"] = '123456'
executor = ThreadPoolExecutor(max_workers=1)
task = None
ALLOWED_EXTENSIONS = {'png', 'jpg', 'JPG', 'PNG', 'bmp'}

version = ''  # 全局变量，自检时获取，并且用来生成测试报告文件夹

#item_hook = 'https://oapi.dingtalk.com/robot/send?access_token=67c876fd99b898c9de1cf7f0c0fd302c328008bba4f1cd7a5e6dc54292cdb868'#wb群地址
#item_hook = 'https://oapi.dingtalk.com/robot/send?access_token=a585fd72c2f3a239322e7ca87d513caf323b76cbd6383b2a3e7537a8e8bf110f'#告警群地址
item_hook = 'https://oapi.dingtalk.com/robot/send?access_token=fb118e7f6588d8c37b27ddf154eebb4cb36a6f5ba7be983d9addb65a401d6dea'#大吉大利群
trade_hook = 'https://oapi.dingtalk.com/robot/send?access_token=55fbf24d632f546fc23024ef12b3640c144530b5aa9881035aae2a9929e42094'
# trade_hook = 'https://oapi.dingtalk.com/robot/send?access_token=04719c50dc51b95cba593ea766819937dd96c38d7dc3daea55f9fc4d904f0cd5'# 3ren qu
# 'https://oapi.dingtalk.com/robot/send?access_token=a585fd72c2f3a239322e7ca87d513caf323b76cbd6383b2a3e7537a8e8bf110f'# 测试群
# 'https://oapi.dingtalk.com/robot/send?access_token=55fbf24d632f546fc23024ef12b3640c144530b5aa9881035aae2a9929e42094'
# 'https://oapi.dingtalk.com/robot/send?access_token=55fbf24d632f546fc23024ef12b3640c144530b5aa9881035aae2a9929e42094' 交易环境
#  https://oapi.dingtalk.com/robot/send?access_token=a81c8b7b727f4511aa9ca5f60bec2d0b6949edaa00104a03d4c7bfbb616daf0f 中台环境
# 'https://oapi.dingtalk.com/robot/send?access_token=67c876fd99b898c9de1cf7f0c0fd302c328008bba4f1cd7a5e6dc54292cdb868' debug
dd_trade = DingDingTalk(trade_hook)
dd_item = DingDingTalk(item_hook)


class TradeDataForm(FlaskForm):
    WAIT_BUYER_PAY_ORDER = StringField('待付款订单号', validators=[DataRequired()])
    WAIT_BUYER_PAY_ORDER_CART = StringField('待付款购物车订单号', validators=[DataRequired()])
    submit = SubmitField('提交')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def run(category, mode):
    """
    执行测试，生成报告，钉钉推送消息
    :param category: trade 交易测试/item 商品测试
    :param mode: dev 扫二维码测试/prd 线上环境测试/debug 调试
    :return:
    """
    if category == 'trade':
        if mode == 'dev':
            r = Runner(category='trade', mode='dev')
        else:
            r = Runner(category='trade', mode='prd')
        dd = dd_trade
    else:
        if mode == 'dev':
            r = Runner(category='item', mode='dev')
        else:
            r = Runner(category='item', mode='prd')
        dd = dd_item
    dd.push_start_info(_category=category,
                       _version=r.version)
    r.run()
    sumary = r.get_test_summary()
    dd.push_test_results(category, sumary)


def run_by_level(category, mode, level):
    """
    执行测试，生成报告，钉钉推送消息
    :param category: trade 交易测试/item 商品测试
    :param mode: dev 扫二维码测试/prd 线上环境测试/debug 调试
    :param level: 用例的优先级
    :return:
    """
    if category == 'trade':
        if mode == 'dev':
            r = Runner(category='trade', mode='dev')
        else:
            r = Runner(category='trade', mode='prd')
        dd = dd_trade
    else:
        if mode == 'dev':
            r = Runner(category='item', mode='dev')
        else:
            r = Runner(category='item', mode='prd')
        dd = dd_item
        DingDingTalk(item_hook).push_start_info(_category=category,
                                                _version=r.version)
    if level == 'p1':
        r.run_p1()
    elif level == 'p2':
        r.run_p2()
    sumary = r.get_test_summary()
    dd.push_test_results(category, sumary)


@server.route('/trade/run_dev', methods=['get', 'post'])
def run_test_dev_for_trade():
    global task
    if not task or task.done():
        task = executor.submit(run, 'trade', 'dev')
        return '已提交测试，完成后会推送消息到钉钉，请勿重复提交'
    else:
        dd_trade.push_error_info('当前已有测试任务，请在收到测试结果消息推送后重试')
        return '当前已有测试任务，请在收到测试结果消息推送后重试'


@server.route('/trade/run_prd', methods=['get', 'post'])
def run_test_prd_for_trade():
    global task
    if not task or task.done():
        task = executor.submit(run, 'trade', 'prd')
        return '已提交测试，完成后会推送消息到钉钉，请勿重复提交'
    else:
        dd_trade.push_error_info('当前已有测试任务，请在收到测试结果消息推送后重试')
        return '当前已有测试任务，请在收到测试结果消息推送后重试'


@server.route('/item/run_dev', methods=['get', 'post'])
def run_test_dev_for_item():
    global task
    if not task or task.done():
        task = executor.submit(run, 'item', 'dev')
        return '已提交测试，完成后会推送消息到钉钉，请勿重复提交'
    else:
        dd_item.push_error_info('当前已有测试任务，请在收到测试结果消息推送后重试')
        return '当前已有测试任务，请在收到测试结果消息推送后重试'


@server.route('/item/run_prd', methods=['get', 'post'])
def run_test_prd_for_item():
    global task
    if not task or task.done():
        task = executor.submit(run, 'item', 'prd')
        return '已提交测试，完成后会推送消息到钉钉，请勿重复提交'
    else:
        dd_item.push_error_info('当前已有测试任务，请在收到测试结果消息推送后重试')
        return '当前已有测试任务，请在收到测试结果消息推送后重试'

@server.route('/stop', methods=['get', 'post'])
def stop_test():
    global executor
    executor.shutdown()
    dd_trade.push_error_info('人为触发终止')
    return '测试已终止'

@server.route('/item/run_prd_p1', methods=['get', 'post'])
def run_test_prd_for_item_p1():
    global task
    if not task or task.done():
        task = executor.submit(run_by_level, 'item', 'prd', 'p1')
        return '已提交p1优先级测试，完成后会推送消息到钉钉，请勿重复提交'
    else:
        dd_item.push_error_info('当前已有测试任务，请在收到测试结果消息推送后重试')
        return '当前已有测试任务，请在收到测试结果消息推送后重试'


@server.route('/item/run_prd_p2', methods=['get', 'post'])
def run_test_prd_for_item_p2():
    global task
    if not task or task.done():
        task = executor.submit(run_by_level, 'item', 'prd', 'p2')
        return '已提交p2优先级测试，完成后会推送消息到钉钉，请勿重复提交'
    else:
        dd_item.push_error_info('当前已有测试任务，请在收到测试结果消息推送后重试')
        return '当前已有测试任务，请在收到测试结果消息推送后重试'


# @server.route('/stop', methods=['get', 'post'])
# def stop_test():
#     global executor
#     executor.shutdown()
#     dd_trade.push_error_info('人为触发终止')
#     return '测试已终止'


@server.route('/trade/upload', methods=['POST', 'GET'])  # 添加路由
def upload_for_trade():
    if request.method == 'POST':
        f = request.files['file']
        if not (f and allowed_file(f.filename)):
            return flask.jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
        user_input = request.form.get("name")
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'static/trade', 'test.png')  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        return render_template('trade/upload_ok.html', userinput=user_input, val1=time.time())
    return render_template('trade/upload.html')


@server.route('/item/upload', methods=['POST', 'GET'])  # 添加路由
def upload_for_item():
    if request.method == 'POST':
        f = request.files['file']
        if not (f and allowed_file(f.filename)):
            return flask.jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
        user_input = request.form.get("name")
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'static/item', 'test.png')  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        return render_template('item/upload_ok.html', userinput=user_input, val1=time.time())
    return render_template('item/upload.html')


@server.route('/trade/data', methods=['POST', 'GET'])  # 添加路由
def change_data():
    form = TradeDataForm()
    if form.validate_on_submit():
        wait_buyer_pay = form.WAIT_BUYER_PAY_ORDER.data
        wait_buyer_pay_cart = form.WAIT_BUYER_PAY_ORDER_CART.data
        f_path = TRADE_ROOT / 'data.py'
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
    return render_template('trade/change_data.html', title='Change Order Data', form=form)


@server.route('/')
@server.route('/index')
def index():
    return render_template('index.html', title='Home')


@server.route('/trade/index')
def index_for_trade():
    return render_template('trade/index_for_trade.html', title='Trade Home')


@server.route('/item/index')
def index_for_item():
    return render_template('item/index_for_item.html', title='Trade Home')


if __name__ == '__main__':
    server.run(port=9002, debug=True, host='0.0.0.0')
    # run(category='trade', mode='prd')
