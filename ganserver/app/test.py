# import sys
# import os


# user_id = 'SH'

# with open('../model/assets/source/script.sh', 'r') as rf:
#     with open(f'../model/assets/source/{user_id}.sh', 'w') as wf:
#         script = rf.read()
#         wf.write(script.replace('uid',user_id))

# os.system(f'sh ../model/assets/source/{user_id}.sh')

# '''
# # making training set
# python ./tools/src-font-image-generator.py --label-file labels/210.txt
# python ./tools/trg-skeleton-image-generator.py --font-image-dir inversed_SH --output-dir skeleton_SH
# python ./tools/combine_images.py --input_dir src-image-data/images --b_dir inversed_SH --c_dir skeleton_SH/images --operation combine --label-file 210.txt --output-dir combined_SH
# python ./tools/images-to-tfrecords.py --image-dir combined_SH/images --output-dir train-tfrecords_SH

# # training
# python main.py --mode train --max_epochs 300 --input_dir tfrecords_SH --output_dir trained_model_SH
# # python main.py --mode train --output_dir finetuned_model_SH --max_epochs 500 --checkpoint trained_model_SH/ 

# # export 2350 hangul 
# python main.py --mode test --output_dir result_SH --checkpoint trained_model_SH
# python split.py result_SH
# '''

# from tensorflow.python.client import device_lib
# print(device_lib.list_local_devices())

# from db import crud, models, schemas
# from db.database import SessionLocal, engine, get_db

# db = next(get_db())
# items = crud.get_items(db)


# import smtplib
# from email.mime.text import MIMEText
# import os

# s = smtplib.SMTP('smtp.gmail.com',587)
# s.starttls()
# s.login('sbgt40766@gmail.com','znqfplailzcjlgah')

# manager = "sbgt40766@gmail.com"
# s.quit()
# s = smtplib.SMTP('smtp.gmail.com',587)
# s.starttls()
# s.login('sbgt40766@gmail.com','znqfplailzcjlgah')
# s.quit()
# msg = MIMEText('내용 : 본문내용 테스트입니다.')
# msg['Subject'] = '제목 : 메일 보내기 테스트입니다.'
# msg['To'] = user
# s.sendmail(f"{manager}", f"{user}", msg.as_string())
# s.quit()

# user = crud.get_user_by_email(db,manager)
# user_id = user.id
# for item in user.items:
#     parent_dir = os.path.dirname(item.image_url)[-14:]
#     print(parent_dir)
#     feedback_url = f"http://127.0.0.1:8000/feedback/{user_id}/{parent_dir}"
#     msg = MIMEText(f'학습이 완료되었습니다./n/n {feedback_url} /n 위 url을 통해 여러분이 낳은 폰트를 다운로드하세요.')
#     msg['Subject'] = '폰트 서비스 베타버전을 이용해주셔서 감사합니다. 학습이 완료 되었습니다.'
#     msg['To'] = user.email
#     s.sendmail(f"{manager}", f"{user.email}", msg.as_string()) 
import os
module = "model/assets/source/tools/make_font.py"
user_id = "6"
output = "C:/Users/user/Desktop/myproject/fontgan/media/uploads/userwords/sbgt40766@gmail.com/22-12-03-11-10"
item_dir = os.path.join(output,f"result_sbgt40766@gmail.com")
command = f"python {module} {user_id} {item_dir} {output}"
os.system(command)