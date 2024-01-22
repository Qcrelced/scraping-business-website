import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from modules.util import create_file_with_list
from modules.util import regex_tel
from modules.util import retrieve_list_from_file

# Default style attribute for the button
# Use for click button next page when = transform: scale(0)
villes = [
    "narbonne"
]
DELAY = 10
button_attr_style_default: str = 'transform: scale(1);'
request: str = str(input("Ville : "))
request = "narbonne"  # Temporary, replace with user input
options = Options()  # Set up Chrome options
# options.add_argument('--headless=new')  # Commented for testing
driver = webdriver.Chrome(
    service=Service(),
    options=options
)


# Function to handle the cookie dialog
def cookie_dialog():
    try:
        cookie_dialog = driver.find_element(By.ID, "CXQnmb")
        accept_button = cookie_dialog.find_element(By.ID, "L2AGLb")
        if accept_button is not None:
            accept_button.click()
    except NoSuchElementException:
        print("Cookie dialog not present")
    except:
        print("cookie_dialog error")
    finally:
        print("---cookie_dialog clause---")


# Function to navigate to the last page of Google search results
def go_last_page(omitted_result_page=False):
    last_page_google: bool = False
    scroll_first_page: bool = True
    sleep(2)
    button_page = "T7sFge.sW9g3e.VknLRd"

    # Scroll to the bottom of the first pageb
    while scroll_first_page:
        scrollY_before = driver.execute_script('return window.scrollY')
        driver.execute_script('window.scrollTo({top: document.documentElement.scrollHeight})')
        sleep(1)
        scrollY_after = driver.execute_script('return window.scrollY')
        if scrollY_after == scrollY_before:
            scroll_first_page = False
    try:
        driver.find_element(By.CLASS_NAME, "T7sFge.sW9g3e.VknLRd")
    except NoSuchElementException:
        print("Element not found")
    except:
        print("Button error")
    # Continue navigating to the next page until the last page
    while not last_page_google:
        try:
            button_page_style = driver.find_element(By.CLASS_NAME, button_page).get_attribute('style')
        except NoSuchElementException:
            print("Button page style attribute not present")
            last_page_google = True
        except:
            print("Error in button page style attribute")
        else:
            if button_page_style != button_attr_style_default:
                last_page_google = True
                print('info: last_page_google end while button page')
            else:
                wait = WebDriverWait(driver, 10)
                next_button_page = wait.until(EC.element_to_be_clickable(
                    (By.CLASS_NAME, button_page)))
                driver.execute_script("arguments[0].click();", next_button_page)
        finally:
            sleep(2)

    # If omitted result page, click on the "Omitted results" button and call the function recursively
    if omitted_result_page == False:
        try:
            button_omitted_result = driver.find_element(By.ID, 'ofr')
        except NoSuchElementException:
            print("Element button omitted result not present")
        except:
            print("Error in button omitted result")
        else:
            button_omitted_result.find_element(By.TAG_NAME, 'a').click()
            go_last_page(omitted_result_page=True)
        finally:
            pass
    print("---go_last_page clause---")


def scraping_urls():
    valeur_a_supprimer = ""
    urls = []
    i = 0
    for url in driver.find_elements(By.CLASS_NAME, "byrV5b"):
            urls.append(url.find_element(By.TAG_NAME, "cite").text)
    while i < len(urls):
        if urls[i] == valeur_a_supprimer:
            urls.remove(urls[i])
        else:
            i += 1
    create_file_with_list(f"list_{request}", urls)
    return urls

def scrapping_datas(urls):
    entreprise_contact = {}
    i = 0
    #get num and name
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        # get name and tel of the website
        soup_name = soup.find("h1").getText()
        soup_tel = regex_tel(soup.find('a', attrs={"itemprop": "telephone"}).get("href"))
        # Update dict for excel
        entreprise_contact.update({soup_name: soup_tel})

        print(soup_name + '\n' + soup_tel + '\n -----------')
        sleep(DELAY)  # delay request
        i += 1
        if i == 1:
            break

def test_input():
    driver.get("https://cityphone66.business.site/")
    driver.execute_script('let nom = document.querySelector(".whsOnd.zHQkBf[type=\"text\"]"); nom.setAttribute("data-initial-value", "Declercq"); let tel = document.querySelector(".whsOnd.zHQkBf[type=\"tel\"]"); tel.setAttribute("data-initial-value", "06 26"); let email = document.querySelector(".whsOnd.zHQkBf[type=\"email\"]"); email.setAttribute("data-initial-value", "declercq@gmail.com"; let description = document.querySelector(".KHxj8b.tL9Q4c"); description.setAttribute("data-initial-value", "Bonjour");')


# def search(ville):
#     driver.get(f'https://www.google.com/search?q=inurl%3Abusiness.site+%2B+%22{ville}%22')
#     sleep(25)
#     cookie_dialog()
#     go_last_page()  # Navigate to the last page of search results
#     urls = scraping_urls()
#     create_file_with_list(ville, urls)

# for ville in villes:
#     search(ville)
#     liste = retrieve_list_from_file(ville)
# list_temp = retrieve_list_from_file('narbonne')
# scrapping_datas(list_temp)
test_input()

while 1==1:
    sleep(2)
