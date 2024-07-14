'''
Author: david
Date: 2024-07-03 22:02:17
LastEditors: david
LastEditTime: 2024-07-06 10:05:38
FilePath: /top_eleven/parse.py
Description: 

Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
'''

import pandas as pd

import os
import numpy as np

# input data path
src_dir = "/home/qcraft/Downloads/exp/exp2/xlsx/"
file_list = sorted(os.listdir(src_dir))
out_file = "/home/qcraft/Downloads/exp/exp2/output/result.xlsx"


# 读取表格
# 序号	物质	保留时间(min)	化合物类型	CAS号	分子量	峰面积	峰高	含量	单位	加标回收率(%)
def read_excel(idx, data_path, sheet_data, materials):
    # 打开文件
    data_frame = pd.read_excel(data_path, sheet_name=sheet_data)
    temp_map = {}
    for index, material_name in enumerate(data_frame['物质']):
        if type(data_frame['峰面积'][index]) == str:
            continue

        content = float(data_frame['峰面积'][index])
        if material_name in temp_map.keys():
            temp_map[material_name] = max(content,temp_map[material_name])
        else:
            temp_map[material_name] = content

    for key, val in temp_map.items():
        if key in materials.keys():
            materials[key].append(val)
        else:
            materials[key] = [0] * idx + [val]
    for key, val in materials.items():
        if key in temp_map.keys():
            continue
        materials[key].append(0)
    return materials


materials = {}
num = 0
for idx, xls_file in enumerate(file_list):
    print(">>>", xls_file)
    materials = read_excel(idx, os.path.join(
        src_dir, xls_file), 'Sheet1', materials)
    num += 1

# print(materials)
writer = pd.ExcelWriter(out_file)

out_data_frame = pd.DataFrame(materials)
out_data_frame["患病概率"] = 100.
out_data_frame.to_excel(writer, sheet_name="Sheet1", index=False)
writer.save()