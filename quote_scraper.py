import requests
from bs4 import BeautifulSoup
from random import choice

#main url to which relative urls will be appended 
BASE_URL = "http://quotes.toscrape.com/"

print("Welcome to the random quote game!\n") 
    
def scrape_quotes():
     #find all quote tags on the page and assign them to variable quotes. find_all will return a list
    quotes = []
    page_url = "/page/1"


    #as long as there is a next button on the page, get the url for the next page and request the text
    while page_url:
        #request the main page, then request each additional page using the base url plus each page url
        response = requests.get(BASE_URL+page_url)
        
        #show scraping progress for debugging
        print("loading quotes, please wait...")

        #use beautiful soup to parse each page
        soup = BeautifulSoup(response.text, "html.parser")        
        
        #For each new page, find all quotes and add them to the quotes list
        quotes.extend(soup.find_all(class_="quote"))

        next_btn = soup.find(class_="next")

        #update next_btn variable with the contents of the next button on the current page
        page_url = next_btn.find("a")["href"] if next_btn else None
        
        

    #return the list of quotes
    return quotes

def start_game(quotes):

    #select a random quote from the list of all quotes
    random_quote = choice(quotes)

    #grab just the text of the quote and assign to variable quote_text
    quote_text = random_quote.find(class_="text").get_text()

    #use the author class to locate the author info
    author = random_quote.find(class_="author").get_text()

    #in the random quote, find a url which will be a link to the author's bio page
    about_url = BASE_URL + random_quote.find("a")["href"] 

    #request the contents of the about page
    about_response = requests.get(about_url)

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
    print(quote_text + "\n")
    
    #user starts with 4 guesses
    guesses_remaining = 4

    #create a variable to track/iterate the hints given to the user
    hint_index = 0

    #as long as the user hasn't used all their guesses, prompt them to guess
    while guesses_remaining > 0 :
        guess = input("Who said this? ")

        # if guess is right, game ends and loop breaks out            
        if guess == author:
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
    while replay_response not in ("n", "no", "y", "yes"):
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



