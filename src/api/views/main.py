from flask import Blueprint, session
from flask import request, render_template, redirect, url_for
from api.core import core_logger, create_response
from api.scrapper import collect_articles
from api.repository.mongo import save_articles
import json


def construct_views_blueprint(mongo):
    main = Blueprint("main", __name__)  # initialize blueprint

    @main.route("/", methods=['GET'])
    def index():
        return render_template("index.html")

    @main.route('/api/news', methods=['GET'])
    def news():
        news_url = request.args.get("url")
        if not news_url:
            err = "Please provide url"
            return render_template("error.html", error_msg=err)
        try:
            data = collect_articles(news_url)
            return render_template("news.html", news=data, saved_to_db=False)
        except NotImplementedError:
            err = (f"Scrapper for {news_url} not implemented")
            return render_template("error.html", error_msg=err)

    @main.route('/api/news/save', methods=['POST'])
    def save():
        data = json.loads(request.data)
        try:
            save_articles(mongo, data)
            return create_response(message=str("Success"), status=200)
        except TypeError as e:
            core_logger.error(e)
            user_msg = str(e)
            return create_response(message=str(user_msg), status=400)
        except Exception as e:
            core_logger.error(e)
            user_msg = "Something went wrong"
            return create_response(message=str(user_msg), status=500)

    return main
