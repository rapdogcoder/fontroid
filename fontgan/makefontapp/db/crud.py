#parameters and have better type checks and completion in your functions.

#Import model (the SQLAlchemy model) and schemas (the Pydantic model / schemas).

#Read a single user by ID and by email.
#Read multiple users.
#Read multiple items.

from sqlalchemy.orm import Session
from . import model, schemas
from ..models import Images


def get_user(db: Session, user_id: int):
    return db.query(model.User).filter(model.User.id == user_id).first()

def get_user_items(db: Session, user_id: int):
    return db.query(model.User).filter(model.User.id == user_id).first().items

def get_user_by_email(db: Session, email: str):
    return db.query(model.User).filter(model.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = model.User(email=user.email, hashed_password=fake_hashed_password, is_active = True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Item).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = model.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

#이미지 저장 함수, 파일 이름은 db

        # files = request.FILES.getlist('file')
        # for file in files:
        #     image = Images()
        #     print(file)
        #     image.attached=file
        #     image.save()

def save_image(file, email):
    image = Images()
    image.owner_id = email
    image.attached= file
    image.save()

    return image