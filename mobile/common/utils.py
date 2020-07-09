import os
import shutil
import socket
import yaml

from mobile.config.path_config import CONFIG


def get_ip():
    # 获取本机电脑名
    my_name = socket.getfqdn(socket.gethostname())
    # 获取本机ip
    my_ip_addr = socket.gethostbyname(my_name)
    return my_ip_addr


def get_yaml_data(yaml_file):
    # 打开yaml文件
    file = open(yaml_file, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()
    # 将字符串转化为字典或列表
    data = yaml.load(file_data, Loader=yaml.FullLoader)
    return data


def millisecond2minute(t: int):
    m = t // 1000 // 60
    s = t // 1000 % 60
    return '{}分{}秒'.format(m, s)

def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    # 判断结果
    if isExists:
        shutil.rmtree(path)
    os.makedirs(path)

if __name__ == '__main__':
    print(get_ip())
    test_file = CONFIG / "person"
    t = get_yaml_data(test_file)
    print(t['item']['mobile'])


