from selenium import webdriver

MAX_PAGES = 5

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
    
        options.add_argument('--headless') # it being working whenever it feels like i swear

        options.page_load_strategy = 'normal'
       
        return webdriver.Chrome(options=options)

def clean_data(df):
    try:
        df['price'] = df['price'].str.replace('[\$,]', '', regex=True).astype(float).astype(int)
        
    except:
        pass
    df = df.dropna(subset=['Specs'])
    df.reset_index(drop=True, inplace=True)

    # print(df.head(10))
    df.to_csv("output.csv")

    print("Cleaned data successfully")
