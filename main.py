from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import re

# inurl:business.site + "perpignan"

DELAY = 1 / 1.39  # Calculate the delay for 1.39 requests per second

##### TEMP #####
urls = [
    'https://cityphone66.business.site/',
    'https://depmenager66.business.site/'
]

entreprise_contact = {}

# RegEx
def regex_tel(soup_tel):
    soup_tel = soup_tel.replace('-', ' ')
    soup_tel = re.sub(r"[a-zA-Z+=]", "", soup_tel)
    soup_tel = "0" + soup_tel[4:]
    return soup_tel


def get_datas():
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        #get name and tel of the website
        soup_name = soup.find("h1").getText()
        soup_tel = regex_tel(soup.find('a', attrs={"itemprop": "telephone"}).get("href"))
        # Update dict for excel import
        entreprise_contact.update({soup_name: soup_tel})

        print(soup_name + '\n' + soup_tel + '\n -----------')
        time.sleep(DELAY)  # delay request

    excel_contact = pd.Series(entreprise_contact)
    excel_contact.to_excel('contact_entreprise.xlsx')

if __name__ == '__main__':
    get_datas()
