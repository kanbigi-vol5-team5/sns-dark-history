import tweepy
import os,sys
from dotenv import load_dotenv

class XPoster:
    def __init__(self):
        load_dotenv()
        self.client = tweepy.Client(
            bearer_token= os.getenv('X_BEARER_TOKEN'),
            consumer_key= os.getenv('X_CONSUMER_KEY'),
            consumer_secret= os.getenv('X_CONSUMER_SECRET'),
            access_token= os.getenv('X_ACCESS_TOKEN'),
            access_token_secret= os.getenv('X_ACCESS_TOKEN_SECRET'))

    def post(self, content):
        try:
            self.client.create_tweet(text=content)
            return True
        except Exception as e:
            print(f'[XPoster] Error: {e}', file=sys.stdout, flush=True)
            return False
