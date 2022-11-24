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


def search_for_authors(keyword):
    global db, collection
    authors = []
    cursor = collection.find({'authors': re.compile(keyword, re.IGNORECASE)})
    for item in cursor:
        for author in item['authors']:
            if keyword.upper() in author.upper():
                authors.append(author)
    authors = set(authors)
    authors = list(authors)
    return authors

def get_author_pub_count(author):
    global db, collection
    
    count = collection.count_documents({'authors': author})
    
    return count

def get_author_details(author_name):
    global db, collection
    
    author_details = collection.find({'authors': author_name}, {'title': 1, 'year': 1, 'venue': 1}).sort('year', -1)

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

    pipeline = [
                {
                   '$group': {
                                '_id': '$venue',
                                'art_in_ven': {'$sum': '$references'},
                                'paper_count': {'$sum': 1}
                             } 
                }
               ]
    
    aggregation = collection.aggregate(pipeline)

    return aggregation
