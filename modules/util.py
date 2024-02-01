import pandas as pd
import re


# RegEx for tel href
def regex_tel(soup_tel):
    soup_tel = soup_tel.replace('-', ' ')
    soup_tel = re.sub(r"[a-zA-Z+=]", "", soup_tel)
    soup_tel = "0" + soup_tel[4:]
    return soup_tel


def regex_liens(url):
    regex = r'https?://[^\s]+'
    url = re.findall(regex, url)
    return url


# Function to create a file and store a Python list in it
def create_file_with_list(file_name, list_urls):
    try:
        with open(f"{file_name}_urls.txt", 'w') as file:
            file.write(str(list_urls))
    except Exception as e:
        print(e)
    print(f"The list has been stored in the file '{file_name}'.")


# Function to retrieve a list from a file
def retrieve_list_from_file(file_name):
    try:
        with open(file_name, 'r') as file:
            list_urls = file.read()
            return list_urls
    except FileNotFoundError:
        print(f"The file '{file_name}' does not exist.")
    except Exception as e:
        print(f"An error occurred while retrieving the list: {e}")


# Creates an Excel file with company data, named based on the city.
def create_excel_datas(datas, city_search):
    excel_contact = pd.Series(datas)
    excel_contact.to_excel(f'contact_entreprises_{city_search}.xlsx')
    return excel_contact
