import re
import sys
import pandas as pd
from datetime import datetime, timedelta
import ssl
import urllib3

# snscrapeライブラリ
import snscrape.modules.twitter as sntwitter

# SSL警告を無効化
urllib3.disable_warnings()

# SSL検証を無効化
ssl._create_default_https_context = ssl._create_unverified_context

def get_username_from_input(user_input: str) -> str:
    """
    入力が @ユーザ名 か URL だった場合に対応してユーザ名を抽出する。
    """
    user_input = user_input.strip()
    
    # もしURL形式(例: https://twitter.com/xxxx や https://x.com/xxxx)の場合は正規表現でユーザ名を取得
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

def scrape_user_tweets(username: str, days: int):
    """
    snscrapeを用いて指定ユーザの過去days日間のツイートを取得し、リストとして返す。
    """
    try:
        # 現在時刻を基準にdays日前の日付を計算
        since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        until_date = datetime.now().strftime("%Y-%m-%d")
        
        query = f"from:{username} since:{since_date} until:{until_date}"
        tweets_data = []
        
        print(f"ユーザ: {username}, 過去{days}日分のツイートを取得します...")
        print(f"期間: {since_date} から {until_date}")
        
        scraper = sntwitter.TwitterSearchScraper(query)
        tweet_count = 0
        
        for tweet in scraper.get_items():
            tweets_data.append([
                tweet.date.strftime("%Y-%m-%d %H:%M:%S"),
                tweet.id,
                tweet.content,
                tweet.user.username,
                tweet.likeCount,
                tweet.retweetCount
            ])
            tweet_count += 1
            if tweet_count % 10 == 0:
                print(f"取得済み: {tweet_count}件")
    
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        return []
    
    print(f"合計 {len(tweets_data)}件のツイートを取得しました。")
    return tweets_data

def main():
    # コマンドライン引数のチェック
    if len(sys.argv) != 3:
        print("Usage: python script.py <username_or_url> <days>")
        sys.exit(1)
    
    # 第1引数: ユーザ名(@は任意) または X(Twitter) のプロフィールURL
    user_input = sys.argv[1]
    # 第2引数: 過去何日分取得するか
    days_str = sys.argv[2]

    # ユーザ名抽出
    username = get_username_from_input(user_input)

    # 日数を整数変換
    try:
        days = int(days_str)
    except ValueError:
        print("整数値を入力してください。")
        sys.exit(1)
    
    # スクレイピング実行
    tweets_data = scrape_user_tweets(username, days)

    if not tweets_data:
        print("取得できるツイートがありませんでした。")
        return

    # DataFrameとして整形してから出力
    df = pd.DataFrame(
        tweets_data,
        columns=["DateTime", "TweetID", "Content", "Username", "Likes", "Retweets"]
    )
    
    # 表示オプションを設定
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    
    print("\n=== ツイート一覧 ===")
    print(df.to_string(index=False))
    
    # 基本的な統計情報を表示
    print("\n=== 統計情報 ===")
    print(f"総ツイート数: {len(df)}")
    print(f"平均いいね数: {df['Likes'].mean():.1f}")
    print(f"平均リツイート数: {df['Retweets'].mean():.1f}")

if __name__ == "__main__":
    main()
