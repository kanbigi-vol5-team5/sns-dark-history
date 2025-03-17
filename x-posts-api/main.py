from flask import Flask, request, Response
from XPostsScraper import XPostsScraper
from DarkEvaluator import DarkEvaluator
import json

app = Flask(__name__)
scraper = XPostsScraper()
dark = DarkEvaluator()

def response_as_json(content):
    result = json.dumps(content)
    return Response(result, mimetype='application/json')

@app.route('/posts/<user_id>', methods=['GET'])
def get_posts(user_id):
    pages = request.args.get('pages', default=3, type=int)
    return response_as_json(scraper.getPosts(user_id, pages))

@app.route('/eval_dark', methods=['GET'])
def eval_dark():
    content = request.args.get('content')
    return response_as_json(dark.Evaluate(content))

@app.route('/dark_posts/<user_id>', methods=['GET'])
def get_dark_posts(user_id):
    pages = request.args.get('pages', default=3, type=int)
    posts = scraper.getPosts(user_id, pages)
    result = []
    for post in posts:
        if dark.Evaluate(post):
            result += [post]
    return response_as_json(result)

if __name__ == '__main__':
    app.run(port = 5001, debug = True, host = "0.0.0.0") 

