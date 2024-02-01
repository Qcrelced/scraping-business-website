import random
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

DELAY = random.randint(50, 70)
global_urls = []
entreprise_contact = {}
# Use for click button next page when = transform: scale(0)
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


def scroll_down():
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


# Function to navigate to the last page of Google search results
def click_next_button(omitted_result_page=False, with_omitted_result=False, click=False):
    print("---go_last_page open---")
    button_page: str = "T7sFge.sW9g3e.VknLRd"
    last_page_google: bool = False

    # Find button "more result"
    if click == True:
        try:
            driver.find_element(By.CLASS_NAME, button_page)
        except NoSuchElementException:
            print("Element button next page")
        except Exception as e:
            print("Button next page error, ", e)
        # Continue navigating to the next page until the last page
        while not last_page_google:
            try:
                button_page_style = driver.find_element(By.CLASS_NAME, button_page).get_attribute('style')
            except NoSuchElementException:
                print("Button page style attribute not present")
                last_page_google = True
                continue
            except Exception as e:
                print("Error in button page style attribute", e)
                continue
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


# Scrap les URls après avoir parcouru toutes les pages
def scraping_urls(div):
    counter = 0
    temp = []
    # Récupère toutes les URLs
    print("scraping url")
    for url in driver.find_element(By.ID, div).find_elements(By.CLASS_NAME, "tjvcx.GvPZzd.cHaqb"):
        print(url.text)
        try:
            span_text = url.find_element(By.TAG_NAME, "span").text
            sleep(random.randint(20, 30))
            url = url.text.replace(span_text, "")
            global_urls.append(url)
            temp.append(url)
        except NoSuchElementException:
            print(url.text)
            global_urls.append(url.text)
            temp.append(url.text)
        except Exception as e:
            print("Append url in urls, ", e)
        else:
            counter += 1
    return temp


def clear_globals_urls(urls):
    valeur_a_supprimer = ""  # Supprimes les liens vides
    i = 0
    # Parcours la liste pour supprimer les elements vides
    while i < len(urls):
        if urls[i] == valeur_a_supprimer:
            urls.remove(urls[i])
        else:
            i += 1
    # Créer un fichier avec toutes les URL


def scrapping_datas(urls):
    clear_globals_urls(urls)
    print(urls)
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    ]    # get num and name
    for url in urls:
        print(url)
        sleep(random.randint(25, 35))
        try:
            driver_options = Options()
            driver_options.add_argument(f'user-agent={random.choice(user_agents)}')
            driver_options.add_argument('--headless=new')  # Commented for testing
            driver = webdriver.Chrome(options = driver_options)
            driver.get(f'https://webcache.googleusercontent.com/search?q=cache%3A{url}')
            # r = requests.get(f'https://webcache.googleusercontent.com/search?q=cache%3A{url}')
        except Exception as e:
            print(e)
            continue
        # On regarde le Code de page
        #if driver.status_code == 429:
        #    print('Rate limit reached')
        #    break
        #elif r.status_code == 404:
        #    print(f'Info: Error 404')
        #    continue
        #elif r.status_code != 200:
        #    print(f'Error: {r.status_code}. Try a different proxy or user-agent')
        #    break

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # get name and tel of the website
        soup_name = soup.find("h1").getText()
        soup_tel = regex_tel(soup.find('a', attrs={"itemprop": "telephone"}).get("href"))
        # Update dict for excel
        entreprise_contact.update({soup_name: soup_tel})
        print(soup_name + '\n' + soup_tel + '\n -----------')


def form_input():
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
    is_possible = True
    is_possible2 = True
    name_div = "arc-srp_"
    num_div = 110
    div = name_div + str(num_div)

    driver.get(f'https://www.google.com/search?q=inurl%3Abusiness.site+%2B+%22{ville}%22')
    sleep(15)
    cookie_dialog()
    scroll_down()
    try:
        urls = scraping_urls("search")  # Navigate to the last page of search results
        scrapping_datas(urls)
        print("hello")
    except Exception as e:
        print("Error div search ", e)
    # Before click button
    while is_possible == True:
        try:
            print(div)
            urls = scraping_urls(div)
            scrapping_datas(urls)

        except Exception as e:
            is_possible = False
            print('Error num_div', e)
        finally:
            print(global_urls)
            print(entreprise_contact)
        if num_div == 190:
            num_div = 1100
        else:
            num_div = num_div + 10
        div = name_div + str(num_div)

    # After click button
    while is_possible2 == True:
        try:
            click_next_button(click=True)
            urls = scraping_urls(div)
            scrapping_datas(urls)
            num_div += 10
        except:
            is_possible2 == False
            print("STOP")

    clear_globals_urls()
    # create_file_with_list(ville, urls)
    # companies_urls = retrieve_list_from_file(f"{ville}.txt")
    create_excel_datas(entreprise_contact, ville)
    mail_export(f'contact_entreprises_{ville}.xlsx')
