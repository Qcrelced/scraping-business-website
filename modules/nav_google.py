from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

# Default style attribute for the button
# Use for click button next page when = transform: scale(0)
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
    xpath_button_page = "/html/body/div[6]/div/div[12]/div[1]/div[4]/div/div[3]/div[4]/a[1]"

    # Adjust XPath for omitted result page
    if omitted_result_page == True:
        xpath_button_page = "/html/body/div[5]/div/div[12]/div/div[4]/div/div[3]/div[4]/a[1]"

    # Scroll to the bottom of the first page
    while scroll_first_page:
        scrollY_before = driver.execute_script('return window.scrollY')
        driver.execute_script('window.scrollTo({top: document.documentElement.scrollHeight})')
        sleep(1.5)
        scrollY_after = driver.execute_script('return window.scrollY')
        if scrollY_after == scrollY_before:
            scroll_first_page = False

    # Continue navigating to the next page until the last page
    while not last_page_google:
        try:
            button_page_style = driver.find_element(By.XPATH, xpath_button_page).get_attribute('style')
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
                    (By.XPATH, xpath_button_page)))
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


def scraping():
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
    print(urls)
    return urls


# Connect to the target page (Google Search)
driver.get(f'https://www.google.com/search?q=inurl%3Abusiness.site+%2B+%22{request}%22')
sleep(20)

# Handle the cookie dialog
cookie_dialog()
# Navigate to the last page of search results
go_last_page()
scraping()
