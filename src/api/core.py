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
    """Wraps response in a consistent format throughout the API."""
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary")

    response = {"success": 200 <= status < 300,
                "message": message,
                "result": data}
    return jsonify(response), status


def prepare_error_response(error: Exception) -> Tuple[Response, int]:
    status = error.code or 500
    message = error.description or "Internal Server Error"
    return create_response(message=message, status=status)
