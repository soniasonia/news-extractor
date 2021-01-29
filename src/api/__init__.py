import os
import logging

from flask import Flask, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_session import Session

from api.config import config
from api.core import prepare_error_response

# import and register blueprints
from api.views.main import construct_views_blueprint


class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        return super().format(record)


# why we use application factories
# http://flask.pocoo.org/docs/1.0/patterns/appfactories/#app-factories
def create_app(test_config=None):
    app = Flask(__name__)

    CORS(app)  # add CORS

    # check environment variables to see which config to load
    env = os.environ.get("FLASK_ENV", "dev")

    app.config.from_object(config[env])  # config dict is from api/config.py

    # logging
    formatter = RequestFormatter(
        "%(asctime)s %(remote_addr)s: requested %(url)s: %(levelname)s "
        "in [%(module)s: %(lineno)d]: %(message)s"
    )
    if app.config.get("LOG_FILE"):
        fh = logging.FileHandler(app.config.get("LOG_FILE"))
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        app.logger.addHandler(fh)

    strm = logging.StreamHandler()
    strm.setLevel(logging.DEBUG)
    strm.setFormatter(formatter)

    app.logger.addHandler(strm)
    app.logger.setLevel(logging.DEBUG)

    root = logging.getLogger("core")
    root.addHandler(strm)

    # Mongo DB
    mongo = PyMongo(app)

    # Use Session from Flask-Session
    # Flask-Session is an extension that adds support for server-side session
    # It means that session data is stored on server instead of cookie
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Register blueprint
    # why blueprints http://flask.pocoo.org/docs/1.0/blueprints/
    app.register_blueprint(construct_views_blueprint(mongo))

    # register error response that logs to app.logger and returns unified response
    def exception_handler_wrapper(error):
        root.error(error)
        return prepare_error_response(error)

    app.register_error_handler(Exception, exception_handler_wrapper)

    return app
