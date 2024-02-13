import random
from datetime import datetime
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

global_urls = []
# Use for click button next page when = transform: scale(0)
button_attr_style_default: str = 'transform: scale(1);'
options = Options()  # Set up Chrome options
options.add_argument('--headless=new')  # Commented for testing
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


def scroll_down():
    print("---scroll_down open ---")
    scroll_first_page: bool = True
    sleep(2)  # Sleep for load page
    # Scroll to the bottom of the first page
    while scroll_first_page:
        scrollY_before = driver.execute_script('return window.scrollY')
        driver.execute_script('window.scrollTo({top: document.documentElement.scrollHeight})')
        sleep(1)  # Sleep for load page
        scrollY_after = driver.execute_script('return window.scrollY')
        if scrollY_after == scrollY_before:  # Button more result appear
            scroll_first_page = False
    print("---end scroll ---")


def verify_response():
    try:
        driver.find_element(By.ID, 'infoDiv')
    except:
        pass
    else:
        print("ERROR : Limit request, TOO MANY REQUEST !")
        print(datetime.now().strftime("%D %H:%M:%S"))
        print("TAPER: GO , pour continuez")
        restart = str(input(" > "))
        while restart != 'GO':
            restart = str(input(" > "))


# Function to navigate to the last page of Google search results
def click_next_button():
    button_page: str = "T7sFge.sW9g3e.VknLRd"
    last_page_google: bool = False
    try:
        button_page_style = driver.find_element(By.CLASS_NAME, button_page).get_attribute('style')
    except NoSuchElementException:
        print("Button page style attribute not present")
        # last_page_google = True
    except Exception as e:
        print("Error in button page style attribute", e)
    else:
        if button_page_style != button_attr_style_default:
            last_page_google = True
            print('info: last_page_google end while button page')
            return last_page_google
        else:
            wait = WebDriverWait(driver, 10)
            next_button_page = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, button_page)))
            driver.execute_script("arguments[0].click();", next_button_page)
    finally:
        sleep(2)

    # if with_omitted_result:
    #     # If omitted result page, click on the "Omitted results" button and call the function recursively
    #     if omitted_result_page == False:
    #         try:
    #             button_omitted_result = driver.find_element(By.ID, 'ofr')
    #         except NoSuchElementException:
    #             print("Element button omitted result not present")
    #         except Exception as e:
    #             print("Error in button omitted result", e)
    #         else:
    #             button_omitted_result.find_element(By.TAG_NAME, 'a').click()
    #             go_last_page(omitted_result_page=True)
    #         finally:
    #             pass
    print("---go_last_page clause---")


def clear_globals_urls(urls):
    valeur_a_supprimer = ""  # Supprimes les liens vides
    i = 0
    # Parcours la liste pour supprimer les elements vides
    while i < len(urls):
        if urls[i] == valeur_a_supprimer:
            urls.remove(urls[i])
        else:
            i += 1
    return urls


# Scrap les URls après avoir parcouru toutes les pages
def scraping_urls():
    print("---scraping_url open---")
    liste = []
    # Récupère toutes les URLs
    for url in driver.find_elements(By.CLASS_NAME, "tjvcx.GvPZzd.cHaqb"):
        try:
            span_text = url.find_element(By.TAG_NAME, "span").text
            url = url.text.replace(span_text, "")
            liste.append(url)
        except NoSuchElementException:
            liste.append(url.text)
        except Exception as e:
            print("Append url in urls, ", e)
    print("---scraping_url clause")
    clear_globals_urls(liste)
    return liste


def scrapping_datas(urls, entreprise_contact):
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    ]  # get num and name
    for url in urls:
        print("SCRAP URL : ", url)
        sleep(random.randint(35, 40))
        try:
            verify_response()
            driver_options = Options()
            driver_options.add_argument(f'user-agent={random.choice(user_agents)}')
            driver_options.add_argument('--headless=new')  # Commented for testing
            driver = webdriver.Chrome(options=driver_options)
            driver.get(f'https://webcache.googleusercontent.com/search?q=cache%3A{url}')
        except Exception as e:
            print(e)
            continue
        try:

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # get name and tel of the website
            soup_name = soup.find("h1").getText()
            soup_tel = regex_tel(soup.find('a', attrs={"itemprop": "telephone"}).get("href"))
            entreprise_contact.update({soup_name: soup_tel})
            print(soup_name + '\n' + soup_tel + '\n -----------')
        except:
            pass

        # Update dict for excel


def form_input():
    sleep(5)
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
    try:
        driver.execute_script("""
            let email = document.querySelector('.whsOnd.zHQkBf[type="email"]');
            email.value = 'email@gmail.com';
            email.dispatchEvent(new Event('input', { bubbles: true })); // Déclencher l'événement 'input'

            let desc = document.querySelector('.KHxj8b.tL9Q4c');
            desc.value = 'Bonjour, cest Moi';
            desc.dispatchEvent(new Event('input', { bubbles: true })); // Déclencher l'événement 'input'

            let button_form = document.querySelector('.U26fgb.O0WRkf.zZhnYe.e3Duub.C0oVfc.SS9F9d.M9Bg4d');
            button_form.click();
        """)
    except Exception as e:
        print("Error on execute script", e)


# Execute la recherche pour chaque ville
def search(ville):
    contact = {}
    print(ville)
    end = False
    driver.get(f'https://www.google.com/search?q=inurl%3Abusiness.site+%2B+%22{ville}%22')
    sleep(15)
    cookie_dialog()
    scroll_down()
    sleep(5)
    try:
        urls = scraping_urls()
        print("URls: ", urls)
        for url in urls:
            global_urls.append(url)
        scrapping_datas(urls, contact)
    except Exception as e:
        print("erreur sur la premiere page", e)
    finally:
        print("fin de la premiere page")
    while not end:
        click = click_next_button()
        if click:
            end = True
        else:
            list = []
            urls = scraping_urls()
            for element in urls:
                if element not in global_urls:
                    list.append(element)
            print(list)
            scrapping_datas(list, contact)
            for url in list:
                global_urls.append(url)
    print(global_urls)
    print(contact)
    clear_globals_urls(global_urls)
    # create_file_with_list(ville, urls)
    # companies_urls = retrieve_list_from_file(f"{ville}.txt")
    create_excel_datas(contact, ville)
    mail_export(f'contact_entreprises_{ville}.xlsx')
