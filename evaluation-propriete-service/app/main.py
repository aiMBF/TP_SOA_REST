from fastapi import FastAPI
from api import evaluation


app = FastAPI()

app.include_router(evaluation.router)



