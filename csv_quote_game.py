import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice
from csv import DictReader


BASE_URL = 'http://quotes.toscrape.com/'

def read_quotes_from_csv(filename):
    with open(filename, 'r') as file:
        csv_reader = DictReader(file)
        return list(csv_reader)
        

def start_game(quotes):

    random_quote = choice(quotes)
    print('Here is a quote:')
    print(random_quote['text'])
    print(random_quote['author'])

    remaining_guesses = 4
    players_guess = ''

    while players_guess.lower() != random_quote['author'].lower() and remaining_guesses > 0:
        players_guess = input(f"Who's quote is this? You have {remaining_guesses} guesses \n")
        if players_guess.lower() == random_quote['author'].lower():
            print('Well done! That is a correct answer!')
            break
        remaining_guesses -= 1
        
        if remaining_guesses == 3: # if he has guessed once
            res = requests.get(f"{BASE_URL}{random_quote['url']}") # base url + link to the bio
            soup = BeautifulSoup(res.text, 'html.parser')
            b_date = soup.find(class_ = 'author-born-date').get_text()
            b_location = soup.find(class_ = 'author-born-location').get_text()
            print(f"Here is the hint, the author was born on {b_date} in {b_location}")
        elif remaining_guesses == 2:
            print(f"Here is another hint, author's name starts with: {random_quote['author'][0]}")
        elif remaining_guesses == 1:
            last_name_initial = random_quote['author'].split(' ')[1][0]
            print(f"Last hint, author's last name starts with:{last_name_initial}")
        else:
            print(f"Game over, author was: {random_quote['author']}")

    again = ''
    while again.lower() not in ('yes', 'y', 'no', 'n'):
            again = input('Play again (y/n)?')
    if again.lower() in ('yes', 'y'):
            return start_game(quotes)
    else:
            print('Good bye!')

# read from file instead of scraping every time
quotes = read_quotes_from_csv('quotes.csv')
start_game(quotes)