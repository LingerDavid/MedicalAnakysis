'''
Author: david
Date: 2024-07-06 10:03:20
LastEditors: david
LastEditTime: 2024-07-14 16:14:00
FilePath: /MedicalAnakysis/combine.py
Description: 

Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
'''
import pandas as pd


def read_data(heaalth_abs_path, cancer_abs_path, save_abs_path):
    health_df = pd.read_excel(heaalth_abs_path)
    health_df["健康"] = 1
    cancer_df = pd.read_excel(cancer_abs_path)
    cancer_df["健康"] = 0

    cmb_df = pd.concat([health_df.T, cancer_df.T], axis=1).T
    cmb_df.fillna(0, inplace=True)

    new_health_df = cmb_df[cmb_df["健康"] == 1]
    new_cancer_df = cmb_df[cmb_df["健康"] == 0]

    label = cmb_df['健康']

    new_health_df.drop('健康', axis=1)
    new_health_df.drop('患病概率', axis=1)
    new_cancer_df.drop('健康', axis=1)
    new_cancer_df.drop('患病概率', axis=1)
    cmb_df.drop('健康', axis=1)
    cmb_df.drop('患病概率', axis=1)

    out_file = save_abs_path
    writer = pd.ExcelWriter(out_file)
    cmb_df.to_excel(writer, sheet_name="Sheet1", index=False)
    writer.save()

    return cmb_df, label
