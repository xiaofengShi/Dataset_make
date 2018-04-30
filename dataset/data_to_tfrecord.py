#!/usr/bin/env python
# -*- coding: utf-8 -*-
_Author_ = 'xiaofeng'

'''
将自己的数据集制作成为tfrecord的格式,以进行网络训练 
'''

import tensorflow as tf
import os, random
from dataset.data_find_all_dirs import GetFileFromThisRootDir
import config as cfg
from PIL import Image

slim = tf.contrib.slim

print('Please confirm the resize shape is :', cfg.IMAGE_HEIGHT, cfg.IMAGE_WIDTH, cfg.IMAGE_CHANNEL)


# 生成整数型的属性
def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


# 生成浮点类型的属性
def _float_feature(value):
    if not isinstance(value, list):
        value = [value]
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))


# 生成字符串类型的属性
def _bytes_feature(value):
    if not isinstance(value, list):
        value = [value]
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=value))


# Make the TfRecord file
def createTFRecord(dataset_dir, tfrecorder_dir, mapfile, shuffling, train_or_test):
    if not tf.gfile.Exists(dataset_dir):
        print('The directory : %s is wrong' % dataset_dir)
        exit()
    # labels make
    classes = []
    class_map = {}  # is a dict
    if cfg.CLASSES_NAMES is None:
        print('不存在类别名称')
        data_labels_list = os.listdir(dataset_dir)
        # delete the file('.DS_Store')
        how_many_files = len(data_labels_list)
        for i in data_labels_list:
            if i == '.DS_Store':
                continue
            classes.append(i)
    if cfg.CLASSES_NAMES is not None:
        print('存在类别名称')
        how_many_files = len(cfg.CLASSES_NAMES)
        for i in cfg.CLASSES_NAMES:
            classes.append(i)
    # 输出TFRecord文件的地址
    files_count = 1
    with tf.python_io.TFRecordWriter(tfrecorder_dir) as tfrecorder_writer:
        for index, name in enumerate(classes):
            class_path = os.path.join(dataset_dir, name)
            class_map[index] = name
            # 直接得到文件夹下的图片的路径
            img_name_list = GetFileFromThisRootDir([class_path], ext=cfg.EXTENSION)
            if shuffling:
                random.seed(cfg.RANDOM_SEED)
                random.shuffle(img_name_list)
            for img_path in img_name_list:
                img = Image.open(img_path)
                img = img.resize((cfg.IMAGE_HEIGHT, cfg.IMAGE_WIDTH))
                img_raw = img.tobytes()
                example = tf.train.Example(features=tf.train.Features(feature={
                    'label': _int64_feature(index),
                    'image_raw': _bytes_feature(img_raw)
                }))
                tfrecorder_writer.write(example.SerializeToString())
            print('\n  %s / %s___Completed the filename: %s' % (files_count, how_many_files, name))
            files_count += 1
    print('\nFinished converting the %s dataset!' % train_or_test)
    with open(mapfile, 'w+') as label_txt:
        for key in class_map.keys():
            label_txt.writelines(str(key) + ":" + class_map[key] + "\n")
    label_txt.close()


def get_output_filename(output_dir, project_name, train_or_test):
    if not tf.gfile.Exists(output_dir):
        tf.gfile.MkDir(output_dir)
    tfrecord = '%s/%s_%s.tfrecord' % (output_dir, project_name, train_or_test)
    txt = '%s/%s_%s.txt' % (output_dir, project_name, train_or_test)
    return tfrecord, txt


# 读取生成的tfrecord，并进行resize
def read_and_decode(filename):
    # 创建一个reader来读取TFRecord文件中的样例
    reader = tf.TFRecordReader()
    # 创建一个队列来维护输入文件列表
    filename_queue = tf.train.string_input_producer([filename])
    # 从文件中读出一个样例，也可以使用read_up_to一次读取多个样例
    _, serialized_example = reader.read(filename_queue)
    # 解析读入的一个样例，如果需要解析多个，可以用parse_example
    features = tf.parse_single_example(
        serialized_example,
        features={'label': tf.FixedLenFeature([], tf.int64),
                  'image_raw': tf.FixedLenFeature([], tf.string), })
    # 将字符串解析成图像对应的像素数组
    img = tf.decode_raw(features['image_raw'], tf.uint8)
    img = tf.reshape(img, [cfg.IMAGE_HEIGHT, cfg.IMAGE_WIDTH, cfg.IMAGE_CHANNEL])  # reshape为128*128*3通道图片
    img = tf.cast(img, tf.float32)
    img = tf.cast(img, tf.float32) * (1. / 255) - 0.5
    labels = tf.cast(features['label'], tf.int32)
    return img, labels


# 生成batch
def createBatch(filename, batchsize, depth, istraing=True):
    images, labels = read_and_decode(filename)
    if istraing:
        min_after_dequeue = 90000
        capacity = 100000
    if not istraing:
        min_after_dequeue = 20000
        capacity = 26000
    image_batch, label_batch = tf.train.shuffle_batch([images, labels],
                                                      batch_size=batchsize,
                                                      num_threads=2,
                                                      capacity=capacity,
                                                      min_after_dequeue=min_after_dequeue
                                                      )

    label_batch = tf.one_hot(label_batch, depth=depth)
    return image_batch, label_batch


def run_dataset_tfrecord(shuffling=False, is_training=True):
    output_tfrecord_txt = cfg.TFRECORD_SAVED_DIR

    # 根据是否进行训练来匹配不同的数据集和创建的和tfreocrd名称，以及batch_size的大小，并创建batch
    if is_training:
        dataset = cfg.TRAIN_DATASET
        tfrecord, txt = get_output_filename(output_tfrecord_txt, cfg.Project_NAME, cfg.TRAIN)
        batch_size = cfg.BATCH_SIZE
    if not is_training:
        dataset = cfg.TEST_DATASET
        tfrecord, txt = get_output_filename(output_tfrecord_txt, cfg.Project_NAME, cfg.TEST)
        batch_size = cfg.BATCH_SIZE_TEST
    print('Start to  make tfrecord!!')

    if not os.path.exists(tfrecord):
        createTFRecord(dataset_dir=dataset,
                       tfrecorder_dir=tfrecord,
                       mapfile=txt,
                       shuffling=shuffling,
                       train_or_test=cfg.TRAIN)
    print('Tfrecord is ready, the directory is :', cfg.TFRECORD_SAVED_DIR)

    image_batch, label_batch = createBatch(filename=tfrecord, batchsize=batch_size,
                                           depth=cfg.CLASSES, istraing=is_training)

    print('Batches  are ready, batch size is :', batch_size)

    return image_batch, label_batch
    # print(type(image), type(label))
    # return image, label
    # run_dataset_tfrecord(cfg.DATASET)
