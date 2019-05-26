# -*- coding: utf-8 -*-
# @Time    : 2019/5/11 12:45
# @Author  : WHS
# @File    : Original_csv2kml.py
# @Software: PyCharm
"""
原始轨迹在路网上可视化，转换为kml文件，直接打开即可
"""
import pandas as pd
import os
"""格式
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.0">
<Document>
<Placemark>
<description>2</description>
<Point><coordinates>116.56184,39.566791,0</coordinates></Point>
</Placemark>
<Placemark>
<description>2</description>
<Point><coordinates>116.557926,39.5619,0</coordinates></Point>
</Placemark>
</Document>
</kml>
"""
def original_csvtokml(filename,savepath,cavfilepath):
    """

    :param filename: kml文件名
    :param savepath: 保存路径
    :param cavfilepath: 网格化后的单个车辆路径
    :return:
    """
    df = pd.read_csv(cavfilepath, header=None, usecols=[2, 3],names=[0,1])  # 读经纬度，标记
    fullname = filename+'.kml'
    with open(os.path.join(savepath,fullname), 'a') as file:
        file.write('<?xml version="1.0" encoding="UTF-8"?>' +'\n')
        file.write('<kml xmlns="http://earth.google.com/kml/2.0">' +'\n')
        file.write('<Document>' +'\n')
        for num in range(df.shape[0]):
            file.write('<Placemark>' +'\n')
            coordinate = "<Point><coordinates>"+str(df.iloc[num,0])+","+str(df.iloc[num,1])+",0</coordinates></Point>"#此处0代表海拔，如果有海拔，可更改
            file.write(coordinate +'\n')
            file.write('</Placemark>' +'\n')
        file.write('</Document>' +'\n')
        file.write('</kml>' +'\n')
#示例
original_csvtokml('text','H:\GPS_Data\\20170901\Top20\KML','H:\GPS_Data\20170901\Top20\Meshed\0d3a589e-77a9-4704-b2a8-d01c5e1af4c3.csv')