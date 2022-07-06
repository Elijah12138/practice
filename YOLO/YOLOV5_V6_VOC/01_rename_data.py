from hashlib import new
import os

def rename_files(path):
    filelist = os.listdir(path)
    filelist.sort()
    total_num = len(filelist)
    print("total number: {}".format(total_num))
    i = 1
    for item in filelist:
        if item.endswith('.jpg'):
            original_name = os.path.join(path, item)
            try:
                new_name = os.path.join(path, str(i).zfill(4) + ".jpg")
                i = i + 1
                os.rename(original_name, new_name)
                print("{} rename ----> {}".format(original_name, new_name))
            except Exception as e:
                print(e)
                print("rename dir fail")

path = "./data"

rename_files(path)
