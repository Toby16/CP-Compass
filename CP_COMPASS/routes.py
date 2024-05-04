from CP_COMPASS import app
#import CP_COMPASS
from fastapi import status, Depends, HTTPException
from CP_COMPASS.models import User
from CP_COMPASS.helper import email_validator
from CP_COMPASS.pydantic_models import signup_User, signin_User, get_User
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/login", status_code=status.HTTP_200_OK)
@app.post("/login/", status_code=status.HTTP_200_OK)
def sign_in(data: signin_User, db: db_dependency):
    """
    Endpoint to sign-in users
    {
        "email": "test@example.com",
        "password": "testpassword"
    }
    """
    # validate and normalize email
    data.email = email_validator(data.email)
    data = data.dict()

    check_user = db.query(User).filter(User.email == data["email"]).first()

    if check_user is None:
        raise HTTPException(status_code=400, detail="invalid email or password!")

    if check_user.password != data["password"]:
        raise HTTPException(status_code=400, detail="invalid email or password!")
    else:
        return {
            "statusCode": 200,
            "message": "login successful!",
            "email": check_user.email
        }



@app.post("/signup", status_code=status.HTTP_201_CREATED)
@app.post("/signup/", status_code=status.HTTP_201_CREATED)
def sign_up(data: signup_User, db: db_dependency):
    """
    Endpoint to sign-up users
    """
    # validate and normalize email
    data.email = email_validator(data.email)
 

    # skip otp
    # data.activated defaults to True
    # check if user exists
    check_user = db.query(User).filter(User.email == data.email).first()
    if check_user is not None:
        raise HTTPException(status_code=400, detail="User already esists")


    # store t0 db
    data = data.dict()
    new_user = User(
        email=data["email"],
        password=data["password"],
        phone=data["phone"],
        country_code=data["country_code"],
        is_activated=data["is_activated"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        middle_name=data["middle_name"],
        profile_photo=data["profile_photo"],
        country=data["country"],
        state=data["state"]
    )

    db.add(new_user)
    db.commit()
    return {
        "statusCode": 201,
        "message": "Account created successfully!"
    }, 201



@app.post("/get_user", status_code=status.HTTP_200_OK)
@app.post("/get_user/", status_code=status.HTTP_200_OK)
def get_user(data: get_User, db: db_dependency):
    """
    Endpoint to return details of a user
    """
    # validate email
    data.email = email_validator(data.email)


    # return data.email
    check_user = db.query(User).filter(User.email == data.email).first()
    if check_user is None:
        raise HTTPException(status_code=404, detail="User not found!")

    user_dict = {}
    user_dict["email"] = check_user.email
    user_dict["phone"] = check_user.phone
    user_dict["first_name"] = check_user.first_name
    user_dict["last_name"] = check_user.last_name
    user_dict["middle_name"] = check_user.middle_name
    user_dict["country_code"] = check_user.country_code
    user_dict["country"] = check_user.country
    user_dict["state"] = check_user.state
    user_dict["profile_photo"] = check_user.profile_photo
    
    #del check_user["password"]
    return {
        "statusCode": 200,
        "message": "success!",
        "data": user_dict
    }
