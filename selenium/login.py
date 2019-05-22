from selenium import webdriver
import time

driver = webdriver.Ie()
driver.get('http://www.126.com')


def mkdir(path):
    import os
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)

    if not isExists:
        os.(path)
        print
        path + '创建成功'
        return True
    else:
        print
        path + '目录已经存在'
        return False


mkpath = "C:\\Users\\jianc\\learngit\\cd\\"
mkdir(mkpath)
