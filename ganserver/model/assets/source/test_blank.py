from scipy.misc import imread, imsave
import numpy as np
import glob

files = glob.glob('src-image-data\\images\\*.png')
for file in files:
    src_img = imread(file)
    filename = file.split('\\')[-1]
    black_img = np.zeros([256,256], dtype=np.uint8)
    combined_img = np.concatenate((src_img, black_img, black_img), axis=1)
    imsave('combine-image-data\\images\\'+filename, combined_img)