from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import BasePage


class ConfigPage(BasePage):

    def config1(self):
        poco("android.support.v7.app.ActionBar$Tab")[2].child().child().click()
        poco(text="核对地址短语").click()
        poco("__react-content").child().child().child()[0].child()[2].child().child().child()[0].child().click()