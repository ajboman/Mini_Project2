import pymongo
import json

# === GET JSON FILE NAME AND PORT ===
filename = ''
while filename == '':
    filename = input("Enter the json filename: ")
if filename[-5:] != ".json":
      filename = filename + ".json"

portnum = ''
while not portnum.isdigit():
    portnum = input("Enter the mongodb port number: ")

# === INIT DATABASE ===
client = pymongo.MongoClient("mongodb://localhost:" + str(portnum))

dblist = client.list_database_names()
if "291db" not in dblist:
    db = client["291db"]

db = client["291db"]


# === INIT COLLECTION ===
collist = db.list_collection_names()
if "dblp" in collist:
    collection = db["dblp"]
    collection.drop()

collection = db["dblp"]

# === CREATE INDICES === #
db.dblp.create_index([
("authors", "text"),
("venue", "text"),
("abstract", "text"),
("year", "text"),
("title", "text")
])
db.dblp.create_index(
[('authors', -1)])

# === LOAD JSON INTO COLLECTION ===
jsonfile = open(filename, 'r')

for jsonObj in jsonfile:
    data = json.loads(jsonObj)
    collection.insert_one(data)



