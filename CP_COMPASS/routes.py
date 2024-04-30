from CP_COMPASS import app


@app.get("/")
def index():
    return {
        "statusCode": 200,
        "message": "successful!"
    }
