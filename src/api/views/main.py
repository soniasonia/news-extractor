from flask import Blueprint, session
from flask import request, render_template, redirect, url_for
from api.scrapper.news_get import extract, ALLOWED_URLS


def construct_views_blueprint(mongo):
    main = Blueprint("main", __name__)  # initialize blueprint

    @main.route("/")
    def index():
        err = session.get("error_msg")
        session["error_msg"] = ""
        return render_template("index.html", error_msg=err)

    @main.route('/api/news', methods=['GET'])
    def news():
        if not request.args.get("url") \
                or request.args.get("url") not in ALLOWED_URLS.keys():
            session["error_msg"] = "Scrapper for this page is not implemented"
            return redirect(url_for('.index'))
        else:
            session["error_msg"] = ""
        news_url = request.args.get('url')
        data = extract(news_url)
        session["articles"] = data
        return render_template("news.html", news=data, saved_to_db=False)

    @main.route('/api/news/save', methods=['POST'])
    def save():
        data = session["articles"]
        result = mongo.db.articles.insert(data)
        if len(result) == len(data):
            return render_template("news.html", news=data, saved_to_db=True)
        else:
            err = "Something went wrong..."
            return render_template("news.html", news=data, error_msg=err)

    return main
