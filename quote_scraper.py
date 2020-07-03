import requests
from bs4 import BeautifulSoup
from random import choice
from datetime import datetime, date
import json
import os

#main url to which relative urls will be appended
BASE_URL = "http://quotes.toscrape.com/"


print("Welcome to the random quote game!\n")


#function that scrapes the quotes website and collects all the required info
def scrape_quotes():

    #create empty list to hold all of the quotes
    all_quotes = []
    page_url = "/page/1"

    #set the folder and filename for the cache file
    current_dir = os.getcwd()
    cache_location = os.path.join(current_dir, "cache")
    cache_file = os.path.join(cache_location, "quotes.json")
  
 
    #if the local cache already exists, check the age to determine whether or not to update it
    if os.path.exists(cache_file):

    
        cache_last_modified = datetime.fromtimestamp(os.path.getmtime(cache_file)).date().day
        current_date = datetime.today().date().day
        cache_age = current_date - cache_last_modified
        
    #if the local cache doesn't exist, create the directory, then create the empty json file
    else:
             
        try:
            
            if not os.path.exists(cache_location):
                os.mkdir(cache_location)
                cache_write_access = True
                
            with open(cache_file, "w"):
                cache_write_access = True
                
        except PermissionError:
            
            #print("Local cache could not be created. Game data will be downloaded instead of read locally.\n")
            cache_write_access = False
            pass
           
    #check to see if quotes have been cached locally. If there is no saved quotes file, or if it hasn't been updated in 30 days, scrape the quotes again
    if not os.path.exists(cache_file) or os.stat(cache_file).st_size == 0 or cache_age >= 30:

        #as long as there is a url for the next page, get the url for the next page and request the text
        while page_url:

            #request the main page, then request each additional page using the base url plus each page url
            response = requests.get(BASE_URL+page_url)

            #show scraping progress for debugging
            print("loading quotes, please wait...")

            #use beautiful soup to parse each page
            soup = BeautifulSoup(response.text, "html.parser")

            #find all quote tags on each page and assign them to variable page_quotes. find_all will return a list
            page_quotes = soup.find_all(class_="quote")
            
            
            #parse through each of the quote divs and extract the quote text, author, and about info
            for item in page_quotes:
                
                quote_text = item.find(class_="text").get_text()
                author_name = item.find(class_="author").get_text()
                about_url = BASE_URL + item.find("a")["href"]
        
                #create a new dictionary and populate it with the relevent info for each quote    
                quote_dict = {"quote": quote_text, "author": author_name, "author_about_link": about_url}

                #add each new dictionary to a list that holds all quote dictionaries
                all_quotes.append(quote_dict)
               
            #check to see if there is a "next" button on the page
            next_btn = soup.find(class_="next")
            
            #update next_btn variable with the contents of the next button on the current page. if there is no next button, page_url set to None
            page_url = next_btn.find("a")["href"] if next_btn else None

        #if we have permission to write to the cache folder, write all the quote data to a json file
        if cache_write_access == True:
            with open(cache_file, "w") as json_file:
                json.dump(all_quotes, json_file, indent=2)


    #if we don't need to scrape the quotes, read the quote data from the local cache
    else:
       
       #open the local cache and store the contents to the all_quotes list
        with open(cache_file, "r") as json_file:
            all_quotes = json.load(json_file)

    
    return all_quotes
    

#main game logic
def start_game(quotes):

    #select a random quote from the list of all quotes
    random_quote = choice(quotes)

    #grab just the text of the quote and assign to variable quote_text
    quote = random_quote["quote"]

    #use the author class to locate the author info
    author = random_quote["author"]

    #in the random quote, find a url which will be a link to the author's bio page
    #about_url = random_quote["author_about_link"]
    
    #request the contents of the about page
    about_response = requests.get(random_quote["author_about_link"])

    #parse the about page with beautiful soup
    about_soup = BeautifulSoup(about_response.text, "html.parser")

    #search about page for "author-born-date" class to locate the dob
    born_date = about_soup.find(class_="author-born-date").get_text()

    #search about page for "author-born-location" to locate where author was born
    born_location = about_soup.find(class_="author-born-location").get_text()

    fname = author.split()[0]
    lname = author.split()[-1]

    #create the list of hints
    hints = [f"Author's date of birth: {born_date}", f"Author was born: {born_location}", f"Author's initials are: {fname[0]}. {lname[0]}."]

    #display the random quote to the user
    print("\nHere's a random quote: \n")
    print(quote + "\n")

    #user starts with 4 guesses
    guesses_remaining = 4

    #create a variable to track/iterate the hints given to the user
    hint_index = 0

    #as long as the user hasn't used all their guesses, prompt them to guess
    while guesses_remaining > 0 :
        guess = input("Who said this? ")

        # if guess is right, game ends and loop breaks out
        if guess.lower() == author.lower():
            print("That's correct!")
            break

        # if guess is incorrect, and they haven't used all their hints, give the use a hint. After each incorrect guess a different hint will be displayed by iterating through the hints list
        elif guess.lower() != author.lower() and guesses_remaining > 1:
            guesses_remaining -= 1
            print("\nThat is not correct. Here's a hint: \n")
            print(hints[hint_index] + "\n")
            hint_index += 1

        else:
            guesses_remaining -= 1
            print(f"\nSorry! You lose! The correct answer was {author}.\n")

    #ask user if they want to play the game again
    replay_response = input("Would you like to play again (y/n)? ")

    #if use enters anything other than y, yes, n, no keep propmpting them
    while replay_response.lower() not in ("n", "no", "y", "yes"):
        replay_response = input("\nPlease enter 'y' or 'n'. ")

    #if user enters y or yes, call the start_game function again
    if replay_response.lower() in ("y", "yes"):
        return start_game(quotes)
    else:
        print("\nThanks for playing!")


#call the scrape quotes funtcion to populate the quotes list
quotes = scrape_quotes()


#call the main game function
start_game(quotes)



