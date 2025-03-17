from flask import Flask, request, Response
from XPostsScraper import XPostsScraper
from DarkEvaluator import DarkEvaluator
import json
import asyncio

app = Flask(__name__)
scraper = XPostsScraper()
dark = DarkEvaluator()

def response_as_json(content):
    result = json.dumps(content)
    return Response(result, mimetype='application/json')

@app.route('/posts/<user_id>', methods=['GET'])
async def get_posts(user_id):
    pages = request.args.get('pages', default=3, type=int)
    return response_as_json(await scraper.getPosts(user_id, pages))

@app.route('/eval_dark', methods=['GET'])
async def eval_dark():
    content = request.args.get('content')
    return response_as_json(dark.Evaluate(content))

@app.route('/dark_posts/<user_id>', methods=['GET'])
async def get_dark_posts(user_id):
    pages = request.args.get('pages', default=3, type=int)
    posts = await scraper.getPosts(user_id, pages)
    result = []
    for post in posts:
        print(f"[確認中] {post}")
        if dark.Evaluate(post):
            print(f"[黒歴史] {post}")
            result += [post]
    return response_as_json(result)

if __name__ == '__main__':
    app.run(port = 5001, debug = True, host = "0.0.0.0") 

