"""
-------------------------------------------------
   date：          2021/11/16
   Author :        aGrass
   File Name：     app.py
   Description :   创建flask对象
-------------------------------------------------
   Change Activity:
                   2021/11/16
-------------------------------------------------
"""
from flask import Flask, Blueprint
from werkzeug.wrappers import Response
from typing import Iterable, Tuple, Callable


class MakeApp:
    def __init__(self, name: str = __name__,
                 plugins: Iterable = None,
                 blue_prints: Iterable[Blueprint] = None,
                 mount: Iterable[Tuple[str, callable]] = None,
                 after_requests: Iterable[Callable[[Response], Response]] = None):
        self.name = name
        self.blue_prints = blue_prints
        self.plugins = plugins
        self.mount = mount
        self.after_requests = after_requests

    def make_app(self) -> Flask:
        app = Flask(self.name)
        app.config.from_pyfile("config.py")
        if self.blue_prints:
            for bl in self.blue_prints:
                app.register_blueprint(bl)
        if self.plugins:
            for p in self.plugins:
                p(app)
        if self.mount:
            for r, f in self.mount:
                app.route(r)(f)
        if self.after_requests:
            for m in self.after_requests:
                app.after_request(m)
        return app
