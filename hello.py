from flask import Flask, request
from api.news_get import extract


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/news', methods=['POST', 'GET'])
def news():
    news_url = request.args.get('url')
    extract(news_url)
    return news_url
