
import pandas as pd
import re
import pickle

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


# Function to create a file and store a Python list in it
def create_file_with_list(file_name, list_urls):
    with open(file_name, 'wb') as file:
        pickle.dump(list_urls, file)
    print(f"The list has been stored in the file '{file_name}'.")

# Function to retrieve a list from a file
def retrieve_list_from_file(file_name):
    try:
        with open(file_name, 'rb') as file:
            list_urls = pickle.load(file)
            return list_urls
    except FileNotFoundError:
        print(f"The file '{file_name}' does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred while retrieving the list: {e}")
        return None

# Creates an Excel file with company data, named based on the city.
def write_file_datas(datas, city_search):
    excel_contact = pd.Series(datas)
    excel_contact.to_excel(f'contact_entreprises_{city_search}.xlsx')


