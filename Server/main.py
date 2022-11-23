from pstats import Stats
import re
from fastapi import FastAPI, Request
from numpy import append
from Server.db.db import db

app = FastAPI()

@app.get("/")
def get_tiles():
    return {"Hello": "World"}

@app.put("/")
def put_tile(request : Request):
    print(request.client.host)
    db.Place.find_one_and_update({"_id": {"x":0, "y":0}},{'$set': {"color": 0x001110}})
    db.Place.insert_one({
        "_id": {"x": 4, "y": 4},
        "color": 0xFF0000
    })
    return {"Gomu Gomu no mi": "Elephant Gun"}

@app.post('/my-endpoint')
async def my_endpoint(request: Request):
    x = 'x-forwarded-for'.encode('utf-8')
    print(request.headers.raw)
    for header in request.headers.raw:
        if header[0] == x:
            print("Find out the forwarded-for ip address")
            origin_ip, forward_ip = re.split(', ', header[1].decode('utf-8'))
            print(f"origin_ip:\t{origin_ip}")
            print(f"forward_ip:\t{forward_ip}")
    return {'status': 1, 'message': 'ok'}
