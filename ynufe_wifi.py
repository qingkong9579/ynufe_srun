from datetime import datetime, timedelta
import json
import requests
import time
import re
from encryption.srun_md5 import *
from encryption.srun_sha1 import *
from encryption.srun_base64 import *
from encryption.srun_xencode import *
header={
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36'
}
init_url="http://172.16.130.31"
get_challenge_api="http://172.16.130.31/cgi-bin/get_challenge"

srun_portal_api="http://172.16.130.31/cgi-bin/srun_portal"
get_info_api="http://172.16.130.31/cgi-bin/rad_user_info?callback=jQuery112406118340540763985_1556004912581&_=1556004912582"
n = '200'
type = '1'
ac_id='1'
enc = "srun_bx1"

def get_chksum():
	chkstr = token+username
	chkstr += token+hmd5
	chkstr += token+ac_id
	chkstr += token+ip
	chkstr += token+n
	chkstr += token+type
	chkstr += token+i
	return chkstr
def get_info():
	info_temp={
		"username":username,
		"password":password,
		"ip":ip,
		"acid":ac_id,
		"enc_ver":enc
	}
	i=re.sub("'",'"',str(info_temp))
	i=re.sub(" ",'',i)
	return i
def init_getip():
	global ip
	init_res=requests.get(init_url,headers=header)
	print("初始化获取ip")
	pattern = r'<script>.*?ip\s*:\s*"(.*?)",.*?</script>'
	ip=re.search(pattern,init_res.text, re.DOTALL).group(1)
	
def get_token():
	# print("获取token")
	global token
	get_challenge_params={
		"callback": "jQuery112404953340710317169_"+str(int(time.time()*1000)),
		"username":username,
		"ip":ip,
		"_":int(time.time()*1000),
	}
	get_challenge_res=requests.get(get_challenge_api,params=get_challenge_params,headers=header)
	token=re.search('"challenge":"(.*?)"',get_challenge_res.text).group(1)

def do_complex_work():
	global i,hmd5,chksum
	i=get_info()
	i="{SRBX1}"+get_base64(get_xencode(i,token))
	hmd5=get_md5(password,token)
	chksum=get_sha1(get_chksum())

def login():
	srun_portal_params={
	'callback': 'jQuery11240645308969735664_'+str(int(time.time()*1000)),
	'action':'login',
	'username':username,
	'password':'{MD5}'+hmd5,
	'ac_id':ac_id,
	'ip':ip,
	'chksum':chksum,
	'info':i,
	'n':n,
	'type':type,
	'os':'windows+10',
	'name':'windows',
	'double_stack':'0',
	'_':int(time.time()*1000)
	}
	# print(srun_portal_params)
	srun_portal_res=requests.get(srun_portal_api,params=srun_portal_params,headers=header)
	if srun_portal_res.status_code==200:
		print("登录成功")

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

if __name__ == '__main__':
	global username,password
	username = '******'
	username = username +'@ynufe'
	password="******"
	init_getip()
	get_token()
	do_complex_work()
	login()
	res=requests.get(get_info_api,headers=header)
	info=json.loads(res.text[42:-1])
	sum_bytes=info['sum_bytes']
	print("用户名:", info['user_name'])
	print("产品名称:", info['products_name'])
	print("用户MAC:", info['user_mac'])
	print("在线IP:",info['online_ip']) 
	print("登陆时间:", datetime.fromtimestamp(info['add_time']).strftime('%Y-%m-%d %H:%M:%S'))
	print("在线时长:", seconds_to_hms(info['keepalive_time']-info['add_time']))
	print("已用流量:", convert_bytes_to_human_readable(sum_bytes))
	print("已用时长:", seconds_to_hms(info['sum_seconds']))
	print("程序执行完毕")
	input("按Enter键退出...")
	