from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import statistics
import name_parser

def setup_drivers():
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"

        options = webdriver.ChromeOptions()
        
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument("--disable-dev-shm-usage")  # Disable /dev/shm usage
        # options.add_argument("--disable-javascript") 
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        options.add_argument("window-size=1920,1080")

    

        # options.add_argument('--headless')

        options.page_load_strategy = 'normal'
       
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_end_time(start_time):
    end_time = time.time()
    time_taken = round(end_time - start_time, 4)+1 #add 1 because it takes some time to load the webpage
    print("Time Taken on this page:", time_taken)
    time_arr.append(time_taken)

def amazon_scraper(url):
    #make a variable for the results array seperately
    #or you can make it here and then return it but when I do that my computer freezes :P
    
    start_time_local = time.time()
    driver.get(url)
    running = True
    while running:
        # comps = WebDriverWait(driver,5).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@data-index]")))
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
                specs = name_parser.get_data(name.lower())
                result_arr.append({"name":name,"Specs":specs,"price":price,"url":url})
        
        try:
            # next_button = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.CLASS_NAME, 's-pagination-next')))
            next_url = driver.find_element(By.CLASS_NAME, 's-pagination-next').get_attribute("href")
            get_end_time(start_time_local)
            start_time_local=time.time()
            driver.get(next_url)
            
        except:
            print("closing drivers")
            driver.close()
            driver.quit()
            print("leaving loop")
            break
        
            
            

result_arr = []
start_time = time.time()
driver = setup_drivers()
time_arr=[]

url = "https://www.amazon.com/s?k=laptop"
amazon_scraper(url)

df = pd.DataFrame(result_arr)
df.to_csv("output.csv")

end_time = time.time()
print("Time taken: ", round(end_time - start_time, 4))

time_arr.pop()
print("Average time: ",statistics.mean(time_arr))

