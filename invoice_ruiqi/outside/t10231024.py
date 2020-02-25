import time
import requests
import hashlib
from urllib import parse
import json
from tkinter import messagebox
from outside import MongoDB


def test1023(list_dict, qiybh, secretKey):
    #url1023 = 'http://www.taxunion.net/base/1023/httpService'正式
    url1023 = 'http://www.taxdata.com.cn/base/1023/httpService'
    application_1023 = '1023'
    request_id = '1562644531442'  # 请求ID
    request_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    data = json.dumps(list_dict).replace(' ', '')
    url_data = parse.quote(data)
    sign = "application=" + application_1023 + "&data=" + url_data + "&qiybh=" + qiybh + "&request_id=" + request_id + "&request_time=" + request_time + secretKey
    m = hashlib.md5()
    m.update(sign.encode('utf-8'))
    sign_MD5 = m.hexdigest().upper()
    body = {'request_time': request_time, 'application': application_1023,
            'data': data, 'sign': sign_MD5, 'request_id': request_id,
            'qiybh': qiybh}

    print(body)
    r = requests.post(url1023, data=body)
    if r.status_code != 200:
        print("failed to identify file: ")
    else:
        result = r.json()
        print(result)
        return result['result_msg']



def test1024(Url, list_dict, qiybh, secretKey):
    #url1024 = 'http://www.taxunion.net/base/1024/httpService'正式
    url1024 = 'http://www.taxdata.com.cn/base/1024/httpService'
    application_1024 = '1024'
    request_id = '1562644531442'  # 请求ID
    request_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    data = json.dumps(list_dict).replace(' ', '')
    url_data = parse.quote(data)
    sign = "application=" + application_1024 + "&data=" + url_data + "&qiybh=" + qiybh + "&request_id=" + request_id + "&request_time=" + request_time + secretKey
    m = hashlib.md5()
    m.update(sign.encode('utf-8'))
    sign2 = m.hexdigest().upper()
    body = {'request_time': request_time, 'application': application_1024, 'data': data, 'sign': sign2, 'request_id': request_id, 'qiybh': qiybh}

    r = requests.post(url1024, data=body)

    if r.status_code != 200:
        print("failed to identify file: ")
        messagebox.showinfo("错误", "查验接口有误，请稍后再试！")
        return "error"
    else:
        hefa_list = []
        buhefa_list = []
        flag = 1
        result = r.json()
        print(result)
        for x in json.loads(result['data']):
            if not('yanpzt' in x):
                continue
            print(x['yanpzt'])
            if x['yanpzt'] == "d01" or x['yanpzt'] == "5":
                #hefa_list.append({'code': x['fapdm'], 'number': x['faphm'], 'type': x['faplx']})
                hefa_list.append(x)
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "0":
                flag = 2
            elif x['yanpzt'] == "2":
                flag = 2
            elif x['yanpzt'] == "4":
                flag = 2
            elif x['yanpzt'] == "a01":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",验票失败：请求不合法")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "b01":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",验票失败：验证码失效")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "b02":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",验票失败：验证码错误")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "b03":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",验票失败：获取Session失败")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "b07":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",验票失败：验证码识别失败")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "c01":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",超过该张发票的单日查验次数(5次），请于24小时之后再进行查验")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "c02":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",验票失败：本IP地址提交的查验请求过于频繁，请稍后再试")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "c03":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",验票失败：超过服务器最大请求数，请稍后访问")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "c04":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",认证失败，请重新登录")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "c05":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",验票失败：发票查验系统发生异常，请稍后再试")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "d02":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",发票作废")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "d03":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",信息不一致")
                print("test11111111111111111111111")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "d04":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",查无此票")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "d05":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",未开通")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "d06":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",已过期")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "d07":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",日期不足8位")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "d08":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",日期格式错误")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "d09":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",开票时间不能大于今天")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "d10":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",发票代码有误")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "d11":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",发票号码有误")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "d12":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",开票日期错误")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'code': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "d13":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",金额有误")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "d14":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",验证码有误")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "000":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",验票失败：未知或无法归类错误")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "001":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",验票失败：日期当天的不能查验")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            elif x['yanpzt'] == "002":
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",验票失败：暂不支持的发票类型")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'faphm': x['faphm']})
            else:
                messagebox.showerror("错误", "发票代码：" + x['fapdm'] + " 发票号码：" + x['faphm'] + ",验票失败：未知或无法归类错误")
                buhefa_list.append({'code': x['fapdm'], 'number': x['faphm']})
                list_dict.remove({'fapdm': x['fapdm'], 'number': x['faphm']})

        #修改查验结果字段
        for hefa in hefa_list:
            try:
                del hefa['details']
                if MongoDB.select_invoice_info(Url, {'code': hefa['fapdm'], 'number': hefa['faphm']}, hefa['faplx']):
                    hefa.update({'check_state': '查验一致'})
                    MongoDB.update_invoice1024_info(Url, hefa, hefa['faplx'])
            except:
                None
        for buhefa in buhefa_list:
            try:
                del buhefa['details']
                if MongoDB.select_invoice_info(Url, {'code': buhefa['fapdm'], 'number': buhefa['faphm']}, buhefa['faplx']):
                    buhefa.update({'check_state': '查验失败'})
                    MongoDB.update_invoice1024_info(Url, buhefa, buhefa['faplx'])
            except:
                None

        return list_dict



#test1023([{'fapdm': '3600163160', 'faphm': '01301047', 'kaiprq': '20190620', 'jine': '174.76', 'waibid': 'uuid', 'faplx': '004', 'goufsbh': '91371000866696280H'}, {'fapdm': '3700163160', 'faphm': '03178628', 'kaiprq': '20190704', 'jine': '2837.86', 'waibid': 'uuid', 'faplx': '004', 'goufsbh': '91371000866696280H'}, {'fapdm': '3700164160', 'faphm': '04861135', 'kaiprq': '20190628', 'jine': '776.70', 'waibid': 'uuid', 'faplx': '004', 'goufsbh': '91371000866696280H'}])
#test1024([{'fapdm': '1100191130', 'faphm': '11847836'}, {'fapdm': '3700182130', 'faphm': '03791779'}],'91371000866696280HNY01' ,'password')
#test1024([{'fapdm': '011001900311', 'faphm': '70514517'}, {'fapdm': '1100183130', 'faphm': '29538664'}, {'fapdm': '032001700611', 'faphm': '62498138'}, {'fapdm': '2102192130', 'faphm': '01575337'}, {'fapdm': '021021800107', 'faphm': '03497480'}, {'fapdm': '050001800211', 'faphm': '65045381'}, {'fapdm': '011001900311', 'faphm': '11101715'}], '91310113MA1GM5488WHL01', 'password')
#test1023([{'fapdm': '3600163160', 'faphm': '01301047', 'kaiprq': '20190620', 'jine': '174.76', 'waibid': 'uuid', 'faplx': '004', 'goufsbh': '91371000866696280H'}], '91310113MA1GM5488WHL01', 'password')