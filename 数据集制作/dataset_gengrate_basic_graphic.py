#!/usr/bin/env python
# -*- coding: utf-8 -*-
_Author_ = 'xiaofeng'

'''
本程序用来生成基准几何图形
圆形，三角形，矩形，平行四边形，菱形，椭圆形，抛物线，直线，平行线，等
进行类别划分：
0-直线
1-矩形
2-三角形
3-四边形(非矩形)
4-五边形及以上
5-椭圆形
6-圆形
7-抛物线？
'''

import cv2
import numpy as np
import random
import os, shutil
import config as cfg

size_height = 500
size_width = 700
channel = 3
blackground = 255  # 白色背景
graphic_color = (0, 0, 0)
count_want = 4  # 一次生成多少个随机数-生成直线
saved_path = '/Users/xiaofeng/Work_Guanghe/datasets/img/'
label_path = '/Users/xiaofeng/Work_Guanghe/datasets/label/'
# 生成背景
epoch_nums = 1000
count = 1
THICK = [0.5, 1, 1.5]

'''
查询当前目录下是否有子目录，如果有则清除1
'''
list = os.listdir(saved_path)
temp = os.listdir(label_path)
print('please confirm ')
print(saved_path, '\n', label_path)
if list or temp:
    print('目录中存在子目录或文件，进行该目录清空操作。')
    shutil.rmtree(saved_path)
    shutil.rmtree(label_path)
    os.makedirs(saved_path)
    os.makedirs(label_path)
print('已完成目录文件清空，开始生成随机几何图形文件夹.')
'''
生成随机直线
'''
single_file = saved_path + 'linear/'
# txt_single_file = label_path + 'linear/'
if not os.path.exists(single_file):
    os.makedirs(single_file)
# if not os.path.exists(txt_single_file):
#     os.mkdir(txt_single_file)
for i in range(epoch_nums):
    for j in range(3, 5):
        img = 255 * np.ones((size_height, size_width, cfg.IMAGE_CHANNEL), dtype=np.int8)
        random_generate = random.sample(range(0, size_height), count_want)
        img = cv2.line(img, (random_generate[0], random_generate[1]),
                       (random_generate[2], random_generate[2]),
                       color=graphic_color,
                       thickness=int(j))
        img_count = '00000%s.png' % count
        label_out = '00000%s.txt' % count
        save_name = os.path.join(single_file, img_count)
        # label_save_name = os.path.join(txt_single_file, label_out)
        label_save_name = os.path.join(label_path, label_out)
        cv2.imwrite(save_name, img)
        with open(label_save_name, 'w+') as tx:
            tx.writelines('line')
        tx.close()
        count += 1
print(count, 'line done ')
'''
生成随机矩形
'''
single_file = saved_path + 'retangle/'
# txt_single_file = label_path + 'retangel/'
if not os.path.exists(single_file):
    os.makedirs(single_file)
# if not os.path.exists(txt_single_file):
#     os.mkdir(txt_single_file)
for i in range(epoch_nums):
    for k in range(2, 5):
        img = 255 * np.ones((size_height, size_width, channel), dtype=np.int8)
        random_generate_x1 = random.sample(range(50, 345), 1)
        random_generate_y1 = random.sample(range(50, 245), 1)
        random_generate_x2 = random.sample(range(355, 690), 1)
        random_generate_y2 = random.sample(range(255, 490), 1)
        img = cv2.rectangle(img, (random_generate_x1[0], random_generate_y1[0]),
                            (random_generate_x2[0], random_generate_y2[0]),
                            color=graphic_color,
                            thickness=k)
        img_count = '00000%s.png' % count
        label_out = '00000%s.txt' % count
        save_name = os.path.join(single_file, img_count)
        # label_save_name = os.path.join(txt_single_file, label_out)
        label_save_name = os.path.join(label_path, label_out)
        cv2.imwrite(save_name, img)
        with open(label_save_name, 'w+') as tx:
            tx.writelines('retangle')
        tx.close()
        count += 1
print(count, 'retangle done')
'''
生成随机多边形,3,4,5,6,7,8
'''
point_want = [3, 4, 5, 6]
name = ['triangle', 'quadrilateral', 'Pentagons', 'hexagon']
for points in range(len(point_want)):
    single_file = saved_path + str(name[points]) + '/'
    # txt_single_file = label_path + str(name[points]) + '/'
    if not os.path.exists(single_file):
        os.makedirs(single_file)
    # if not os.path.exists(txt_single_file):
    #     os.mkdir(txt_single_file)
    for i in range(epoch_nums):
        for k in range(2, 5):
            img = 255 * np.ones((size_height, size_width, channel), dtype=np.int8)
            random_generate = np.random.randint(0, size_height, (point_want[points], 2))
            # print(random_generate)
            pts = random_generate.reshape((-1, 1, 2))
            img = cv2.polylines(img=img, pts=[pts], isClosed=True, color=graphic_color, thickness=int(k))
            img_count = '00000%s.png' % count
            label_out = '00000%s.txt' % count
            save_name = os.path.join(single_file, img_count)
            # label_save_name = os.path.join(txt_single_file, label_out)
            label_save_name = os.path.join(label_path, label_out)
            cv2.imwrite(save_name, img)
            with open(label_save_name, 'w+') as tx:
                tx.writelines(str(name[points]))
            tx.close()
            count += 1
print(count, '多边形完成')
'''
生成随机圆形
'''
circle_point_r = 2
single_file = saved_path + 'circle/'
# txt_single_file = label_path + 'circle/'
if not os.path.exists(single_file):
    os.makedirs(single_file)
# if not os.path.exists(txt_single_file):
#     os.mkdir(txt_single_file)
# for i in range(epoch_nums):
#     for k in range(2, 5):
#         img = 255 * np.ones((size_height, size_width, channel), dtype=np.int8)
#         random_generate_center_x = random.sample(range(250, 450), 1)
#         random_generate_center_y = random.sample(range(50, 450), 1)
#         temp = [random_generate_center_y[0] - 10,
#                 480 - np.max([random_generate_center_x[0], random_generate_center_y[0]])]
#         random_generate_radius = random.sample(range(10, min(temp)), 1)
#         img = cv2.circle(img=img, center=(random_generate_center_x[0], random_generate_center_y[0]),
#                          radius=random_generate_radius[0],
#                          color=graphic_color,
#                          thickness=int(k))
#         img_count = '00000%s.png' % count
#         label_out = '00000%s.txt' % count
#         save_name = os.path.join(single_file, img_count)
#         # label_save_name = os.path.join(txt_single_file, label_out)
#         label_save_name = os.path.join(label_path, label_out)
#         cv2.imwrite(save_name, img)
#         with open(label_save_name, 'w+') as tx:
#             tx.writelines('circle')
#         tx.close()
#         count += 1
'''
生成中心位置圆形
'''
for i in range(epoch_nums):
    for k in range(2, 5):
        img = 255 * np.ones((size_height, size_width, channel), dtype=np.int8)
        random_generate_center_x = random.sample(range(320, 380), 1)
        random_generate_center_y = random.sample(range(230, 280), 1)
        temp = [random_generate_center_y[0] - 10,
                450 - np.max([random_generate_center_x[0], random_generate_center_y[0]])]
        random_generate_radius = random.sample(range(10, min(temp)), 1)
        img = cv2.circle(img=img, center=(random_generate_center_x[0], random_generate_center_y[0]),
                         radius=random_generate_radius[0],
                         color=graphic_color,
                         thickness=int(k))
        img_count = '00000%s.png' % count
        label_out = '00000%s.txt' % count
        save_name = os.path.join(single_file, img_count)
        # label_save_name = os.path.join(txt_single_file, label_out)
        label_save_name = os.path.join(label_path, label_out)
        cv2.imwrite(save_name, img)
        with open(label_save_name, 'w+') as tx:
            tx.writelines('circle')
        tx.close()
        count += 1
print(count, 'circle done')

'''
随机椭圆
'''
long_axel = 1
short_axel = 1
single_file = saved_path + 'ellipse/'
# txt_single_file = label_path + 'ellipse/'
if not os.path.exists(single_file):
    os.makedirs(single_file)
# if not os.path.exists(txt_single_file):
#     os.mkdir(txt_single_file)
# for i in range(epoch_nums):
#     for k in range(2, 5):
#         img = 255 * np.ones((size_height, size_width, channel), dtype=np.int8)
#         random_generate_center_x = random.sample(range(250, 450), 1)
#         random_generate_center_y = random.sample(range(50, 450), 1)
#         temp = [random_generate_center_y[0] - 15,
#                 480 - np.max([random_generate_center_x[0], random_generate_center_y[0]])]
#         random_generate_long = random.sample(range(15, min(temp)), 1)
#         random_generate_short = random.sample(range(10, random_generate_long[0]), short_axel)
#         img = cv2.ellipse(img=img, center=(random_generate_center_x[0], random_generate_center_y[0]),
#                           axes=(random_generate_long[0], random_generate_short[0]),
#                           angle=0,
#                           startAngle=0, endAngle=360,
#                           color=graphic_color,
#                           thickness=int(k))
#         img_count = '00000%s.png' % count
#         label_out = '00000%s.txt' % count
#         save_name = os.path.join(single_file, img_count)
#         # label_save_name = os.path.join(txt_single_file, label_out)
#         label_save_name = os.path.join(label_path, label_out)
#         cv2.imwrite(save_name, img)
#         with open(label_save_name, 'w+') as tx:
#             tx.writelines('ellipse')
#         tx.close()
#         count += 1
'''
生成中心位置椭圆
'''
for i in range(epoch_nums):
    for k in range(2, 5):
        img = 255 * np.ones((size_height, size_width, channel), dtype=np.int8)
        random_generate_center_x = random.sample(range(320, 380), 1)
        random_generate_center_y = random.sample(range(230, 280), 1)
        temp = [random_generate_center_y[0] - 15,
                450 - np.max([random_generate_center_x[0], random_generate_center_y[0]])]
        random_generate_long = random.sample(range(15, min(temp)), 1)
        random_generate_short = random.sample(range(10, random_generate_long[0]), short_axel)
        img = cv2.ellipse(img=img, center=(random_generate_center_x[0], random_generate_center_y[0]),
                          axes=(random_generate_long[0], random_generate_short[0]),
                          angle=0,
                          startAngle=0, endAngle=360,
                          color=graphic_color,
                          thickness=int(k))
        img_count = '00000%s.png' % count
        label_out = '00000%s.txt' % count
        save_name = os.path.join(single_file, img_count)
        # label_save_name = os.path.join(txt_single_file, label_out)
        label_save_name = os.path.join(label_path, label_out)
        cv2.imwrite(save_name, img)
        with open(label_save_name, 'w+') as tx:
            tx.writelines('ellipse')
        tx.close()
        count += 1
print(count, 'ellipse done')
