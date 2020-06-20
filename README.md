# quote-scraper

A little game I made as part of Colt Steele's Modern Python Bootcamp Class

## Descripion

### Main Functions
The game consists of two main functions: **scrape_quotes** and **start_game**. 

scrape_quotes will request the html from http://quotes.toscrape.com/, extract all the quotes, then add those quotes to a dictionary along with the quote's author and a link to the author's bio page. On first run, quotes will be scraped and then stored locally in a JSON file. On subsequent runs, the scrape_quotes function will check for the existence of the local cache. If quotes have been cached locally, the game will read from the local JSON rather than request and scrape the HTML again. If the local cache hasn't been updated in over 30 days, scraping will take place again and the JSON will be updated with the current quotes. 

start_game will take the list of quotes provided by the scrape_quotes function as an argument, choose a random quote to display to the player, check if the player's guess is correct, and offer a hint if the guess is incorrect. 

### Game Logic

A quote will be selected at random from a list containing all of the available quotes. The player will be given 4 chances to guess the author correctly. After each incorrect guess, a hint will be given. The hints are obtained by scraping the link for the author's about page. the first hint is the author's date of birth, the second hint is the location where the author was born, and the final hint is the author's first and last intial. 

After guessing correctly the player will have the option to play again or quit the game. 

## What I learned

Making this game was a good way to learn about usng Beatiful Soup for web scraping, and the excessive comments were mainly to solidify my understanding of what I was doing. I know it's basic, but it was the first non-trival project I was able to code completely without looking at a tutorial.

Initially I had the scrape_quotes function grab all the author info and add that to a dictionary, but it took way too long for all of those requests to complete. What I ended up doing was just scraping the quotes themselves, and then only requesting the author info for the quote that was randomly selected. This cuts down on the initial wait time for scraping, but means that the game can't be played offline. 

I did some basic checking before trying to write/access the local cache (file permissions, existence of the directory, etc. ), but I'm sure there was probably a more sophisticated way to handle that. I'll explore that more in future projects. 
