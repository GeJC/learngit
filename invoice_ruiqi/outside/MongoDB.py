import pymongo
import time
import os
import xlsxwriter
from tkinter import messagebox

from outside.register import ServerUrl

MongodbUrl = "mongodb://localhost:27017/"
MongodbManagerUrl = "mongodb://localhost:27017/"


InvoiceKindDict = {'TB_10100_info': 0, 'TB_10101_info': 0, 'TB_10102_info': 0, 'TB_10103_info': 1, 'TB_10505a_info': 2,
'TB_10200_info': 3, 'TB_10400_info': 4, 'TB_10500_info': 5, 'TB_10503_info': 6, 'TB_10505_info':7, 'TB_10506_info': 8,
'TB_20105_info': 9}
InvoiceKindList = [
#增值税发票（专票，普票，电子发票）
{'code': '发票代码','number': '发票号码','date': '开票日期','pretax_amount': '税前金额','total': '总金额','tax': '税额',
 'seller': '销售方名称','seller_tax_id': '销售方纳税人识别号','buyer': '购买方方名称','buyer_tax_id': '购买方纳税人识别号',
 'company_seal': '是否有公司印章（0：没有； 1： 有）','form_type': '发票是第几联','kind': '发票消费类型','ciphertext': '密码区',
 'transit_mark': '通行费标志','oil_mark': '成品油标志','machine_code': '机器编号','travel_tax': '车船税','receiptor': '收款人',
 'reviewer': '复核','issuer': '开票人','province': '省','city': '市','service_name': '服务类型','remark': '备注',
 'item_names': '品名','agent_mark': '是否代开','acquisition_mark': '是否收购','block_chain': '区块链标记',
 'stamp_info': '财务章识别内容', 'insert_date': '录入时间', 'check_state': '查验状态'},

#增值税普通发票 卷票
{'code': '发票代码', 'number': '号码', 'date': '日期',  'check_code': '校验码', 'seller': '销售方名称', 'seller_tax_id': '销售方纳税人识别号',
 'buyer': '购买方方名称', 'buyer_tax_id': '购买方纳税人识别号', 'category': '种类，oil 表示是加油票', 'total': '总金额', 'kind':  '发票消费类型',
 'province': '省', 'city': '市', 'company_seal': '是否有公司印章（0：没有； 1： 有）', 'service_name': '服务类型', 'item_names': '品名',
 'stamp_info': '财务章识别内容', 'insert_date': '录入时间', 'check_state': '查验状态'},

#船票
{'code': '发票代码','number': '发票号码','date': '开票日期','time':'时间','station_geton': '出发站',
 'station_getoff': '达到车站','total': '总金额','name':'姓名','kind':'发票消费类型','province':'省','city':'市','currency_code':'币种',
 'stamp_info': '财务章识别内容', 'insert_date': '录入时间'},

#定额发票
{'code': '发票代码', 'number': '号码', 'total': '总金额', 'kind':  '发票消费类型', 'province': '省', 'city': '市',
 'company_seal': '是否有公司印章（0：没有； 1： 有）',
 'stamp_info': '财务章识别内容', 'insert_date': '录入时间'},

#机打发票
{'code': '发票代码','number': '发票号码','date': '开票日期','time':'时间','check_code':'校验码',
 'category':'种类，oil 表示是加油票','total':'总金额','seller':'销售方名称','seller_tax_id':'销售方纳税人识别号',
 'buyer':'购买方方名称','buyer_tax_id':'购买方纳税人识别号','kind':'发票消费类型','province':'省','city':'市',
 'company_seal':'是否有公司印章（0：没有； 1： 有）',
 'stamp_info': '财务章识别内容', 'insert_date': '录入时间'},

#出租车
{'code': '发票代码', 'number': '发票号码', 'date': '乘车日期', 'time_geton': '上车时间', 'time_getoff': '下车时间', 'mileage': '里程',
 'total': '总金额', 'place': '发票所在地', 'kind':  '发票消费类型', 'province': '省', 'city': '市', 'license_plate': '车牌号',
 'stamp_info': '财务章识别内容', 'insert_date': '录入时间'},

#火车票
{'number': '号码', 'date': '乘车日期', 'time': '乘车时间', 'name': '乘车人姓名', 'station_geton': '上车车站', 'station_getoff': '下车车站',
 'train_number': '车次', 'seat': '座位类型', 'total': '总金额', 'kind':  '发票消费类型', 'serial_number':  '序列号', 'user_id':  '身份证号',
 'stamp_info': '财务章识别内容', 'insert_date': '录入时间'},

#客运汽车
{'code': '发票代码','number': '发票号码','date': '开票日期','time':'时间','check_code':'校验码','station_geton':'出发车站',
 'station_getoff':'达到车站','total':'总金额','name':'姓名','kind':'发票消费类型','user_id':'身份证号',
 'stamp_info': '财务章识别内容', 'insert_date': '录入时间'},

#航空运输电子客票行程单
{'user_name': '乘机人姓名', 'user_id':'身份证号', 'number': '电子客票号码', 'check_code': '验证码', 'date': '填开日期',
 'agentcode': '销售单位代号', 'issue_by': '填开单位', 'fare': '票价', 'tax': '税费', 'fuel_surcharge': '燃油附加费',
 'caac_development_fund': '民航发展基金', 'insurance': '保险费', 'total': '总金额', 'flights': '航班信息', 'kind':  '发票消费类型',
 'international_flag': '国内国际标签', 'print_number': '印刷序号',
 'stamp_info': '财务章识别内容', 'insert_date': '录入时间'},

#滴滴出行行程单
{'date': '申请日期', 'date_start': '行程开始时间', 'date_end': '行程结束时间', 'phone': '行程人手机号', 'total': '总计',
 'items': '行程信息', 'stamp_info': '财务章识别内容', 'insert_date': '录入时间'}
]

#xls output title
Key_dict = {'code': '发票代码', 'number': '发票号码', 'date': '开票日期', 'pretax_amount': '税前金额',
                'tax': '税额', 'check_code': '校验码', 'total': '总金额', 'seller': '销售方名称', 'seller_tax_id': '销售方纳税人识别号',
                'buyer': '购买方名称', 'buyer_tax_id': '购买方纳税人识别号', 'company_seal': '公司印章（0：没有，1：有）',
                'form_type': '发票是第几联', 'form_name': '发票联次', 'kind': '发票消费类型', 'ciphertext': '密码',
                'receiptor': '收款人', 'reviewer': '复核', 'issuer': '开票人', 'province': '省',
                'machine_code': '机器编号', 'city': '市', 'service_name': '服务类型', 'remark': '备注', 'item_names': '品名', 'insert_date': '录入时间',
                'category': '种类', 'mileage': '里程', 'time_geton': '上车时间', 'time_getoff': '下车时间', 'license_plate': '车牌号',
                'name': '乘车人姓名', 'station_geton': '上车车站', 'station_getoff': '下车车站', 'train_number': '车次',
                'seat': '座位类型', 'serial_number': '序列号', 'user_id': '身份证号', 'agentcode': '销售单位代号', 'time': '时间',
                'fare': '票价', 'fuel_surcharge': '燃油附加费', 'caac_development_fund': '民航发展基金', 'insurance': '保险费',
                'flights': '航班', 'place': '发票所在地', 'user_name': '乘机人姓名', 'international_flag': '国内国际标签',
                'check_state': '查验状态', 'stamp_info': '财务章识别内容'}
#'_id': '发票id', need more fix

#all kinds
DB_dict = {'10100': 'TB_10100_info', '004': 'TB_10100_info', '10101': 'TB_10101_info', '007': 'TB_10101_info',
           '10102': 'TB_10102_info', '026': 'TB_10102_info', '014': 'TB_10102_info', '10103': 'TB_10103_info',
           '025': 'TB_10103_info', '10104': 'TB_10104_info', '005': 'TB_10104_info', '10105': 'TB_10105_info',
           '10105a': 'TB_10105a_info', '10200': 'TB_10200_info', '10400': 'TB_10400_info', '10500': 'TB_10500_info',
           '10503': 'TB_10503_info', '10505': 'TB_10505_info', '10506': 'TB_10506_info', '10507': 'TB_10507_info',
           '20105': 'TB_20105_info'}

#check 1024 二手车10105接口暂不开放，暂不查验
DB_check_dict = {'10100': 'TB_10100_info', '004': 'TB_10100_info', '10101': 'TB_10101_info', '007': 'TB_10101_info',
                 '10102': 'TB_10102_info','026': 'TB_10102_info', '014': 'TB_10102_info', '10103': 'TB_10103_info',
                 '025': 'TB_10103_info', '10104': 'TB_10104_info', '005': 'TB_10104_info'}

#1024返回结果和数据库内key的对应关系
Name_1024_dict = {'beiz': 'remark', 'kaiprq': 'date', 'jine': 'pretax_amount', 'shuie': 'tax', 'xiaoym': 'check_code',
                  'xiaofmc': 'seller', 'xiaofsbh': 'seller_tax_id', 'goufmc': 'buyer', 'goufsbh': 'buyer_tax_id',
                  'kaipr': 'issuer', 'shoukr': 'receiptor', 'fuhr': 'reviewer', 'shangpmc': 'item_names',
                  'check_state': 'check_state'}
#睿琪
Name_RQ_dict = {'remark': 'remark', 'date': 'date', 'pretax_amount': 'pretax_amount', 'tax': 'tax', #'check_code': 'check_code',
                'seller': 'seller', 'seller_tax_id': 'seller_tax_id', 'buyer': 'buyer', 'buyer_tax_id': 'buyer_tax_id',
                'issuer': 'issuer', 'receiptor': 'receiptor', 'reviewer': 'reviewer', 'item_names': 'item_names',
                'check_state': 'check_state'}




#11/22 fix register & sign in, using unique user_info database
#Future TODO:
#理想情况：客户端和服务器端各有一个程序，客户端全部数据发送到服务器端，不直接修改数据库
#or：客户通过网页使用系统，前端只做数据传输
#能用就行：没有服务器端程序，客户端直接改数据库，*安全问题*
def insert_DB(Url, info_dict):
    info_dict.update({'insert_date': str(time.strftime("%Y%m%d", time.localtime()))})
    #"mongodb://"+username+"@"+password+"123.177.21.138:27017/"+dbname
    myclient = pymongo.MongoClient(Url)  # 连接DB
    mydb = myclient[Url.split(ServerUrl)[-1]]  # 创建DB
    mycol = mydb["user_table"]  # 创建collection
    mycol.insert_one(info_dict)  # 插入字典

#11/22 fix register & sign in, using unique user_info database
def select_DB(Url, info_dict):
    myclient = pymongo.MongoClient(Url)  # 连接DB
    mydb = myclient[Url.split(ServerUrl)[-1]]  # 创建DB
    mycol = mydb["user_table"]  # 创建collection
    return mycol.find_one(info_dict)


#11/22 fix register & sign in, using unique user_info database
def del_DB(Url):
    myclient = pymongo.MongoClient(Url)  # 连接DB
    mydb = myclient[Url.split(ServerUrl)[-1]]  # 创建DB
    mycol = mydb["user_table"]  # 创建collection
    mycol.delete_many({})


def insert_invoice_info(Url, invoice_info_dict, kind):
    myclient = pymongo.MongoClient(Url)  # 连接DB
    mydb = myclient[Url.split(ServerUrl)[-1]]  # 创建DB
    invoice_info_dict.update({'insert_date': str(time.strftime("%Y%m%d", time.localtime()))})

    #11/21 5kinds to check
    if kind in DB_check_dict:
        invoice_info_dict.update({'check_state':'待查验'})
    #shorter
    if kind in DB_dict:
        mycol = mydb[DB_dict[kind]]  # 增值税专用发票
        mycol.insert_one(invoice_info_dict)
    else:
        return
    '''
    if kind in {'10100', '004'}:
        mycol = mydb["TB_10100_info"]   #增值税专用发票
        mycol.insert_one(invoice_info_dict)
    elif kind in {'10101', '007'}:
        mycol = mydb["TB_10101_info"]   #增值税普通发票
        mycol.insert_one(invoice_info_dict)
    elif kind in {'10102', '026', '014'}:
        mycol = mydb["TB_10102_info"]   #增值税电子普通发票
        mycol.insert_one(invoice_info_dict)
    elif kind in {'10103', '025'}:
        mycol = mydb["TB_10103_info"]   #增值税普通发票(卷票)
        mycol.insert_one(invoice_info_dict)
    elif kind in {'10104', '005'}:
        mycol = mydb["TB_10104_info"]   #机动车销售统一发票
        mycol.insert_one(invoice_info_dict)
    elif kind == '10105':
        mycol = mydb["TB_10105_info"]   #二手车销售统一发票
        mycol.insert_one(invoice_info_dict)
    elif kind == '10105a':
        mycol = mydb["TB_10105a_info"]   #船票
        mycol.insert_one(invoice_info_dict)
    elif kind == '10200':
        mycol = mydb["TB_10200_info"]   #定额发票
        mycol.insert_one(invoice_info_dict)
    elif kind == '10400':
        mycol = mydb["TB_10400_info"]   #机打发票
        mycol.insert_one(invoice_info_dict)
    elif kind == '10500':
        mycol = mydb["TB_10500_info"]   #出租车发票
        mycol.insert_one(invoice_info_dict)
    elif kind == '10503':
        mycol = mydb["TB_10503_info"]   #火车票
        mycol.insert_one(invoice_info_dict)
    elif kind == '10505':
        mycol = mydb["TB_10505_info"]   #客运汽车
        mycol.insert_one(invoice_info_dict)
    elif kind == '10506':
        mycol = mydb["TB_10506_info"]   #航空运输电子客票行程单
        mycol.insert_one(invoice_info_dict)
    elif kind == '10507':
        mycol = mydb["TB_10507_info"]   #过路费发票
        mycol.insert_one(invoice_info_dict)
    elif kind == '20105':
        mycol = mydb["TB_20105_info"]   #滴滴出行行程单
        mycol.insert_one(invoice_info_dict)
    else:
        return
    '''


def select_invoice_info(Url, invoice_info_dict, kind):
    myclient = pymongo.MongoClient(Url)  # 连接DB
    mydb = myclient[Url.split(ServerUrl)[-1]]  # 创建DB

    #11/21 shorter
    if kind in DB_dict:
        mycol = mydb[DB_dict[kind]]  # 创建collection
        return mycol.count_documents({'code': invoice_info_dict['code'], 'number': invoice_info_dict['number']})  # 查找字典
    else:
        return
    '''
    if kind in {'10100', '004'}:
        mycol = mydb["TB_10100_info"]  # 创建collection
        return mycol.count_documents({'code': invoice_info_dict['code'], 'number': invoice_info_dict['number']})  # 查找字典
    elif kind in {'10101', '007'}:
        mycol = mydb["TB_10101_info"]  # 创建collection
        return mycol.count_documents({'code': invoice_info_dict['code'], 'number': invoice_info_dict['number']})  # 查找字典
    elif kind in {'10102', '026', '014'}:
        mycol = mydb["TB_10102_info"]  # 创建collection
        return mycol.count_documents({'code': invoice_info_dict['code'], 'number': invoice_info_dict['number']})  # 查找字典
    elif kind == kind in {'10103', '025'}:
        mycol = mydb["TB_10103_info"]  # 创建collection
        return mycol.count_documents({'code': invoice_info_dict['code'], 'number': invoice_info_dict['number']})  # 查找字典
    elif kind in {'10104', '005'}:
        mycol = mydb["TB_10104_info"]  # 创建collection
        return mycol.count_documents({'code': invoice_info_dict['code'], 'number': invoice_info_dict['number']})  # 查找字典
    elif kind == '10105':
        mycol = mydb["TB_10105_info"]  # 创建collection
        return mycol.count_documents({'code': invoice_info_dict['code'], 'number': invoice_info_dict['number']})  # 查找字典
    elif kind == '10105a':
        mycol = mydb["TB_10105a_info"]  # 创建collection
        return mycol.count_documents({'code': invoice_info_dict['code'], 'number': invoice_info_dict['number']})  # 查找字典
    elif kind == '10200':
        mycol = mydb["TB_10200_info"]  # 创建collection
        return mycol.count_documents({'code': invoice_info_dict['code'], 'number': invoice_info_dict['number']})  # 查找字典
    elif kind == '10400':
        mycol = mydb["TB_10400_info"]  # 创建collection
        return mycol.count_documents({'code': invoice_info_dict['code'], 'number': invoice_info_dict['number']})  # 查找字典
    elif kind == '10500':
        mycol = mydb["TB_10500_info"]  # 创建collection
        return mycol.count_documents({'code': invoice_info_dict['code'], 'number': invoice_info_dict['number']})  # 查找字典
    elif kind == '10503':
        mycol = mydb["TB_10503_info"]  # 创建collection
        return mycol.count_documents({'code': invoice_info_dict['code'], 'number': invoice_info_dict['number']})  # 查找字典
    elif kind == '10505':
        mycol = mydb["TB_10505_info"]  # 创建collection
        return mycol.count_documents({'code': invoice_info_dict['code'], 'number': invoice_info_dict['number']})  # 查找字典
    elif kind == '10506':
        mycol = mydb["TB_10506_info"]  # 创建collection
        return mycol.count_documents({'code': invoice_info_dict['code'], 'number': invoice_info_dict['number']})  # 查找字典
    elif kind == '10507':
        mycol = mydb["TB_10507_info"]  # 创建collection
        return mycol.count_documents({'code': invoice_info_dict['code'], 'number': invoice_info_dict['number']})  # 查找字典
    elif kind == '20105':
        mycol = mydb["TB_20105_info"]  # 创建collection
        return mycol.count_documents({'code': invoice_info_dict['code'], 'number': invoice_info_dict['number']})  # 查找字典
    else:
        return
    '''


def del_invoice_info(Url):
    myclient = pymongo.MongoClient(Url)  # 连接DB
    mydb= myclient[Url.split(ServerUrl)[-1]]  # 创建DB
    mycol = mydb["TB_invoice_info"]
    mycol.drop()

#useless
'''
def update_invoice_info(invoice_info_dict, kind):
    myclient = pymongo.MongoClient(MongodbUrl)  # 连接DB
    mydb = myclient[Url.split(ServerUrl)[-1]]  # 创建DB
    if kind in {'10100', '004'}:#专票
        mycol = mydb["TB_10100_info"]  #创建collection
        mycol.update_one({'code': invoice_info_dict['code'], 'number': invoice_info_dict['number']}, {"$set": invoice_info_dict})
    elif kind in {'10101', '007'}:#普票
        mycol = mydb["TB_10101_info"]  #创建collection
        mycol.update_one({'code': invoice_info_dict['code'], 'number': invoice_info_dict['number']}, {"$set": invoice_info_dict})
    elif kind in {'10102', '026', '014'}:#增值税电子普通发票
        mycol = mydb["TB_10102_info"]  #创建collection
        mycol.update_one({'code': invoice_info_dict['code'], 'number': invoice_info_dict['number']}, {"$set": invoice_info_dict})
    elif kind in {'10104', '005'}:#机动车销售统一发票
        mycol = mydb["TB_10104_info"]  # 创建collection
        mycol.update_one({'code': invoice_info_dict['code'], 'number': invoice_info_dict['number']}, {"$set": invoice_info_dict})
    elif kind in {'10103', '025'}:#增值税普通发票(卷票)
        mycol = mydb["TB_10105_info"]  # 创建collection
        mycol.update_one({'code': invoice_info_dict['code'], 'number': invoice_info_dict['number']}, {"$set": invoice_info_dict})
    else:
        return
'''

#11/21 修改查验结果(查验返回结果和数据库中字段不匹配，先查找再修改)
def update_invoice1024_info(Url, invoice1024_dict, faplx):
    myclient = pymongo.MongoClient(Url)  # 连接DB
    mydb = myclient[Url.split(ServerUrl)[-1]]  # 创建DB
    mycol = mydb[DB_dict[faplx]]
    find_invoice = mycol.find({'code': invoice1024_dict['fapdm'], 'number': invoice1024_dict['faphm']})[0]
    for entry in invoice1024_dict:
        #修改对应字段，忽略数据库不存在的部分
        if (entry in Name_1024_dict) and (Name_1024_dict[entry] in find_invoice) and (invoice1024_dict[entry] != ''):
            find_invoice[Name_1024_dict[entry]] = invoice1024_dict[entry]
    mycol.update_one({'code': invoice1024_dict['fapdm'], 'number': invoice1024_dict['faphm']}, {"$set": find_invoice})
    return

#2/18 修改查验结果(换成睿琪接口)
def update_invoiceRQ_info(Url, invoiceRQ_dict, faplx):
    myclient = pymongo.MongoClient(Url)  # 连接DB
    mydb = myclient[Url.split(ServerUrl)[-1]]  # 创建DB
    mycol = mydb[DB_dict[faplx]]
    find_invoice = mycol.find({'code': invoiceRQ_dict['code'], 'number': invoiceRQ_dict['number']})[0]
    for entry in invoiceRQ_dict:
        #修改对应字段，忽略数据库不存在的部分
        if (entry in Name_RQ_dict) and (Name_RQ_dict[entry] in find_invoice) and (invoiceRQ_dict[entry] != ''):
            find_invoice[entry] = invoiceRQ_dict[entry]
    mycol.update_one({'code': invoiceRQ_dict['code'], 'number': invoiceRQ_dict['number']}, {"$set": find_invoice})
    return

def select_invoice_result(Url, path, start_day1, end_day1, start_day2, end_day2, CheckVar4):
    myclient = pymongo.MongoClient(Url)  # 连接DB
    mydb = myclient[Url.split(ServerUrl)[-1]]  # 创建DB
    TB_list1 = ['TB_10100_info', 'TB_10101_info', 'TB_10102_info', 'TB_10103_info', 'TB_10104_info', 'TB_10105_info', 'TB_10105a_info', 'TB_10200_info', 'TB_10400_info', 'TB_10500_info', 'TB_10503_info', 'TB_10505_info', 'TB_10506_info', 'TB_10507_info', 'TB_20105_info']
    TB_list2 = ['TB_10503_info', 'TB_10505_info', 'TB_10506_info']
    TB_dict = {'TB_10100_info': '增值税专用发票', 'TB_10101_info': '增值税普通发票', 'TB_10102_info': '增值税电子普通发票', 'TB_10103_info': '增值税普通发票(卷票)', 'TB_10104_info': '机动车销售统一发票', 'TB_10105_info': '二手车销售统一发票', 'TB_10505a_info':'船票', 'TB_10200_info': '定额发票', 'TB_10400_info': '机打发票', 'TB_10500_info': '出租车发票', 'TB_10503_info': '火车票', 'TB_10505_info': '客运汽车', 'TB_10506_info': '航空运输电子客票行程单', 'TB_10507_info': '过路费发票', 'TB_20105_info': '滴滴出行行程单'}
    #11/21 fix output



    #挑选展示发票种类
    if CheckVar4 == 0:
        TB_list = TB_list1
    else:
        TB_list = TB_list2

    #写入结果信息
    workbook = xlsxwriter.Workbook(os.path.abspath(os.path.abspath(path)) + '\查询结果.xlsx')

    for TB in TB_list:
        mycol = mydb[TB]  # 创建collection
        if mycol.find_one(): #如果数据不为空
            #print(mycol.find_one())

            #写入header
            i = 0
            #12/5 fix when find result and title dont match, sheettitle contains all titles
            worksheet = workbook.add_worksheet(TB_dict[TB])
            if TB in InvoiceKindDict:
                sheettitle = InvoiceKindList[InvoiceKindDict[TB]]
                for key in sheettitle:
                    worksheet.write(0, i, sheettitle[key])
                    i = i + 1
            else:
                sheettitle = mycol.find_one()
                for key in mycol.find_one():
                    if key in Key_dict:
                        worksheet.write(0, i, Key_dict[key])
                        i = i + 1
                    else:
                        del sheettitle[key]

            #workbook.close()

            #查询数据
            if start_day1 == '':
                start_day1 = str(time.strftime("%Y%m%d", time.localtime()))
            else:
                start_day1 = start_day1[:4]+start_day1[4:6]+start_day1[-2:]

            if end_day1 == '':
                end_day1 = str(time.strftime("%Y%m%d", time.localtime()))
            else:
                end_day1 = end_day1[:4]+end_day1[4:6]+end_day1[-2:]

            if start_day2 == '':
                start_day2 = str(time.strftime("%Y%m%d", time.localtime()))
            else:
                start_day2 = start_day2[:4]+start_day2[4:6]+start_day2[-2:]

            if end_day2 == '':
                end_day2 = str(time.strftime("%Y%m%d", time.localtime()))
            else:
                end_day2 = end_day2[:4]+end_day2[4:6]+end_day2[-2:]

            #正则查询
            if TB in {'TB_10200_info', 'TB_10506_info'}:
                result = mycol.find({"insert_date": {"$gte": start_day1, "$lte": end_day1}})
            else:
                result = mycol.find({"date": {"$gte": start_day2, "$lte": end_day2}, "insert_date": {"$gte": start_day1, "$lte": end_day1}})

            #写入数据
            rownum = 1
            for sub_result in result:
                #colnum = 0
                for item in sheettitle:
                    #12/5 output filter
                    if item in sub_result:
                        worksheet.write(rownum, list(sheettitle.keys()).index(item), str(sub_result[item]))
                    #colnum = colnum + 1
                rownum = rownum + 1

    workbook.close()
    #messagebox.showinfo("提示", "结果文件成功保存在" + os.path.abspath(os.path.dirname(path)) + '\查询结果.xlsx' + "路径下")








# insert_DB({'APP_KEY':'5cf8c7b4','APP_SECRET':'a9e1c57de2532f71272040c2c95f1c2b','NUM':'91371000866696280HNY01','PASSWORD':'password','invoice_path':'C:/Users/jicaibu/Desktop/invoiceClassify/invoice'})
# select_DB()
# del_DB()

# myclient = pymongo.MongoClient(MongodbUrl)  #连接DB
# mydb_vat = myclient["DB_info"]  # 创建DB
# mycol_vat = mydb_vat["TB_invoice_info"]  # 创建collection
# print(mycol_vat.find_one())
#del_invoice_info()



