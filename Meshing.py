# -*- coding: utf-8 -*-
# @Time    : 2019/5/11 11:52
# @Author  : WHS
# @File    : Meshing.py
# @Software: PyCharm
"""
输入每个车辆的文件所在路径
输出网格化后的文件
"""
import pandas as pd
import datetime
import math
import os

def findcsv(path):
    """Finding the *.txt file in specify path"""
    ret = []
    filelist = os.listdir(path)
    for filename in filelist:
        de_path = os.path.join(path, filename)
        if os.path.isfile(de_path):
            if de_path.endswith(".csv"):
                ret.append(de_path)
    return ret
def Meshing(filepath,savepath,filename):
    df = pd.read_csv(filepath, header=None,
                     usecols=[0, 1, 2, 3],low_memory=False)
    #df = df.iloc[:, 2].apply(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d%H%M%S'))
    df.iloc[:,1] = pd.to_datetime(df.iloc[:, 1], format="%Y%m%d ", errors='coerce')
    start = datetime.datetime.strptime("2000-01-01", '%Y-%m-%d')
    end = datetime.datetime.strptime("2099-12-31", '%Y-%m-%d')
    df = df.dropna(axis=0, how='any')  # 删除表中含有任何NaN的行 ,subset=[1]可添加 只关注时间这一列，不添加也会处理其他列为空的行
    df = (df[(df.iloc[:, 1] >= start) & (df.iloc[:, 1] <= end)])  # 筛选某个是时间段
    df = df[(df.iloc[:, 2] < 118) & (df.iloc[:, 2] > 115) & (df.iloc[:, 3] < 42) & (df.iloc[:, 3] > 39)]  # 去除北京外GPS坐标
    df = df.sort_values(by=1)  #时间排序
    row =0
    df[4] = None  #添加列
    df[5] = None
    for num in df.iloc[:, 0]:
        x_grid = math.ceil((df.iloc[row,2]-115)/0.001)  #x方向格子编号
        y_grid = math.ceil((df.iloc[row,3]-39)/0.001)   #y方向格子编号
        df.iloc[row, 4] = str(x_grid)
        df.iloc[row,5] = str(y_grid)
        row += 1
    filenames = filename + ".csv"
    resultpath = os.path.join(savepath,filenames)
    df.to_csv(resultpath,index=0,header=0)
    print("**********网格化完成**********")
"""
#使用举例，同时网格化多个车辆
spath = "H:\GPS_Data\\20170901\Top20\Top20Meshed"
list_dir = findcsv('H:\GPS_Data\\20170901\Top20\Top20Trunk')
#spath = "D:\postgraduate-2017-2020\Data_set\GPS\Top200w\Data_gridding" #文件保存路径
for file in list_dir:
    temname = (str(os.path.split(file)[-1]).split('.')[0])  #提取文件名
    Meshing(file,spath,temname)
"""
