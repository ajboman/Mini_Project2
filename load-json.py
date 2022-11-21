import pymongo
import json

# === GET JSON FILE NAME AND PORT ===
filename = input("Enter the json filename: ") # will need to handle errors l8tor
portnum = int(input("Enter the mongodb port number: "))

# === INIT DATABASE ===
client = pymongo.MongoClient("mongodb://localhost:" + str(portnum))

dblist = client.list_database_names()
if "291db" not in dblist:
    db = client["291db"]
else:
    print("database exists")

# === INIT COLLECTION ===
collist = db.list_collection_names()
if "dblp" in collist:
    collection.drop()
    collection = db["dblp"]
else:
    collection = db["dblp"]

# === LOAD JSON INTO COLLECTION ===
filename = filename + ".json"
jsonfile = open(filename, 'r')

for jsonObj in jsonfile:
    data = json.loads(jsonObj)
    collection.insert_one(data) # should insert line by line?
