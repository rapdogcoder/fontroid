# coding: utf-8
from sqlalchemy import BigInteger, Boolean, CheckConstraint, Column, DateTime, ForeignKey, Integer, SmallInteger, String, Text, UniqueConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .database import Base

class MakefontappImage(Base):
    __tablename__ = 'makefontapp_images'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('makefontapp_images_id_seq'::regclass)"))
    attached = Column(String(100), nullable=False)
    postdate = Column(DateTime(True), nullable=False)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('users_id_seq'::regclass)"))
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean)
    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('images_id_seq'::regclass)"))
    title = Column(String, index=True)
    image_url = Column(String, index=True)
    owner_id = Column(ForeignKey('users.id'))
    flag = Column(Integer)
    
    owner = relationship('User',back_populates="items")

