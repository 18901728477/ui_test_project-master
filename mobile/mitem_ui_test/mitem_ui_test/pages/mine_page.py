
from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import *

class MinePage(BasePage):

    version_number_locator = ('and', (('attr.*=', ('text', '版本号.*')),))  # 版本号

    # 获取版本号
    def get_version(self):
        version_number = init_element(self.version_number_locator)
        version_number_text = version_number.get_text()
        result = version_number_text.split('：')[-1]
        return result

if __name__ == '__main__':
    x = MinePage().get_version()
    print(x)