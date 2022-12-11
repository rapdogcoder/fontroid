import cv2
import os
import sys
import glob

if len(sys.argv) != 3:
    print("Insufficient arguments")
    sys.exit()

# path setting
input_dir = sys.argv[1] # input dir
output_dir = sys.argv[2] # output dir

try: 
    os.makedirs(output_dir)
except FileExistsError:
    pass

pngs = glob.glob( os.path.join(input_dir, '*.png') )
for png in pngs:
    src = cv2.imread(png)
    dst = cv2.bitwise_not(src)
    cv2.imwrite( os.path.join(output_dir, os.path.basename(png)), dst)
