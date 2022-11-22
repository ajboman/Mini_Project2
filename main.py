import pymongo
import database
import os


def more_article_information(article):
    referencing_articles = database.get_referencing_articles(article)
    clear_terminal()
    # Abstract
    try:
        print("Abstract:")
        print(article['abstract'])
    except:
        print('Abstract Not Found.')
    
    # Authors
    try:
        print("\nAuthors:")
        print(article['authors'])
    except:
        print('Author(s) Not Found.')

    # Number of Citations
    try:
        print('\nNumber of Citations:', article['n_citation'])
    except:
        print('Number of Citations Not Found')

    # References
    try:
        print('\nReferences:')
        print(article['references'])
    except:
        print('Reference(s) Not Found.')

    # title
    try:
        print('\nTitle:', article['title'])
    except:
        print('Title Not Found.')

    # venue
    try:
        print('\nVenue:', article['venue'])
    except:
        print('Venue Not Found.')

    # year 
    try:
        print('\nYear:', article['year'])
    except:
        print('Year Not Found.')

    # id
    try:
        print('\nID:', article['id'])
    except:
        print('ID Not Found.')

    # referencing articles
    if referencing_articles != None:
        print('\nOther Articles That Reference This Article:')
        for article in referencing_articles:
            print('ID: ' + str(article['id']) + ', Title: ' + str(article['title']) + ', Year: ' + str(article['year']) + '\n')
    input('Type Enter To Continue.')
    return


def article_menu(articles):
    index = []
    counter = 1
    clear_terminal()
    temp_list = []
    for article in articles:
        temp_list.append(article)
        print(str(counter) + '.', article['id'], article['title'], article['year'], article['venue'])
        index.append(str(counter))
        counter += 1
    if len(index) != 0:
        user_in = ''
        while user_in not in index:
            user_in = input('\nType Menu to Return.\nSelect an Article to See More Information. ')
            if user_in.upper() == 'MENU':
                return 
        more_article_information(temp_list[int(user_in) - 1])
        return 
    else:
        input('No Results Found.\nPress Enter to Continue.')
        return

def search_for_articles():
    clear_terminal()
    user_keywords = ''
    
    print("Search For Articles:")
    while user_keywords == '' or user_keywords.isspace(): # make sure blanks are not entered
        user_keywords = input('Enter Keywords: ')
    keywords = user_keywords.split() # splits the input by spaces
    keywords = set(keywords) # gets rid of duplicates
    articles = database.search_for_articles(keywords)
    return articles

def search_for_authors():
    clear_terminal()
    user_keywords = ''

    print("Search For Authors:")
    while user_keywords == '' or user_keywords.isspace():
        user_keywords = input("Enter Keywords: ")
    keywords = user_keywords.split()
    keywords = set(keywords)
    
    authors, pub_count = database.search_for_authors(keywords)
    
    # === display authors ===
    i = 0
    for author in authors:
        print(str(i) + ". Name: " + author + " Publication Count: " + str(pub_count[i]))
        i += 1
    
    # === select an author ===
    user_in = ''
    while user_in.lower() not in ['y', 'n']:
        user_in = input("Would you like to select an author? (Y/N): ")
    
    if user_in.lower() == 'y':
        # convert list to be workable
        authors_lower = []
        for author in authors:
            authors_lower.append(author.lower())
   
        user_in = ''
        while user_in.lower() not in authors_lower:
            user_in = input("Type an author's name: ")
    
        # === get selected author details ===
        author_details = database.get_author_details(user_in)
        
        # === display the details ===
        clear_terminal()
        print(str(user_in.upper()) + ":") # print the author name at the top
        for i in range(len(author_details)):
            print("Title: " + str(author_details[0][i]) + "\n"
                  "Year: " + str(author_details[1][i]) + "\n"
                  "Venue: " + str(author_details[2 ][i] + "\n\n"))
    elif user_in.lower() == 'n':
        return


def main_menu():
    user_in = ''
    while user_in not in ['5']:
        clear_terminal()
        print('Main Menu:')
        print('1. Search for Articles')
        print('2. Search for Authors')
        print('3. List the Venues')
        print('4. Add an Article')
        print('5. Exit')
        user_in = input('Select an Option: ')
        if user_in == '1': # Search for Articles
            articles = search_for_articles()
            article_menu(articles)
            pass
        elif user_in == '2': # Search for Authors
            search_for_authors()
        elif user_in == '3': # List the Venues
            pass
        elif user_in == '4': # Add an Article
            pass
        elif user_in == '5': # Exit
            return


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    return

def main():
    database.connect_to_db()
    main_menu()
    return


if __name__ == '__main__':
    main()
