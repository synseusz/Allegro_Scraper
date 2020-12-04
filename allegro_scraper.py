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

def reverse_string_order(string):
    # first split the string into words
    words = string.split(' ')

    # reverse the split string list and join using space
    reverse_string = ' '.join(reversed(words))

    return reverse_string

def send_email(new_items, check_results):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login("piotr.mikolaj.orlowski@gmail.com", "gyxpvwfkczllcoio")

    if new_items:
        if len(new_items) > 1:
            variable = "%s items have been added to your listing"%(len(new_items))

        else:
            variable = "%s item has been added to your listing"%(len(new_items))

        subject = variable
        body_initial = "The following %s item(s) listed below was recently added to your listing:"%(len(new_items))

        msg = "Subject: %s\n\n%s\n\n%s"%(subject, body_initial, [new_item for new_item in new_items])
        converted_msg = msg.replace("[", "").replace("]", "").replace("&&", "\n").replace("'", "").replace(", ", "\n\n")

        server.sendmail(
            "piotr.mikolaj.orlowski@gmail.com",
            "thesynseusz@gmail.com",
            converted_msg.encode('ascii', 'ignore')
        )
        print("New Items email has been sent!")

    if check_results:
        subject = "Item found!"
        body_initial = "The following %s item(s) listed below match your expectations:"%(len(check_results))
        
        msg = "Subject: %s\n\n%s\n\nDESIRED PRICE: %s zl or less.\n\n%s"%(subject, body_initial, desired_price, [result for result in check_results])
        converted_msg = msg.replace("[", "").replace("]", "").replace("&&", "\n").replace("'", "").replace(", ", "\n\n").replace('"', "")

        server.sendmail(
            "piotr.mikolaj.orlowski@gmail.com",
            "thesynseusz@gmail.com",
            converted_msg.encode('ascii', 'ignore')
        )
        print("Results email has been sent!")


    server.quit()

def check_for_new_items():
    try:

        with open('listed_items.csv') as reader:
            previously_listed_items = list(csv.reader(reader))
            print("Items listed during last check: ", len(previously_listed_items))

            new_items = []
            for item in currently_listed_items:
                if item not in previously_listed_items:
                    title = item[0]
                    price = item[1]
                    link = item[2]
                    new_items.append("--> %s&&Price: %s zl&&Link: %s"%(title, price, link))
            
            if len(new_items) > 0:
                return new_items
            else:
                return None
          
           
    except:
        print("No previous listings found or error while reading listed_items.csv")
        return None

def save_to_csvfile():
    with open('listed_items.csv', 'w') as writer:
        my_writer = csv.writer(writer)
        my_writer.writerows(currently_listed_items)  

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


    # check for new items on listing
    try:
        new_items = check_for_new_items()
    except:
        print("Unable to check for new items")

    # send email if new item found
    if new_items:
        print("NEW ITEMS: ", new_items)
        send_email(new_items, None)
    else:
        print("\nNo new items listed since last check!")
    
    # send email if results found
    if len(results) > 0:
        print("\nCHECK RESULTS: ",results)
        send_email(None, results)
    else:
        print("\nNo results found!")

    # save current items on listing to a csv file for further reference
    save_to_csvfile()

########################################################################
#CALL MAIN FUNCTION
items_check()