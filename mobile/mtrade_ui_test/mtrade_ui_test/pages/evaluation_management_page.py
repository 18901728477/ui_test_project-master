import time

from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import BasePage, poco, init_element, locate_by_anchor


class EvalutionManagementPage(BasePage):
    pending_bad_evalution_button_locator = ('and', (('attr=', ('text', '待处理差评')),))
    pending_interim_evalution_button_locator = ('and', (('attr=', ('text', '待处理中评')),))
    to_be_evaluated_button_locator = ('and', (('attr=', ('text', '待评价')),))
    missing_evalution_button_locator = ('and', (('attr=', ('text', '近90天漏评')),))
    bad_evalution_button_locator = ('and', (('attr=', ('text', '差评')),))
    interim_evalution_button_locator = ('and', (('attr=', ('text', '中评')),))
    good_evalution_button_locator = ('and', (('attr=', ('text', '好评')),))
    to_others_evalution_button_locator = ('and', (('attr=', ('text', '给他人的评价')),))
    stop_ta_shooting_locator = ('and', (('attr=', ('text', '阻止Ta拍单')),))  # 阻止Ta拍单
    evalution_link_button_locator = ('and', (('attr=', ('text', '改评链接')),))
    evalution_management_button_locator = ('and', (('attr=', ('text', '评价管理')),))

    # 显示待处理差评数量
    def show_pending_bad_evalution_number(self):
        pending_bad_evalution_button = poco(text="待处理差评")
        return locate_by_anchor(pending_bad_evalution_button, 1, 'l0v0l0').get_text()
        # return poco(text="待处理差评").parent().child("android.view.View")[0].child("android.view.View")[0].child(
        #     "android.view.View").get_text()

    # 显示待处理中评数量
    def show_pending_interim_evalution_number(self):
        pending_interim_evalution_button = poco(text="待处理中评")
        return locate_by_anchor(pending_interim_evalution_button, 1, 'l0v0l0').get_text()
        # return poco(text="待处理中评").parent().child("android.view.View")[0].child("android.view.View")[0].child(
        #     "android.view.View").get_text()

        # pending_interim_evalution_number = get_pending_interim_evalution_number(date_2)
        # poco(text=pending_interim_evalution_number)
        # return poco(text=pending_interim_evalution_number).get_text()

    # 显示待评价数量
    def show_to_be_evaluated_number(self):
        to_be_evaluated_button = poco(text="待评价")
        return locate_by_anchor(to_be_evaluated_button, 1, 'l0v0l0').get_text()
        # return poco(text="待评价").parent().child("android.view.View")[0].child("android.view.View")[0].child(
        #     "android.view.View").get_text()

        # to_be_evaluated_number = get_to_be_evaluated_number()
        # poco(text=to_be_evaluated_number)
        # return poco(text=to_be_evaluated_number).get_text()

    # 显示近90天漏评数量
    def show_missing_evalution_number(self):
        missing_evalution_button = poco(text="近90天漏评")
        missing_evalution_button_info = locate_by_anchor(missing_evalution_button, 1, 'l0v0l0')
        time.sleep(2)
        missing_evalution_button_info.invalidate()
        return missing_evalution_button_info.get_text()
        # return poco(text="近90天漏评").parent().child("android.view.View")[0].child("android.view.View")[0].child(
        #     "android.view.View").get_text()

        # missing_evalution_number = get_missing_evalution_number(date_90)
        # poco(text=missing_evalution_number)
        # return poco(text=missing_evalution_number).get_text()

    # 显示差评数量
    def show_bad_evalution_number(self):
        bad_evalution_button = poco(text="差评")
        return locate_by_anchor(bad_evalution_button, 2, 'l0v0').get_text()
        # return poco(text="差评").parent().child("android.view.View").get_text()

    # 显示中评数量
    def show_interim_evalution_number(self):
        interim_evalution_button = poco(text="中评")
        return locate_by_anchor(interim_evalution_button, 2, 'l1v0').get_text()
        # return poco(text="中评").parent().child("android.view.View").get_text()

    # 显示好评数量
    def show_good_evalution_number(self):
        good_evalution_button = poco(text="好评")
        return locate_by_anchor(good_evalution_button, 2, 'l2v0').get_text()
        # return poco(text="好评").parent().child("android.view.View").get_text()

    # 显示给他人的评价数量
    def show_to_others_evalution_number(self):
        to_others_evalution_button = poco(text="给他人的评价")
        return locate_by_anchor(to_others_evalution_button, 2, 'l3v0').get_text()
        # return poco(text="给他人的评价").parent().child("android.view.View").get_text()

    # 跳转差评页面
    def go_bad_evalution_page(self):
        # bad_evalution_button = UIObjectProxy(poco)
        # bad_evalution_button.query = self.bad_evalution_button_locator
        bad_evalution_button = init_element(self.bad_evalution_button_locator)
        bad_evalution_button.wait()
        bad_evalution_button.click()
        return poco(text="阻止Ta拍单").exists()

    # 跳转中评页面
    def go_interim_evalution_page(self):
        # interim_evalution_button = UIObjectProxy(poco)
        # interim_evalution_button.query = self.interim_evalution_button_locator
        interim_evalution_button = init_element(self.interim_evalution_button_locator)
        interim_evalution_button.wait()
        interim_evalution_button.click()
        return poco(text="阻止Ta拍单").exists()

    # 跳转好评页面
    def go_good_evalution_page(self):
        # good_evalution_button = UIObjectProxy(poco)
        # good_evalution_button.query = self.good_evalution_button_locator
        good_evalution_button = init_element(self.good_evalution_button_locator)
        good_evalution_button.wait()
        good_evalution_button.click()
        result = print(poco(text="阻止Ta拍单").exists())
        return str(result)

    # 跳转给他人的评价页面
    def go_to_others_evalution_page(self):
        # to_others_evalution_button = UIObjectProxy(poco)
        # to_others_evalution_button.query = self.to_others_evalution_button_locator
        to_others_evalution_button = init_element(self.to_others_evalution_button_locator)
        to_others_evalution_button.wait()
        to_others_evalution_button.click()
        result = print(poco(text="阻止Ta拍单").exists())
        return str(result)

    # 跳转待处理差评页面
    def go_pending_bad_evalution_page(self):
        # pending_bad_evalution_button = UIObjectProxy(poco)
        # pending_bad_evalution_button.query = self.pending_bad_evalution_button_locator
        pending_bad_evalution_button = init_element(self.pending_bad_evalution_button_locator)
        pending_bad_evalution_button.wait()
        pending_bad_evalution_button.click()
        poco(text="阻止差评买家拍单").wait_for_appearance(3)
        return poco(text="阻止差评买家拍单").exists()

    # 跳转待处理中评页面
    def go_pending_interim_evalution_page(self):
        # pending_interim_evalution_button = UIObjectProxy(poco)
        # pending_interim_evalution_button.query = self.pending_interim_evalution_button_locator
        pending_interim_evalution_button = init_element(self.pending_interim_evalution_button_locator)
        pending_interim_evalution_button.wait()
        pending_interim_evalution_button.click()
        return poco(text="阻止中评买家拍单").exists()

    # 跳转待评价页面
    def go_to_be_evaluated_page(self):
        # to_be_evaluated_button = UIObjectProxy(poco)
        # to_be_evaluated_button.query = self.to_be_evaluated_button_locator
        to_be_evaluated_button = init_element(self.to_be_evaluated_button_locator)
        to_be_evaluated_button.wait()
        to_be_evaluated_button.click()
        return poco(text="批量评价").exists()

    # 跳转近90天漏评页面
    def go_missing_evalution_page(self):
        # missing_evalution_button = UIObjectProxy(poco)
        # missing_evalution_button.query = self.missing_evalution_button_locator
        missing_evalution_button = init_element(self.missing_evalution_button_locator)
        missing_evalution_button.wait()
        missing_evalution_button.click()
        return poco(text="近90天漏评").exists()

    # 跳转提升店铺等级页面
    def go_shop_level_up_page(self):
        poco(text="快速提升店铺等级").wait()
        poco(text="快速提升店铺等级").click()
        return poco(text="提升店铺等级").exists()


if __name__ == '__main__':
    print(EvalutionManagementPage().show_pending_bad_evalution_number())
