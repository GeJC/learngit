import requests
import datetime
import hashlib
from tkinter import messagebox
import sys


def test_info(appkey, appsecret):
    server_receipt_apiverify = "https://fapiao.glority.cn/v1/user/get_user_info"
    # generate timestamp
    timestamp = int(datetime.datetime.now().timestamp())
    # generate token
    m = hashlib.md5()
    token = appkey + "+" + str(timestamp) + "+" + appsecret
    m.update(token.encode('utf-8'))
    token = m.hexdigest()
    # post request
    data = {'app_key': appkey, 'timestamp': str(timestamp), 'token': token}
    r = requests.post(server_receipt_apiverify, data=data, verify=False)

    if r.status_code != 200:
        messagebox.showerror("错误", "用户信息接口服务器繁忙，请稍后再试！")
        sys.exit()
    else:
        result = r.json()
        return result
        messagebox.showinfo("提示", "大票已使用次数：" + str(result['response']['user_info']['big_usage']) + ",小票已使用次数：" + str(result['response']['user_info']['small_usage']) + ",定额发票已使用次数：" + str(result['response']['user_info']['quota_usage']))

#test_info('5cf8c7b4','a9e1c57de2532f71272040c2c95f1c2b')