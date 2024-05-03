from fastapi import FastAPI


app = FastAPI()


from CP_COMPASS import models
from database import engine
models.Base.metadata.create_all(bind=engine)

from CP_COMPASS import routes, pydantic_models


