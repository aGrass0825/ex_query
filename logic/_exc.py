"""
-------------------------------------------------
   date：          2021/11/19
   Author :        aGrass
   File Name：     exc.py
   Description :   异常捕获处理
-------------------------------------------------
   Change Activity:
                   2021/11/19
-------------------------------------------------
"""
import logging
from entry import app


@app.errorhandler(400)
def handler_400_error(e):
    logging.error(e)
    return {"message": "携带参数错误，请检查！"}, 400


@app.errorhandler(401)
def handler_401_error(e):
    logging.error(e)
    return {"message": "未携带身份认证信息"}, 401


@app.errorhandler(403)
def handler_403_error(e):
    logging.error(e)
    return {"message": "认证信息错误，请检查！"}, 403


@app.errorhandler(404)
def handler_403_error(e):
    logging.error(e)
    return {"message": "请求未找到，请检查！"}, 404


@app.errorhandler(405)
def handler_403_error(e):
    logging.error(e)
    return {"message": "请求方式错误，请检查！"}, 405


@app.errorhandler(500)
def handler_500_error(e):
    logging.error(e)
    return {"message": "服务器出错，请联系运维人员!"}, 500
