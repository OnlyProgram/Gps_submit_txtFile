# -*- coding: utf-8 -*-
# @Time    : 2019/5/29 13:43
# @Author  : WHS
# @File    : CombineCsvFile.py
# @Software: PyCharm
import glob
import time
from tqdm import tqdm
import os
def CombineCsv(csvfilespath,savepath,combinename):
    """
    多个csv文件合并
    :param csvfilespath: csv文件的路径
    :param savepath: 合并后的保存路径
    :param combinename: 合并后的文件名
    :return:
    """
    if not os.path.isdir(savepath):
        os.mkdir(savepath)
    #csvx_list = glob.glob('H:\GPS_Data\\20170901\\text\Trunk0803\AllFilled\SimilarFilled\*.csv')
    csvx_list = glob.glob(os.path.join(csvfilespath,'*.csv'))
    csvfilenum = len(csvx_list)
    print('总共发现%s个CSV文件\n' % csvfilenum)
    combinefilename = combinename + ".csv"
    with tqdm(total=csvfilenum) as pbar:
        for i in csvx_list:
            fr = open(i, 'r', encoding='utf-8').read()
            with open(os.path.join(savepath,combinefilename), 'a',
                      encoding='utf_8_sig') as f:
                f.write(fr)
            pbar.update(1)
#示例
CombineCsv("H:\GPS_Data\\20170901\\text\Trunk0803\AllFilled\SimilarFilled",
           "H:\GPS_Data\\20170901\\text\Trunk0803\AllFilled\\Combine","conbine")