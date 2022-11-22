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

def search_for_authors(keywords):
    global db, client, collection
    keywords = list(keywords)
    publication_count = []
    
    authors = collection.find({}, {'authors': re.compile(keywords[0], re.IGNORECASE)})
    
    for author in authors:
        count = collection.countDocuments({}, {'authors': author})
        publication_count.append(count)

    return authors, publication_count

def get_author_details(author_name):
    author = collection.find({}, {'authors': re.compile(author_name, re.IGNORECASE)})
    
    author_details = collection.find({}, {'title': {'authors': author},
                                          'year': {'authors': author},
                                          'venue': {'authors': author}
                                         }).sort({'year': -1})
    return author_details
