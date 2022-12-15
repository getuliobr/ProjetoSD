import pymongo
from pymongo import MongoClient

DuplicatedKeyException = pymongo.errors.DuplicateKeyError

client = MongoClient("mongodb://mongo1:27017,mongo2:27017,mongo3:27017/?replicaSet=dbrs")
db = client["utPlace"]