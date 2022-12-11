import cv2
import glob
import sys
import os
import json


user_id = sys.argv[1]
input_file = sys.argv[2] # input file (template)
output_dir = sys.argv[3] # output directory

file_cur = os.path.dirname(__file__)

# try:
#     os.makedirs(input_file+f'/{user_id}')
# except FileExistsError:
#     pass
# try:
#     os.makedirs(input_file+f'/{user_id}_svg')
# except FileExistsError:
#     pass
# try:
#     os.makedirs(input_file+f'/{user_id}_pnm')
# except FileExistsError:
#     pass

# # s2f img 읽어오기
# pngs = glob.glob(os.path.join(input_file,'s2f/*.png'))



# with open(os.path.join(file_cur,'common/2350.txt'), 'r', encoding='utf-8') as rf:
#     labels = rf.read().split()

# # example.json 파일 읽어오기
# with open(os.path.join(file_cur,'common/example.json'), 'r', encoding='utf-8') as f:
#     json_file = json.load(f)

# # glyphs 초기화
# json_file['glyphs'] = dict()

# for png in pngs:
#     # img 반전
#     src = cv2.imread(png)
#     dst = cv2.bitwise_not(src)

#     # 라벨링
#     png_id = int(os.path.basename(png).split('_')[1].split('-')[0])
#     #cv2.imwrite(f'./{user_id}/{labels[png_id-1]}.png', dst)
#     cv2.imwrite(f'{input_file}/{user_id}/{png_id-1}.png', dst)

#     # svg파일로 변환
#     os.system(f'magick convert {input_file}/{user_id}/{png_id-1}.png {input_file}/{user_id}_pnm/{png_id-1}.pnm')
#     os.system(f'potrace {input_file}/{user_id}_pnm/{png_id-1}.pnm -s -o {input_file}/{user_id}_svg/{png_id-1}.svg')

#     # json 파일 작성
#     json_file['glyphs'][str(hex(ord(labels[png_id-1])))] = dict()
#     json_file['glyphs'][str(hex(ord(labels[png_id-1])))]['src'] = f'{input_file}/{user_id}_svg/{png_id-1}.svg'
#     json_file['glyphs'][str(hex(ord(labels[png_id-1])))]['width'] = 128

# json_file['output'] = [f'{output_dir}/'+user_id+'.ttf', f'{output_dir}/'+user_id+'.svg', f'{output_dir}/'+user_id+'.woff']
# json_file = json.dumps(json_file)


# with open(os.path.join(output_dir,'2350.json'), 'w', encoding='utf-8') as wf:
#     wf.write(json_file)

os.system(f'fontforge -lang=py -script {os.path.join(file_cur,"svgs2ttf.py")} {os.path.join(output_dir,"2350.json")}')