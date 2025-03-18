import requests
import json
import re
import os
from dotenv import load_dotenv

class DarkEvaluator:
    def __init__(self):
        load_dotenv()
        self.ai_endpoint = os.getenv('AI_ENDPOINT')
        self.ai_token = os.getenv('AI_TOKEN')

    def Evaluate(self, content):
        if not self.checkValidText(content):
            return False
        user_post = self.cleanUpText(content)
        data = {
            "inputs": { "user_post": user_post},
            "response_mode": "blocking",
            "user": "abc-123"
        }
        json_data = json.dumps(data)
        response = requests.post(
        self.ai_endpoint,
        data=json_data,
        headers={"Content-Type": "application/json","Authorization": f"Bearer {self.ai_token}"}
        )
        if response.status_code != 200:
            print(response.json())
            return False
        result = response.json()
        if not result['data']['outputs'] or not result['data']['outputs']['output']:
            print(result)
            return False
        return result['data']['outputs']['output'][0] and True
    
    def cleanUpText(self, content):
        return self._remove_urls(content)
    
    def checkValidText(self, content):
        if len(content) > 130:
            return False
        return True
    def _remove_urls(self, text: str) -> str:
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        return url_pattern.sub('', text)
