from classes import *
from time import time
import pandas as pd
import time
import statistics
from datetime import datetime
from selenium.webdriver.common.by import By
import name_parser

time_arr=[]
result_arr = []

driver = setup_drivers_chrome()

start_url = "https://www.amazon.com/s?k=laptop"
running = True

#make a variable for the results array seperately
#or you can make it here and then return it but when I do that my computer freezes :P
print("stared scraping")
driver.get(start_url)
page_num=1

print("started loop")
while page_num<10:
    
    # comps = WebDriverWait(driver,5).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@data-index]")))
    start_time=time.time()
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

    #Time Taken
    end_time = time.time()
    page_num = page_num+1
    time_taken = round(end_time - start_time, 4)
    print("Time Taken on this page:", time_taken)
    time_arr.append(time_taken)   
  
    new_url = start_url+"&page="+str(page_num)
    driver.get(url=new_url)    
    

driver.quit()
df = pd.DataFrame(result_arr)
df.to_csv("output.csv")

average_time = statistics.mean(time_arr)

now = datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")

with open('time.txt', 'w') as f:
    f.write(
        str({'time ran': now,
         'time_taken': sum(time_arr),
         'avergae_time': average_time}) + '\n'
            )


print("Time taken: ", sum(time_arr))
print("Average time: ",average_time)
