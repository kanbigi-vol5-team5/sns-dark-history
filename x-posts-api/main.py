from flask import Flask, request, Response
from XPostsScraper import XPostsScraper
from XPoster import XPoster
from DarkEvaluator import DarkEvaluator
import json
import asyncio

app = Flask(__name__)
scraper = XPostsScraper()
poster = XPoster()
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

@app.route('/icon/<user_id>', methods=['GET'])
async def get_icon(user_id):
    return response_as_json(await scraper.getIcon(user_id))

# Xに任意の内容で投稿するエンドポイント
@app.route('/post', methods=['POST'])
async def post():
    content = request.json['content']
    if poster.post(content):
        return response_as_json({"status": "ok"})
    else:
        return response_as_json({"status": "ng"})

if __name__ == '__main__':
    app.run(port = 5001, host = "0.0.0.0") 
