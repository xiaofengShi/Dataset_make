#!/usr/bin/env python
# -*- coding: utf-8 -*-
_Author_ = 'xiaofeng'

import random, os, cv2
from dataset.data_find_all_dirs import GetFileFromThisRootDir
import config as cfg

size_height = 500
size_width = 700
channel = 3

'''
进行图像叠加，用于分类网络数据集的制作
'''

def add_two_img(input_path, extension, epoch_nums):
    # 从主目录中读取目录中的文件夹，随机选择两个文件夹，并生成新的文件夹的名称，之后再选择的两个文件夹中各自随机选择一张图像，接下来进行
    dirlist = os.listdir(input_path)
    print(dirlist)
    for epoch in range(epoch_nums):
        folder_random_first = random.sample(dirlist, 1)[0]
        dir_random_first = os.path.join(input_path, folder_random_first)
        folder_random_next = random.sample(dirlist, 1)[0]
        dir_random_next = os.path.join(input_path, folder_random_next)
        if not os.path.isdir(dir_random_first) or not os.path.isdir(dir_random_next):
            continue
        generate_folder = folder_random_first + '_' + folder_random_next  # 设置两个文件夹名称，是为了避免出现遗漏
        generate_folder_anotgher = folder_random_next + '_' + folder_random_first
        dir_list_now = os.listdir(input_path)
        if generate_folder not in dir_list_now and generate_folder_anotgher not in dir_list_now:
            generate_folder_dir = os.path.join(input_path, generate_folder)
            if not os.path.exists(generate_folder_dir):
                os.makedirs(generate_folder_dir)  # 如果路径不存在，则创建路径
        else:
            generate_folder_dir = os.path.join(input_path, generate_folder)
        folder_random_first_file_list = GetFileFromThisRootDir([dir_random_first], extension)
        folder_random_next_file_list = GetFileFromThisRootDir([dir_random_next], extension)

        folder_random_first_file = random.sample(folder_random_first_file_list, 1)[0]
        folder_random_next_file = random.sample(folder_random_next_file_list, 1)[0]
        img_first = cv2.imread(folder_random_first_file)
        img_first = cv2.resize(img_first, dsize=(size_width, size_height), interpolation=cv2.INTER_AREA)
        img_next = cv2.imread(folder_random_next_file)
        img_next = cv2.resize(img_next, dsize=(size_width, size_height), interpolation=cv2.INTER_AREA)
        # print(img_first.shape, img_next.shape)

        generate_img = cv2.addWeighted(src1=img_first, alpha=0.5, src2=img_next, beta=0.5, gamma=0)
        generate_name = 'generata_%s.png' % epoch
        generate_dir = os.path.join(generate_folder_dir, generate_name)
        cv2.imwrite(generate_dir, generate_img)
        print('{}/{}'.format(epoch, epoch_nums))
    print(' add function  done')


add_two_img(input_path='/Users/xiaofeng/Work_Guanghe/datasets/img/', extension=cfg.EXTENSION, epoch_nums=20000)
