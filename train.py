'''
Author: david
Date: 2024-07-14 15:59:45
LastEditors: david
LastEditTime: 2024-07-14 16:15:03
FilePath: /MedicalAnakysis/train.py
Description: 

Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
'''

from sklearn.decomposition import PCA
import random
import numpy as np
from sklearn import svm
from tabulate import tabulate


def train(data, label):
    proj_dim = 30
    pca = PCA(n_components=proj_dim, whiten=True)
    random_list = list(range(data.shape[0]))
    random.shuffle(random_list)

    split_index = int(len(random_list) * 0.8)
    train_list = random_list[:split_index]
    train_label = label.iloc[train_list]
    train_data = data.iloc[train_list]
    test_list = random_list[split_index:]
    test_label = label.iloc[test_list]
    test_data = data.iloc[test_list]

    data_desc = [[1, "健康人数", np.sum(train_label == 0), "训练"],
                 [2, "结肠癌人数", np.sum(train_label == 1), "训练"],
                 [3, "健康人数", np.sum(test_label == 0), "测试"],
                 [4, "结肠癌人数", np.sum(test_label == 1), "测试"]]
    print(tabulate(data_desc, headers=["序号", "健康状况", "人数", "标签"]))
    print("\n")
    train_mean = train_data.mean()
    A = train_data - train_mean
    A = A.T @ A

    D, V = np.linalg.eig(A)

    data = []
    sort_idx = np.argsort(D)[::-1]
    names = train_data.columns[sort_idx][:proj_dim]
    values = D[sort_idx][:proj_dim]
    for i in range(proj_dim):
        data.append([i+1, names[i], "%e" % values[i].real])

    print(tabulate(data, headers=["序号", "Material(PCA)", "D"]))
    print("\n")
    pca.fit(train_data)

    train_proj = pca.transform(train_data)
    # projecting test data onto pca axes
    test_proj = pca.transform(test_data)

    # instantiating an SVM classifier
    clf = svm.SVC(gamma=0.001, C=100.)
    clf.fit(train_proj, train_label)
    pred_label = clf.predict(test_proj)
    correct = np.sum(test_label == pred_label)
    print("预测精度:", correct / len(test_label) * 100, "%")
