#!/usr/bin/env python
# -*- coding: utf-8 -*-
_Author_ = 'xiaofeng'

import cv2
import os
from dataset.data_find_all_dirs import GetFileFromThisRootDir

'''
对下载的图片进行处理，转化成黑白图片，阈值为200，保存名称与原始图片名一致
'''


def threshold_image(input_path, extension, outpath):
    filelist = GetFileFromThisRootDir(input_path, extension)
    print('began threshold the image ')
    for file_path in filelist:
        filename = file_path.split('/')[-1]
        img = cv2.imread(file_path)
        outputname = os.path.join(outpath, filename)
        img = 255 - img
        ret, img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
        cv2.imwrite(outputname, img)
    print('image threshold completed! go to the next step')
