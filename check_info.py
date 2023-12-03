from datetime import datetime, timedelta
import json
import os
import time
import requests

header={
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36'
}

def seconds_to_hms(seconds):
    time_delta = timedelta(seconds=seconds)
    hours, remainder = divmod(time_delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    # 构建时间间隔的字符串表示
    time_str = f"{hours}小时 {minutes}分钟 {seconds}秒"
    if time_delta.days > 0:
        time_str = f"{time_delta.days}天 " + time_str
    return time_str

def convert_bytes_to_human_readable(sum_bytes):
    # 定义转换关系
    kb = sum_bytes / 1024
    mb = kb / 1024
    gb = mb / 1024
    tb = gb / 1024

    # 根据大小选择合适的单位
    if tb >= 1:
        return "{:.2f} TB".format(tb)
    elif gb >= 1:
        return "{:.2f} GB".format(gb)
    elif mb >= 1:
        return "{:.2f} MB".format(mb)
    elif kb >= 1:
        return "{:.2f} KB".format(kb)
    else:
        return "{:.2f} Bytes".format(sum_bytes)

while True:
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        get_info_api="http://172.16.130.31/cgi-bin/rad_user_info?callback=jQuery112406118340540763985_1556004912581&_=1556004912582"
        res=requests.get(get_info_api,headers=header)
        info=json.loads(res.text[42:-1])
        sum_bytes=info['sum_bytes']
        print("用户名:", info['user_name'])
        print("产品名称:", info['products_name'])
        print("用户MAC:", info['user_mac'])
        print("在线IP:",info['online_ip']) 
        print("在线设备数", info['online_device_total'])
        print("登陆时间:", datetime.fromtimestamp(info['add_time']).strftime('%Y-%m-%d %H:%M:%S'))
        print("在线时长:", seconds_to_hms(info['keepalive_time']-info['add_time']))
        print("已用流量:", convert_bytes_to_human_readable(sum_bytes))
        print("已用时长:", seconds_to_hms(info['sum_seconds']))
        print("程序执行完毕")
        input("按Enter键退出...")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    time.sleep(5)
