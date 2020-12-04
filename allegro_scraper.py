#!/usr/bin/python3

import requests, time, csv, smtplib
from bs4 import BeautifulSoup

print("*"*50)
print("                 ALLEGRO SCRAPER")
print("*"*50)

###################################################################
item_search = "razer mouse bungee"
desired_price = 80  #ZŁ
###################################################################

print("Searching for: ", item_search)
print("Desired Price(ZŁ): ", desired_price)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
}

current_page = [1]
results = []

def create_url(item_search):
    search_term = item_search.replace(" ", "%20")
    URL = 'https://allegro.pl/listing?string=%s&bmatch=cl-dict20110-m-ctx-ele-1-2-1125' % (search_term)
    return URL
