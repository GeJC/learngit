import os
import zipfile
import time

fileTypeList = ['ffd8ff', '89504e47', '255044462d312e']
#jpg, png, pdf


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print('root_dir:', root)  # 当前目录路径
        print('sub_dirs:', dirs)  # 当前路径下所有子目录
        print('files:', files)  # 当前路径下所有非目录子文件
    retfiles = []
    for i in range(len(files)):
        files[i] = root + '/' + files[i]
        #文件类型检查，只处理jpg/png/pdf类型，以文件头为准
        binfile = open(files[i], 'rb')
        bins = binfile.read(20)
        binfile.close()
        hexstr = u""
        for bit in range(len(bins)):
            t = u"%x" % bins[bit]
            if len(t) % 2:
                hexstr += u"0"
            hexstr += t
        bins = hexstr.lower()
        for tp in fileTypeList:
            if bins[:len(tp)] == tp:
                retfiles.append(files[i])
    print(retfiles)
    return retfiles


def zipDir(dirpath, outFullName):
    zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath, '')

        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()

def new_folder(path):
    lists = os.listdir(path)                                    #列出目录的下所有文件和文件夹保存到lists
    if len(lists) == 1:
        file_new = os.path.join(path,'result_' + time.strftime("%Y%m%d%H%M%S", time.localtime()))
    else:
        lists.sort(key=lambda fn:os.path.getmtime(path + "\\" + fn))#按时间排序
        lists.remove('invoice')

        file_new = os.path.join(path, lists[-1])
    return file_new





