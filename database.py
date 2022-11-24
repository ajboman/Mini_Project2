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
    global db, collection
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
    global db, collection
    keywords = list(keywords)
    
    authors = collection.find({'authors': re.compile(keywords[0], re.IGNORECASE)})

    return authors

def get_author_pub_count(author):
    global db, collection
    
    count = collection.count_documents({'titles': {'authors': author}})
    
    return count

def get_author_details(author_name):
    global db, collection
    
    author_details = collection.find({'authors': author_name}, {'title': 1, 'year': 1, 'venue': 1})

    return author_details

def get_referencing_articles(article):
    global db, collection
    article_id = article['id']
    references = collection.find({'references': article_id})
    referencing_articles = []
    for item in references:
        referencing_articles.append(item)
    if len(referencing_articles) == 0:
        return None
    return referencing_articles


def check_unique_id(id):
    global db, collection
    cursor = db.collection.find({'id':id})
    result = list(cursor)
    if len(result) == 0:
        return True
    return False

def add_article(id, title, authors, year):
    global db, collection
    # create document to be inserted
    document = {}
    document['abstract'] = "" # equivalent to NULL
    document['authors'] = authors
    document['n_citation'] = 0
    document['references'] = []
    document['title'] = title
    document['venue'] = "" # equivalent to NULL
    document['year'] = year
    document['id'] = id
    # insert data
    result = db.dblp.insert_one(document)
    return result.inserted_id

def get_venues():
    global db, client, collection
    venue_details = []
    
    # === get all venues ===
    venues = collection.find({'venue': 1})

    # === get the number of articles for each venue ===
    for venue in venues:
        articles_num = collection.count_documents({'title': {'venue': venue}}) # get the number of articles in the venue?
    # === numbers of articles that reference a paper ===
    references = collection.count_documents({'references': 1}) # get all references?
    for reference in references and venue in venues:
        reference_num = collection.count_documents({'$and': [{'id': reference},
                                                             {'venue': venue}]})
    # === sort ===
    for reference in references and venue in venues:
        venues_sorted = collection.find(collection.find({'venue': 1})).sort({'$and': [{'id': reference},
                                                                                      {'venue': venue}]})
    
    # === append lists to venue details and return ===
    venue_details.append(venues_sorted)
    venue_details.append(articles_num)
    venue_details.append(reference_num)
    return venue_details
