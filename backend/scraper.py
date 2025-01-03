from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import pandas as pd
from backend.name_parser import get_specs

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
                # review = i.find_element(By.XPATH, "//a[contains(@class, 'a-popover-trigger')]").get_attribute("aria-label")
                # review = i.find_element(By.CSS_SELECTOR, "div.a-row.a-size-small > span.a-declarative > a[aria-label]")
                review = i.find_element(By.XPATH, ".//span[@class='a-icon-alt']").get_attribute("innerHTML")
                #string
                
            except:
                review = ""

            # get number of reviews
            try:
                # numberOfReviews = i.find_element(By.XPATH, "//span[contains(@class, 'a-size-small puis-normal-weight-text s-underline-text')]")
                numberOfReviews = i.find_element(By.CSS_SELECTOR, "div.a-row.a-size-small > span:nth-of-type(2) > div > a > span").get_attribute("innerHTML")
                
            except:
                numberOfReviews = -1

            try:
                specs = get_specs(name.lower())
                pass
            except:
                specs = {}
            finally:
                result_arr.append({"name":name,
                                "specs":specs,
                                "price":price,
                                "url":url, 
                                "amountPurchased":amountPurchased,
                                "review":review,
                                "numberOfReviews":numberOfReviews})
       
        page_num = page_num+1
        

    driver.quit()
    df = pd.DataFrame(result_arr)
    print(df)
    return clean_data(df)
   
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

        options.add_argument('--headless') # it being working whenever it feels like i swear

        options.page_load_strategy = 'normal'
       
        return webdriver.Chrome(options=options)

def clean_data(df):
    try:
        df['price'] = df['price'].str.replace('[\$,]', '', regex=True).astype(float).astype(int)
    except:
        pass

    print("Cleaning data...")
    # df = df.dropna(subset=['Specs'])
    # df = df[df['numberOfReviews'] != -1]
    print("Cleaning data2.....")

    df = df[~df['name'].str.contains("customers|consider", case=False, na=False)]
    df = df[df['name'].str.len() > 30]    

    df.reset_index(drop=True, inplace=True)
    result_arr = df.to_dict('records')
    print("Cleaned data successfully")
    # print(result_arr)
    return result_arr

if __name__ == "__main__":
    get_data("laptops",1)

