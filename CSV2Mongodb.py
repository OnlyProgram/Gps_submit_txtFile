# -*- coding: utf-8 -*-
# @Time    : 2019/5/11 11:36
# @Author  : WHS
# @File    : CSV2Mongodb.py
# @Software: PyCharm
"""
实现将csv文件存入到MongoDB数据库
"""
from pymongo import MongoClient
import csv
import os
import json
import pandas as pd
import time
import  datetime
import re
#import SortTrunk
# 1:连接本地MongoDB数据库服务
conn=MongoClient("localhost")
# 2:连接本地数据库。没有时会自动创建,可更改数据库名称
db=conn.GPSTXTData
# 3:创建集合
#myset=db.totaldata

# 4:看情况是否选择清空(两种清空方式，第一种不行的情况下，选择第二种)
#第一种直接remove
#myset.remove(None)
#第二种remove不好用的时候
# set1.delete_many({})
def Insert(insertpath,collection):
    """
    :param collection 集合名称，类似关系型数据中的表名
    :param insertpath: 要保存到数据库的文件路径，如：H:\GPS_Data\\20170901\\20170901.csv
    :return:
    """
    myset = db[collection]
    myset.remove(None)
    counts = 0  # 记录添加记录数
    PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))  # 获取项目根目录

    # 读txt文档
    chunker = pd.read_table(insertpath, sep=',', chunksize=2000000, header=0,
                            names=['TrunkNumber', 'Time', 'lon', 'lat'], encoding='utf-8')
    # chunker = pd.read_csv(insertpath, chunksize=2000000, header=None,
    # names=['TrunkNumber', 'Time', 'lon',
    # 'lat'],encoding='utf-8')  # 分块读取 每一块200万条数据,如果不加header=None 第一行会被当做索引，而不被处理
    for df in chunker:
        for index, row in df.iterrows():

            try:
                row['TrunkNumber'] = str(row['TrunkNumber'])
                row['Time'] = str(datetime.datetime.strptime(str(row['Time']), '%Y%m%d%H%M%S'))
                row['lon'] = float(row['lon'])
                row['lat'] = float(row['lat'])
                # row['x_grid'] = int(row['x_grid'])
                # row['y_grid'] = int(row['y_grid'])
                row_dict = {"TrunkNumber": row['TrunkNumber'], "Time": row['Time'], "lon": row['lon'],
                            "lat": row['lat']}
                # "x_grid":row['x_grid'],"y_grid":row['y_grid']}
                myset.insert(row_dict)
                counts += 1
            except Exception as e:
                with open(os.path.join(PROJECT_ROOT,"To qdatabase.log"), 'a') as file:
                    file.write("第{}条数据插入数据库出错：".format(counts+1)+str(e) +"\n")
    print('成功添加了' + str(counts) + '条数据 ')
def Inquire(Trunknumber_lists,savepath,collection):
    myset = db[collection]
    flag = 0
    #starttime = 0
    if not os.path.isdir(savepath):
        os.mkdir(savepath)
    for number in Trunknumber_lists:  #number代表车牌号
        starttime = time.time()
        flag += 1
        pattern = re.compile(r'([\u4e00-\u9fa5])')
        Trunknumber = re.sub(pattern, '', str(number))  #文件名是车牌号，但是要去重中文
        fname = Trunknumber + ".csv"
        results = myset.find({'TrunkNumber':number})
        with open(os.path.join(savepath, fname), 'a', newline='',encoding='utf_8_sig') as csvfile:
            fileheader = ["TrunkNumber", "Time", "lon", "lat"]
            dict_writer = csv.DictWriter(csvfile,fileheader)
            #dict_writer.writeheader()  #不加文件头
            for result in results:
                del result['_id']
                dict_writer.writerow(result)
        print("处理第{}辆车数据时间消耗为：{}".format(flag,datetime.timedelta(seconds=(time.time()-starttime))))

#运行示例
#Insert("H:\GPS_Data\\20170901\\text\Trunk0803\\WBHC_20180803_PX_0.txt","WBHC_20180803_PX_0")

"""
lis =SortTrunk.Get_top_trunk_list("H:\GPS_Data\\20170901\\text\Trunk0803\\Top20Sort.json")
print("此部分共计{}辆车".format(len(lis)))
start = time.time()
Inquire(lis,"H:\GPS_Data\\20170901\Top20\\Top20Trunk","WBHC_20180803_PX_0")
print("总共消耗时间为：{}".format(datetime.timedelta(seconds=(time.time()-start))))
"""