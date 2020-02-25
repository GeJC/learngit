import os
import zipfile
import time


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print('root_dir:', root)  # 当前目录路径
        print('sub_dirs:', dirs)  # 当前路径下所有子目录
        print('files:', files)  # 当前路径下所有非目录子文件
    for i in range(len(files)):
        files[i] = root + '/' + files[i]
    return files


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





