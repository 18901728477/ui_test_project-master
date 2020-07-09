import datetime

def get_current_time():
    now_time = datetime.datetime.now()
    return now_time.strftime('%Y%m%d_%H%M%S')  # 固定语法获取时间戳