import json
from pstats import Stats
import time
from fastapi import FastAPI, HTTPException, Request
import redis

from Server.src.db.db import db
from Server.src.dbHandler import getPlaceFromDb, putTileOnDb, getClientTimeFromDb
from Server.src.entities.tile import Tile
from Server.src.entities.user import User
from Server.src.redisHandler import getPlaceFromRedis


app = FastAPI()

@app.on_event("startup")
async def startup_event():
    app.redisBase = redis.from_url('redis://localhost:6379', db=0)
    app.redisBase.reset()
    app.UserCollection = db.Users
    app.PlaceCollection = db.Place
    app.COOLDOWN = 0

@app.get("/timeStampUser")
async def timeStampUser(request: Request):
    ip = request.client.host
    user = getClientTimeFromDb(ip)
    converted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(user['time_from_last_tile']))
    userResponse = {'ip': ip, 'time_from_last_tile': converted_time}
    return userResponse

@app.get("/place")
async def get_tiles():
    place = getPlaceFromRedis()
    return {"place": place}

@app.post("/")
async def put_tile(tile: Tile, request : Request):
    ip = request.client.host
    tile.ip = ip
    currTime = time.time()
    user = User(ip=ip, time_from_last_tile=currTime)

    try:
        tile = putTileOnDb(user, tile, currTime)
        place = getPlaceFromDb()
        app.redisBase.set('place', place)
        return { 'success': True, 'tile': tile }
    except HTTPException as e:
        raise e
    except Exception as e: 
        raise HTTPException(status_code=500, content={'success': False, "message": "Internal not treated server error"})