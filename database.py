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
    # only works for one keyword right now
    global db, client, collection
    keywords = list(keywords)
    query = []
    if len(keywords) == 1:
        query.append({'authors': re.compile(keywords[0], re.IGNORECASE)})
        query.append({'title': re.compile(keywords[0], re.IGNORECASE)})
        query.append({'abstract': re.compile(keywords[0], re.IGNORECASE)})
        query.append({'venue': re.compile(keywords[0], re.IGNORECASE)})
        query.append({'year': re.compile(keywords[0], re.IGNORECASE)})
        articles = collection.find({'$or' : query})
        return articles
    else:
        for keyword in keywords:
            temp_query = []
            temp_query2 = {}
            temp_query.append({'authors': re.compile(keyword, re.IGNORECASE)})
            temp_query.append({'title': re.compile(keyword, re.IGNORECASE)})
            temp_query.append({'abstract': re.compile(keyword, re.IGNORECASE)})
            temp_query.append({'venue': re.compile(keyword, re.IGNORECASE)})
            temp_query.append({'year': re.compile(keyword, re.IGNORECASE)})
            temp_query2['$or'] = temp_query
            query.append(temp_query2)
        articles = collection.find({'$and': query})
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
    global db, client, collection
    author = collection.find({}, {'authors': re.compile(author_name, re.IGNORECASE)})
    
    author_details = collection.find({}, {'title': {'authors': author},
                                          'year': {'authors': author},
                                          'venue': {'authors': author}
                                         }).sort({'year': -1})
    return author_details

def get_referencing_articles(article):
    global db, client, collection
    article_id = article['id']
    references = collection.find({'references': article_id})
    referencing_articles = []
    for item in references:
        referencing_articles.append(item)
    if len(referencing_articles) == 0:
        return None
    return referencing_articles