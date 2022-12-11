from typing import List

from fastapi import Depends, FastAPI, HTTPException
# from fastapi_sqlalchemy import db
from sqlalchemy.orm import Session

from .db import crud, models, schemas
from .db.database import SessionLocal, engine, get_db
import smtplib
from email.mime.text import MIMEText

import os
import sys
from pathlib import Path
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency


manager = "sbgt40766@gmail.com"

@app.get("/")
def print_hi():

    return "font server 입니다."


#웹서버에게 get 요청이 왔을 때.. 혹은 주기적으로 db를 확인한다..
@app.post("/train/{user_id}")
def train(user_id: int, db :Session = Depends(get_db)):


    db_user = crud.get_user(db,user_id= user_id)
    print(f"DB 유저 접근 {db_user.email}")
    # 유저가 없거나 서비스 이용 중이 아닐 때
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.is_active is False:
        return "user is no active"
    
    for item in db_user.items:
        user_email = db_user.email

        s = smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        s.login('sbgt40766@gmail.com','znqfplailzcjlgah')
        msg = MIMEText('저희 서비스를 이용해주셔서 감사합니다. \n 예상 소요시간은 약 10시간 입니다.')
        msg['Subject'] = '폰트 서비스 베타버전을 이용해주셔서 감사합니다.'
        msg['To'] = user_email
        s.sendmail(f"{manager}", f"{user_email}", msg.as_string())     
        s.quit()
        #flag가 0일 때는 전처리를 해야함.
        if item.flag == 0:

            
            print(item.title)
            module = 'model/assets/source/tools/src-font-image-generator.py'
            label_file = "model/assets/data/labels"
            trg_input = 'model/assets/data/trg_font'
            src_input = "model/assets/data/src_font"
            output = os.path.dirname(item.image_url)
            command = f"python {module} --label-file {os.path.join(label_file,'210.txt')} --target-font-dir {trg_input} --src-font-dir {src_input} --output-dir {output}"
            
            print("소스폰트 이미지 생성 중")
            os.system(command)
            print(f"{output} 소스폰트 이미지 생성 끝")

            module = 'model/assets/source/tools/trg-skeleton-image-generator.py'
            label_file = os.path.join(label_file,'256-common-hangul.txt')

            dir_input = os.path.join(output,f"inverse_{user_email}")
            print(dir_input)
            dir_output = os.path.join(output,f"skeleton_{user_email}")
            command = f"python {module} --font-image-dir {dir_input} --output-dir {dir_output}"
            
            print("타겟 스켈레톤 이미지 생성 중")
            os.system(command)
            print(f"{dir_output} 타겟 스켈레톤 이미지 생성 끝")

            module = 'model/assets/source/tools/combine_images.py'
            
            command = f"python {module} --input_dir {output}/images --b_dir {dir_input} --c_dir {dir_output}/images --operation combine --label-file {os.path.join(label_file,'210.txt')} --output-dir {os.path.join(output,f'combined_{user_email}')}"
            
            print("이미지 combine 중")
            os.system(command)
            print(f"{os.path.join(output,'combined_SH')} 이미지 combine 생성 끝")

            module = 'model/assets/source/tools/images-to-tfrecords.py'
            combine_dir = os.path.join(output,f'combined_{user_email}/images')
            tf_dir = os.path.join(output,f'train-tfrecords_{user_email}')
            
            command = f"python {module} --image-dir {combine_dir} --output-dir {tf_dir} "
            
            try:
                print("학습 데이터 생성")
                os.system(command)
                
            except:
                print("학습 데이터 생성 실패")
                continue
            print(f"{tf_dir} 학습 데이터 생성 완료")
            item.flag = 1
        if item.flag == 1:
            
            output = os.path.dirname(item.image_url)
            tf_dir = os.path.join(output,f'train-tfrecords_{user_email}')
            train_path = os.path.join(output,f'trained_model_{user_email}')
            # training
            module = 'model/assets/source/main.py'
            max_epochs = 300         
            # python main.py --mode train --max_epochs 300 --input_dir tfrecords_SH --output_dir trained_model_SH
            command = f"python {module} --mode train --max_epochs {max_epochs} --input_dir {tf_dir} --output_dir {train_path}"
            os.system(command)
            # python main.py --mode train --output_dir finetuned_model_SH --max_epochs 500 --checkpoint trained_model_SH/ 
            try:
                print("사용자 폰트 이미지 학습 시작")
                os.system(command)
                
            except:
                print("사용자 폰트 이미지 학습 실패")
                continue 
            print("사용자 폰트 이미지 학습 완료")        
            item.flag = 2
        if item.flag == 2:
            # export 2350 hangul
            # python main.py --mode test --output_dir result_SH --checkpoint trained_model_SH
            module = 'model/assets/source/main.py'
            output = os.path.dirname(item.image_url)
            result_dir = os.path.join(output,f'result_{user_email}')
            train_path = os.path.join(output,f'trained_model_{user_email}')
            command = f"python {module} --mode test --output_dir {result_dir} --checkpoint {train_path}"
            try:
                print("사용자 폰트 이미지 생성 중")
                os.system(command)
                
            except:
                print("사용자 폰트 이미지 생성 실패")
                continue
            print("사용자 폰트 이미지 생성 완료")  
            item.flag= 3
            #python split.py result_SH
            module = 'model/assets/source/split.py'

            command = f"python {module} {result_dir}"

            try :
                print("생성 이미지 이동중")
                os.system(command)
            except:
                print("생성 이미지 이동 실패")
                continue              
            
            print("생성 이미지 이동 완료")

            #폰트 만들기

            module = "model/assets/source/tools/make_font.py"
            user_id = db_user.id
            item_dir = os.path.join(output,f"result_{db_user.email}")
            command = f"python {module} {user_id} {item_dir} {output}"

            print("폰트를 생성합니다.")
            os.system(command)
        
            s = smtplib.SMTP('smtp.gmail.com',587)
            s.starttls()    
            s.login('sbgt40766@gmail.com','znqfplailzcjlgah')

            parent_dir = os.path.dirname(item.image_url)[-14:]
            feedback_url = f"http://127.0.0.1:8000/feedback/{user_id}/{parent_dir}"
            msg = MIMEText(f'학습이 완료되었습니다.\n {feedback_url} \n 위 url을 통해 여러분이 낳은 폰트를 다운로드하세요.')
            msg['Subject'] = '폰트 서비스 베타버전을 이용해주셔서 감사합니다. 학습이 완료 되었습니다.'
            msg['To'] = user_email
            s.sendmail(f"{manager}", f"{user_email}", msg.as_string())
            s.quit()
            

            
        db.commit()
        
        


# django로 이전
# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email= user.email)
#     if db_user :
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db , email=user.email)

# @app.get("/users/", response_model=List[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users

# @app.get("/users/{user_id}/", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id= user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item:schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id= user_id)

# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit= limit)
#     return items

