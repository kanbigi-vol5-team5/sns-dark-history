from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle,os,sys
import time
import asyncio

COOKIES_PATH = 'sessions.pkl' # クッキーを保存するファイルの名前
X_URL = 'https://x.com' # XのURL
CHROME_UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
CHROME_WINDOW_SIZE = "2400x100"

class XPostsScraper:

    def __init__(self):
        logOutput("Initializing..")
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument(f"--window-size={CHROME_WINDOW_SIZE}")
        options.add_argument(f"--user-agent={CHROME_UA}")
        logOutput(f"Connecting to {os.environ['SELENIUM_URL']}..")
        self.driver = webdriver.Remote(
        command_executor = os.environ["SELENIUM_URL"],
        options=options)
        logOutput("Connected!")
        asyncio.run(self.login())

    async def login(self):
        logOutput("Loading cookies..")
        cookies = pickle.load(open(COOKIES_PATH,'rb'))
        self.driver.get(X_URL)
        for c in cookies:
            self.driver.add_cookie(c)
        logOutput("Loading cookies success!")

    async def getPosts(self, id, scroll_count=10):
        logOutput("Getting posts...")
        if id == "white":
            return []
        elif id == "black":
            return ["DARK_CONTENT"]
        self.driver.get(f'{X_URL}/{id}')
        tweets_text = []
        before_data = [""]
        for _ in range(scroll_count):
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                logOutput("Scrolling...")
                time.sleep(2)
                tweets_elements =  self.driver.find_elements(By.CSS_SELECTOR, "*[data-testid=\"tweetText\"]")
                logOutput("Text got!")
                current = [el.text.strip() for el in tweets_elements if el.text.strip()]
                tweets_text += current
                if len(before_data) > 0 and len(current) > 0 and (before_data[-1] == current[-1]):
                    break
                before_data = current
            except Exception as e:
                logOutput(f"Error: {e}")
        tweets_text = list(set(tweets_text))
        return tweets_text
    
    async def getIcon(self, id):
        self.driver.get(f'{X_URL}/{id}/photo')
        time.sleep(1)
        return self.driver.find_element(By.CSS_SELECTOR, "img[draggable=\"true\"]").get_attribute('src')

def logOutput(message):
    print(f"[XPostsScraper] {message}", file=sys.stdout, flush=True)

def login():
    options = webdriver.ChromeOptions()
    options.add_argument(f"--window-size={CHROME_WINDOW_SIZE}")
    options.add_argument(f"--user-agent={CHROME_UA}")
    driver = webdriver.Chrome(options=options)
    driver.get(f'{X_URL}/login')
    input("Xにログインしてください。ログインが完了したらEnterを押してください。")
    cookies = driver.get_cookies()
    pickle.dump(cookies,open(COOKIES_PATH,'wb'))
    driver.quit()
