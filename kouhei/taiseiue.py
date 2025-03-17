from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pickle
import json

def get_twitter_posts(username, scroll_count=10):
    # ヘッドレスモードでChromeドライバーを起動
    options = Options()
    cookies_file = 'morokoshi.pkl'
    
    # Chromeドライバーのパスが通っているか確認してください
    driver = webdriver.Chrome(options=options)
    url = f"https://twitter.com/{username}"
    driver.get("")
    time.sleep(30)
    save_cookies(driver)
    load_cookies(driver)
    driver.get(url)
    
    # ページの読み込みを待機
    time.sleep(5)
    cookies = driver.get_cookies() # クッキーを取得する
    pickle.dump(cookies,open(cookies_file,'wb')) #
    
    # ページ下部までスクロールして投稿をロード（必要に応じてscroll_countを調整）
    for _ in range(scroll_count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
    
    # ツイートの本文を含む要素を取得（TwitterのHTML構造によりXPathは変更の可能性あり）
    tweets_elements = driver.find_elements(By.CSS_SELECTOR, "*[data-testid=\"tweetText\"]")
    print(len(tweets_elements))
    tweets_text = [el.text.strip() for el in tweets_elements if el.text.strip()]
    pickle.dump(cookies,open(cookies_file,'wb')) 
    driver.quit()
    return tweets_text

def save_cookies(driver, filepath="cookies.json"):
    # 現在のCookie情報を取得してJSONファイルに保存
    cookies = driver.get_cookies()
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(cookies, file, ensure_ascii=False, indent=2)
    print(f"Cookieは'{filepath}'に保存されました。")

def load_cookies(driver, filepath="cookies.json"):
    # 保存したCookie情報を読み込んで設定
    with open(filepath,
              "r", encoding="utf-8") as file:
        cookies = json.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

if __name__ == "__main__":
    username = input("対象のTwitterユーザー名（@は不要）を入力してください: ")
    posts = get_twitter_posts(username)
    print("取得した投稿:")
    for idx, post in enumerate(posts, start=1):
        print(f"{idx}: {post}")
