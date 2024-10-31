from settings import *
from time import time
import pandas as pd
import time
import statistics
from datetime import datetime
from selenium.webdriver.common.by import By
import name_parser
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from analyze_data import *

time_arr=[]
result_arr = []
driver = setup_drivers_chrome()
start_url = "https://www.amazon.com/s?k=laptop"

start_time=time.time()


page_num=1

print("started loop")
while page_num<=MAX_PAGES:
    print("opened url")
    new_url = start_url+"&page="+str(page_num)
    driver.get(url=new_url) 


    while True:
        try:
            comps = WebDriverWait(driver,3).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@data-index]")))
            break
        except TimeoutException:
            driver.refresh()
    for i in comps:
        
        #get the name
        try:
            name = i.find_element(By.CSS_SELECTOR, 'h2').text
            name = name.replace('\n', ' ')
        except:
            name = ""
        #get the price        
        try:
            priceElement = i.find_element(By.CLASS_NAME, 'a-price').text
            price = priceElement.replace('\n', '.')
        except:
            price = -1
        #get the url
        try:
            url = i.find_element(By.CSS_SELECTOR, 'a.a-link-normal').get_attribute("href")
        except:
            url = ""

        #get the amountPurchased  
        try:
            amountPurchased = i.find_element(By.CSS_SELECTOR, 'div.a-row.a-size-base > span.a-size-base.a-color-secondary').text
            #parse the amountPurchased
            amountPurchased = amountPurchased[:amountPurchased.find("+")]
            if amountPurchased.find("K") > -1:
                amountPurchased = int(float(amountPurchased.replace("K",""))*1000)       
            if amountPurchased == "More Buying Choice":
                amountPurchased = -1
        except:
            amountPurchased = -1

        #get reviews
    
        try:
            review = i.find_element(By.XPATH, ".//span[contains(@aria-label, 'out of 5 stars')]").get_attribute("aria-label")
            review = int(review[:3])
        except:
            review = ""

        # get number of reviews
        try:
            numberOfReviews = i.find_element(By.XPATH, ".//span[contains(@aria-label, 'ratings')]").get_attribute("aria-label")
        except:
            numberOfReviews = -1

        try:
            specs = name_parser.get_data(name.lower())
        except:
            specs = {}
        finally:
            result_arr.append({"name":name,
                               "Specs":specs,
                               "price":price,
                               "url":url, 
                               "amountPurchased":amountPurchased,
                               "review":review,
                               "numberOfReviews":numberOfReviews})

    #Time Taken
    end_time = time.time()
    time_taken = round(end_time - start_time, 4)
    # print("Time Taken on this page:", time_taken)
    time_arr.append(time_taken)   
  
    page_num = page_num+1
    
    start_time = time.time()
    
# print(result_arr)
driver.quit()
df = pd.DataFrame(result_arr)
print(df.head(10))
clean_data(df)
average_time = round(statistics.mean(time_arr), 4)

print("Time taken: ", sum(time_arr))
print("Average time: ",str(average_time)+" seconds per page")
