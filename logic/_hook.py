"""
-------------------------------------------------
   date：          2021/11/18
   Author :        aGrass
   File Name：     _hook.py
   Description :   flask钩子函数
-------------------------------------------------
   Change Activity:
                   2021/11/18
-------------------------------------------------
"""
from flask import request, abort

from entry import app


@app.before_request
def before_request():
    """利用请求前的钩子函数验证登录信息"""
    auth = request.headers.get("Authorization")
    if not auth == "Axqwerasdf1agrassuWRRTuotznBBAkJB":
        abort(403)


@app.after_request
def after_request(response):
    """利用请求后的钩子函数对响应类型统一处理"""
    response.headers = {
        "Content-Type": "application/json",
        "name": "ex_query"
    }
    return response
