# fontroid
2022 오픈소프트웨어 텀프로젝트
# fontroid
2022 오픈소프트웨어 텀프로젝트

<img width="1299" alt="img" src="https://user-images.githubusercontent.com/88870857/206910793-13c5453b-9337-4613-8cf8-c00a89282995.png">

# 서비스 개요

한글은 28자의 글자를 조합하여 11,172자를 생성할 수 있다.
초성(19) * 중성(21) * 종성(28) = 11,172 자
이 중 상용 글자는 2350자
폰트 디자이너는 아래와 같이 수작업으로 폰트를 제작함.

![img (1)](https://user-images.githubusercontent.com/88870857/206910830-282a48c5-13f9-48c8-8504-b50b85c71360.png)

때문에 폰트를 제작하는 필요한 비용은 생각보다 높음.

<img width="603" alt="img (2)" src="https://user-images.githubusercontent.com/88870857/206910940-32798fa7-b27c-48dd-9d66-0fd763058be2.png">

# 시연 영상

1
https://user-images.githubusercontent.com/88870857/206912695-09aa5b47-677a-4e09-8b98-62d3e64e7643.mp4

2
https://user-images.githubusercontent.com/88870857/206912736-e64f135f-344e-41d3-a2bd-73a2054797ee.mp


# 모델

이미지 생성 모델 고려, gan과 diffusion 고려.
gan 기반 이미지 변환 모델인 pix2pix로 선정. 이미지의 스타일을 바꾸어줄 수 있음. (소스 이미지를 타겟 이미지로)
(고딕체 -> 학습 모델 -> 손글씨)

낮 사진 ---> 밤 사진

<img width="546" alt="img (3)" src="https://user-images.githubusercontent.com/88870857/206910999-f4fb9a05-cd29-4fa1-924b-207cdfa1b20b.png">

위성 사진 --> 지도 사진

<img width="733" alt="img (4)" src="https://user-images.githubusercontent.com/88870857/206911154-f3230101-c59d-498c-b83d-c285871548ab.png">

모델 구조

![img (5)](https://user-images.githubusercontent.com/88870857/206911180-4f294b81-9b46-4a42-91cb-352179db6d7a.png)

해당 모델 참고 url
https://github.com/jeina7/GAN-handwriting-styler﻿

사전 학습 (고딕체 (소스 이미지), 다양한 폰트 (타겟 이미지))
![img (6)](https://user-images.githubusercontent.com/88870857/206911228-d6ee72f8-e819-478e-bf90-a12d2233ead9.png)

210자 템플릿 작성 후 전이 학습(고딕체 (소스 이미지), 손글씨 이미지)
![img](https://user-images.githubusercontent.com/88870857/206911247-b51ef006-0232-45c8-8225-cc238f965bf2.jpg)

opencv를 통해 라인 감지, crop, resize 과정을 거침.
![img (7)](https://user-images.githubusercontent.com/88870857/206911266-f2c50e07-4d19-4bb8-a548-97228923d5fa.png)

아래와 같은 이미지 210자 생성
![img (8)](https://user-images.githubusercontent.com/88870857/206911278-496ebc99-a19c-43b6-8d27-eb08c5b97645.png)

학습 결과 ) 코랩으로 다양한 테스트 결과 성능이 좋지 않음. (loss funtion, normalization,epoch 수 변경 등)
![img (9)](https://user-images.githubusercontent.com/88870857/206911410-3f6ee7cd-2faf-4ab9-8a48-acda8051986f.png)

생성 결과
![img (10)](https://user-images.githubusercontent.com/88870857/206911478-c5925bc1-b438-4016-b131-92110d194ac5.png)

결론! 모델 변경.
위 pix2pix 모델에서 골격을 추가적으로 학습할 수 있는 구조를 가진 SKFont 사용
![img (11)](https://user-images.githubusercontent.com/88870857/206911509-e30cf1d1-d230-46c3-a426-51067cd9eb5f.png)

아래 모델을 참고
https://github.com/ammar-deep/SKFont﻿

전처리를 통해 crop, resize, inverse (글자의 스켈레톤을 뽑아내기 위함.)
![img (12)](https://user-images.githubusercontent.com/88870857/206911781-90bb30b6-ba7f-4893-a7e7-a3b60694560b.png)

스켈레톤 추출
![img (13)](https://user-images.githubusercontent.com/88870857/206911798-af390362-90fb-46b4-bf52-5829905d6786.png)

소스 이미지, 타겟 이미지, 스켈레톤 이미지을 combine해서 학습 데이터 셋 구성
![img (14)](https://user-images.githubusercontent.com/88870857/206911809-de47a13c-4d2a-46f5-a70f-5832f951b1c9.png)

바이너리 파일로 바꾸어 학습 가속.
![img (15)](https://user-images.githubusercontent.com/88870857/206911826-452d817e-45c7-4ba1-a981-eec68d9e1003.png)

모델 학습 완료되면 2350 글자 생성.
기존 모델과 결과 비교
![img (16)](https://user-images.githubusercontent.com/88870857/206911867-8e5c1215-386f-4c2b-bbe5-fbb8916e85de.png)

# 머신러닝 웹 애플리케이션


머신러닝 애플리케이션 개발자가 되기 위해서.
데이터 파이프라인 고찰 
두개의 서버가 각자의 전처리를 수행하고 유저 인터페이스를 제공하는 웹 서버와 학습을 수행하는 모델 서버를 구성.
![img (17)](https://user-images.githubusercontent.com/88870857/206911899-342b1d91-f6fa-4db8-9a91-f5fd64036c2c.png)

web server - conda, python 3.6.13, django, cv2, PIL, glob

model server - conda, python 3.6.13, fastapi, tensorflow-gpu (cuda10, cudnn7,64..)

# web server 구조
![img (18)](https://user-images.githubusercontent.com/88870857/206911928-60e6e3e4-a000-47ad-b42e-fcc477a68fb5.png)

# model server 구조
![img (19)](https://user-images.githubusercontent.com/88870857/206911943-98a0fc41-bd10-4c48-b39a-c92e7fead163.png)

# db 구조 (postgreSQL)
![img (20)](https://user-images.githubusercontent.com/88870857/206911956-baef5557-a688-48c7-9b8b-6332b207cca7.png)


