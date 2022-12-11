import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import sys
import os

if len(sys.argv) != 3:
    print("Insufficient arguments")
    sys.exit()

# path setting
input_file = sys.argv[1] # input file (template)
output_dir = sys.argv[2] # output directory

recent_path = os.path.abspath(os.path.dirname(__file__))

handwritten_file = input_file
hangul_file = os.path.join(recent_path,'common/210_hangul.txt')

save_path = os.path.join(output_dir, '1_') # needed for model training

# 아웃풋 폴더 만들기
try:
    os.makedirs(output_dir)
except FileExistsError:
    pass

# read handwritten image
img = cv2.imread(handwritten_file)

# column detection
edges = cv2.Laplacian(img, cv2.CV_8U)
kernel = np.zeros((31, 5), np.uint8)
kernel[:, 2] = 1
eroded = cv2.morphologyEx(edges, cv2.MORPH_ERODE, kernel)
indices = np.nonzero(eroded)
cols = np.unique(indices[1])
filtered_cols = []
for ii in range(len(cols)):
    if ii == 0:
        filtered_cols.append(cols[ii])
    else:
        if np.abs(cols[ii] - cols[ii - 1]) >= 10:
            filtered_cols.append(cols[ii])

# row detection
edges = cv2.Laplacian(img, cv2.CV_8U)
kernel = np.zeros((5, 31), np.uint8)
kernel[2, :] = 1
eroded = cv2.morphologyEx(edges, cv2.MORPH_ERODE, kernel)
indices = np.nonzero(eroded)
rows = np.unique(indices[0])
filtered_rows = []
for ii in range(len(rows)):
    if ii == 0:
        filtered_rows.append(rows[ii])
    else:
        if np.abs(rows[ii] - rows[ii - 1]) >= 10:
            filtered_rows.append(rows[ii])


# labeling
with open(hangul_file, 'r', encoding='utf-8') as rf:
    hangul = rf.read().replace("'", '').replace(",", '').split()

#k = iter(hangul)
k = iter([str(i) for i in range(1, len(hangul)+1)])

from common import preprocessing

for i in range(len(filtered_rows)-1):
    if i%2 == 0:
        continue
    for j in range(len(filtered_cols)-1):
        cropped = img[filtered_rows[i]+3:filtered_rows[i+1]-2,
                                filtered_cols[j]+3:filtered_cols[j+1]-2, :]
        Image.fromarray(cropped).save(save_path + next(k) + '.png')
