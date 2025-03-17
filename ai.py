#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seleniumを使用してTwitterにログインし、Cookieを保存するサンプルコードです。
次回以降、保存したCookieを利用してスクレイピングを行うことができます。

【前提】
- SeleniumとChromeDriverがインストールされていること
  pip install selenium
- ChromeDriverのパスが通っているか、適切に設定されていること

【使用方法】
1. このスクリプトを実行すると、Twitterのユーザー名（またはメールアドレス）とパスワードの入力を求められます。
2. 自動でTwitterのログインページが開かれ、入力情報を用いてログインが試みられます。
3. ログイン後、現在のCookieが"cookies.json"に保存されます。
"""

import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def login_twitter(username, password):
    # Chromeオプションの設定
    options = Options()
    options.add_argument("--disable-notifications")
    # 必要に応じてヘッドレスモードを有効にする場合は以下のコメントを解除
    # options.add_argument("--headless")

    # ChromeDriverの初期化（chromedriverがパスにある場合）
    driver = webdriver.Chrome(options=options)
    
    # Twitterのログインページにアクセス
    driver.get("https://twitter.com/login")
    time.sleep(5)  # ページの読み込みを待機
    time.sleep(99)  # ログイン処理完了まで待機
    return driver

def save_cookies(driver, filepath="cookies.json"):
    # 現在のCookie情報を取得してJSONファイルに保存
    cookies = driver.get_cookies()
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(cookies, file, ensure_ascii=False, indent=2)
    print(f"Cookieは'{filepath}'に保存されました。")

def main():
    # ユーザーからTwitterの認証情報を入力
    username = input("Twitterのユーザー名またはメールアドレスを入力してください：")
    password = input("Twitterのパスワードを入力してください：")

    # TwitterにログインしてCookieを保存
    driver = login_twitter(username, password)
    save_cookies(driver)
    
    # ブラウザを終了
    driver.quit()

if __name__ == "__main__":
    main()
