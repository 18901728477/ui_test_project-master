
from mobile.mitem_ui_test.mitem_ui_test.pages.base_page import *
import random

class DetailProperty(BasePage):

    select_props = '\ue6ab' # 选择属性图标
    props_after_choose = '\ue618' # 属性选中后的选择框

    # 方法：编辑可选、不可填属性
    def edit_props_enum(self,props_name:str,props_dict:dict) -> str:
        """

        :param props_name:
        可选属性的属性名
        :param props_dict:
        可选属性的属性值，字典类型，不翻页，每次从字典中随机抽1个
        {0：'属性值1', 1：'属性值2', 2：'属性值3'}
        :return:
        返回编辑后的随机属性值
        """
        ele = poco(text=props_name).parent().parent().offspring(text=self.select_props)
        ele.click()
        poco(text='搜索').wait_for_appearance(30) # 获取属性显示等待15秒
        random_key = random.randrange(0, len(props_dict.keys()), 1)  # props_dict的随机key
        props = props_dict.get(random_key)  # rops_dict的随机key获取的随机属性
        poco(text=props).click()
        # 如果随机选的属性值正好和原属性值一样，继续随机选属性值
        while (not poco(text=self.props_after_choose).exists()):
            random_key = random.randrange(0,len(props_dict.keys()),1) # props_dict的随机key
            props = props_dict.get(random_key) # rops_dict的随机key获取的随机属性
            poco(text=props).click()
        poco(text='保存').click()
        return props


    # 方法：编辑可填、不可选属性
    def edit_props_input(self, props_name:str, props_dict:dict) ->str:
        """

        :param props_name:
        :param props_dict:
        :return:
        属性值
        """
        poco(text=props_name).parent().parent().offspring(text=self.select_props).click()
        sleep(3) # 判断属性是否可填，3秒sleep
        random_key = random.randrange(0, len(props_dict.keys()), 1)  # props_dict的随机key
        props = props_dict.get(random_key)  # rops_dict的随机key获取的随机属性
        poco(name='android.widget.EditText').set_text(props)
        return props


    # 方法：编辑多选属性
    def edit_props_multi(self,props_name:str,props_dict:dict):
        """

        :param props_name:
        属性名
        :param props_dict:
        多选属性的dict
        {0:'属性值1', 1:'属性值2', 2:'属性值3'}
        :return:
        """
        poco(text=props_name).parent().parent().offspring(text=self.select_props).click()
        poco(text='搜索').wait_for_appearance(15)  # 获取属性显示等待15秒
        # 取消所有多选属性的勾选
        for x in range(len(poco(text=self.props_after_choose))):
            poco(text=self.props_after_choose).click()
        # 勾选所有多选属性
        for x in range(len(props_dict.keys())):
            poco(text=props_dict.get(x)).click()
        poco(text='保存').click()


    # 方法：返回某个属性的属性值
    def get_props_value(self,props_name) -> str:
        """

        :param props_name:
        :return:
        """
        anchor = poco(text=props_name)
        ele = locate_by_anchor(anchor, 2, 'l1l0l0')
        return get_text_of_view(ele)



