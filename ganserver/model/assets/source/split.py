import os
import sys
import shutil

if len(sys.argv) != 2:
    print ("Insufficient arguments")
    sys.exit()

dir = sys.argv[1]

try:
    os.makedirs(os.path.join(dir, 'f2f'))
    os.makedirs(os.path.join(dir, 'f2s'))
    os.makedirs(os.path.join(dir, 's2f'))
except:
    pass
file_dir = os.path.join(dir,'images')
file_list = os.listdir(file_dir)
print(file_list)
for file in file_list:

    if 'f2f' in file:
        shutil.move(os.path.join(file_dir,file),os.path.join(dir, 'f2f'))
    if 'f2s' in file:
        shutil.move(os.path.join(file_dir,file),os.path.join(dir, 'f2s'))
    if 's2f' in file:
        shutil.move(os.path.join(file_dir,file),os.path.join(dir, 's2f'))
    