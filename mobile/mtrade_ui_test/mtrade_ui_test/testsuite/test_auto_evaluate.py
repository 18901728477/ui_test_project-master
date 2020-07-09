import allure
import pytest

from mobile.mitem_ui_test.mitem_ui_test.utils import get_current_time


class TestAutoEvaluate:

    @allure.feature('自动评价')
    @allure.story('自动评价，黑名单管理页面，可以正常添加用户')
    def test_add_user(self, auto_evaluate):
        """
        1.进入自动评价页面
        2.点击黑名单管理，进入黑名单页面
        3.新增一个用户
        4.调用api，判断是否实际添加成功
        :param auto_evaluate:
        :return:
        """
        auto_evaluate_page = auto_evaluate
        auto_evaluate_blacklist_page = auto_evaluate_page.go_blacklist_page()
        blacknick = '高小轩' + get_current_time()
        blackreason = '拉黑咯，开心不'
        auto_evaluate_blacklist_page.add_user(blacknick, blackreason)
        latest_nick = auto_evaluate_blacklist_page.api_get_blacklist_latest_user_info()['blacknick']
        latest_reason = auto_evaluate_blacklist_page.api_get_blacklist_latest_user_info()['blackreason']
        info = auto_evaluate_blacklist_page.get_latest_nick_reason()
        assert blacknick == info['usernick'] and blackreason in info[
            'reason'], '新增的用户：{}，原因{}；页面上显示的最新用户：{}，原因：{}'.format(blacknick, blackreason, info['usernick'],
                                                                  info['reason'])
        assert blacknick == latest_nick and blackreason == latest_reason, '新增的用户：{}，原因{}；接口返回的最新用户：{}，原因：{}'.format(
            blacknick, blackreason, latest_nick, latest_reason)

    @allure.feature('自动评价')
    @allure.story('自动评价，黑名单管理页面，可以正常删除用户')
    def test_delete_latest_nick(self, auto_evaluate):
        """
        1.进入自动评价页面
        2.点击黑名单管理，进入黑名单页面
        3.新增一个用户，然后立刻删除
        4.调用api，判断是否实际删除成功
       :param auto_evaluate:
       :return:
        """
        auto_evaluate_page = auto_evaluate
        auto_evaluate_blacklist_page = auto_evaluate_page.go_blacklist_page()
        blacknick = '高小轩' + get_current_time()
        blackreason = '拉黑咯，开心不'
        auto_evaluate_blacklist_page.add_user(blacknick, blackreason)
        auto_evaluate_blacklist_page.delete_latest_nick()
        latest_nick = auto_evaluate_blacklist_page.api_get_blacklist_latest_user_info()['blacknick']
        latest_nick = auto_evaluate_blacklist_page.get_latest_nick_reason()['usernick']
        assert blacknick != latest_nick, '删除的用户：{}；页面上显示的最新用户：{}'.format(blacknick, latest_nick)
        assert blacknick != latest_nick, '删除的用户：{}；接口返回的最新用户：{}'.format(blacknick, latest_nick)

    @allure.feature('自动评价')
    @allure.story('自动评价，评价短语页面，新增短语后，实际新增成功')
    def test_create_phrase(self, auto_evaluate):
        """
          1.进入自动评价页面
          2.点击评价短语，进入评价短语页面
          3.新增一条短语
          4.调用api，判断是否实际新增成功
          :param auto_evaluate:
          :return:
        """
        auto_evaluate_page = auto_evaluate
        auto_evaluate_phrase_page = auto_evaluate_page.go_evalaute_phrase()
        phrase = '我新增的短语' + get_current_time()
        auto_evaluate_phrase_page.create_phrase(phrase)
        api_latest_phrase = auto_evaluate_phrase_page.api_latest_auto_evaluate_phrase()
        auto_evaluate_phrase_page.delete_phrase(phrase)
        assert api_latest_phrase == phrase, '自动评价，评价短语页面，新增短语后，无法正常新增！新增短语：{}，接口返回的短语：{}'.format(phrase,
                                                                                                 api_latest_phrase)

    @allure.feature('自动评价')
    @allure.story('自动评价，评价短语页面，编辑短语后，实际编辑成功')
    def test_edit_phrase(self, auto_evaluate):
        """
        1.进入自动评价页面
        2.点击评价短语，进入评价短语页面
        3.编辑一条短语
        4.调用api，判断是否实际编辑成功
        :param auto_evaluate:
        :return:
        """
        auto_evaluate_page = auto_evaluate
        auto_evaluate_phrase_page = auto_evaluate_page.go_evalaute_phrase()
        phrase1 = '我新增的短语' + get_current_time()
        auto_evaluate_phrase_page.create_phrase(phrase1)
        phrase2 = '我编辑的短语' + get_current_time()
        auto_evaluate_phrase_page.edit_phrase(phrase2)
        api_latest_phrase = auto_evaluate_phrase_page.api_latest_auto_evaluate_phrase()
        auto_evaluate_phrase_page.delete_phrase(phrase2)
        assert api_latest_phrase == phrase2, '自动评价，评价短语页面，编辑短语后，无法正常编辑！编辑后的短语：{}，接口返回的短语：{}'.format(phrase2,
                                                                                                    api_latest_phrase)

    @allure.feature('自动评价')
    @allure.story('自动评价，评价短语页面，删除短语后，实际删除成功')
    def test_delete_phrase(self, auto_evaluate):
        """
        1.进入自动评价页面
        2.点击评价短语，进入评价短语页面
        3.删除一条短语
        4.调用api，判断是否实际删除成功
        :param auto_evaluate:
        :return:
        """
        auto_evaluate_page = auto_evaluate
        auto_evaluate_phrase_page = auto_evaluate_page.go_evalaute_phrase()
        phrase = '我删除的短语' + get_current_time()
        auto_evaluate_phrase_page.create_phrase(phrase)
        auto_evaluate_phrase_page.delete_phrase(phrase)
        api_latest_phrase = auto_evaluate_phrase_page.api_latest_auto_evaluate_phrase()
        assert api_latest_phrase != phrase, '自动评价，评价短语页面，短语无法删除！删除的短语：{}，接口返回的短语：{}'.format(phrase, api_latest_phrase)

    @allure.feature('自动评价')
    @allure.story('自动评价，评价记录页面，成功记录tab下，最新一条记录显示正确')
    def test_api_get_latest_success_record(self, auto_evaluate):
        """
          1.进入自动评价页面
          2.点击评价记录，进入评价记录页面
          3.进入成功记录tab
          4.校验最新一条记录
        :param auto_evaluate:
        :return:
        """
        auto_evaluate_page = auto_evaluate
        auto_evaluate_record_page = auto_evaluate_page.go_evaluate_record()
        auto_evaluate_record_page.go_success_list()
        flag = True
        get_list = auto_evaluate_record_page.get_latest_success_record_info()
        api_list = auto_evaluate_record_page.api_get_latest_success_record()
        for x in get_list.keys():
            if get_list[x] != api_list[x]:
                flag = False
        assert flag, '自动评价，评价记录页面，成功记录tab下，最新一条记录显示有误！页面上显示的：{}，接口返回的：{}'.format(get_list, api_list)

    @allure.feature('自动评价')
    @allure.story('自动评价，评价记录页面，失败记录tab下，最新一条记录显示正确')
    # @pytest.mark.skip(reason="error")
    def test_api_get_latest_fail_record(self, auto_evaluate):
        """
          1.进入自动评价页面
          2.点击评价记录，进入评价记录页面
          3.进入失败记录tab
          4.校验最新一条记录
        :param auto_evaluate:
        :return:
        """
        auto_evaluate_page = auto_evaluate
        auto_evaluate_record_page = auto_evaluate_page.go_evaluate_record()
        auto_evaluate_record_page.go_failure_list()
        flag = True
        get_list = auto_evaluate_record_page.get_latest_failure_record_info()
        api_list = auto_evaluate_record_page.api_get_latest_fail_record()
        for x in get_list.keys():
            if x == 'reason':
                if api_list[x] in get_list[x]:
                    pass
                else:
                    flag = False
            else:
                if get_list[x] != api_list[x]:
                    flag = False
        assert flag, '自动评价，评价记录页面，失败记录tab下，最新一条记录显示有误！页面上显示的：{}，接口返回的：{}'.format(get_list, api_list)

    @allure.feature('自动评价')
    @allure.story('自动评价，评价记录页面，tab下，点击任意记录，能进入订单详情页，显示的订单信息正确')
    def test_go_order_detail(self, auto_evaluate):
        """
          1.进入自动评价页面
          2.点击评价记录，进入评价记录页面
          3.点击记录进入订单详情页
          4.校验订单信息
        :param auto_evaluate:
        :return:
        """
        auto_evaluate_page = auto_evaluate
        auto_evaluate_record_page = auto_evaluate_page.go_evaluate_record()
        info_list = auto_evaluate_record_page.get_latest_excited_record_info()
        res = auto_evaluate_record_page.go_order_detail()
        assert res, '跳转详情页失败或者详情页订单号与评价记录订单号不一致'

    @allure.feature('自动评价')
    @allure.story('自动评价页面，可以正常更改评价方式')
    @pytest.mark.skip(reason="避免影响其他调试工作")
    def test_change_evaluate_methods(self, auto_evaluate):
        """
         1.进入自动评价页面
         2.评价方式更改为立即评价，再更改为评价后回评
         3.返回首页，再次进入自动评价页面
         4.判断评价方式是否修改成功
        :param auto_evaluate:
        :return:
        """
        auto_evaluate_page = auto_evaluate
        auto_evaluate_page.change_evaluate_methods(auto_evaluate_page.evaluate_methods_immediatly_locator)
        auto_evaluate_page.change_evaluate_methods(auto_evaluate_page.evaluate_methods_after_locator)
        auto_evaluate_page.back()
        first_page = FirstPage()
        first_page.go_auto_evaluate_page()
        methond = auto_evaluate_page.get_evaluate_methods()
        assert methond == '指定回评', '自动评价页面，评价方式无法正常修改'

    @allure.feature('自动评价')
    @allure.story('自动评价页面，四个子开关可以正常开关')
    @pytest.mark.skip(reason="避免影响其他调试工作")
    def test_four_evaluate_methods(self, auto_evaluate):
        """
         1.进入自动评价页面
         2.关闭四个子开关
         3.返回首页，再次进入自动评价页面
         4.判断子开关是否实际关闭
        :param auto_evaluate:
        :return:
        """
        auto_evaluate_page = auto_evaluate
        auto_evaluate_page.turn_four_switch()
        auto_evaluate_page.back()
        first_page = FirstPage()
        first_page.go_auto_evaluate_page()
        flag = True
        try:
            loop_find(Template(r"pic_data/tpl1582190203262.png", record_pos=(-0.001, -0.064), resolution=(1080, 2340),
                               threshold=0.95))
        except:
            flag = False
        auto_evaluate_page.recover_four_swtich()
        assert flag, '自动评价页面，四个子开关无法正常关闭！'

    @allure.feature('自动评价')
    @allure.story('自动评价页面，主开关，子账号不能切换')
    @pytest.mark.skip(reason="避免影响其他调试工作")
    def test_turn_main_switch(self, auto_evaluate):
        """
         1.进入自动评价页面
         2.切换总开关
         3.判断总开关状态是否变化
        :param auto_evaluate:
        :return:
        """
        auto_evaluate_page = auto_evaluate
        auto_evaluate_page.turn_main_switch()
        flag = True
        try:
            loop_find((Template(r"pic_data/tpl1582194810604.png", record_pos=(-0.004, -0.762), resolution=(1080, 2340),
                                threshold=0.95)))
        except:
            flag = False
        assert flag, '自动评价页面，主开关，子账号切换主开关时，页面显示异常！'
