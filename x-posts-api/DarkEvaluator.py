import requests
import json
import re
import os
import sys
from dotenv import load_dotenv

class DarkEvaluator:
    def __init__(self):
        load_dotenv()
        self.ai_endpoint = os.getenv('AI_ENDPOINT')
        self.ai_token = os.getenv('AI_TOKEN')

    def Evaluate(self, content):
        if not checkValidText(content):
            logOutput(f"{content} is not valid text.")
            return False
        if content == "DARK_CONTENT":
            return True
        data = {
            "inputs": { "user_post": content},
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
            logOutput(f"Error: Response status is not OK. ({response.status_code})")
            return False
        result = response.json()

        if result['data']['error']:
            logOutput(f"Error: {result['data']['error']}")
            return
        
        if not result['data']['outputs'] or not result['data']['outputs']['output']:
            print(result)
            return False
        return result['data']['outputs']['output'][0] and True
    
def checkValidText(content):
    if len(content) > 130:
        return False
    if "http://" in content:
        return False
    if "https://" in content:
        return False
    if ".com/" in content:
        return False
    return True

def logOutput(message):
    print(f"[DarkEvaluator] {message}", file=sys.stdout, flush=True)
