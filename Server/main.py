import logging
import time

import redis
from fastapi import (FastAPI, HTTPException, Request, WebSocket,
                     WebSocketDisconnect)

from Server.src.db.db import db
from Server.src.dbHandler import (getClientTimeFromDb, getPlaceFromDb,
                                  putTileOnDb)
from Server.src.entities.tile import Tile
from Server.src.entities.user import User
from Server.src.redisHandler import getPlaceFromRedis

app = FastAPI()
logger = logging.getLogger()

@app.on_event("startup")
async def startup_event():
    app.redisBase = redis.from_url('redis://localhost:6379', db=0)  # type: ignore
    app.redisBase.reset()  # type: ignore
    app.UserCollection = db.Users  # type: ignore
    app.PlaceCollection = db.Place  # type: ignore
    app.COOLDOWN = 0  # type: ignore
    app.clients = []  # type: ignore

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

@app.post("/tile")
async def put_tile(tile: Tile, request : Request):
    ip = request.client.host
    tile.ip = ip
    currTime = time.time()
    user = User(ip=ip, time_from_last_tile=currTime)

    try:
        tile = putTileOnDb(user, tile, currTime)
        place = getPlaceFromDb()
        app.redisBase.set('place', place)  # type: ignore
        for client in app.clients:  # type: ignore
            await client.send_json(tile)
        return { 'success': True, 'tile': tile }
    except HTTPException as e:
        raise e
    except Exception as e: 
        raise HTTPException(status_code=500, content={'success': False, "message": "Internal not treated server error"})  # type: ignore

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    app.clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect as e:
        logger.warn(f"Websocket disconnected: {websocket.client.host}")
        app.clients.remove(websocket)