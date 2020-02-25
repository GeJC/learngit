import os
import time

import requests
import datetime
import hashlib
from tkinter import messagebox
import sys

from outside import MongoDB

RuiQiErrorDict = {'10001': '查无此票', '10002': '查验信息不一致', '10003': '验真次数超过限制，同一张票一天最多可以查验5次',
                  '10004': '不支持验真发票类型', '10005': '无效参数', '10006': '其它错误', '10007': '正在运行'}

def testapi(filepath, appkey, appsecret):
    server_receipt_apiverify = "https://fapiao.glority.cn/v1/item/get_multiple_items_info"
    """
    get receipt info and save the result to .json file
    """
    if not os.path.isfile(filepath):
        print("file not exist")
        return None

    # generate timestamp
    timestamp = int(datetime.datetime.now().timestamp())
    # generate token
    m = hashlib.md5()
    token = appkey + "+" + str(timestamp) + "+" + appsecret
    m.update(token.encode('utf-8'))
    token = m.hexdigest()
    # post request
    files = {'image_file': (os.path.basename(filepath), open(filepath, "rb"), "image/jpeg")}
    data = {'app_key': appkey, 'timestamp': str(timestamp), 'token': token}
    r = requests.post(server_receipt_apiverify, data=data, files=files, verify=False)

    if r.status_code != 200:
        print("failed to identify file: ", filepath)
        messagebox.showerror("错误", "识别接口服务器繁忙，请稍后再试！")
        sys.exit()
    else:
        result = r.json()
        #print(result)
        return result

def ruiqi_chayan(Url, list_dict, appkey, appsecret):
    server_receipt_apiverify = "https://fapiao.glority.cn/v1/item/fapiao_validation"
    #server_async = "https://fapiao.glority.cn/v1/item/get_async_validation"

    result_list = []
    #result async tokens
    error_list = []
    #error subdicts
    #success_list = []
    #check sucess

    for sub_dict in list_dict:
        # generate timestamp
        timestamp = int(datetime.datetime.now().timestamp())
        # generate token
        m = hashlib.md5()
        token = appkey + "+" + str(timestamp) + "+" + appsecret
        m.update(token.encode('utf-8'))
        token = m.hexdigest()
        # post request
        data = {'app_key': appkey, 'timestamp': str(timestamp), 'token': token, 'code': sub_dict['code'], 'number': sub_dict['number'],
            'check_code': sub_dict['check_code'], 'pretax_amount': sub_dict['pretax_amount'], 'date': sub_dict['date'],
            'type': sub_dict['type'], 'is_async': 0}
        r = requests.post(server_receipt_apiverify, data=data, verify=False)
        #print(r.json())

        if r.status_code != 200:
            messagebox.showerror("错误", "识别接口服务器繁忙，请稍后再试！")
            sys.exit()
        else:
            if r.json()['result'] == 0:
            # check error
                messagebox.showerror("错误", "发票代码：" + sub_dict['code'] + " 发票号码：" + sub_dict['number'] + ",验票失败，请求失败")
                tmp_dict = sub_dict.copy()
                #tmp_dict.update(r.json()['response']['data']['identify_results'][0]['details'])
                tmp_dict.update({'check_state': '请求失败'})
                error_list.append(tmp_dict)
            elif r.json()['response']['data']['identify_results'][0]['validation']['code'] in RuiQiErrorDict:
                messagebox.showerror("错误", "发票代码：" + sub_dict['code'] + " 发票号码：" + sub_dict['number'] +
                                     ",验票失败，" + RuiQiErrorDict[r.json()['response']['data']['identify_results'][0]['validation']['code']])
                tmp_dict = sub_dict.copy()
                #tmp_dict.update(r.json()['response']['data']['identify_results'][0]['details'])
                tmp_dict.update({'check_state': RuiQiErrorDict[r.json()['response']['data']['identify_results'][0]['validation']['code']]})
                error_list.append(tmp_dict)
            else:
                tmp_dict = sub_dict.copy()
                tmp_dict.update(r.json()['response']['data']['identify_results'][0]['details'])
                tmp_dict.update({'check_state': '查验一致'})
                result_list.append(tmp_dict)
        # print(result)

    print(result_list)
    print('########################')
    print(error_list)

    #获取异步查验结果(useless)
    #while len(result_list) > 0:
    #time.sleep(60)
    '''
    for result in result_list:
        #tmpr_list = []
        # generate timestamp
        timestamp = int(datetime.datetime.now().timestamp())
        # generate token
        m = hashlib.md5()
        token = appkey + "+" + str(timestamp) + "+" + appsecret
        m.update(token.encode('utf-8'))
        token = m.hexdigest()
        # post request
        data = {'app_key': appkey, 'timestamp': str(timestamp), 'token': token, 'async_token': result['async']}
        r = requests.post(server_async, data=data, verify=False)
        print(r.json())

        if r.status_code != 200:
            messagebox.showerror("错误", "识别接口服务器繁忙，请稍后再试！")
            sys.exit()
        else:
            if r.json()['result'] == 0:
                # check error
                messagebox.showerror("错误", "发票代码：" + result['code'] + " 发票号码：" + result['number'] + ",验票失败，请求失败")
                error_list.append(result)
            elif r.json()['response']['data']['identify_results'][0]['validation']['code'] in RuiQiErrorDict:
                messagebox.showerror("错误", "发票代码：" + result['code'] + " 发票号码：" + result['number'] +
                                     ",验票失败，" + RuiQiErrorDict[r.json()['response']['data']['identify_results'][0]['validation']['code']])
                error_list.append(result)
            else:
                tmpd = result.copy()
                tmpd.update(r.json()['response']['data']['identify_results'][0]['details'])
                sucess_list.append(tmpd)
    #result_list = tmpr_list
    #print(result_list)
    print(sucess_list)
    print('!!!!!!!!!!!!!!!!!!')
    print(error_list)
    print('============')
    '''
    for r in result_list:
        try:
            if MongoDB.select_invoice_info(Url, {'code': r['code'], 'number': r['number']}, r['type']):
                MongoDB.update_invoiceRQ_info(Url, r, r['type'])
        except:
            None
    for e in error_list:
        try:
            if MongoDB.select_invoice_info(Url, {'code': e['code'], 'number': e['number']}, e['type']):
                MongoDB.update_invoiceRQ_info(Url, e, e['type'])
        except:
            None
    return


# testapi("C:\\Users\\jianc\\Desktop\\beta\\invoice\\2019-10-24-13-14-59-01.png", '5cf8c7b4', 'a9e1c57de2532f71272040c2c95f1c2b')
