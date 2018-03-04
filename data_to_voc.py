# 输出voc数据中的image/main中的文件test.txt , train.txt, val.txt ,trainval.txt.
import os
import random

trainval_percent = 0.66
train_percent = 0.5
xmlfilepath = '/home/sxf/MyProject_Python/normal_code/data_make/my_data_to_voc/made_normal/Annotations'
txtsavepath = '/home/sxf/MyProject_Python/normal_code/data_make/my_data_to_voc/made_normal/ImageSets/Main'
total_xml = os.listdir(xmlfilepath)

num = len(total_xml)
list = range(num)
tv = int(num * trainval_percent)
tr = int(tv * train_percent)
trainval = random.sample(list, tv)
train = random.sample(trainval, tr)

ftrainval = open(
    '/home/sxf/MyProject_Python/normal_code/data_make/my_data_to_voc/made_normal/ImageSets/Main/trainval.txt', 'w')
ftest = open('/home/sxf/MyProject_Python/normal_code/data_make/my_data_to_voc/made_normal/ImageSets/Main/test.txt', 'w')
ftrain = open('/home/sxf/MyProject_Python/normal_code/data_make/my_data_to_voc/made_normal/ImageSets/Main/train.txt',
              'w')
fval = open('/home/sxf/MyProject_Python/normal_code/data_make/my_data_to_voc/made_normal/ImageSets/Main/val.txt', 'w')

# 对存在的xml进行读取
for i in list:
    name = total_xml[i][:-4] + '\n'
    if i in trainval:
        ftrainval.write(name)
        if i in train:
            ftrain.write(name)
        else:
            fval.write(name)
    else:
        ftest.write(name)

ftrainval.close()
ftrain.close()
fval.close()
ftest.close()
