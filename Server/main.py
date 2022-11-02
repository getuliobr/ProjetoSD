from fastapi import FastAPI
from numpy import append

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

