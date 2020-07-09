# 测试机序列号
# SERIALNO = 'RKKDU17B29021713'
# 旧手机
# SERIALNO = 'RKKDU18517006681'
# 新手机
# SERIALNO = 'XPU4C16B15005800'
# 黑色手机
SERIALNO = 'RKKDU17B29021713'



#  购物车订单号
RE_ORDER = r'\d{18}'
# 待付款订单号
WAIT_BUYER_PAY_ORDER = '1051383618969620411'
# 待付款购物车订单号
WAIT_BUYER_PAY_ORDER_CART = '1051354209726620411'
# 已发货订单号
WAIT_BUYER_CONFIRM_GOODS = '1040495617643477590'
# 待评价订单号  TRADE_FINISHED
NEED_RATE = '837697763781436522'
# 待发货订单号
WAIT_SELLER_SEND_GOODS = '901571584336620411'
# 待发货购物车订单号
WAIT_SELLER_SEND_GOODS_CART = '808961987092436522'
# 待发货合并订单号
WAIT_SELLER_SEND_GOODS_COMBINE = ('896125728574153634', '896135424450153634')
# 待发货有打印记录的订单号
WAIT_SELLER_SEND_GOODS_WITH_PRINT_HISTORY = '884085411371313181'
# 待发货无打印记录的订单号
WAIT_SELLER_SEND_GOODS_WITHOUT_PRINT_HISTORY = '874629024301313181'
# 退款中订单号
WAIT_REFUND_ORDER = '820907490767712910'
# 打印信息
PRINT_HISTORY = ''

# 订单信息
ORDER_INFO = {"收件人手机": "18621729133", "收件人手机f": "186-2172-9133", "买家昵称": "crutisgu94",
              "收货地址": "上海，上海市，宝山区，高境镇新二路55号皇冠，201900",
              "收件人姓名": "顾超", "备注": "自动化测试备注", "留言": "自动化测试留言", "卖家昵称": "赵东昊的测试店铺"}
ORDER_INFO_CART = {"收件人手机": "18621729133", "收件人手机f": "186-2172-9133", "买家昵称": "crutisgu94",
                   "收货地址": "上海，上海市，宝山区，高境镇新二路55号皇冠，201900",
                   "收件人姓名": "顾超", "备注": "自动化测试备注", "留言": "自动化测试留言", "卖家昵称": "赵东昊的测试店铺"}
# 订单中的商品信息
ITEM_INFO = {"商品标题": "自动化测试专用商品1", "商家编码": "商家编码：主商家编码", "属性": ["40X40cm", "测试属性1", "泰麂绒"]}
ITEM_INFO_CART = [{"商品标题": "自动化测试专用商品1", "商家编码": "商家编码：主商家编码", "属性": ["40X40cm", "测试属性1", "泰麂绒"]},
                  {"商品标题": "自动化测试专用商品2", "商家编码": "商家编码：测试子编码2", "属性": "测试属性2"}]

# 收货信息
RECEIVER_INFO = '顾超，18621729133，上海，上海市，宝山区，高境镇新二路55号皇冠，201900'

# 旺旺催付短语
WW_REMIND = '我们仓库是四点前统一发货的哦，您四点前方便付款么，\
我们可以及时给您安排发货，这样您就能早一天收到我们的产品和礼物哦。http://trade.taobao.com/trade/detail/trade_item_detail.htm?bizOrderId={}\t'.format(
    WAIT_BUYER_PAY_ORDER)

# 核对地址短语
CHECK_ADDRESS_PHRASE = '''亲，请核对下地址哦：
买家姓名：顾超
收货地址：上海，上海市，宝山区，高境镇新二路55号皇冠，201900
联系方式：18621729133 
买家邮编：201900'''

# 核对订单短语
CHECK_ORDER_PHRASE = '''亲，请核对您购买的宝贝信息
标题：自动化测试专用商品1
属性：尺寸:40X70CM;颜色分类:测试属性1;材质:麂皮绒
数量:1
买家姓名：顾超
收货地址：上海,上海市,宝山区,高境镇 新二路55号皇冠
联系方式：18621729133
买家邮编：201900'''
