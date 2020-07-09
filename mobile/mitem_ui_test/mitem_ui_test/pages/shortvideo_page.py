# -*- encoding=utf8 -*-
__author__ = 'xiaoxuan'

from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import *
from mobile.mitem_ui_test.mitem_ui_test.pages.common_list_page import *

class ShortVideo(CommonList):

    single_submit_locator = ('and', (('attr.*=', ('text', '.*生成.*')),))
