from http.client import HTTPResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from pydantic import BaseModel
import os
import sys

from .db.database import get_db
from .db.schemas import UserBase,UserCreate,ItemCreate
from .db.crud import create_user, create_user_item, save_image, get_user_by_email, get_user, get_user_items

import requests,json
import smtplib
from email.mime.text import MIMEText

import glob


root = "./"


def index(request):
    # if request.method == "GET":
    return render(request, 'makefontapp/index_proto.html')

@csrf_exempt
def howtouse(request):
    print(request)
    if request.method == "POST":

        now = datetime.now()
        print(now)
        db_gen = get_db()
        db = next(db_gen)
        db_user = get_user_by_email(db, request.POST['email'])
        
        
        #db 유저 생성
        if db_user == None:
            user = UserCreate(email = request.POST['email'], password = request.POST['password'])
            db_user = create_user(db, user)
        print(db_user)

        #이미지 저장
        image = save_image(request.FILES['file'], db_user.email)
        print(type(image.attached))
        item = ItemCreate(
            flag = 0,
            image_url = image.attached.path,
            title = f' #{db_user.id}_{db_user.email} {now.strftime("%Y-%m-%d %H:%M:%S")}'
        )
        print(item)
        #db에 아이템 생성 
        db_item = create_user_item(db, item, db_user.id)
        print(db_item.image_url)
        
        print(db_item)
        #데이터 전처리 데이터 오퍼레이터 준비
                
        module = "makefontapp/tools/handwritten_split_256.py"
        command = os.path.abspath(os.path.join(root,module))
        out_dir = os.path.join(os.path.dirname(db_item.image_url), f'handwritten_{db_user.email}')
        terminal_command = f"python {command} {db_item.image_url} {out_dir}"
        
        print("***템플릿 이미지 스플릿 시작***")
        os.system(terminal_command)
        print("***템플릿 이미지 스플릿 종료***")


        
        module = "makefontapp/tools/handwritten_preprocessing_256.py"
        command = os.path.abspath(os.path.join(root,module))        
        input_dir = out_dir
        out_dir = os.path.join(os.path.dirname(db_item.image_url), f'preprocessed_{db_user.email}')
        terminal_command = f"python {command} {input_dir} {out_dir}"

        print("***스플릿 이미지 전처리 시작***")        
        os.system(terminal_command)
        print("***스플릿 이미지 전처리 끝***")

        module = "makefontapp/tools/handwritten_inverse.py"
        command = os.path.abspath(os.path.join(root,module))        
        input_dir = out_dir
        out_dir = os.path.join(os.path.dirname(db_item.image_url), f'inverse_{db_user.email}')
        terminal_command = f"python {command} {input_dir} {out_dir}"
        
        print("***스플릿 이미지 inverse 시작***")        
        os.system(terminal_command)
        print("***스플릿 이미지 inverse 끝***")
        
        #http 요청을 줄 경우 return이 올 때까지 대기해야함.
        db.close()
        url = f"http://127.0.0.1:8001/train/{db_user.id}"
        data = {'user_id' : db_user.id}
        try :
            post = requests.post(url,data=data,timeout=1)
            print(post)
        finally:
            print(f"송신 완료")
            return redirect('/')
        

    return render(request,'makefontapp/HowToUse.html')

@csrf_exempt
def feedback(request, user_id, date):




    db_gen = get_db()
    db = next(db_gen)
    db_user = get_user(db,user_id) 
    #폰트 만들기
    user_id = db_user.id

    items = get_user_items(db, user_id)
    items = [item for item in items if os.path.dirname(item.image_url)[-14:] == date]
        
    item_dir = os.path.join(os.path.dirname(items[0].image_url),f"result_{db_user.email}")


    font_path = os.path.join(os.path.dirname(item_dir),'*.ttf')

    font_path = glob.glob(font_path)[0].split("userwords\\")[-1].replace("\\","/")
    print(font_path)
    

    print(font_path)
    
    db.close()

    if request.method == "POST": 
        db_gen = get_db()
        db = next(db_gen)      

         
        print("POST")
        file = request.FILES['char_img0']
        print(file)
        image = save_image(request.FILES['char_img0'], db_user.email)
        now = datetime.now()        
        print(type(image.attached))
        item = ItemCreate(
            flag = 0,
            image_url = image.attached.path,
            title = f' #{db_user.id}_{db_user.email} {now.strftime("%Y-%m-%d %H:%M:%S")}'
        )        
        db.close()

    return render(request,'makefontapp/feedback_page.html', {'font_path': font_path})

def detail(request):
    if request.method == "GET":
        return render(request, 'makefontapp/Detail.html')

def aboutus(request):
    if request.method == "GET":
        return render(request, 'makefontapp/AboutUs.html')

def contact(request):
    if request.method == "POST":
        uname = request.POST['uname']
        phone_number = request.POST['phone_number1']+'-'+request.POST['phone_number2']+'-'+request.POST['phone_number3']
        email = request.POST['email']
        content = request.POST['content']
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # TLS 보안 시작
        s.starttls()
        # 로그인 인증
        s.login('ksglm1231@gmail.com', 'bwbebfzslisjytgc')
        # 보낼 메시지 설정
        
        msg['Subject'] = f'제목 : {uname}님의 문의 메일입니다.'
        # 메일 보내기
        s.sendmail("ksglm1231@gmail.com", "ksglm1231@gmail.com", msg.as_string())
        # 세션 종료
        s.quit()
    return render(request, 'makefontapp/Contact.html')