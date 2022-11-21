import pymongo
import database
import os


def search_for_articles():
    clear_terminal()
    user_keywords = ''
    
    print("Search For Articles:")
    while user_keywords == '' or user_keywords.isspace(): # make sure blanks are not entered
        user_keywords = input('Enter Keywords: ')
    keywords = user_keywords.split() # splits the input by spaces
    keywords = set(keywords) # gets rid of duplicates
    results = database.search_for_articles(keywords)



    return


def main_menu():
    user_in = ''
    while user_in not in ['1','2','3','4','5']:
        clear_terminal()
        print('Main Menu:')
        print('1. Search for Articles')
        print('2. Search for Authors')
        print('3. List the Venues')
        print('4. Add an Article')
        print('5. Exit')
        user_in = input('Select an Option: ')
        if user_in == '1': # Search for Articles
            search_for_articles()
            pass
        elif user_in == '2': # Search for Authors
            pass
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