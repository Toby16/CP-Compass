from CP_COMPASS import app
from CP_COMPASS.models import User
from email_validator import validate_email, EmailNotValidError


@app.get("/login")
@app.get("/login/")
def sign_in():
    """
    Endpoint to sign-in users
    {
        "email": "test@example.com",
        "password": "testpassword"
    }
    """
    return {
        "statusCode": 200,
        "message": "Login Page - successful!"
    }


@app.post("/signup")
@app.post("/signup/")
def sign_up(data: User):
    """
    Endpoint to sign-in users


    {
        "id": 1
        "first_name": "test",
        "last_name": "user",
        "email": "test@example.com",
        "phone_number": 08012356789,
        "country_code": 234,
        "password": "testpassword"
    }
    """

    # validate email
    try:
        emailinfo = validate_email(data.email, check_deliverability=False)
        data.email = emailinfo.normalized  # using normalized email version | [ stored in DB ]
    except EmailNotValidError as e:
        return {
                "statusCode": 400,
                "error": str(e)
        }
    except Exception as e:
        raise

    # skip otp
    # data.activated defaults to True
    # Next, saving data to db/fle storage
    return {
        "statusCode": 200,
        "data.email": data.email,
        "message": "Sign-Up Page - Successful!",
        "data": data
    }
