import json
import time

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pymongo import ReturnDocument

from Server.src.entities.tile import Tile
from Server.src.entities.user import User

from .. import main


def getClientTimeFromDb(ip):
    user = main.app.UserCollection.find_one({'ip': ip},{'_id': False}
    )
    if user:
        return user
    return 0


def getPlaceFromDb():
    placeItems = main.app.PlaceCollection.find({}, {'_id': False, 'ip': False})
    placeItemsCount = main.app.PlaceCollection.count_documents({})

    place = "["
    for i, document in enumerate(placeItems, 1):
        place = place + (json.dumps(document, default=str))
        if i != placeItemsCount:
            place = place + (',')
    place = place + "]"
    return place

def putTileOnDb(user: User, tile: Tile, currTime):
    dbUser = getClientTimeFromDb(user.ip)
    if dbUser != 0:
        if (currTime - dbUser['time_from_last_tile'] < main.app.COOLDOWN):
            raise HTTPException(400, 'Not so fast sanic!')
    userDb = main.app.UserCollection.find_one_and_update({
            'ip': user.ip,
            'time_from_last_tile': {
                '$lte': currTime - main.app.COOLDOWN
            }
        }, {
            '$set': jsonable_encoder(user)
        }, upsert=True, return_document=ReturnDocument.AFTER)

    if not userDb:
        raise HTTPException(status_code=400, content={'success': False, "message": "You can't put a tile so fast"})
    
    tile.color = tile.color.as_hex()

    if tile.x < 0 and tile.x >= 1000 or tile.y < 0 and tile.y >= 1000:
        raise HTTPException(status_code=400, content={'success': False, "message": "Out of bounds"})

    tile = main.app.PlaceCollection.find_one_and_update({
        'x': tile.x,
        'y': tile.y
    }, {
        '$set': jsonable_encoder(tile)
    }, upsert=True, return_document=ReturnDocument.AFTER)

    del tile['_id']
    del tile['ip']
    return tile