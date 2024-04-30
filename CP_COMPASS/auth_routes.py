from CP_COMPASS import app


@app.get("/login")
@app.get("/login/")
def sign_in():
    """
    Endpoint to sign-in users
    """
    return {
        "statusCode": 200,
        "message": "Login Page - successful!"
    }


@app.get("/signup")
@app.get("/signup/")
def sign_up():
    """
    Endpoint to sign-in users
    """
    return {
        "statusCode": 200,
        "message": "Sign-Up Page - Successful!"
    }
