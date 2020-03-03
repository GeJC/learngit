from tkinter import *
from tkinter import messagebox

import pymongo

from outside import MongoDB

#TODO: change server
MongoFront = "mongodb://"
ServerUrl = "123.177.21.138:27017/"
#ServerUrl = "localhost:27017/"
MongoManagerUrl = "mongodb://123.177.21.138:27017/"
#MongoManagerUrl = "mongodb://localhost:27017/"
UserEnd = "user_info"
InvoiceEnd = "_DB_invoice_info"

def zhuce():
    top_zhuce = Toplevel()
    top_zhuce.wm_attributes('-topmost', 1)
    top_zhuce.title('注册窗口')
    top_zhuce.geometry('470x180+350+250')
    top_zhuce.resizable(0, 0)
    e_name = StringVar()
    e_number = StringVar()
    password = StringVar()
    que_password = StringVar()
    Label(top_zhuce, text="注册").grid(row=0, column=0)
    Label(top_zhuce, text="用户名").grid(row=2, column=1)
    Label(top_zhuce, text="企业邮箱地址").grid(row=2, column=3)
    username = Entry(top_zhuce, width=40)
    username.grid(row=2, column=2)
    Label(top_zhuce, text="企业名").grid(row=3, column=1)
    Label(top_zhuce, text="公司名称").grid(row=3, column=3)
    entname = Entry(top_zhuce, width=40, textvariable=e_name)
    entname.grid(row=3, column=2)
    Label(top_zhuce, text="税号").grid(row=4, column=1)
    Label(top_zhuce, text="公司税号").grid(row=4, column=3)
    entnumber = Entry(top_zhuce, width=40, textvariable=e_number)
    entnumber.grid(row=4, column=2)
    Label(top_zhuce, text="密码").grid(row=5, column=1)
    Label(top_zhuce, text="长度8-16位").grid(row=5, column=3)
    passwd = Entry(top_zhuce, width=40, textvariable=password, show='*')
    passwd.bind('<Key>', lambda p:delPasswd(passwd, 16))
    passwd.grid(row=5, column=2)
    Label(top_zhuce, text="确认密码").grid(row=6, column=1)
    Label(top_zhuce, text="与密码相同").grid(row=6, column=3)
    que_passwd = Entry(top_zhuce, width=40, textvariable=que_password, show='*')
    que_passwd.grid(row=6, column=2)
    Button(top_zhuce, text='注册', bd='3', relief=RAISED,
           command=lambda: zhuce_command(username.get(), entname.get(), entnumber.get(), passwd.get(), que_passwd.get(),top_zhuce)).grid(
        row=7, column=2, sticky=E, pady=4)
    mainloop()

#限制输入长度，tkinter触发不稳定，小概率不能删除
def delPasswd(p, lmt):
    if len(p.get()) > lmt:
        p.delete(lmt, END)

def zhuce_command(user_name, e_name, e_number, password, que_password,top):
    if len(user_name) > 50:
    #mongodb库名长度不超过64个字符，username实际限制为52，用username作为库名的后果，未来考虑修改
        messagebox.showerror("错误", "用户名长度过长，请重新输入")
    if len(password) < 8 or len(password) > 16:
        messagebox.showerror("错误", "密码长度需要在8-16位之间，请重新输入")
    if password != que_password:
        messagebox.showerror("错误", "密码确认有误，请重新输入")
    else :
        info_dict_jiben = {'user_name': user_name, 'e_number': e_number}
        #print(info_dict_jiben)
        info_dict = {'user_name': user_name, 'e_name': e_name, 'e_number': e_number, 'user_password': password,
                     'APP_KEY': '', 'APP_SECRET': '', 'NUM': '', 'PASSWORD': ''}
        if MongoDB.select_DB(MongoManagerUrl + UserEnd, info_dict_jiben) != None:
            messagebox.showerror("错误", "该用户名已经注册过，请登录")
        else:
            MongoDB.insert_DB(MongoManagerUrl + UserEnd, info_dict)
            messagebox.showinfo("提示", "注册成功，请等待管理员开通查询权限")
            MongoDB.insert_DB(MongoManagerUrl + user_name + InvoiceEnd, info_dict)
            top.destroy()








