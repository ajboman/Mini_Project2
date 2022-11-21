import pymongo
import re

client = None
db = None
collection = None


def connect_to_db():
    global db, client, collection
    portnum = int(input("Enter the mongodb port number: "))
    client = pymongo.MongoClient("mongodb://localhost:" + str(portnum))
    db = client["291db"]
    collection = db["dblp"]
    return

def search_for_articles(keywords):
    global db, client, collection
    keywords = list(keywords)
    
    articles = collection.find({'$and':[
                                    {'authors': re.compile(keywords[0], re.IGNORECASE)},
                                    {'title': re.compile(keywords[0], re.IGNORECASE)}
                                ]})
    for article in articles:
        print(article) 
    return articles