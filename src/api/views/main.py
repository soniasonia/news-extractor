from flask import Blueprint, session
from flask import request, render_template, redirect, url_for
from api.core import logger, create_response
from api.scrapper.news_get import extract
from api.repository.mongo import save_articles
import json


def get_error_msg_if_exists():
    err = session.get("error_msg")
    if err:
        session["error_msg"] = ""
        return err


def construct_views_blueprint(mongo):
    main = Blueprint("main", __name__)  # initialize blueprint

    @main.route("/")
    def index():
        err = get_error_msg_if_exists()
        return render_template("index.html", error_msg=err)

    @main.route('/api/news', methods=['GET'])
    def news():
        if not request.args.get("url"):
            session["error_msg"] = "Please provide url"
            return redirect(url_for('.index'))
        try:
            news_url = request.args.get("url")
            data = extract(news_url)
            return render_template("news.html", news=data, saved_to_db=False)
        except Exception as e:
            session["error_msg"] = e
            return redirect(url_for('.index'))

    @main.route('/api/news/save', methods=['POST'])
    def save():
        data = json.loads(request.data)
        try:
            save_articles(mongo, data)
            return create_response(message=str("Success"), status=200)
        except Exception as e:
            logger.error(e)
            user_msg = "Something went wrong"
            return create_response(message=str(user_msg), status=500)
    return main
