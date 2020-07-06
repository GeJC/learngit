from tkinter import *
from tkinter import filedialog
from outside import file
from outside import recognize
from outside import t10231024
from tkinter import messagebox
from tkinter import font
import os
import time
from outside import MongoDB
from outside import info
from outside.register import zhuce, MongoManagerUrl, InvoiceEnd, MongoFront, ServerUrl, UserEnd
import shutil


# -*- coding: utf-8 -*-

#默认用户名数据文件
#如果加入自动登录功能，在本地存储密码，需要数据加密，暂不考虑
DefaultConfig = 'config.cfg'


def selectPath(path):
    path_ = filedialog.askdirectory()
    path.set(path_)  # 询问路径


def del_file(path):
    if messagebox.askyesno("提示", "确定删除所有发票吗？"):
        ls = os.listdir(path)
        for i in ls:
            c_path = os.path.join(path, i)
            if os.path.isdir(c_path):
                del_file(c_path)
            else:
                os.remove(c_path)
        messagebox.showinfo("提示", "invoice删除成功！")

#backup invoices, (cover/rename/skip(chosen now)/question, need more discuss) if same filename
#backup all files, no filter now
#os.walk遍历文件夹下所有子目录，backup位置修改为工作文件夹外
def backup(file):
    dir = os.path.dirname(os.path.dirname(file))
    bdir = os.path.join(dir, 'backup')
    if not os.path.isdir(bdir):
        os.mkdir(bdir)
    if not os.path.isfile(os.path.join(bdir, os.path.basename(file))):
        shutil.copy(file, bdir)
    return

def duplicate(Url, FoldPath,APP_KEY,APP_SECRET):
    if len(FoldPath) > 0:  # 如果路径不是空的话
        files = file.file_name(FoldPath)  # 返回所有选择目录下所有图片路径的list
        flag = 0
        MongoDB.invoicethisList = []
        for sub_file in files:
            backup(sub_file)
            result = recognize.testapi(sub_file, APP_KEY, APP_SECRET)
            for sub_result in result['response']['data']['identify_results']:
                type = sub_result['type']

                #三种票查重
                detail_dict = sub_result['details']
                print(detail_dict)
                if 'code' in detail_dict:
                    MongoDB.invoicethisList.append([detail_dict['code'], detail_dict['number']])
                else:
                #invoice has no code(such as plane ticket)
                    MongoDB.invoicethisList.append([0, detail_dict['number']])
                if type in {'10100', '10101', '10102'}:

                    if MongoDB.select_invoice_info(Url, detail_dict, type) > 0:
                        flag = flag + 1
                        messagebox.showwarning('警告', '发票代码：' + detail_dict['code'] + ',发票号码：' + detail_dict['number'] + '是重复发票')
                    else:
                        detail_dict['date'] = detail_dict['date'][:4] + detail_dict['date'][5:7] + detail_dict['date'][8:10]
                        MongoDB.insert_invoice_info(Url, detail_dict, type)

                #不查重的票直接入库

                else:
                    if type != '10200' and type != '10506':
                        detail_dict['date'] = detail_dict['date'][:4] + detail_dict['date'][5:7] + detail_dict['date'][8:10]
                        MongoDB.insert_invoice_info(Url, detail_dict, type)
                    else:
                        MongoDB.insert_invoice_info(Url, detail_dict, type)

        if flag == 0:
            messagebox.showinfo('提示', '验重完毕，发票无重复！')
            time.sleep(6)
            messagebox.showinfo('提示', '发票查验通过！')

def verify(Url, FoldPath,APP_KEY,APP_SECRET,NUM,PASSWORD):
    if len(FoldPath) > 0:  # 如果路径不是空的话
        files = file.file_name(FoldPath)  # 返回所有选择目录下所有图片路径的list
        list1023 = []
        list1024 = []
        listRuiQi = []
        MongoDB.invoicethisList = []
        for sub_file in files:
            backup(sub_file)
            flag = 0
            result = recognize.testapi(sub_file, APP_KEY, APP_SECRET)  # 识别
            print(result)
            for sub_result in result['response']['data']['identify_results']:
                type = sub_result['type']
                duplicate_flag = False

                # 三种票查重
                detail_dict = sub_result['details']
                if 'code' in detail_dict:
                    MongoDB.invoicethisList.append([detail_dict['code'], detail_dict['number']])
                else:
                #invoice has no code(such as plane ticket)
                    MongoDB.invoicethisList.append([0, detail_dict['number']])
                if type in {'10100', '10101', '10102'}:

                    if MongoDB.select_invoice_info(Url, detail_dict, type) > 0:
                        flag = flag + 1
                        duplicate_flag = True
                        messagebox.showwarning('警告', '发票代码：' + detail_dict['code'] + ',发票号码：' + detail_dict['number'] + '是重复发票')
                    else:
                        if 'date' in detail_dict:
                            detail_dict['date'] = detail_dict['date'][:4] + detail_dict['date'][5:7] + detail_dict['date'][8:10]
                        MongoDB.insert_invoice_info(Url, detail_dict, type)

                # 不查重的票直接入库
                else:
                    if type != '10200' and type != '10506' and 'date' in detail_dict:
                        detail_dict['date'] = detail_dict['date'][:4] + detail_dict['date'][5:7] + detail_dict['date'][8:10]
                        MongoDB.insert_invoice_info(Url, detail_dict, type)
                    else:
                        MongoDB.insert_invoice_info(Url, detail_dict, type)

                # 准备查验
                #if not duplicate_flag:
                #waibid = "uuid"
                checkcode = ''
                pretax_amount = ''
                date = ''
                if (type in ['10100', '10101', '10102', '10103', '10104', '10105']):
                    if ('check_code' in detail_dict):
                        checkcode = detail_dict['check_code'][-6:]
                    if ('pretax_amount' in detail_dict):
                        pretax_amount = detail_dict['pretax_amount']
                    if ('date' in detail_dict):
                        date = detail_dict['date']
                    dicRuiQi = {'code': detail_dict['code'], 'number': detail_dict['number'],
                                'check_code': checkcode, 'pretax_amount': pretax_amount,
                                'date': date, 'type': type}
                    listRuiQi.append(dicRuiQi)
                '''
                    if type == '10100':  #专票
                        kaiprq_yuan = detail_dict['date']
                        kaiprq = kaiprq_yuan
                        faplx = "004"
                        dic1023 = {"fapdm": detail_dict['code'], "faphm": detail_dict['number'], "kaiprq": kaiprq, "jine": detail_dict['pretax_amount'], "waibid": waibid, "faplx": faplx}
                        dic1024 = {"fapdm": detail_dict['code'], "faphm": detail_dict['number']}
    
                        list1023.append(dic1023)
                        list1024.append(dic1024)
                    elif type == '10101':  #普票
                        kaiprq_yuan = detail_dict['date']
                        kaiprq = kaiprq_yuan
                        xiaoym = detail_dict['check_code']
                        faplx = "007"
                        dic1023 = {"fapdm": detail_dict['code'], "faphm": detail_dict['number'], "kaiprq": kaiprq, 'xiaoym': xiaoym, "waibid": waibid, "faplx": faplx}
                        dic1024 = {"fapdm": detail_dict['code'], "faphm": detail_dict['number']}
                        list1023.append(dic1023)
                        list1024.append(dic1024)
                    elif type == '10102' and ('transit_mark' not in detail_dict.keys()):  #增值税电子普通发票
                        kaiprq_yuan = detail_dict['date']
                        kaiprq = kaiprq_yuan
                        xiaoym = detail_dict['check_code']
                        faplx = "026"
                        dic1023 = {"fapdm": detail_dict['code'], "faphm": detail_dict['number'], "kaiprq": kaiprq, 'xiaoym': xiaoym,"waibid": waibid, "faplx": faplx}
                        dic1024 = {"fapdm": detail_dict['code'], "faphm": detail_dict['number']}
                        list1023.append(dic1023)
                        list1024.append(dic1024)
                    elif type == '10102' and ('transit_mark' in detail_dict.keys()):  #增值税电子普通发票(通行类)
                        kaiprq_yuan = detail_dict['date']
                        kaiprq = kaiprq_yuan
                        xiaoym = detail_dict['check_code']
                        faplx = "014"
                        dic1023 = {"fapdm": detail_dict['code'], "faphm": detail_dict['number'], "kaiprq": kaiprq, 'xiaoym': xiaoym,"waibid": waibid, "faplx": faplx}
                        dic1024 = {"fapdm": detail_dict['code'], "faphm": detail_dict['number']}
                        list1023.append(dic1023)
                        list1024.append(dic1024)
                    elif type == '10104':  #机动车销售统一发票
                        kaiprq_yuan = detail_dict['date']
                        kaiprq = kaiprq_yuan
                        faplx = "005"
                        dic1023 = {"fapdm": detail_dict['code'], "faphm": detail_dict['number'], "kaiprq": kaiprq, "waibid": waibid, "faplx": faplx}
                        dic1024 = {"fapdm": detail_dict['code'], "faphm": detail_dict['number']}
                        list1023.append(dic1023)
                        list1024.append(dic1024)
                    elif type == '10105':  #二手车销售统一发票
                        kaiprq_yuan = detail_dict['date']
                        kaiprq = kaiprq_yuan
                        faplx = "005"
                        dic1023 = {"fapdm": detail_dict['code'], "faphm": detail_dict['number'], "kaiprq": kaiprq, "waibid": waibid, "faplx": faplx}
                        dic1024 = {"fapdm": detail_dict['code'], "faphm": detail_dict['number']}
                        list1023.append(dic1023)
                        list1024.append(dic1024)
                    elif type == '10103':  #增值税普通发票(卷票)
                        kaiprq_yuan = detail_dict['date']
                        kaiprq = kaiprq_yuan
                        xiaoym = detail_dict['check_code']
                        faplx = "025"
                        dic1023 = {"fapdm": detail_dict['code'], "faphm": detail_dict['number'], "kaiprq": kaiprq, 'xiaoym': xiaoym, "waibid": waibid, "faplx": faplx}
                        dic1024 = {"fapdm": detail_dict['code'], "faphm": detail_dict['number']}
                        list1023.append(dic1023)
                        list1024.append(dic1024)
                '''

        print('###############')
        print(listRuiQi)
        print('______________________')
        recognize.ruiqi_chayan(Url, listRuiQi, APP_KEY, APP_SECRET)
        '''
        if len(list1023) > 0:
            tijiao_result = t10231024.test1023(list1023, NUM, PASSWORD)  # 1023提交信息到税务网站
            if tijiao_result == '接收成功 ':
                for i in range(5):
                    time.sleep(60)
                    in1024_result_list = t10231024.test1024(Url, list1024, NUM, PASSWORD)
                    if len(in1024_result_list) == 0:  # 1024获得查验结果
                        messagebox.showinfo("提示", "验真完毕")
                        break
                    else:
                        list1024 = in1024_result_list
        '''

def select_result(Url, FoldPath, start_day1, end_day1, start_day2, end_day2, CheckVarall, CheckVarkind, CheckVartime):
    #判断路径是否输入
    if FoldPath == '':
        #messagebox.showerror("错误", "请填入发票路径")
        return 0
    MongoDB.select_invoice_result(Url, FoldPath, start_day1, end_day1, start_day2, end_day2, CheckVarall, CheckVarkind, CheckVartime)
    return 1

def count_recognize(APP_KEY, APP_SECRET):
    result = info.test_info(APP_KEY, APP_SECRET)
    messagebox.showinfo("提示", "大票已使用次数：" + str(result['response']['user_info']['big_usage']) + ",小票已使用次数：" + str(
        result['response']['user_info']['small_usage']) + ",定额发票已使用次数：" + str(result['response']['user_info']['quota_usage']))

#changed, useless now
def run_button(Url, CheckVar1, CheckVar2, CheckVar3, CheckVar4, path1, path2, start_day1, end_day1, start_day2, end_day2, e_info):
    # 如果结果文件存在先删除结果文件，避免异常
    if os.path.exists(os.path.abspath(path1) + '\查询结果.xlsx'):
        os.remove(os.path.abspath(path1) + '\查询结果.xlsx')
    if CheckVar1 == 1 and CheckVar2 == 0:
        duplicate(Url, path1, e_info['APP_KEY'], e_info['APP_SECRET'])
    if CheckVar2 == 1:

        #duplicate(path1, e_info['APP_KEY'], e_info['APP_SECRET'])

        verify(Url, path1, e_info['APP_KEY'], e_info['APP_SECRET'], e_info['NUM'], e_info['PASSWORD'])
    if CheckVar3 == 1:
        if path2 == '':
            # default path2 = path1
            if path1 == '':
                messagebox.showerror("错误", "请填入结果路径")
            else:
                path2 = path1
        # 如果结果文件存在就删除结果文件
        if os.path.exists(os.path.abspath(path2) + '\查询结果.xlsx'):
            os.remove(os.path.abspath(path2) + '\查询结果.xlsx')

        if select_result(Url, path2, start_day1, end_day1, start_day2, end_day2, CheckVar4):
            #if path1 != path2:
                #print(os.path.abspath(os.path.dirname(path1)) + '/查询结果.xlsx')
                #print(path2 + '/查询结果.xlsx')
                #shutil.copyfile(os.path.abspath(os.path.dirname(path1)) + '/查询结果.xlsx', path2 + '/查询结果.xlsx')
                #os.remove(os.path.abspath(os.path.dirname(path1)) + '/查询结果.xlsx')
            messagebox.showinfo("提示", "结果文件保存在" + path2 + '/查询结果.xlsx' + "路径下")

    #messagebox.showinfo("提示", "程序执行结束！")


#11/21 fix ui 登录界面->输入，点击登录->成功，转到main界面
#                                    |失败，弹出信息，提示注册
#                    ->点击注册->转到注册界面
#11/22 user info *手动分配数据库user*
#注册界面->提交user注册信息->点击注册将信息存入user数据库->提示等待分配
#                                                       管理员手动分配user，外部接口相关
#use username & password to sign in
def denglu(username, passwd, top):

    info_dict = {'user_name': username, 'user_password': passwd}
    signinUser = MongoDB.select_DB(MongoManagerUrl + UserEnd, info_dict)
    if signinUser != None:
        #管理员尚未分配user，拒绝登录
        if (signinUser['APP_KEY'] == '') or (signinUser['APP_SECRET'] == '') or (signinUser['NUM'] == '') or (signinUser['PASSWORD'] == ''):
            messagebox.showerror("错误", "尚未取得权限，请联系管理员")
        else:
            e_name = signinUser['e_name']
            UserDBUrl = MongoManagerUrl + username + InvoiceEnd
            #UserDBUrl = MongoFront + username + ":" + passwd + "@" + ServerUrl + username + InvoiceEnd
            cfg = open(DefaultConfig, mode='w')
            cfg.write(username)
            cfg.close()
            top.destroy()
            main(username, passwd, UserDBUrl)

    else:
        messagebox.showerror("错误", "用户名或密码错误，请重新登录或注册")

# duplicate
def run_dup(Url, path1, e_info):
    #判断路径是否输入
    if path1 == '':
        messagebox.showerror("错误", "请填入发票路径")
        return
    if os.path.exists(os.path.abspath(path1) + '\查询结果.xlsx'):
        os.remove(os.path.abspath(path1) + '\查询结果.xlsx')
    duplicate(Url, path1, e_info['APP_KEY'], e_info['APP_SECRET'])
    #enable thistime filter
    MongoDB.thisFlag = True
    return

# verify
def run_ver(Url, path1, e_info):
    #判断路径是否输入
    if path1 == '':
        messagebox.showerror("错误", "请填入发票路径")
        return
    if os.path.exists(os.path.abspath(path1) + '\查询结果.xlsx'):
        os.remove(os.path.abspath(path1) + '\查询结果.xlsx')
    verify(Url, path1, e_info['APP_KEY'], e_info['APP_SECRET'], e_info['NUM'], e_info['PASSWORD'])
    #enable thistime filter
    MongoDB.thisFlag = True
    return

# output to file
def run_out(Url, path2, start_day1, end_day1, start_day2, end_day2, CheckVarall, CheckVarkind, CheckVartime):
    if path2 == '':
        messagebox.showerror("错误", "请填入结果路径")

    # 如果结果文件存在就删除结果文件
    if os.path.exists(os.path.abspath(path2) + '\查询结果.xlsx'):
        os.remove(os.path.abspath(path2) + '\查询结果.xlsx')

    if select_result(Url, path2, start_day1, end_day1, start_day2, end_day2, CheckVarall, CheckVarkind, CheckVartime):
        messagebox.showinfo("提示", "结果文件保存在" + path2 + '/查询结果.xlsx' + "路径下")

#enable/disable time filter
def changetimeflag(e1,e2,e3,e4):
    if e1.cget('state') == 'disabled':
        e1.config(state='normal')
        e2.config(state='normal')
        e3.config(state='normal')
        e4.config(state='normal')
        return
    if e1.cget('state') == 'normal':
        e1.config(state='disabled')
        e2.config(state='disabled')
        e3.config(state='disabled')
        e4.config(state='disabled')
        return

def outputTK(Url):
    top_out = Toplevel()
    top_out.attributes('-topmost', 1)
    top_out.title('票库导出')
    top_out.geometry('550x220+300+385')
    top_out.resizable(0, 0)

    start_day1 = StringVar()
    end_day1 = StringVar()
    start_day2 = StringVar()
    end_day2 = StringVar()
    CheckVarkind = IntVar()
    CheckVarall = IntVar()
    CheckVartime = IntVar()
    path2 = StringVar()

    Label(top_out, text="    ").grid(row=0, column=4)
    Label(top_out, text="    ").grid(row=0, column=0)

    Label(top_out, text="    结果路径：").grid(row=0, column=1)
    Entry(top_out, width=45, textvariable=path2).grid(row=0, column=2, columnspan=2)
    Button(top_out, text='选择路径', command=lambda: selectPath(path2), width='10').grid(row=0, column=5, sticky=W, pady=4)
    Button(top_out, text='票库导出', command=lambda: run_out(Url, path2.get(), e1.get(), e2.get(), e3.get(), e4.get(),
        CheckVarall.get(), CheckVarkind.get(), CheckVartime.get()), width='10').grid(row=1, column=5, sticky=W, pady=4)

    Label(top_out, text="起始入库日期").grid(row=7, column=1)
    e1 = Entry(top_out, width=10, textvariable=start_day1)
    e1.insert(END, str(time.strftime("%Y%m%d", time.localtime())))
    e1.grid(row=7, column=2, sticky=W)
    e1.config(state='disabled')

    Label(top_out, text="终止入库日期").grid(row=8, column=1)
    e2 = Entry(top_out, width=10, textvariable=end_day1)
    e2.insert(END, str(time.strftime("%Y%m%d", time.localtime())))
    e2.grid(row=8, column=2, sticky=W)
    e2.config(state='disabled')

    Label(top_out, text="起始开票日期").grid(row=7, column=2, sticky=E)
    e3 = Entry(top_out, width=10, textvariable=start_day2)
    e3.insert(END, str(time.strftime("%Y%m%d", time.localtime())))
    e3.grid(row=7, column=3, sticky=W)
    e3.config(state='disabled')

    Label(top_out, text="终止开票日期").grid(row=8, column=2, sticky=E)
    e4 = Entry(top_out, width=10, textvariable=end_day2)
    e4.insert(END, str(time.strftime("%Y%m%d", time.localtime())))
    e4.grid(row=8, column=3, sticky=W)
    e4.config(state='disabled')

    Rthis = Radiobutton(top_out, text='本次发票', variable=CheckVarall, value='0')
    Rall = Radiobutton(top_out, text='全部发票', variable=CheckVarall, value='1')
    Rtime = Checkbutton(top_out, text='按时间筛选(YYYYMMDD)', command=lambda :changetimeflag(e1,e2,e3,e4), variable=CheckVartime)
    Rthis.grid(row=1, column=2, sticky=W, pady=4)
    Rall.grid(row=1, column=3, sticky=W, pady=4)
    Rtime.grid(row=3, column=2, sticky=W, pady=4)

    if MongoDB.thisFlag:
    #select invoices this time/all, using MongoDB.thisFlag as global variable
        Rthis.select()
    else:
        Rthis.config(state='disabled')
        Rall.select()

    R1 = Radiobutton(top_out, text='全票种', variable=CheckVarkind, value='0')
    R2 = Radiobutton(top_out, text='抵扣税票种', variable=CheckVarkind, value='1')
    R1.select()
    R1.grid(row=2, column=2, sticky=W, pady=4)
    R2.grid(row=2, column=3, sticky=W, pady=4)
    top_out.mainloop()

KindDescriptList = ['增值税专用发票，增值税普通发票，增值税电子普通发票，增值税普通发票(卷票)，机动车销售统一发票，二手车销售统一发票',
                    '机打发票，出租车发票，火车票，客运汽车，航空运输电子客票行程单，过路费发票，可报销其他发票，国际小票，滴滴出行行程单，完税证明',
                    '定额发票']

#explain count info
def countInfoPointed(countinfo, index):
    infotop = Toplevel()
    infotop.overrideredirect(True)
    infotop.geometry("%sx%s+%s+%s" % (205, 80, countinfo.winfo_pointerx(), countinfo.winfo_pointery() + 20))
    infotop.wm_attributes('-topmost',1)
    Label(infotop, text=KindDescriptList[index], wraplength=200, justify='left').grid(row=1, column=1)
    countinfo.bind("<Leave>", lambda _: infotop.destroy())


def main(username, passwd, Url):
    #print(Url)
    master = Tk()
    master.wm_attributes('-topmost', 1)
    master.title('发票自动识别验真')
    master.geometry('520x200+300+150')
    #master.iconbitmap('favicon.ico')
    master.resizable(0, 0)
    CheckVar1 = IntVar()
    CheckVar2 = IntVar()
    CheckVar3 = IntVar()
    CheckVar4 = IntVar()
    path1 = StringVar()
    path2 = StringVar()
    start_day1 = StringVar()
    end_day1 = StringVar()
    start_day2 = StringVar()
    end_day2 = StringVar()

    frm1 = Frame(master)
    frm1.grid(row=0, column=0)

    '''
    C1 = Checkbutton(master, text="识别查重", variable=CheckVar1, onvalue=1, offvalue=0, height=2, width=20)
    #C2选中时连带选中C1
    C2 = Checkbutton(master, text="发票验真", command = lambda: C1.select() if CheckVar2.get() else None, variable=CheckVar2, onvalue=1, offvalue=0, height=2, width=20)
    C3 = Checkbutton(master, text="票库导出", variable=CheckVar3, onvalue=1, offvalue=0, height=2, width=20)
    C1.select()
    C1.grid(row=4, column=0)
    C2.select()
    C2.grid(row=5, column=0)
    C3.select()
    C3.grid(row=6, column=0)
    '''
    dict = {'user_name': username, 'user_password': passwd}
    e_info = MongoDB.select_DB(MongoManagerUrl + UserEnd, dict)
    e_name = e_info['e_name']
    e_number = e_info['e_number']
    APP_KEY = e_info['APP_KEY']
    APP_SECRET = e_info['APP_SECRET']
    Label(frm1, text='公司名：').grid(row=0, column=1)
    Label(frm1, text='公司税号：').grid(row=1, column=1)
    Label(frm1, text=e_name).grid(row=0, column=2, sticky=W)
    Label(frm1, text=e_number).grid(row=1, column=2, sticky=W)


    Label(frm1, text="发票路径：").grid(row=2, column=1)
    Entry(frm1, width=45, textvariable=path1).grid(row=2, column=2)

    cishu = info.test_info(APP_KEY, APP_SECRET)
    dapiao = cishu['response']['user_info']['big_usage']
    xiaopiao = cishu['response']['user_info']['small_usage']
    dinge = cishu['response']['user_info']['quota_usage']

    Label(frm1, text="    ").grid(row=9, column=0)

    frm2 = Frame(master)
    frm2.grid(row=1, column=0)
    uft = font.Font(family = font.nametofont("TkDefaultFont").cget("family"), size = 9, underline = 1)
    dcnt = Label(frm2, text="大票", borderwidth=0)
    dcnt.grid(row=1, column=1, sticky=W)
    dcnt.configure(font = uft, fg = 'blue')
    dcnt.bind("<Enter>", lambda _: countInfoPointed(dcnt, 0))
    Label(frm2, text="已识别:" + str(dapiao) + "次    ", borderwidth=0).grid(row=1, column=2, sticky=W)
    xcnt = Label(frm2, text="小票", borderwidth=0)
    xcnt.grid(row=1, column=3, sticky=W)
    xcnt.configure(font = uft, fg = 'blue')
    xcnt.bind("<Enter>", lambda _: countInfoPointed(xcnt, 1))
    Label(frm2, text="已识别:" + str(xiaopiao) + "次    ", borderwidth=0).grid(row=1, column=4, sticky=W)
    ecnt = Label(frm2, text="定额", borderwidth=0)
    ecnt.grid(row=1, column=5, sticky=W)
    ecnt.configure(font = uft, fg = 'blue')
    ecnt.bind("<Enter>", lambda _: countInfoPointed(ecnt, 2))
    Label(frm2, text="已识别:" + str(dinge) + "次", borderwidth=0).grid(row=1, column=6, sticky=W)

    Button(frm1, text='选择路径', command=lambda: selectPath(path1), width='10').grid(row=2, column=3, sticky=W, pady=4)

    Button(frm1, text='识别+查重', command=lambda: run_dup(Url, path1.get(), e_info), width='10').grid(row=4, column=1, sticky=N, pady=4)
    Button(frm1, text='识别+查重+验真', command=lambda: run_ver(Url, path1.get(), e_info), width='16').grid(row=4, column=2, sticky=N, pady=4)
    Button(frm1, text='票库导出', command=lambda: outputTK(Url), width='10').grid(row=4, column=3, sticky=N, pady=4)

    #Button(master, text='删除发票', width='10', command=lambda: del_file(path.get())).grid(row=2, column=4, sticky=W, pady=4)
    #Button(master, text='执行', width='9', bd='3', relief=RAISED, fg="blue", command=lambda: run_button(Url, CheckVar1.get(), CheckVar2.get(), CheckVar3.get(), CheckVar4.get(), path1.get(), path2.get(), e1.get(), e2.get(), e3.get(), e4.get(), e_info)).grid(row=6, column=2, pady=4)

    mainloop()


top = Tk()
top.wm_attributes('-topmost', 1)
top.title('注册登录窗口')
top.geometry('410x180+300+200')
top.resizable(0, 0)
Label(top, text="      ").grid(row=0, column=0)
Label(top, text="      ").grid(row=1, column=0)
Label(top, text="用户名").grid(row=2, column=1)
frm = Frame(top)
frm.grid(row=4, column=2, sticky=E)
uft = font.Font(family = font.nametofont("TkDefaultFont").cget("family"), size = 9, underline = 1)
wcnt = Label(frm, text="忘记密码?", borderwidth=0)
wcnt.grid(row=1, column=1, sticky=W)
wcnt.configure(font=uft, fg='blue')
if not os.path.isfile(DefaultConfig):
    cfg = open(DefaultConfig, mode='w+')
else:
    cfg = open(DefaultConfig, mode='r')
default_name = cfg.read()
cfg.close()
username = Entry(top, width=40)
username.insert(END, default_name)
username.grid(row=2, column=2)
Label(top, text="密码").grid(row=3, column=1)
passwd = Entry(top, width=40, show='*')
passwd.grid(row=3, column=2)
Label(top, text="    ").grid(row=4, column=0)
Button(top, text='注册', bd='3', relief=RAISED, command=lambda: zhuce()).grid(row=6, column=2, sticky=W, pady=4)
Button(top, text='登录', bd='3', relief=RAISED, command=lambda: denglu(username.get(), passwd.get(), top)).grid(row=6, column=2, sticky=E, pady=4)
top.mainloop()