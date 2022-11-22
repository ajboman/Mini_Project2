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
                  "Venue: " + str(author_details[2 ][i] + "\n\n")
 
    
    else if user_in.lower() == 'n':
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
