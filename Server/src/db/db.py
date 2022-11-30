import pymongo
from pymongo import MongoClient

DuplicatedKeyException = pymongo.errors.DuplicateKeyError

client = MongoClient("mongodb://localhost:27021/?replicaSet=dbrs&directConnection=true")
db = client["utPlace"]