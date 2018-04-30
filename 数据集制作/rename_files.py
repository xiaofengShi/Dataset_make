import os
import shutil


def rename(path_ori, newpath, flage=True):
    newname_front = input("please input the new name style:")
    print('new name is the format like %s_1.....' % (newname_front))
    newname_front = newname_front.strip()
    file_list = os.listdir(path_ori)
    i = 0
    for file in file_list:
        i += 1
        olddir = os.path.join(path_ori, file)
        if os.path.isdir(olddir):
            continue
        filename = os.path.splitext(file)[0]
        filetype = os.path.splitext(file)[1]
        newname = newname_front + '_' + str(i)
        rename_dir = os.path.join(path_ori, newname + filetype)
        rename_new_dir = os.path.join(newpath, newname + filetype)
        os.rename(olddir, rename_dir)
        # savedatapath = os.path.join(strangedatafile, filename)
        if flage:
            shutil.copyfile(rename_dir, rename_new_dir)
    newfile_list = os.listdir(newpath)
    return newfile_list


###########################//
# test
###########################//
path = '/home/sxf/MyProject_Python/normal_code/data_make/my_data_to_voc/ori_data/image'
newpath = '/home/sxf/MyProject_Python/normal_code/data_make/my_data_to_voc/made_normal'
list = rename(path, newpath, flage=True)
print(list)
