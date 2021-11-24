"""
-------------------------------------------------
   date：          2021/11/16
   Author :        aGrass
   File Name：     api_exception_handler.py
   Description :   重写flask_restful里提供的异常处理方法
-------------------------------------------------
   Change Activity:
                   2021/11/16
-------------------------------------------------
"""
from json import dumps
from flask_restful.utils import PY3
from flask_restful import Api as _Api
from flask import make_response, current_app
from werkzeug.exceptions import HTTPException


def output_json(data, code, headers=None):
    """Makes a Flask response with a JSON encoded body"""

    if "message" not in data:
        data = {
            "status": 1,
            "message": "success",
            "data": data
        }
    settings = current_app.config.get('RESTFUL_JSON', {})

    # If we're in debug mode, and the indent is not set, we set it to a
    # reasonable value here.  Note that this won't override any existing value
    # that was set.  We also set the "sort_keys" value.
    if current_app.debug:
        settings.setdefault('indent', 4)
        settings.setdefault('sort_keys', not PY3)

    # always end the json dumps with a new line
    # see https://github.com/mitsuhiko/flask/pull/1262
    dumped = dumps(data, **settings) + "\n"

    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp


class Api(_Api):
    """重写Api中error_router方法"""

    def error_router(self, original_handler, e):
        """不采用flask_restful里定义的异常处理方法"""
        # if self._has_fr_route() and isinstance(e, HTTPException):
        #     try:
        #         return self.handle_error(e)
        #     except Exception:
        #         pass  # Fall through to original handler
        return original_handler(e)
