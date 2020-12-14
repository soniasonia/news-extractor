from flask import Blueprint, request
from api.core import create_response, serialize_list, logger
from api.news_get import extract


def construct_views_blueprint(mongo):
    main = Blueprint("main", __name__)  # initialize blueprint

    # function that is called when you visit /
    @main.route("/")
    def index():
        return "<h1>Hello World!</h1>"


    @main.route('/api/news', methods=['GET'])
    def news():
        news_url = request.args.get('url')
        data = extract(news_url)
        mongo.db.articles.insert(data)
        output = bieda_html(data)
        return output

    return main

def bieda_html(data):
    output = "<table>"
    for item in data:
        output = output + "<tr><td>{}</td><td>{}</td></tr>".format(item["title"], item["url"])
    return output + "</table>"