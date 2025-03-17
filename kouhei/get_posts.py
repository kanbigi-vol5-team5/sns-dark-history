from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle,os
import time

login_url = 'https://x.com/login' # ログインのページ
web_url = 'https://x.com/windymelt' # 入りたいページ
cookies_file = 'sessions.pkl' # クッキーを保存するファイルの名前
scroll_count = 30 # 何回スクロールするか

options = webdriver.ChromeOptions()
if(os.path.exists(cookies_file)):
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1200x1000")
    options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")
    # pass
driver = webdriver.Chrome(options=options)

# まだクッキーを持っていない場合新しくログインして保存する
if(not os.path.exists(cookies_file)):
    driver.get(login_url)
    time.sleep(500)
    
    cookies = driver.get_cookies()
    pickle.dump(cookies,open(cookies_file,'wb'))
# すでにクッキーを持っている場合読み込んで使う
else:
    cookies = pickle.load(open(cookies_file,'rb'))
    driver.get(web_url)
    for c in cookies:
        driver.add_cookie(c)

# やりたいことなど
tweets_text = []
before_data = [""]
driver.get(web_url)
for _ in range(scroll_count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        tweets_elements = driver.find_elements(By.CSS_SELECTOR, "*[data-testid=\"tweetText\"]")
        current = [el.text.strip() for el in tweets_elements if el.text.strip()]
        tweets_text += current
        if len(before_data) > 0 and len(current) > 0 and (before_data[-1] == current[-1]):
            break
        before_data = current
driver.save_screenshot("screenshot.png")
tweets_text = list(set(tweets_text))
print(tweets_text)
print(f"完了: {len(tweets_text)}件のツイートを取得しました。")
driver.quit()
pickle.dump(cookies,open(cookies_file,'wb')) 
driver.quit()
