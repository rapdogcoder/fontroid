import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# import django
# django.setup()

# from pathlib import Path
# print(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# BASE_PATH = Path(__file__).resolve().parent.parent
# print(BASE_PATH)

# PARENT_PATH = Path(__file__).resolve().parent.parent


root = "./"
module = "makefontapp/tools/handwritten_split_256.py"
command = os.path.abspath(os.path.join(root,module))
print(command)
image_url = 'C:\\Users\\jangyunsik\\Downloads\\fontgan\\fontgan\\media\\uploads\\userwords\\pseojung1124@naver.com\\22-11-30-14-36\\handwritten_SH.jpg'
out_dir = 'C:\\Users\\jangyunsik\\Downloads\\fontgan\\fontgan\\media\\uploads\\userwords\\pseojung1124@naver.com\\22-11-30-14-36\\handwritten_SH'
terminal_command = f"python {command} {image_url} {out_dir}"
os.system(terminal_command)

module = "makefontapp/tools/handwritten_preprocessing_256.py"
command = os.path.abspath(os.path.join(root,module))        
input_dir = out_dir
out_dir = os.path.join(os.path.dirname(image_url), f'preprocessed_handwritten_SH')

print("***스플릿 이미지 전처리 시작***")
terminal_command = f"python {command} {input_dir} {out_dir}"
os.system(terminal_command)
print("***스플릿 이미지 전처리 끝***")

module = "makefontapp/tools/handwritten_inverse.py"
command = os.path.abspath(os.path.join(root,module))        
input_dir = out_dir
out_dir = os.path.join(os.path.dirname(image_url), f'inverse_handwritten_SH')

print("***스플릿 이미지 inverse 시작***")
terminal_command = f"python {command} {input_dir} {out_dir}"
os.system(terminal_command)
print("***스플릿 이미지 inverse 끝***")