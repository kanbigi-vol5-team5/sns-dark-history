import re
import sys
import pandas as pd
from datetime import datetime, timedelta

# snscrapeライブラリ
import snscrape.modules.twitter as sntwitter

def get_username_from_input(user_input: str) -> str:
    """
    入力が @ユーザ名 か URL だった場合に対応してユーザ名を抽出する。
    """
    user_input = user_input.strip()
    
    # もしURL形式(例: https://twitter.com/xxxx)の場合は正規表現でユーザ名を取得
    if "twitter.com" in user_input or "x.com" in user_input:
        pattern = r"(?:twitter\.com|x\.com)/([A-Za-z0-9_]+)"
        match = re.search(pattern, user_input)
        if match:
            return match.group(1)
        else:
            print("URLからユーザ名を抽出できませんでした。")
            sys.exit(1)
    
    # @が先頭についている場合は取り除く
    if user_input.startswith("@"):
        user_input = user_input[1:]
    
    return user_input


def scrape_user_tweets(username: str, days: int, output_csv: str):
    """
    snscrapeを用いて指定ユーザの過去days日間のツイートを取得し、CSVに書き出す。
    """
    # 現在時刻を基準にdays日前の日付を計算
    since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    # untilは「その日付の直前まで」が対象になるため、本日の日付を指定
    until_date = datetime.now().strftime("%Y-%m-%d")
    
    # snscrape用のクエリ文字列を作成
    # 例: "from:elonmusk since:2025-03-01 until:2025-03-16"
    query = f"from:{username} since:{since_date} until:{until_date}"
    
    # ツイートを格納するリスト
    tweets_data = []
    
    print(f"ユーザ: {username}, 過去{days}日分のツイートを取得します...")
    
    # TwitterSearchScraperでツイート取得
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        # 必要に応じて取りたいフィールドを追加・削除してください
        tweets_data.append([
            tweet.date,          # ツイート日時 (datetime型)
            tweet.id,            # ツイートID
            tweet.content,       # ツイート本文
            tweet.user.username, # ユーザID(スクリーンネーム)
        ])
    
    if not tweets_data:
        print("取得できるツイートがありませんでした。")
        return
    
    # pandasのDataFrameに変換
    df = pd.DataFrame(tweets_data, columns=["DateTime", "TweetID", "Content", "Username"])
    
    # CSVとして保存
    df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"完了しました。CSVファイルとして '{output_csv}' に保存しました。")


def main():
    # ユーザ名またはURLを入力
    user_input = input("ユーザ名(@は任意) または XのプロフィールURLを入力してください: ")
    username = get_username_from_input(user_input)
    
    # 過去何日分取得するか
    days_str = input("過去何日分を取得しますか(整数)？: ")
    try:
        days = int(days_str)
    except ValueError:
        print("整数値を入力してください。")
        sys.exit(1)
    
    # 保存先CSVファイル名
    output_csv = f"{username}_tweets_{days}days.csv"
    
    # スクレイピング実行
    scrape_user_tweets(username, days, output_csv)

if __name__ == "__main__":
    main()
