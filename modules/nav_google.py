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
from modules.util import regex_tel
from modules.mail_export import mail_export
from modules.util import create_excel_datas

# Use for click button next page when = transform: scale(0)
DELAY = 50
button_attr_style_default: str = 'transform: scale(1);'
options = Options()  # Set up Chrome options
# options.add_argument('--headless=new')  # Commented for testing
driver = webdriver.Chrome(
    service=Service(),
    options=options
)


# Function to handle the cookie dialog
def cookie_dialog():
    print("---cookie_dialog open---")
    try:
        cookie = driver.find_element(By.ID, "CXQnmb")
        accept_button = cookie.find_element(By.ID, "L2AGLb")
        if accept_button is not None:
            accept_button.click()
    except NoSuchElementException:
        print("Cookie dialog not present")
    except Exception as e:
        print("cookie_dialog error, ", e)
    finally:
        print("---cookie_dialog clause---")


# Function to navigate to the last page of Google search results
def go_last_page(omitted_result_page=False):
    print("---go_last_page open---")
    last_page_google: bool = False
    scroll_first_page: bool = True
    sleep(2)  # Sleep for load page
    button_page = "T7sFge.sW9g3e.VknLRd"

    # Scroll to the bottom of the first page
    while scroll_first_page:
        scrollY_before = driver.execute_script('return window.scrollY')
        driver.execute_script('window.scrollTo({top: document.documentElement.scrollHeight})')
        sleep(1)  # Sleep for load page
        scrollY_after = driver.execute_script('return window.scrollY')
        if scrollY_after == scrollY_before:  # Button more result appear
            scroll_first_page = False
    # Find button "more result"
    try:
        driver.find_element(By.CLASS_NAME, "T7sFge.sW9g3e.VknLRd")
    except NoSuchElementException:
        print("Element not found")
    except Exception as e:
        print("Button error, ", e)
    # Continue navigating to the next page until the last page
    while not last_page_google:
        try:
            button_page_style = driver.find_element(By.CLASS_NAME, button_page).get_attribute('style')
        except NoSuchElementException:
            print("Button page style attribute not present")
            last_page_google = True
        except Exception as e:
            print("Error in button page style attribute", e)
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
        except Exception as e:
            print("Error in button omitted result", e)
        else:
            button_omitted_result.find_element(By.TAG_NAME, 'a').click()
            go_last_page(omitted_result_page=True)
        finally:
            pass
    if omitted_result_page == True:
        print("---go_last_page clause---")


# Scrap les URls après avoir parcouru toutes les pages
def scraping_urls():
    valeur_a_supprimer = ""  # Supprimes les liens vides
    urls = []
    i = 0
    # Récupère toutes les URLs
    for url in driver.find_elements(By.CLASS_NAME, "tjvcx.GvPZzd.cHaqb"):
        try:
            toto = url.find_element(By.TAG_NAME, "span").text
            url.text.replace(toto, "")
            urls.append(url)
        except NoSuchElementException:
            urls.append(url.text)
        except Exception as e:
            print("Append url in urls, ", e)
    # Parcours la liste pour supprimer les elements vides
    while i < len(urls):
        if urls[i] == valeur_a_supprimer:
            urls.remove(urls[i])
        else:
            i += 1
    # Créer un fichier avec toutes les URL
    return urls


def scrapping_datas(urls):
    entreprise_contact = {}
    i = 0
    # get num and name
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        # get name and tel of the website
        soup_name = soup.find("h1").getText()
        soup_tel = regex_tel(soup.find('a', attrs={"itemprop": "telephone"}).get("href"))
        # Update dict for excel
        entreprise_contact.update({soup_name: soup_tel})
        print(soup_name + '\n' + soup_tel + '\n -----------')
        i += 1
        if i == 1:
            return entreprise_contact
        sleep(45)


def form_input():
    driver.get("https://dermatologue-perpignan-blog-dinformations.business.site/")
    sleep(5)
    print('start')
    get_iframe = driver.execute_script("""
        let header = document.getElementsByClassName('SnapformContent tzdnMe')
        console.log(header)
        let frame = document.getElementsByClassName('SnapformFrame lud4Oc')
        frame = frame[0].querySelector('iframe')
        frame = frame.getAttribute('id')
        //frame = frame.getAttribute('src')
        return frame
    """)
    try:
        driver.switch_to.frame(get_iframe)
        print('switch réussi')
    except Exception as e:
        print('Error switch', e)

    driver.execute_script("""
        let email = document.querySelector('.whsOnd.zHQkBf[type="email"]');
        email.value = 'email@gmail.com';
        email.dispatchEvent(new Event('input', { bubbles: true })); // Déclencher l'événement 'input'
        
        let desc = document.querySelector('.KHxj8b.tL9Q4c');
        desc.value = 'Bonjour, cest Moi';
        desc.dispatchEvent(new Event('input', { bubbles: true })); // Déclencher l'événement 'input'
    """)
    driver.execute_script("""
        let button_form = document.querySelector('.U26fgb.O0WRkf.zZhnYe.e3Duub.C0oVfc.SS9F9d.M9Bg4d');
        button_form.click();
    """)


# Execute la recherche pour chaque ville
def search(ville):
    driver.get(f'https://www.google.com/search?q=inurl%3Abusiness.site+%2B+%22{ville}%22')
    sleep(15)
    cookie_dialog()
    go_last_page()  # Navigate to the last page of search results
    urls = scraping_urls()
    # create_file_with_list(ville, urls)
    # companies_urls = retrieve_list_from_file(f"{ville}.txt")
    datas = scrapping_datas(urls)
    create_excel_datas(datas, ville)
    mail_export(f'contact_entreprises_{ville}.xlsx')
