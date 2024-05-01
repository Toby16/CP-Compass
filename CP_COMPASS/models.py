from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    email: EmailStr
    password: str
    phone_number: int
    country_code: int
    activated: bool = True  # should automatically activate account after successful signup to skip sending otp for now
    first_name: str
    last_name: str
