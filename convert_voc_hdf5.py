'''
description: convert the voc2007+2012 datasets to he format of hdf5
date:2017.12.10
'''
import argparse
import os
import numpy as np
import xml.etree.ElementTree as ElementTree
import h5py
from collections import namedtuple

Parameter = namedtuple('Datasets_Parameters',
                       ['datasets_dir', 'saved_path', 'saved_name', 'datasets_train', 'datasets_test', 'datasets_val',
                        'datasets_classes'])


class dataset_to_net_input(object):
    default_params = Parameter(datasets_dir='/home/sxf/MyProject_Python/TFtest/datasets/voc2007+2012',
                               saved_path='/home/sxf/MyProject_Python/TFtest/datasets/voc2007+2012/output',
                               saved_name='voc_2007_2012_h5',
                               datasets_train=[('2007_trainval', 'train'), ('2012_trainval', 'train')],
                               datasets_test=[('2007_test', 'test')],
                               datasets_val=[('2012_trainval', 'val'), ('2007_trainval', 'val')],
                               datasets_classes=["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat",
                                                 "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person",
                                                 "pottedplant", "sheep", "sofa", "train", "tvmonitor"])

    def __init__(self, params=None):
        if isinstance(params, Parameter):
            self.params = params
        else:
            self.params = dataset_to_net_input.default_params


##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#########get the dataset's classes###########
##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def get_classes(voc_path, year, image_index):
    labels = []
    for i in range(len(image_index)):
        single_data_index_list = image_index[i]
        for single_data in single_data_index_list:
            fname = os.path.join(voc_path, 'VOC{}/Annotations/{}.xml'.format(year[i], single_data))
            tree = ElementTree.parse(fname)
            root = tree.getroot()
            for obj in root.findall('object'):
                label = obj.find('name').text
                if label not in labels:
                    labels.append(label)
    return labels


##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#########get the pic's index ################
##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def get_index(voc_path, datasets):
    index = []
    years = []
    for year, image_set in datasets:
        years.append(year)
        ins1 = []
        id_file = os.path.join(voc_path, 'VOC{}/ImageSets/Main/{}.txt'.format(year, image_set))
        with open(id_file, 'r') as image_ids:
            ins1.extend(map(str.strip, image_ids.readlines()))
        index.append(ins1)
    nums = np.sum(len(single) for single in index)
    return index, years, nums


##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%##
#########get the pic's location################
##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%##
def get_groundtruth(voc_path, year, image_index, classes):
    fname = os.path.join(voc_path, 'VOC{}/Annotations/{}.xml'.format(year, image_index))
    with open(fname) as in_file:
        xml_tree = ElementTree.parse(in_file)
    root = xml_tree.getroot()
    groundtruth = []
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        label = obj.find('name').text
        if label not in classes or int(
                difficult) == 1:  # exclude difficult or unlisted classes
            continue
        xml_box = obj.find('bndbox')
        bbox = (classes.index(label), int(xml_box.find('xmin').text),
                int(xml_box.find('ymin').text), int(xml_box.find('xmax').text),
                int(xml_box.find('ymax').text))
        groundtruth.extend(bbox)
    return np.array(groundtruth)


##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#########get the pic#########################
##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def get_pics(voc_path, year, image_index):
    fname = os.path.join(voc_path, 'VOC{}/JPEGImages/{}.jpg'.format(year, image_index))
    with open(fname, 'rb') as in_file:
        pics = in_file.read()
    # Use of encoding based on: https://github.com/h5py/h5py/issues/745
    return np.fromstring(pics, dtype='uint8')


##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#########add data and labels into hdf5#######
##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def add_to_dataset(voc_path, years, image_index_total, images, boxes, labels):
    """Process all given ids and adds them to given datasets."""
    length_list = [len(image) for image in image_index_total]
    length_list.insert(0, 0)
    for which in range(len(image_index_total)):
        image_index = image_index_total[which]
        start = length_list[which]
        for i, voc_id in enumerate(image_index):
            image_data = get_pics(voc_path, years[which], voc_id)
            image_boxes = get_groundtruth(voc_path, years[which], voc_id, labels)
            images[start + i] = image_data
            boxes[start + i] = image_boxes


###################run#####################
def HDF5(datasets_dir=dataset_to_net_input.default_params.datasets_dir,
         save_dir=dataset_to_net_input.default_params.saved_path,
         saved_name=dataset_to_net_input.default_params.saved_name,
         train_set=dataset_to_net_input.default_params.datasets_train,
         val_set=dataset_to_net_input.default_params.datasets_val,
         test_set=dataset_to_net_input.default_params.datasets_test
         ):
    # Get the index,years,nums
    data_path = os.path.expanduser(datasets_dir)
    train_ids, train_years, train_nums = get_index(data_path, train_set)
    val_ids, val_years, val_nums = get_index(data_path, val_set)
    test_ids, test_years, test_nums = get_index(data_path, test_set)
    # labels
    labels = get_classes(data_path, test_years, test_ids)
    # Create HDF5 dataset structure...
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    print('Creating HDF5 dataset structure...')
    fname = os.path.join(save_dir, saved_name + '.hdf5')
    voc_h5file = h5py.File(fname, 'w')

    uint8_dt = h5py.special_dtype(vlen=np.dtype('uint8'))
    vlen_int_dt = h5py.special_dtype(vlen=np.dtype(int))

    train_group = voc_h5file.create_group('train')
    val_group = voc_h5file.create_group('val')
    test_group = voc_h5file.create_group('test')

    # store class list for reference class ids as csv fixed-length numpy string
    voc_h5file.attrs['classes'] = np.string_(str.join(',', labels))

    # store images as variable length uint8 arrays
    train_images = train_group.create_dataset('images', shape=(train_nums,), dtype=uint8_dt)
    val_images = val_group.create_dataset('images', shape=(val_nums,), dtype=uint8_dt)
    test_images = test_group.create_dataset('images', shape=(test_nums,), dtype=uint8_dt)

    # store boxes as class_id, xmin, ymin, xmax, ymax
    train_boxes = train_group.create_dataset('boxes', shape=(train_nums,), dtype=vlen_int_dt)
    val_boxes = val_group.create_dataset('boxes', shape=(val_nums,), dtype=vlen_int_dt)
    test_boxes = test_group.create_dataset('boxes', shape=(test_nums,), dtype=vlen_int_dt)

    # process all ids and add to datasets
    print('Processing  datasets for training set.')
    add_to_dataset(data_path, train_years, train_ids, train_images, train_boxes, labels)
    print('Processing dataset for  val set.')
    add_to_dataset(data_path, val_years, val_ids, val_images, val_boxes, labels)
    print('Processing dataset for  test set.')
    add_to_dataset(data_path, test_years, test_ids, test_images, test_boxes, labels)
    print('Closing HDF5 file.')
    voc_h5file.close()
    print('Done.')


if __name__ == '__main__':
    HDF5()
