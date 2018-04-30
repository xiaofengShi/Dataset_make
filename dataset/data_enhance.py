#!/usr/bin/env python
# -*- coding: utf-8 -*-
_Author_ = 'xiaofeng'
'''
该程序进行图片增强
'''

from keras.preprocessing.image import ImageDataGenerator
import cv2
import os
from dataset.data_find_all_dirs import GetFileFromThisRootDir
import config as cfg

'''
使用Keras进行数据增强，对图像进行随机旋转，缩放，翻转，剪切等操作
'''


def enhance_img(input_path, extension):
    datagen = ImageDataGenerator(
        rotation_range=0.2,  # 图片随机旋转的角度
        width_shift_range=0.2,  # 图片宽度的变化比例
        height_shift_range=0.2,  # 图片高度的变化比例
        shear_range=0.2,  # 逆时针方向的剪切变换角度
        zoom_range=0.2,  # 随机缩放的幅度
        horizontal_flip=True,  # 进行随机水平翻转
        vertical_flip=False,  # 进行随机竖直方向的翻转
        rescale=0.9,  # 重缩放因子
        fill_mode='nearest',
        data_format='channels_last')

    dirlist = os.listdir(input_path)
    for dir in dirlist:
        file_dir = os.path.join(input_path, dir)
        filelist = GetFileFromThisRootDir([file_dir], extension)
        if len(filelist) <= 1500:
            for file in filelist:
                img = cv2.imread(file)
                img = img.reshape((1,) + img.shape)
                # saves the results to the `preview/` directory
                i = 0
                for _ in datagen.flow(img,
                                          batch_size=1,
                                          save_prefix='0000',
                                          save_to_dir=file_dir,
                                          save_format='png'):
                    i += 1
                    if i > 2:
                        break  # otherwise the generator would loop indefinitely
        print('ok')

    print('done')


enhance_img(input_path='/Users/xiaofeng/Work_Guanghe/datasets/img/', extension=cfg.EXTENSION)

'''
# tensorflow method
import tensorflow as tf
import cv2
import numpy as np

flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_boolean('random_flip_up_down', True, 'If uses flip')
flags.DEFINE_boolean('random_flip_left_right', True, 'If uses flip')
flags.DEFINE_boolean('random_brightness', False, 'If uses brightness')
flags.DEFINE_boolean('random_contrast', False, 'If uses contrast')
flags.DEFINE_boolean('random_saturation', True, 'If uses saturation')
flags.DEFINE_integer('image_height', 500, 'image size.')
flags.DEFINE_integer('image_width', 700, 'image size.')

"""
#flags examples
flags.DEFINE_float('learning_rate', 0.01, 'Initial learning rate.')
flags.DEFINE_integer('max_steps', 2000, 'Number of steps to run trainer.')
flags.DEFINE_string('train_dir', 'data', 'Directory to put the training data.')
flags.DEFINE_boolean('fake_data', False, 'If true, uses fake data for unit testing.')
"""


def pre_process(images):
    if FLAGS.random_flip_up_down:
        images = tf.image.random_flip_up_down(images)
    if FLAGS.random_flip_left_right:
        images = tf.image.random_flip_left_right(images)
    if FLAGS.random_brightness:
        images = tf.image.random_brightness(images, max_delta=0.3)
    if FLAGS.random_contrast:
        images = tf.image.random_contrast(images, 0.8, 1.2)
    if FLAGS.random_saturation:
        tf.image.random_saturation(images, 0.3, 0.5)
    new_size = tf.constant([FLAGS.image_height, FLAGS.image_width], dtype=tf.int32)
    images = tf.image.resize_images(images, new_size)
    return images

# extension = ['png', 'jpg']
# input_path = ['./data/1/']
# enhance_img_out = './data/enhance'
# enhance_img(input_path, extension, enhance_img_out)

# raw_image = cv2.imread('./data/train/1/1.png')
# image = tf.placeholder(dtype='uint8', shape=[None, None, 3])
# images = pre_process(image)
# with tf.Session() as session:
#     result = session.run(images, feed_dict={image: raw_image})
# cv2.imshow("image", result.astype(np.uint8))
# cv2.waitKey(1000)
# cv2.imwrite('./data/1/2.png', result)
'''
