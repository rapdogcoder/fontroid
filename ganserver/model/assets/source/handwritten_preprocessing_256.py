import random
import numpy as np
import glob
from common.images import get_single_font_image, arr_to_img, merge_img_array
from common import preprocessing
from common.utils import round_function, centering_image
from torchvision.transforms.functional import to_pil_image
from PIL import Image
import os
import sys

if len(sys.argv) != 3:
    print("Insufficient arguments")
    sys.exit()

random.seed(1)


# path setting
input_dir = sys.argv[1] # input dir
output_dir = sys.argv[2] # output dir

path = './'
target_path = os.path.join(path, input_dir)
save_path = os.path.join(path, output_dir)

# 아웃풋 폴더 만들기
try:
    os.makedirs(save_path)
except FileExistsError:
    pass


# initialize
img_size = 256
font_size = 180


# 타겟 폰트당 랜덤 3000자 이미지 생성
target = glob.glob(os.path.join(target_path,'*.png'))
for ch in target: # random 3000 hangul
    charid = os.path.basename(ch).split('.')[0]
    # image generation
    tgt_img = Image.open(ch).convert('L')
    tgt_arr = np.asarray(tgt_img).astype(np.float)

    # preprocessing
    tgt_arr = preprocessing.resizing(tgt_arr, img_size, resize_fix=float(img_size))
    crop_tgt = preprocessing.cropping(tgt_arr)
    resize_tgt = preprocessing.resizing(crop_tgt, font_size, resize_fix=font_size)
    pad_tgt = preprocessing.padding(resize_tgt, img_size)

    # merge images and save
    img = arr_to_img(pad_tgt)
    img = img.convert('L')
    img.save(os.path.join(save_path, charid + '.png'))
