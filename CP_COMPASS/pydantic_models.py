from typing import Optional
from pydantic import BaseModel, EmailStr



class signup_User(BaseModel):
    # id: int
    email: EmailStr
    password: str
    phone: str
    country_code: str
    is_activated: bool = True  # should automatically activate account after successful signup to skip sending otp for now
    first_name: str
    last_name: str
    profile_photo: str = ""
    middle_name: str = ""
    country: str = ""
    state: str = ""


class signin_User(BaseModel):
    email: EmailStr
    password:  str


class get_User(BaseModel):
    email: EmailStr


class wallet_model(BaseModel):
    email: EmailStr
    balance: float = 00.00
    currency: str = "NGN"


class withdraw_model(BaseModel):
    email: EmailStr
    amount: float


class deposit_model(BaseModel):
    email: EmailStr
    amount: float
