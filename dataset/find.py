#!/usr/bin/env python
# -*- coding: utf-8 -*-
_Author_ = 'xiaofeng'

from dataset.data_find_all_dirs import GetFileFromThisRootDir
import os

data_dir = '/Users/xiaofeng/Work_Guanghe/datasets/train_2/'

classes = {}
total = 0

with open('find.txt', 'w+') as file:
    file_list = os.listdir(data_dir)
    for i in file_list:
        if i == '.DS_Store':
            continue
        dir = os.path.join(data_dir, i)
        classes[i] = len(GetFileFromThisRootDir([dir], ['png', 'jpg']))
        total += len(GetFileFromThisRootDir([dir], ['png', 'jpg']))
    classes['total'] = total
    a = sorted(classes.items(), key=lambda i: i[1])
    # print(a)
    # print(classes)
    for j in a:
        file.writelines(str(j[0]) + ":" + str(j[1]) + "\n")
