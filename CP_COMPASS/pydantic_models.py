from typing import Optional
from pydantic import BaseModel, EmailStr



class signup_User(BaseModel):
    # id: int
    email: EmailStr
    password: str
    phone: str
    country_code: str
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


class update_user_model(BaseModel):
    email: EmailStr
    phone: Optional[str] = None
    country_code: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    profile_photo: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
