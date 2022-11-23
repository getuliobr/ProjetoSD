from pstats import Stats
import re, time
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from numpy import append
from pydantic import BaseModel
from pydantic.color import Color
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pymongo import ReturnDocument

from Server.db.db import db, DuplicatedKeyException

app = FastAPI()
UserCollection = db.Users
PlaceCollection = db.Place

COOLDOWN = 0
class User(BaseModel):
    ip: str
    time_from_last_tile: float

class Tile(BaseModel):
    x: int
    y: int
    color: Color
    ip: Optional[str]

def putTileOnDb(user: User, tile: Tile, currTime):
    userDb = UserCollection.find_one_and_update({
            'ip': user.ip,
            'time_from_last_tile': {
                '$lte': currTime - COOLDOWN
            }
        }, {
            '$set': jsonable_encoder(user)
        }, upsert=True, return_document=ReturnDocument.AFTER)

    if not userDb:
        raise HTTPException(status_code=400, content={'success': False, "message": "You can't put a tile so fast"})
    
    color = tile.color

    if tile.x < 0 and tile.x >= 1000 or tile.y < 0 and tile.y >= 1000:
        raise HTTPException(status_code=400, content={'success': False, "message": "Out of bounds"})

    tile = PlaceCollection.find_one_and_update({
        'x': tile.x,
        'y': tile.y
    }, {
        '$set': jsonable_encoder(tile)
    }, upsert=True, return_document=ReturnDocument.AFTER)

    del tile['_id']
    del tile['ip']
    return tile


@app.get("/")
def get_tiles():
    return {"Hello": "World"}

@app.post("/")
def put_tile(tile: Tile, request : Request):
    ip = request.client.host
    tile.ip = ip
    currTime = time.time()
    
    
    user = User(ip=ip, time_from_last_tile=currTime)

    try:
        tile = putTileOnDb(user, tile, currTime)
        return { 'success': True, 'tile': tile }
    except HTTPException as e:
        raise e
    except Exception as e: 
        raise HTTPException(status_code=500, content={'success': False, "message": "Internal not treated server error"})