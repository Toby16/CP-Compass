from CP_COMPASS import app
#import CP_COMPASS
from fastapi import status, Depends, HTTPException
from CP_COMPASS.models import User, Wallet
from CP_COMPASS.helper import email_validator
from CP_COMPASS.pydantic_models import (
    signup_User, signin_User,
    get_User, wallet_model,
    withdraw_model, deposit_model
)
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




# [ AUTH ]

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
def sign_up(data: signup_User, db: db_dependency, wallet_data=wallet_model):
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

    # initialize user wallet
    new_wallet = Wallet(
        email=data["email"],
        currency="NGN",
        balance=00.00
    )
    db.add(new_wallet)

    db.commit()
    return {
        "statusCode": 201,
        "message": "Account created successfully!"
    }, 201





#  [ Profile ]

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




#  [ Wallet ]
@app.post("/get_wallet", status_code=status.HTTP_200_OK)
@app.post("/get_wallet/", status_code=status.HTTP_200_OK)
def get_wallet(data: get_User, db: db_dependency):
    """
    return wallet details of a user
    """
    # validate email
    data.email = email_validator(data.email)

    details_ = db.query(Wallet).filter(Wallet.email == data.email).first()

    if details_ is None:
        raise HTTPException(status_code=404, detail="User not found!")

    wallet_details = {}
    wallet_details["currency"] = details_.currency
    wallet_details["balance"] = details_.balance

    return {
        "statusCode": 200,
        "message": "success!",
        "wallet_details": wallet_details
    }


@app.post("/withdrawal", status_code=status.HTTP_200_OK)
@app.post("/withdrawal/", status_code=status.HTTP_200_OK)
def withdraw(data: withdraw_model, db: db_dependency):
    """
    withdraw from wallet balance
    """
    # validate email
    data.email = email_validator(data.email)
    wallet_details = db.query(Wallet).filter(Wallet.email == data.email).first()
    if wallet_details is None:
        raise HTTPException(status_code=404, detail="User not found!")

    # check withdrawal request
    if data.amount <= 0:
        return {
            "statusCode": 400,
            "error": "Invalid withdrawal amount!"
        }

    # check is withdrawal amount > wallet balance
    if data.amount >= wallet_details.balance:
        return {
            "statusCode": 400,
            "error": "insufficent balance!"
        }

    # withdraw successfully
    wallet_details.balance -= data.amount
    db.commit()


    return {
        "statusCode": 200,
        "message": "successful!",
        "details": {
            "withdrawal": data.amount,
            "balance": wallet_details.balance
        }
    }


@app.post("/deposit", status_code=status.HTTP_200_OK)
@app.post("/deposit/", status_code=status.HTTP_200_OK)
def deposit(data: deposit_model, db: db_dependency):
    """
    deposit amount into wallet
    """
    # validate email
    data.email = email_validator(data.email)
    wallet_details = db.query(Wallet).filter(Wallet.email == data.email).first()
    if wallet_details is None:
        raise HTTPException(status_code=404, detail="User not found!")

    # validate deposit amount
    if data.amount <= 0:
        return {
            "statusCode": 400,
            "error": "Invalid deposit amount!"
        }

    wallet_details.balance += data.amount
    db.commit()

    return {
        "statusCode": 200,
        "message": "successful!",
        "details": {
            "deposit": data.amount,
            "balance": wallet_details.balance
        }
    }
