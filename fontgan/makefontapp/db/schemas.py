from typing import List, Union

from pydantic import BaseModel

#데이터를 만들거나 읽는 동안 공통 속성을 갖도록 ItemBase 및 UserBase Pydantic 모델(또는 "schema"라고 합니다)을 만듭니다. 
# 그리고 이들로부터 상속되는 ItemCreate 및 UserCreate를 생성하고(같은 속성을 갖도록) 생성에 필요한 추가 데이터(속성)를 생성합니다. 
# 그래서, 사용자는 그것을 만들 때 비밀번호도 갖게 될 것입니다. 그러나 보안을 위해 암호는 다른 파이단틱 모델에는 없을 것이며, 예를 들어 사용자를 읽을 때 API에서 전송되지 않을 것이다.

# api에서 데이터를 읽을 때, 반환할 때 사용할 스키마를 만듬.


class ItemBase(BaseModel):  
    title: str
    flag : int
    image_url: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int    
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True