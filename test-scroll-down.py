from time import time
from time import sleep
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

last_page_google: bool = False
button_attr_style: str = 'transform: scale(1);'
button_page = None
request: str = str(input("Ville : "))
request = "perpignan"
serp_element = []
serp_rank: int = 1

# to control a Chrome window in headless mode
options = Options()
# options.add_argument('--headless=new') # comment it for testing

# initialize a web driver instance with the
# specified options
driver = webdriver.Chrome(
    service=Service(),
    options=options
)

# connect to the target page
driver.get(f"https://www.google.com/search?q=inurl%3Abusiness.site+%2B+%22{request}%22")

# scraping logic...
try:
    # select the dialog and accept the cookie policy
    cookie_dialog = driver.find_element(By.ID, "CXQnmb")
    accept_button = cookie_dialog.find_element(By.ID, "L2AGLb")
    if accept_button is not None:
        accept_button.click()
        sleep(5)
except NoSuchElementException:
    print("Cookie dialog not present")
finally:
    pass

driver.execute_script("window.scrollTo(0,20000)")
sleep(2)

while last_page_google == False:
    # Get element button
    try:
        button_page_find = driver.find_element(By.XPATH,"/html/body/div[6]/div/div[12]/div[1]/div[4]/div/div[3]/div[4]/a[1]")
        button_page = button_page_find
    except NoSuchElementException:
        print("No Element")
        pass
    if (button_page.get_attribute('style')) != button_attr_style:
        last_page_google = True
    else:
        wait = WebDriverWait(driver, 10)
        button_page = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div/div[12]/div[1]/div[4]/div/div[3]/div[4]/a[1]")))
        driver.execute_script("arguments[0].scrollIntoView();", button_page)
        button_page2 = driver.find_element(By.XPATH,"/html/body/div[6]/div/div[12]/div[1]/div[4]/div/div[3]/div[4]/a[1]")
        driver.execute_script("arguments[0].click();", button_page2)
        sleep(2)



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


    links = driver.find_elements(By.CLASS_NAME, "tjvcx GvPZzd cHaqb")
    print(links)
    # data extraction logic
    url = serp_title_a.get_attribute("href")
    title = serp_title_h3.get_attribute("innerText")
    description = serp_description_div.get_attribute("innerText")

    # populate a new SERP data element and
    # add it to the list
    serp_element = {
        'rank': serp_rank,
        'url': url,
        'title': title,
        'description': description
    }
    serp_element.update(serp_element)
    serp_rank += 1
    print(serp_element)

while (1 == 1):
    sleep(10)
# close the browser and free up the resources
driver.quit()
