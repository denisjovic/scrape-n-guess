import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice
from csv import DictWriter

BASE_URL = 'http://quotes.toscrape.com/'

def scrape_quotes():

    next_page_url = '/page/1'
    quotes_list = []

    while next_page_url:


        response = requests.get(f'{BASE_URL}{next_page_url}')
        # print(f'Now printing {BASE_URL}{next_page_url}...')
        soup = BeautifulSoup(response.text, 'html.parser')


        quotes =  soup.find_all(class_ = 'quote')

        for quote in quotes:
            q_text = quote.find(class_ = 'text').get_text()
            q_author = quote.find(class_ = 'author').get_text()
            q_href = quote.find('a')['href']

            quotes_list.append({
                'text': q_text,
                'author': q_author,
                'url': q_href
            })

        sleep(1)

        # next page button
        next_btn = soup.find(class_ = 'next')
        # go and parse next page IF there is next button, if not, then it's false and WHILE loop breaks
        next_page_url = next_btn.find('a')['href'] if next_btn else None

    return quotes_list


def write_to_csv(quotes):
    with open('quotes.csv', 'w') as file:
        headers = ['text', 'author', 'url']
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        for quote in quotes:
            csv_writer.writerow(quote)

quotes = scrape_quotes()
write_to_csv(quotes)
