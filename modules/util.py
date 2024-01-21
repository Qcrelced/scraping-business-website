from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import re

# def choose_driver(navigator="chrome", endless=False):
#     options = Options()
#     if endless:
#         options.add_argument('--headless=new')
#     match navigator:
#         case "chrome":
#             driver = webdriver.Chrome(
#                 service=Service(),
#                 options=options
#             )
#             return driver


# RegEx for tel href
def regex_tel(soup_tel):
    soup_tel = soup_tel.replace('-', ' ')
    soup_tel = re.sub(r"[a-zA-Z+=]", "", soup_tel)
    soup_tel = "0" + soup_tel[4:]
    return soup_tel


# Creates an Excel file with company data, named based on the city.
def write_file(datas, city_search):
    excel_contact = pd.Series(datas)
    excel_contact.to_excel(f'contact_entreprises_{city_search}.xlsx')


