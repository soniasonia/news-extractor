import logging
from typing import Tuple

from werkzeug.local import LocalProxy
from flask import current_app, jsonify
from flask.wrappers import Response

# logger object for all views to use
logger = LocalProxy(lambda: current_app.logger)
core_logger = logging.getLogger("core")


def create_response(
        data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.

    Format inspired by
    https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use
      one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself
    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {"success": 200 <= status < 300,
                "message": message,
                "result": data}
    return jsonify(response), status


def prepare_error_response(error: Exception) -> Tuple[Response, int]:
    status = error.code or 500
    message = error.description or "Internal Server Error"
    return create_response(message=message, status=status)
