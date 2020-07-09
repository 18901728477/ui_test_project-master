from time import sleep

from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import *
import requests
import json


class BlacklistPage(BasePage):

    nick_textbox_anchor = ('and', (('attr=', ('text', '买家旺旺')),))
    reason_textbox_anchor = ('and', (('attr=', ('text', '拉黑原因')),))
    confirm_add_locator = ('and', (('attr=', ('text', '添加')),))
    latest_info_anchor = ('and', (('attr=', ('text', '黑名单用户')),))
    latest_delete_locator = ('and', (('attr=', ('text', '删除')),))

    # 方法：黑名单新增一个用户
    def add_user(self, my_nick: str, my_reason: str):
        """
        黑名单新增一个用户
        :param my_nick: 买家旺旺昵称
        :param my_reason: 拉黑原因
        :return: 如果方法有返回值，这里对返回值进行说明
        """
        nick_textbox_element = init_element(self.nick_textbox_anchor).parent().offspring('android.widget.EditText')
        reason_textbox_element = init_element(self.reason_textbox_anchor).parent().offspring('android.widget.EditText')
        nick_textbox_element.set_text(my_nick)
        reason_textbox_element.set_text(my_reason)
        ay_click(self.confirm_add_locator)


    # 方法：获取黑名单中，最新的一个用户名和拉黑理由
    def get_latest_nick_reason(self):
        latest_nick_element = locate_by_anchor(init_element(self.latest_info_anchor), 1, 'v1l0v0')
        latest_reason_element = locate_by_anchor(init_element(self.latest_info_anchor), 1, 'v1l0v1')
        latest_info = {'usernick': get_text_of_view(latest_nick_element),
                       'reason': get_text_of_view(latest_reason_element)}
        return latest_info

    # def check_result_get_latest_nick_reason(self, element):
    #     try:
    #         element.waitforapp(3)
    #     return

    # 方法：删除黑名单中，最新的一个用户
    def delete_latest_nick(self):
        ay_click(self.latest_delete_locator)
        sleep(3)

    # 方法：调用ratebalckname接口，获取自动评价黑名单信息
    @ staticmethod
    def api_blacklist_info_auto_evaluate():
        url = 'https://trade.aiyongbao.com/iytrade2/ratebalckname?'
        headers = {
            'User-Agent': 'python'
        }
        parmas = {
            'page': 1,
            'trade_source': 'TAO'
        }
        cookies = {
            'PHPSESSID': get_sessionId()
        }
        resp = requests.get(url, headers=headers, params=parmas, cookies=cookies)
        return resp.text

    # 方法：返回api获取到的最新的一个拉黑用户的信息
    def api_get_blacklist_latest_user_info(self):
        resp = self.api_blacklist_info_auto_evaluate()
        black_list_info_dict = json.loads(resp)
        latest_info = {'blacknick': black_list_info_dict['zdpj'][0]['blacknick'],
                       'blackreason': black_list_info_dict['zdpj'][0]['blackreason']}
        return latest_info


if __name__ == "__main__":
    x = BlacklistPage()
    t = x.get_latest_nick_reason()
    print(t)