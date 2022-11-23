import pymongo
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27021/?replicaSet=dbrs&directConnection=true")
db = client["utPlace"]
# collection = db["test"]

# tutorial1 = {
#     "name": "tutorial1",
#     "description": "tutorial1 description",
#     "tags": ["mongodb", "database", "NoSQL"],
#     "likes": 100,
# }

# tutorial = db.tutorial
# tutorial.insert_one(tutorial1)