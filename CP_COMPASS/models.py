from sqlalchemy import (
    Boolean, Column, Integer,
    String, Text, Float, ForeignKey
)
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(121), unique=True, index=True)
    password = Column(String(200))
    phone = Column(String(30))
    country_code = Column(String(10))
    is_activated = Column(Boolean)
    first_name = Column(String(41))
    last_name = Column(String(41))
    middle_name = Column(String(41))
    profile_photo = Column(Text)
    country = Column(String(81))
    state = Column(String(81))


class BankInfo(Base):
    __tablename__ = "bankinfo"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)  # foreign key for User.id
    bank_code = Column(String(21))
    account_number = Column(String(51))
    account_name = Column(String(51))
    status = Column(String(21))
    bank_name = Column(String(201))


class Wallet(Base):
    __tablename__ = "wallet"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(121), unique=True, index=True)
    currency = Column(String(10))
    balance = Column(Float)
