from fastapi import FastAPI
from numpy import append

app = FastAPI()

@app.get("/")
def get_tiles():
    return {"Hello": "World"}

@app.put("/")
def put_tile():
    return {"Gomu Gomu no mi": "Elephant Gun"}
