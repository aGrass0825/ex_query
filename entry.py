"""
-------------------------------------------------
   date：          2021/11/16
   Author :        aGrass
   File Name：     entry.py
   Description :   flask启动入口
-------------------------------------------------
   Change Activity:
                   2021/11/16
-------------------------------------------------
"""
from flask import Blueprint

from web.ex_view import ex
from web.app import MakeApp
from tools import initialize_logger

# 添加蓝图
__all__ = ["ex"]

app = MakeApp(name=__name__,
              blue_prints=(filter(lambda item: isinstance(item, Blueprint), globals().values()))).make_app()

initialize_logger(app.config.get("LOG_CNF"))

from web import _test
from logic import _hook, _exc
