from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

button_attr_style_default: str = 'transform: scale(1);'
request: str = str(input("Ville : "))  ###TEMP###
request = "perpignan"  ###TEMP###
options = Options()
# options.add_argument('--headless=new')  # comment it for testing
driver = webdriver.Chrome(
    service=Service(),
    options=options
)
WebDriverWait(driver, 5)


def cookie_dialog():
    try:
        # select the dialog and accept the cookie policy
        cookie_dialog = driver.find_element(By.ID, "CXQnmb")
        accept_button = cookie_dialog.find_element(By.ID, "L2AGLb")
        if accept_button is not None:
            accept_button.click()
    except NoSuchElementException:
        print("Cookie dialog not present")
    except:
        print("fiend element error")
    finally:
        print("---cookie_dialog clause---")


def go_last_page(omitted_result_page=False):
    last_page_google: bool = False
    scroll_first_page: bool = True
    xpath_button_page = "/html/body/div[6]/div/div[12]/div[1]/div[4]/div/div[3]/div[4]/a[1]"
    if omitted_result_page == True:
        xpath_button_page = "/html/body/div[5]/div/div[12]/div/div[4]/div/div[3]/div[4]/a[1]"
    while scroll_first_page:
        scrollY_before = driver.execute_script('return window.scrollY')
        driver.execute_script('window.scrollTo({top: document.documentElement.scrollHeight})')
        sleep(1.5)
        scrollY_after = driver.execute_script('return window.scrollY')
        if scrollY_after == scrollY_before:
            scroll_first_page = False
    while not last_page_google:
        # Get element button
        try:
            button_page_style = driver.find_element(By.XPATH, xpath_button_page).get_attribute('style')
        except NoSuchElementException:
            print("button page style attribut not present")
            last_page_google = True
        except:
            print("Error button page style attribut")
        else:
            if button_page_style != button_attr_style_default:
                last_page_google = True
                print('info: last_page_google end while button page')
            else:
                wait = WebDriverWait(driver, 10)
                next_button_page = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, xpath_button_page)))
                driver.execute_script("arguments[0].click();", next_button_page)  # click with JS the button
        finally:
            sleep(2)

    if omitted_result_page == False:
        try:
            button_omitted_result = driver.find_element(By.ID, 'ofr')
        except NoSuchElementException:
            print("Element button omitted result not present")
        except:
            print("Error button omitted result")
        else:
            button_omitted_result.find_element(By.TAG_NAME, 'a').click()
            go_last_page(omitted_result_page=True)
        finally:
            pass
    print("---go_last_page clause---")


def scrap_urls():
    search_div = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'search')))
    serp_divs = search_div.find_elements(By.CSS_SELECTOR, "div[jscontroller][jsaction][data-hveid][data-ved]")
    for serp_div in serp_divs:
        # to ignore not useful SERP elements
        try:
            serp_title_h3 = serp_div.find_element(By.CSS_SELECTOR, "h3")
            serp_title_a = serp_title_h3.find_element(By.XPATH, './..')
            serp_description_div = serp_div.find_element(By.CSS_SELECTOR, "[data-sncf='1']")
        except NoSuchElementException:
            continue

        list_link = []
        for link in driver.find_elements(By.CLASS_NAME, "tjvcx GvPZzd cHaqb"):
            list_link.append(link)
        for link in list_link:
            print(link)


# connect to the target page
driver.get(f'https://www.google.com/search?q=inurl%3Abusiness.site+%2B+%22{request}+%2B+"vin"')
cookie_dialog()
go_last_page()
sleep(500)
