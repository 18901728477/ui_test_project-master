from airtest.core.cv import Template

######高志轩测试机######
# 测试机序列号：
# SERIALNO = 'H8B4C19628020848'
#
# # 活动日历名称
# ACTIVITY_NAME = '夏新势力X'
#
# # 测试机相册路径：
# ADB_PIC_URL = '/sdcard/Pictures'
#
# # adb命令，扫描：
# ADB_SCAN_FILE = 'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/Pictures/test.png'
#
# # 标题优化页面，更新到淘宝按钮,高志轩安卓
# TEMPLATE_UPDATE_TITLE = Template(r'C:\Users\17378\PycharmProjects\ui_test_project\mobile\mitem_ui_test\mitem_ui_test\pic_data\tpl1588920874984.png',
#                                 record_pos=(0.322, -0.202), resolution=(1080, 2340), threshold=0.95)
#
# # 标题优化页面，一键优化按钮,高志轩安卓
# TEMPLATE_ONE_CLICK_IMPOVR = Template(r"C:\Users\17378\PycharmProjects\ui_test_project\mobile\mitem_ui_test\mitem_ui_test\pic_data\tpl1588927371641.png",
#                                      record_pos=(-0.149, -0.195), resolution=(1080, 2340))
#
# # 标题优化页面，一键优化后的更新到淘宝按钮，高志轩安卓
# TEMPLATE_UPDATE_TITLE_AFTER_IMPROVE = Template(r"C:\Users\17378\PycharmProjects\ui_test_project\mobile\mitem_ui_test\mitem_ui_test\pic_data\tpl1588927425322.png",
#                                                record_pos=(0.322, -0.123), resolution=(1080, 2340))
#
# # 出售中的宝贝，有sku，带长图
# ITEM_ONSALE = 'http://item.taobao.com/item.htm?id=615055673244'
# ITEM_ONSALE_TITLE = '自动化专用sku宝贝'
#
# # 仓库中的宝贝，无sku，无长图
# ITEM_INVENTORY = 'http://item.taobao.com/item.htm?id=615305354200'
# ITEM_INVENTORY_TITLE  = '自动化专用无sku宝贝'
#
# # 出售中的宝贝，含有格式要求属性：
# ITEM_PROPERTY_FORMAT = 'http://item.taobao.com/item.htm?id=615388922817'
# ITEM_PROPERTY_FORMAT_TITLE  = '自动化测试专用属性格式宝贝'
#
# # 出售中的宝贝，修改标题的宝贝：
# ITEM_EDIT_TITLE_ONSELA = 'http://item.taobao.com/item.htm?id=618636139934'
# ITEM_EDIT_TITLE_ONSELA_TITLE  = '自动化编辑标题宝贝'
#
# # 已售完的宝贝
# ITEM_SOLDOUT = 'http://item.taobao.com/item.htm?id=609901219488'
# ITEM_SOLDOUT_TITLE  = '自动化专用已售完宝贝'
#
# # 复制链接
# ITEM_COPY_LINK_TITLE = '测试多sku属性宝贝'
# TAOBAO_LINK = 'https://detail.tmall.com/item.htm?id=607499837237'
# WEIXIN_LINK = 'http://2tb.co/i/607499837237'
#
# # 批量修改详情宝贝
# ITEM_UPDATE_DETAIL_NUMID = '615967053902'
# ITEM_UPDATE_DETAIL = 'http://item.taobao.com/item.htm?id=615967053902'
# ITEM_UPDATE_DETAIL_TITLE = '批量修改test自动化宝贝详情批量修改'
#
# # 批量修改标题宝贝
# ITEM_UPDATE_TILTE_NUMID = '618324055508'
# ITEM_UPDATE_TILTE = 'http://item.taobao.com/item.htm?id=618324055508'
# ITEM_UPDATE_TILTE_TITLE = '修改标题标题修改专用宝贝修改标题'
#
# # 列表上下架宝贝
# ITEM_LIST_DETAIL = 'https://item.taobao.com/item.htm?id=614823551101'
# ITEM_LIST_TITLE = '列表页下架专用宝贝'
#
# # 标题优化专用宝贝
# ITEM_TITLE_IMPROVE = 'http://item.taobao.com/item.htm?id=616629564273'
# ITEM_TITLE_IMPROVE_TITLE = '标题优化专用宝贝'


# ######服务器测试机######
# # 测试机序列号：
# SERIALNO = 'RKKDU17B29021713'

# SERIALNO = 'XPU4C16B15005800'
SERIALNO = 'RKKDU18517006681'
# SERIALNO = '229380bc0304'

# 活动日历名称
ACTIVITY_NAME = '夏新势力X'

# 测试机相册路径：
ADB_PIC_URL = '/sdcard/Pictures'

# adb命令，扫描：
ADB_SCAN_FILE = 'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/Pictures/test.png'

# 标题优化页面，更新到淘宝按钮,testphone
TEMPLATE_UPDATE_TITLE = Template(r'C:\mitem_ui_test\mitem_ui_test\pic_data\tpl1588927244635.png',
                                 record_pos=(0.323, -0.147), resolution=(1080, 2160), threshold=0.95)

# 标题优化页面，一键优化按钮,testphone
TEMPLATE_ONE_CLICK_IMPOVR = Template(r'mobile/mitem_ui_test/mitem_ui_test/pic_data/tpl1592412091894.png',
                                     record_pos=(-0.156, 0.074), resolution=(1080, 2160))

# # 标题优化页面，一键优化后的更新到淘宝按钮，testphone
TEMPLATE_UPDATE_TITLE_AFTER_IMPROVE = Template(r"C:\mitem_ui_test\mitem_ui_test\pic_data\tpl1588927425322.png",
                                               record_pos=(0.317, -0.152), resolution=(1080, 2160))
# 出售中的宝贝，有sku，带长图
ITEM_ONSALE = 'http://item.taobao.com/item.htm?id=615055673244'
ITEM_ONSALE_TITLE = '自动化专用sku宝贝'

# 仓库中的宝贝，无sku，无长图
ITEM_INVENTORY = 'http://item.taobao.com/item.htm?id=615305354200'
ITEM_INVENTORY_TITLE = '自动化专用无sku宝贝'

# 出售中的宝贝，含有格式要求属性：
ITEM_PROPERTY_FORMAT = 'http://item.taobao.com/item.htm?id=615388922817'
ITEM_PROPERTY_FORMAT_TITLE = '自动化测试专用属性格式宝贝'

# 出售中的宝贝，修改标题的宝贝：
ITEM_EDIT_TITLE_ONSELA = 'http://item.taobao.com/item.htm?id=618636139934'
ITEM_EDIT_TITLE_ONSELA_TITLE = '自动化编辑标题宝贝'

# 已售完的宝贝
ITEM_SOLDOUT = 'http://item.taobao.com/item.htm?id=609901219488'
ITEM_SOLDOUT_TITLE = '自动化专用已售完宝贝'

# 复制链接
ITEM_COPY_LINK_TITLE = '测试多sku属性宝贝'
TAOBAO_LINK = 'https://detail.tmall.com/item.htm?id=607499837237'
WEIXIN_LINK = 'http://2tb.co/i/607499837237'

# 批量修改详情宝贝
ITEM_UPDATE_DETAIL_NUMID = '615967053902'
ITEM_UPDATE_DETAIL = 'http://item.taobao.com/item.htm?id=615967053902'
ITEM_UPDATE_DETAIL_TITLE = '批量修改test自动化宝贝详情批量修改'

# 批量修改标题宝贝
ITEM_UPDATE_TILTE_NUMID = '618324055508'
ITEM_UPDATE_TILTE = 'http://item.taobao.com/item.htm?id=618324055508'
ITEM_UPDATE_TILTE_TITLE = '修改标题标题修改专用宝贝修改标题'

# 列表上下架宝贝
ITEM_LIST_DETAIL = 'https://item.taobao.com/item.htm?id=614823551101'
ITEM_LIST_TITLE = '列表页下架专用宝贝'

# 标题优化专用宝贝
ITEM_TITLE_IMPROVE = 'http://item.taobao.com/item.htm?id=616629564273'
