from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle,os
import time

class XPostsScraper:
    login_url = 'https://x.com/login' # ログインのページ
    web_url = 'https://x.com/' # 入りたいページ
    cookies_file = 'sessions.pkl' # クッキーを保存するファイルの名前

    options = webdriver.ChromeOptions()
    if(os.path.exists(cookies_file)):
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=2400x100")
        options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)

    def __init__(self):
        self.login()

    def login(self):
        if(not os.path.exists(self.cookies_file)):
            self.performLogin()
        else:
            cookies = pickle.load(open(self.cookies_file,'rb'))
            self.driver.get(self.web_url)
            for c in cookies:
                self.driver.add_cookie(c)

    def performLogin(self):
        self.driver.get(self.login_url)
        time.sleep(60)
        cookies = self.driver.get_cookies()
        pickle.dump(cookies,open(self.cookies_file,'wb'))
    def getPosts(self, id, scroll_count=3):
        self.driver.get(f'https://x.com/{id}')
        tweets_text = []
        before_data = [""]
        for _ in range(scroll_count):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                tweets_elements = self.driver.find_elements(By.CSS_SELECTOR, "*[data-testid=\"tweetText\"]")
                current = [el.text.strip() for el in tweets_elements if el.text.strip()]
                tweets_text += current
                if len(before_data) > 0 and len(current) > 0 and (before_data[-1] == current[-1]):
                    break
                before_data = current
        tweets_text = list(set(tweets_text))
        return tweets_text

