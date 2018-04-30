#!/usr/bin/env python
# -*- coding: utf-8 -*-
_Author_ = 'xiaofeng'

import os

'''
找到路径下的所有置顶后缀名的文件，返回的是包含目录路径的文件名
'''


def GetFileFromThisRootDir(dir_list, ext=None):
    '''
    :param dir_list: 路径列表
    :param ext:指定的后缀，可以为列表形式，例子：['xml', 'java']
    :return: 路径下所有指定后缀名的文件
    '''
    allfiles = []
    if type(dir_list) != list:
        print('You must input a path list, please correct it!!')
        exit(EOFError)
    else:
        for dir in dir_list:
            if not os.path.isdir(dir):
                print('Wrong Ptah ,Correct It.----:', dir)
            needExtFilter = (ext != None)
            for root, dirs, files in os.walk(dir):
                for filespath in files:
                    filepath = os.path.join(root, filespath)
                    extension = os.path.splitext(filepath)[1][1:]
                    if needExtFilter and extension in ext:
                        allfiles.append(filepath)
                    elif not needExtFilter:
                        allfiles.append(filepath)
    return allfiles
