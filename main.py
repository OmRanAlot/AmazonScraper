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
from datetime import datetime

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
        options.add_argument("--log-level=3")  # Suppress JavaScript errors in logs
    
        # options.add_argument('--headless')

        options.page_load_strategy = 'normal'
       
        return webdriver.Chrome(options=options)


def amazon_scraper(url):
    #make a variable for the results array seperately
    #or you can make it here and then return it but when I do that my computer freezes :P
    print("stared scraping")
    driver.get(url)
    running = True
    print("started loop")
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

global result_arr; result_arr = []
start_time = time.time()
driver = setup_drivers()
time_arr=[]
start_url = "https://www.amazon.com/s?k=laptop"

for i in range(25):
    start_time_local=time.time()
    amazon_scraper(start_url+"&page="+str(i))
    end_time = time.time()
    time_taken = round(end_time - start_time, 4)+1 #add 1 because it takes some time to load the webpage
    print("Time Taken on this page:", time_taken)
    time_arr.append(time_taken)
    

driver.quit()
df = pd.DataFrame(result_arr)
df.to_csv("output.csv")

end_time = time.time()
time_taken = round(end_time - start_time, 4)
time_arr.pop()
average_time = statistics.mean(time_arr)

now = datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")

with open('time.txt', 'w') as f:
    f.write(
        str({'time ran': now,
         'time_taken': time_taken,
         'avergae_time': average_time}) + '\n'
            )


print("Time taken: ", time_taken)
print("Average time: ",average_time)

