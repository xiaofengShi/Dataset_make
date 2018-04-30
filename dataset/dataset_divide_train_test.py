#!/usr/bin/env python
# -*- coding: utf-8 -*-
_Author_ = 'xiaofeng'

'''
将数据集切分成测试集和训练集
'''
import random, os, shutil
from dataset.data_find_all_dirs import GetFileFromThisRootDir
import config as cfg

dataset_dir = '/Users/xiaofeng/Work_Guanghe/datasets/img_2/'
saved_dir = '/Users/xiaofeng/Work_Guanghe/datasets/'


def dataset_diviede(dataset_dir, out_dir):
    train_dir = os.path.join(out_dir, cfg.TRAIN)
    test_dir = os.path.join(out_dir, cfg.TEST)
    img_list_all = GetFileFromThisRootDir([dataset_dir], cfg.EXTENSION)
    how_many_imgs = len(img_list_all)
    print(how_many_imgs)
    files_divide_to_test = int(how_many_imgs * cfg.PROPORTION)
    count = 1
    print('copy to the test')
    while count < files_divide_to_test:
        print(len(img_list_all))
        files_random = random.sample(img_list_all, 1)[0]
        # print(files_random)
        img_name = files_random.split('/')[-1]
        img_dir = files_random.split('/')[-2]
        # img_dir_name = os.path.join(img_dir, img_name)
        saved_dir = os.path.join(test_dir, img_dir)
        if not os.path.exists(saved_dir):
            os.makedirs(saved_dir)
        save_name = os.path.join(saved_dir, img_name)
        shutil.copy(files_random, save_name)
        # os.remove(files_random)
        img_list_all.remove(files_random)
        count += 1
        print(count, '/', files_divide_to_test)
    print('copy to train')
    num = 1
    for file_rest in img_list_all:
        img_name = file_rest.split('/')[-1]
        img_dir = file_rest.split('/')[-2]
        saved_dir = os.path.join(train_dir, img_dir)
        if not os.path.exists(saved_dir):
            os.makedirs(saved_dir)
        save_name = os.path.join(saved_dir, img_name)
        shutil.copy(file_rest, save_name)
        num += 1
        print(num, '/', len(img_list_all))

    print('done')


dataset_diviede(dataset_dir=dataset_dir, out_dir=saved_dir)
