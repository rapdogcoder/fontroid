import numpy as np
from PIL import Image
import scipy.misc as misc
import ast
import glob
from PIL import ImageFont
from scipy.misc import imresize
import pickle as pickle
import random
import os
from common.dataset import save_fixed_sample
from common.function import init_embedding
from PIL import Image, ImageDraw
from pathlib import Path

PARENT_PATH = Path(__file__).resolve().parent.parent






##################################### 이건 템플릿 받을 때 ###########################################
# user_name = input('사용자 이름 : ')
# img = misc.imread(f'./handwritten_{user_name}.jpg', mode='L')
# with open('./rand_hangul.txt','r',encoding='utf-8') as f:
#     label = ast.literal_eval(f.read())
# def crop_full(img_arr):
#     img_size1, img_size2 = img_arr.shape[0], img_arr.shape[1]
#     full_white = np.asarray(Image.new('L', (img_size2, img_size1), color=255)).astype(np.float)
#     col_sum = np.where(np.sum(full_white, axis=0) - np.sum(img_arr, axis=0) > 100)
#     row_sum = np.where(np.sum(full_white, axis=1) - np.sum(img_arr, axis=1) > 100)
#     y1, y2 = row_sum[0][0], row_sum[0][-1]
#     x1, x2 = col_sum[0][0]+3, col_sum[0][-1]
#     cropped_image = img_arr[y1:y2, x1:x2]
#     return cropped_image
# print(label)
# cropped = crop_full(img)
# im = Image.fromarray(cropped)
# y = cropped.shape[0]
# x = cropped.shape[1]
# print(x,y)
# y = int(cropped.shape[0]/14)
# x = int(cropped.shape[1]/15)
# img = []
# cnt = 0
# for i in range(7):
#     for j in range(15):
#         img = cropped[i*y+45+3:(i+1)*y-3,j*x+10:(j+1)*x-5]
#         im = Image.fromarray(img)
#         im.save(f"./handwritten/{user_name}_{label[cnt]}.jpg")
#         cnt+=1
###################################################################################################











def draw_single_char(ch, font, canvas_size):
    image = Image.new('L', (canvas_size, canvas_size), color=255)
    drawing = ImageDraw.Draw(image)
    w, h = drawing.textsize(ch, font=font)
    drawing.text(
        ((canvas_size-w)/2, (canvas_size-h)/2),
        ch,
        fill=(0),
        font=font
    )
    flag = np.sum(np.array(image))
    
    # 해당 font에 글자가 없으면 return None
    if flag == 255 * 128 * 128:
        return None
    
    return image

def normalize_image(img_arr): # 글씨 부분은 -1, 배경은 1로 normalize
    normalized = img_arr / 127.5 -1.
    return normalized


def cropping(img_arr):
    img_size1, img_size2 = img_arr.shape[0], img_arr.shape[1]
    full_white = np.asarray(Image.new('L', (img_size2, img_size1), color=255)).astype(np.float)
    col_sum = np.where(np.sum(full_white, axis=0) - np.sum(img_arr, axis=0) > 200)
    row_sum = np.where(np.sum(full_white, axis=1) - np.sum(img_arr, axis=1) > 200)
    y1, y2 = row_sum[0][0], row_sum[0][-1]
    x1, x2 = col_sum[0][0], col_sum[0][-1]
    cropped_image = img_arr[y1:y2, x1:x2]
    return cropped_image

def resizing(img_arr, max_size, resize_fix=False):
    if type(resize_fix) == int: # 큰 쪽을 resize_fix로 고정
        origin_h, origin_w = img_arr.shape
        if origin_h > origin_w:
            resize_w = int(origin_w * (resize_fix / origin_h))
            resize_h = resize_fix
        else:
            resize_h = int(origin_h * (resize_fix / origin_w))
            resize_w = resize_fix
    elif type(resize_fix) == float: # resize_fix 만큼 곱하기
        origin_h, origin_w = img_arr.shape
        resize_h, resize_w = int(origin_h * resize_fix), int(origin_w * resize_fix)
        if resize_h > max_size: # max_size보다 글씨가 크면 max_size로 고정
            resize_h = max_size
            resize_w = int(resize_w * max_size / resize_h)
        if resize_w > max_size:
            resize_w = max_size
            resize_h = int(resize_h * max_size / resize_w)
    
    # resize
    if resize_fix != False:
        img_arr = imresize(img_arr, (resize_h, resize_w))
        img_arr = normalize_image(img_arr)

    return img_arr

def padding(img_arr, size, pad_value=255):
    height, width = img_arr.shape
    if not pad_value:
        pad_value = img_arr[0][0]

    # Adding padding of x axis
    pad_x_width = (size - width) // 2
    pad_x = np.full( (height, pad_x_width), pad_value, dtype=np.float32)
    img_arr = np.concatenate( (pad_x, img_arr), axis=1)
    img_arr = np.concatenate( (img_arr, pad_x), axis=1)
    width = img_arr.shape[1]

    # Adding padding of y axis
    pad_y_height = (size - height) // 2
    pad_y = np.full( (pad_y_height, width), pad_value, dtype=np.float32)
    img_arr = np.concatenate((pad_y, img_arr), axis=0)
    img_arr = np.concatenate((img_arr, pad_y), axis=0)

    # match to original image size
    width = img_arr.shape[1]
    if img_arr.shape[0] % 2: # where height is size-1
        pad = np.full( (1, width), pad_value, dtype=np.float32)
        img_arr = np.concatenate((pad, img_arr), axis=0)
    height = img_arr.shape[0]
    if img_arr.shape[1] % 2: # where width is size-1
        pad = np.full( (height, 1), pad_value, dtype=np.float32)
        img_arr = np.concatenate( (pad, img_arr), axis=1)

    return img_arr

def merge_img_array(tgt_arr, src_arr):
    return np.concatenate((tgt_arr, src_arr), axis=1)

def arr_to_img(img_arr):
    img_arr_255 = ((img_arr + 1.) * 127.5)
    img = Image.fromarray(img_arr_255).convert('L')
    return img

def pickle_examples(from_dir, train_path, val_path, train_val_split=0.2, with_charid=False):
    """
    Compile a list of examples into pickled format, so during
    the training, all io will happen in memory
    """
    paths = glob.glob(os.path.join(from_dir, "*.jpg"))
    hangul = []
    with open(str(PARENT_PATH/'makefontapp/static/makefontapp/txt/2350-common-hangul.txt'),'r',encoding='utf-8') as f:
        hangul = [line.rstrip() for line in f]
    with open(train_path, 'wb') as ft:
        with open(val_path, 'wb') as fv:
            print('all data num:', len(paths))
            c = 1
            val_count = 0
            train_count = 0
            if with_charid:
                print('pickle with charid')
                for p in paths:
                    c += 1
                    label = 0
                    charid = hangul.index(p.split('_')[-1].split('.')[0])
                    with open(p, 'rb') as f:
                        img_bytes = f.read()
                        example = (label, charid, img_bytes)
                        r = random.random()
                        if r < train_val_split:
                            pickle.dump(example, fv)
                            val_count += 1
                            if val_count % 10000 == 0:
                                print("%d imgs saved in val.obj" % val_count)
                        else:
                            pickle.dump(example, ft)
                            train_count += 1
                            if train_count % 10000 == 0:
                                print("%d imgs saved in train.obj" % train_count)
                print("%d imgs saved in val.obj, end" % val_count)
                print("%d imgs saved in train.obj, end" % train_count)
            else:
                for p in paths:
                    c += 1
                    label = 0
                    with open(p, 'rb') as f:
                        img_bytes = f.read()
                        example = (label, img_bytes)
                        r = random.random()
                        if r < train_val_split:
                            pickle.dump(example, fv)
                            val_count += 1
                            if val_count % 10000 == 0:
                                print("%d imgs saved in val.obj" % val_count)
                        else:
                            pickle.dump(example, ft)
                            train_count += 1
                            if train_count % 10000 == 0:
                                print("%d imgs saved in train.obj" % train_count)
                print("%d imgs saved in val.obj, end" % val_count)
                print("%d imgs saved in train.obj, end" % train_count)
            return




def get_static():
    
    src_font = ImageFont.truetype(str(PARENT_PATH/'makefontapp/static/makefontapp/font/source_font.ttf'), 110)
    real_font = glob.glob(str(PARENT_PATH/'media/uploads/user_words/*.jpg'))
    real_font.extend(glob.glob(str(PARENT_PATH/'/media/uploads/user_words/*.png')))
    for i in real_font:
        char_id = i.split('_')[-1].split('.')[0]
        real_img = misc.imread(i, mode='L')
        src_img = draw_single_char(char_id, src_font, 128)

        real_arr = np.array(real_img).astype(np.float)
        src_arr = np.array(src_img).astype(np.float)

        crop_real = cropping(real_arr)
        resize_real = resizing(crop_real, 110, resize_fix=10.)
        pad_real = padding(resize_real, 128)
        
        crop_src = cropping(src_arr)
        resize_src = resizing(crop_src, 110, resize_fix=10.)
        pad_src = padding(resize_src, 128)
        
        merged = merge_img_array(pad_real, pad_src)
        pil_image = arr_to_img(merged)

        pil_image = pil_image.convert('L')
        pil_image.save(str(PARENT_PATH/'makefontapp/handwritten_jpg/final_'+char_id+'.jpg'))

    pickle_examples(str(PARENT_PATH/'makefontapp/handwritten_jpg'), str(PARENT_PATH/'makefontapp/handwritten_obj/train.obj'),str(PARENT_PATH/'makefontapp/handwritten_obj/val.obj'),with_charid=True)
    save_fixed_sample(32, 128, str(PARENT_PATH/'makefontapp/handwritten_obj/'), str(PARENT_PATH/'makefontapp/handwritten_fixed_dir/'), val=0.2, with_charid=True)

    handwritten_embedding = init_embedding(1, 128)
    with open(str(PARENT_PATH/'makefontapp/handwritten_fixed_dir/EMBEDDINGS.pkl'), 'wb') as f:
        pickle.dump(handwritten_embedding,f)

