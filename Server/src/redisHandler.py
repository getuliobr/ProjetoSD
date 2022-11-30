import json

from Server.src.dbHandler import getPlaceFromDb

from .. import main


def getPlaceFromRedis():
    place = main.app.redisBase.get('place')
    if not place:
        place = getPlaceFromDb()
        main.app.redisBase.set('place', place)
    place = json.loads(place)
    return place