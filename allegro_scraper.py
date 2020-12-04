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


def items_check():
    if current_page[0] == 1:
        URL = create_url(item_search)
    else:
        URL = create_url(item_search) + '&p=%s' % (current_page[0])

    print("\nCURRENTLY SCRAPING THE FOLLOWING PAGE:\n", URL)
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    number_of_pages = int(
        soup.find(class_="_1h7wt _1fkm6 _g1gnj _3db39_3i0GV _3db39_XEsAE").text)
    listed_items_html = soup.find_all(
        class_="mpof_ki mqen_m6 mp7g_oh mh36_0 mvrt_0 mg9e_8 mj7a_8 m7er_k4 _1y62o _9c44d_1I1gg")
    print("\nTotal items on this page: ", len(listed_items_html))

    # reverse item_search order
    reversed_item_search = reverse_string_order(item_search)

    # currently listed items
    global currently_listed_items
    currently_listed_items = []


    for item in listed_items_html:
        title = item.h2.a.text.replace(',', '')
        price = item(class_="msa3_z4 _9c44d_2K6FN")[0]
        converted_price = float(price.text.replace(",", ".").replace("zł", ""))

        currently_listed_items.append([title, str(converted_price), item.h2.a.get('href')])

        if item_search.lower() in title.lower() or reversed_item_search.lower() in title.lower():

            if converted_price <= float(desired_price):
                
                result_format = "--> %s&&Price: %s zl&&Link: %s"%(title, converted_price, item.h2.a.get('href'))
                
                results.append(result_format)


    if number_of_pages > 1 and number_of_pages > current_page[0]:
        next_page = current_page[0] + 1

        current_page.clear()
        current_page.append(next_page)

        items_check()

    elif number_of_pages == current_page[0]:
        current_page.clear()
        current_page.append(1)


########################################################################
#CALL MAIN FUNCTION
items_check()