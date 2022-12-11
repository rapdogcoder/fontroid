from django.template import engine
from sqlalchemy.orm import Session
from database import engine,get_db
from model import User


db_gen = get_db()
db = next(db_gen)

tom = User(email="gt40766@naver.com", hashed_password="gtsb01098@",is_active=False)

db.add(tom)
db.commit()
db.close()