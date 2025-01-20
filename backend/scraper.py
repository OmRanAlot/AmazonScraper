from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import pandas as pd
from name_parser import get_specs
import csv
import os

def get_data(item, maxPages):
    maxPages = int(str(maxPages))

    print("opened function!")
 
    result_arr = []
    driver = setup_drivers_chrome()
    start_url = "https://www.amazon.com/s?k="+str(item)
    page_num = 1

    while page_num<=int(maxPages):
        print("opened url")
        new_url = start_url+"&page="+str(page_num)
        driver.get(url=new_url) 

        #get all the computer elements or refresh if cant find any
        while True:
            try:
                comps = WebDriverWait(driver,3).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@data-index > 1]")))
                break
            except TimeoutException:
                driver.refresh()
        # elements = driver.find_elements(By.XPATH, "//div[@data-index > 1]")

        #get the data for each computer
        for i in comps:
            result_arr.append(get_data_from_element(i))
            
            
        page_num = page_num+1
        

    driver.quit()
    try:
        df = clean_data(pd.DataFrame(result_arr))
        save = pd.DataFrame(df)
    except:
        save = pd.DataFrame(result_arr)
    

    try:
        save["CPU"] = save["specs"].apply(lambda x: x.get("CPU"))
        save["GPU"] = save["specs"].apply(lambda x: x.get("GPU"))
        save["RAM"] = save["specs"].apply(lambda x: x.get("RAM"))
        save["Storage"] = save["specs"].apply(lambda x: x.get("Storage"))
    except:
        pass

    save.to_csv('output.csv', mode='a', index=False)

    return df
   

def get_data_from_element(element):

    def safe_extract(element, selectorType, selector, attr=None, default=""):
        try:
            x = element.find_element(selectorType, selector)
            return x.get_attribute(attr) if attr else x.text
        except:
            return default


    name = safe_extract(element, By.CSS_SELECTOR, 'h2', attr="innerText").replace('\n', ' ')
    price = str(safe_extract(element, By.CLASS_NAME, 'a-price', default= -1)).replace('\n', '.')
    url = safe_extract(element, By.CSS_SELECTOR, 'a.a-link-normal', attr="href", default="")
    amountPurchased = safe_extract(element, By.CSS_SELECTOR, 'div.a-row.a-size-base > span.a-size-base.a-color-secondary', default=-1)
    review = safe_extract(element, By.XPATH, ".//span[@class='a-icon-alt']", attr="innerHTML")
    numberOfReviews = safe_extract(element, By.CSS_SELECTOR, "div.a-row.a-size-small > span:nth-of-type(2) > div > a > span", attr="innerHTML", default=-1)
    specs = get_specs(name)
    
    try:
        amountPurchased = amountPurchased[:amountPurchased.find("+")]
        if amountPurchased.find("K") > -1:
            amountPurchased = int(float(amountPurchased.replace("K",""))*1000)       
        if amountPurchased == "More Buying Choice":
            amountPurchased = -1
    except:
        pass

    print(name, specs, price, url, amountPurchased, review, numberOfReviews)
    return {"name":name,
            "specs":specs,
            "price":price,
            "url":url, 
            "amountPurchased":amountPurchased,
            "review":review,
            "numberOfReviews":numberOfReviews
    }


def save_to_csv(dataframe):
    dataframe.to_csv('output.csv', mode='a', index=False)

def setup_drivers_chrome():
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
        options.add_argument("--enable-unsafe-swiftshader")
        options.add_argument("--blink-settings=imagesEnabled=false")  # Disable images

        options.add_argument('--headless') # it being working whenever it feels like i swear

        options.page_load_strategy = 'normal'
       
        return webdriver.Chrome(options=options)

def clean_data(df):
    df['price'] = df['price'].str.replace('[\$,]', '', regex=True)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')

    # remove rows with "customers" or "consider" in the name
    df = df[~df['name'].str.contains("customers|consider", case=False, na=False)]
    
    # remove rows with names that are too short
    df = df[df['name'].str.len() > 30]   
    
    # remove rows with prices that are too low
    df = df[df['price'] > 30] 

    df.reset_index(drop=True, inplace=True)
    result_arr = df.to_dict('records')
    print("Cleaned data successfully")
    return result_arr

if __name__ == "__main__":
    get_data("laptop",20)
    get_data("laptops with ryzen CPU",20)
    get_data("laptops with GPU",20)
    get_data("laptops with intel CPU",20)
    get_data("laptops with AMD CPU",20)
    get_data("laptops with 16gb RAM",20)
    get_data("laptops with 32gb RAM",20)
