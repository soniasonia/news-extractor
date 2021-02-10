import os
import logging

from flask import Flask, request
from flask_cors import CORS
from flask_session import Session

from api.config import config
from api.core import prepare_error_response
from flask_pymongo import PyMongo

# import and register blueprints
from api.views.main import construct_views_blueprint


class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        return super().format(record)


def file_handler(path):
    formatter = RequestFormatter(
        "%(asctime)s %(remote_addr)s: requested %(url)s: %(levelname)s "
        "in [%(module)s: %(lineno)d]: %(message)s"
    )
    fh = logging.FileHandler(path)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    return fh


def str_handler():
    formatter = RequestFormatter(
        "%(asctime)s %(remote_addr)s: requested %(url)s: %(levelname)s "
        "in [%(module)s: %(lineno)d]: %(message)s"
    )
    strm = logging.StreamHandler()
    strm.setLevel(logging.DEBUG)
    strm.setFormatter(formatter)
    return strm


# why we use application factories
# http://flask.pocoo.org/docs/1.0/patterns/appfactories/#app-factories
def create_app():
    app = Flask(__name__)

    CORS(app)

    env = os.environ.get("FLASK_ENV", "dev")
    app.config.from_object(config[env])

    if app.config.get("LOG_FILE"):
        app.logger.addHandler(file_handler(app.config.get("LOG_FILE")))
    app.logger.addHandler(str_handler())
    app.logger.setLevel(logging.DEBUG)
    root = logging.getLogger("core")
    root.addHandler(str_handler())

    # MONGO DB
    # We don't provide a URI when running unit tests
    mongo = None
    if env != "test":
        mongo = PyMongo()
        mongo.init_app(app)

    # Use Session from Flask-Session
    # Flask-Session is an extension that adds support for server-side session
    # It means that session data is stored on server instead of cookie
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Register blueprint
    # why blueprints http://flask.pocoo.org/docs/1.0/blueprints/
    app.register_blueprint(construct_views_blueprint(mongo))

    # register error response that logs to app.logger
    # and returns unified response
    def exception_handler_wrapper(error):
        root.error(error)
        return prepare_error_response(error)

    app.register_error_handler(Exception, exception_handler_wrapper)

    return app
