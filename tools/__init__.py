"""
-------------------------------------------------
   date：          2021/11/16
   Author :        aGrass
   File Name：     __init__.py
   Description :   校验与日志初始化
-------------------------------------------------
   Change Activity:
                   2021/11/16
-------------------------------------------------
"""
import json
import logging
from wtforms import Form
from functools import wraps
from typing import Type, Dict
from flask import request, jsonify, g

from .page import Pagination
from ._cache import red_cache
from . import field as wtforms_json

__all__ = ['form_validate', 'Pagination', 'red_cache']

wtforms_json.init()


def form_validate(form: Type[Form], render_json: bool = True):
    """
    表单校验装饰器
    :param form:
    :param render_json:
    :return:
    """

    def _wraps(func):
        @wraps(func)
        def _validate(*args, **kwargs):
            if request.is_json:
                f = form.from_json(request.get_json())
            else:
                f = form(request.args) if request.method == 'GET' else form()

            if not f.validate():
                logging.debug("form validate error %s (%s)", f.errors, request.url)

                try:
                    detail = '\n'.join(map(lambda kv: "\t{}:{}".format(kv[0], '\n\t'.join(kv[1])), f.errors.items()))
                    err_msg = '请求参数异常:\n{}'.format(detail)
                except TypeError:
                    err_msg = '请求参数异常!-{}'.format(json.dumps(f.errors, ensure_ascii=False))
                ret = dict(stats=400, message=err_msg)
                return jsonify(**ret) if render_json else ret
            g.form = f
            return func(*args, **kwargs)

        return _validate

    return _wraps


def initialize_logger(conf: Dict = None):
    if conf:
        root_logger = logging.getLogger()
        for h in root_logger.handlers:
            root_logger.removeHandler(h)
        logging.basicConfig(**conf)
