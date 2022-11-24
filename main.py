import pymongo
import database
import os


def add_article():
    # adds an article to the collection
    unique = False

    clear_terminal()
    print("Adding An Article:")

    # get id from input and make sure it is unique
    id_input = ''
    clear_terminal()
    while (not unique) or (id_input == '' or id_input.isspace()):
        print("Adding An Article:")
        id_input = input('Enter a Unique ID: ')
        unique = database.check_unique_id(id_input)
        print("Error: ID Not Unique. Try Again.")

    # get title from user input
    title_input = ''
    clear_terminal()
    while title_input == '' or title_input.isspace():
        print("Adding An Article:")
        title_input = input("Enter a Title: ")

    # get author list from user input
    author_list = []
    author_input = ''
    while author_input == '' or author_input.isspace():
        clear_terminal()
        print("Adding An Article:")
        author_input = input("Enter Authors Separated by a Comma: ")
    authors = author_input.split(',')
    for author in authors:
        author_list.append(author)
    
    # get year from user input
    year_input = ''
    clear_terminal()
    print("Adding An Article:")
    while year_input == '' or year_input.isspace() or len(year_input) != 4 or not year_input.isdigit():
        year_input = input("Enter a Year: ")
        print("Error: Year Must Be A 4 Digit Integer. Try Again.")
    
    # add and check result
    clear_terminal()
    result = database.add_article(id_input, title_input, author_list, year_input)
    if result != None:
        clear_terminal()
        print("Article Added Successfully!")
        input("Press Enter To Return To The Menu.")
    else:
        print("Error: Article Add Unsuccessful. :(")
    return


def more_article_information(article):
    # Print all fields from the given article if the exist
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
    # get the users choice on which article to select or return to menu
    index = []
    counter = 1
    clear_terminal()
    temp_list = []
    for article in articles:
        temp_list.append(article)
        print('\n' + str(counter) + '. ID:', article['id'], '\nTitle: ', article['title'], '\nYear:', article['year'], '\nVenue:', article['venue'])
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
    # gets keywords and searches for the articles
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
    
    authors = database.search_for_authors(keywords)
    #pub_count = database.get_author_pub_count(authors)
    
    # === display authors ===
    i = 0
    index = []
    temp_list = []
    for author in authors:
        for person in author['authors']:
            for keyword in user_keywords:
                if keyword in person:
                    temp_list.append(person)
                    pub_count = database.get_author_pub_count(person)
                    print(str(i) + ". Name: " + person + " Publication Count: " + str(pub_count))
                    index.append(str(i))
                    i += 1
    
    # === select an author ===
    user_in = ''
    while user_in.lower() not in ['y', 'n']:
        user_in = input("Would you like to select an author? (Y/N): ")
    
    if user_in.lower() == 'y':

        user_in = ''
        while not user_in.isdigit() and user_in not in index:
            user_in = input("Type an author's number: ")
    
        # === get selected author details ===
        author_details = database.get_author_details(temp_list[int(user_in)])
        
        # === display the details ===
        clear_terminal()
        
        print(str(temp_list[int(user_in)].upper()) + ":") # print the author name at the top
        
        for elem in author_details:
            print("Title: " + str(elem['title']) + "\n" + "Year: " + str(elem['year']) + "\n" + "Venue: " + str(elem['venue']) + "\n\n")

        user_in = input("Press Enter To Continue. . .")
    elif user_in.lower() == 'n':
        return

def list_venues():
    clear_terminal()
    user_num = ''
    while type(user_num) != 'int':
        user_num = int(input("Enter a number: "))
    
    venue_details = database.get_venues()
    
    if len(venue_details[0]) <= user_num:
        for i in range(len(venue_details)):
            print("Venue: " + venue_details[0][i] + "Articles: " + str(venue_details[1][i]) + "References: " + str(venue_details[2][i]))
    else:
        for i in range(user_num):
            print("Venue: " + venue_details[0][i] + "Articles: " + str(venue_details[1][i]) + "References: " + str(venue_details[2][i]))

def main_menu():
    # display the main menu screen
    user_in = ''
    # loop unless exit is selected
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
            add_article()
            pass
        elif user_in == '5': # Exit
            return


def clear_terminal():
    # clear terminal for output purposes
    os.system('cls' if os.name == 'nt' else 'clear')
    return

def main():
    database.connect_to_db()
    main_menu()
    return


if __name__ == '__main__':
    main()
