from poco.proxy import UIObjectProxy
from time import sleep
from mobile.mtrade_ui_test.mtrade_ui_test.pages.basepage import BasePage, poco, init_element
from mobile.mtrade_ui_test.mtrade_ui_test.pages.evaluation_operation_page import EvaluationOperationPage


class BatchEvaluationPage(BasePage):
    batch_evaluate_locator = ('and', (('attr=', ('text', '批量评价')), ('attr=', ('name', 'android.widget.Button'))))  # 批量评价按钮

    def click_batch_evaluate(self):
        button = init_element(self.batch_evaluate_locator)
        button.click()
        return EvaluationOperationPage()
