from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import BasePage, poco


class ElementPage(BasePage):
    def find_price(self):
        price = poco("com.taobao.qianniu:id/lyt_ge_view_container").child("android.widget.FrameLayout").child(
            "android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout")[
            0].offspring("android.widget.ScrollView").child("android.widget.FrameLayout").child(
            "android.widget.FrameLayout").child("android.widget.FrameLayout")[0].child(
            "android.widget.FrameLayout").child("android.widget.FrameLayout").offspring("android.widget.EditText")
        return price

    def find_num(self):
        num = poco("com.taobao.qianniu:id/lyt_ge_view_container").child("android.widget.FrameLayout").child(
            "android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout")[
            0].offspring("android.widget.ScrollView").child("android.widget.FrameLayout").child(
            "android.widget.FrameLayout").child("android.widget.FrameLayout")[2].child(
            "android.widget.FrameLayout").child("android.widget.FrameLayout").offspring("android.widget.EditText")
        return num

# 实在找不到...
