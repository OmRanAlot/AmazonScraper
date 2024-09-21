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

print("opened url")
start_time=time.time()
driver.get(start_url)

page_num=1

print("started loop")
while page_num<=MAX_PAGES:
    # time.sleep(3)
    comps = WebDriverWait(driver,5).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@data-index]")))
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

    #Time Taken
    end_time = time.time()
    time_taken = round(end_time - start_time, 4)
    print("Time Taken on this page:", time_taken)
    time_arr.append(time_taken)   
  
    page_num = page_num+1
    new_url = start_url+"&page="+str(page_num)
    start_time = time.time()
    driver.get(url=new_url)    
    

driver.quit()
df = pd.DataFrame(result_arr)
df['price'] = df['price'].str.replace('[\$,]', '', regex=True).astype(float).astype(int)

get_basic_stats(df)

df_filtered = df[df['name'].str.len() >= 40]
get_basic_stats(df_filtered)
df_filtered.to_csv("output.csv")

average_time = round(statistics.mean(time_arr), 4)

print("Time taken: ", sum(time_arr))
print("Average time: ",str(average_time)+" seconds per page")
