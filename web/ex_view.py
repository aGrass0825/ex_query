"""
-------------------------------------------------
   date：          2021/11/17
   Author :        aGrass
   File Name：     ex_api.py
   Description :   提供查询接口
-------------------------------------------------
   Change Activity:
                   2021/11/17
-------------------------------------------------
"""
from flask import Blueprint, g
from flask_restful import Resource

from logic.ex_handler import handler_ex
from tools.rewrite import Api, output_json
from tools import form_validate, Pagination

ex = Blueprint("ex_query", __name__, url_prefix="/ex")
ex_api = Api(ex)
# 对正常结果封装一层信封
ex_api.representation("application/json")(output_json)


@ex_api.resource("/query")
class ExQueryResource(Resource):

    @form_validate(Pagination)
    def get(self):
        form: Pagination = g.form
        resp_result = handler_ex.handler(form=form)
        return resp_result
