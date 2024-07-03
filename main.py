from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time

def setup_drivers():
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"

        options = webdriver.ChromeOptions()
        
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument("--disable-dev-shm-usage")  # Disable /dev/shm usage

        # options.add_argument('--headless')

        options.page_load_strategy = 'eager'
       
        return webdriver.Chrome(options=options)

url = "https://www.amazon.com/s?k=laptop"

driver = setup_drivers()
driver.get(url)

arr =[]
comps = driver.find_elements(By.XPATH, "//div[@data-index]")

for i in comps:
    try:
        name = i.find_element(By.CSS_SELECTOR, 'h2').text
        name = name.replace('\n', ' ')
    except:
        name = None
        
    try:
        priceElement = i.find_element(By.CLASS_NAME, 'a-price').text
        price = priceElement.replace('\n', '.')
    except:
        price =None

    try:
        url = i.find_element(By.CSS_SELECTOR, 'a.a-link-normal').get_attribute("href")
    except:
        url = None
    
    if name is not None and price is not None and url is not None:
        arr.append({"name":name,"price":price,"url":url})
    
df = pd.DataFrame(arr)
df.to_csv("output.csv")


time.sleep(10)
driver.quit()
