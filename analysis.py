'''
Author: david
Date: 2024-07-14 15:59:45
LastEditors: david
LastEditTime: 2024-07-14 16:07:20
FilePath: /MedicalAnakysis/analysis.py
Description: 

Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
'''

import seaborn as sns
import pandas as pd
import matplotlib
import numpy as np
import matplotlib.pyplot as plt


def read_data(file_abs_path) -> pd.DataFrame:
    df = pd.read_excel(file_abs_path)

    columns = df.columns
    left_columns = []
    for column_name in columns:
        num = np.count_nonzero(df[column_name])
        if num >= 20:
            left_columns.append(column_name)

    return pd.DataFrame(columns=left_columns, data=df)


def visualize_hot_results(data):
    # 协方差-热力图
    sns.set_theme()
    plt.rcParams['font.sans-serif'] = 'simhei'
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    correlation_matrix = data.corr()
    g = sns.heatmap(data=correlation_matrix, cmap="RdBu_r",
                    annot=True, xticklabels=True, yticklabels=True, fmt=".2f")
    g.set_title("协方差热力图")
    matplotlib.pyplot.show()


def visualize_corr_results(data):
    # 相关性图-相关图
    data['患病概率等级'] = ""
    for idx, prob in enumerate(data[data.columns[-2]]):
        if 0 <= prob and prob < 15:
            data['患病概率等级'][idx] = "<15"
        elif 15 <= prob and prob < 30:
            data['患病概率等级'][idx] = "<30"
        elif 30 <= prob:
            data['患病概率等级'][idx] = "<100"
        else:
            print(prob)
    g = sns.pairplot(data=data, diag_kind="kde")
    g.fig.suptitle("物质相关性比较")
    matplotlib.pyplot.show()


def visualize_box(data):
    # 箱型图
    data['患病概率'] = 100.
    data['患病概率等级'] = "High"
    for idx, prob in enumerate(data[data.columns[-2]]):
        if 0 <= prob and prob < 15:
            data['患病概率等级'][idx] = "<15"
        elif 15 <= prob and prob < 30:
            data['患病概率等级'][idx] = "<30"
        elif 30 <= prob and prob < 40:
            data['患病概率等级'][idx] = "<40"
        elif 40 <= prob:
            data['患病概率等级'][idx] = "<100"


def visualize_column_chart(data):
    sns.set_theme()
    plt.rcParams['font.sans-serif'] = 'simhei'
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    rows = 4
    cols = 4
    _, ax = plt.subplots(rows, cols, constrained_layout=True, figsize=(8, 3))
    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c
            if idx >= len(data.columns) - 2:
                break
            pic = sns.boxplot(
                x=data.columns[idx], y=data.columns[-1], data=data, ax=ax[r][c])
            pic.set_title("{0} vs {1}".format(
                data.columns[idx], data.columns[-2]))
    matplotlib.pyplot.show()
