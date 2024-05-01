from fastapi import FastAPI


app = FastAPI()

from CP_COMPASS import routes, auth_routes, models
