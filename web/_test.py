"""
-------------------------------------------------
   date：          2021/11/18
   Author :        aGrass
   File Name：     _test.py
   Description :   测试查询项目所有路由信息
-------------------------------------------------
   Change Activity:
                   2021/11/18
-------------------------------------------------
"""
from entry import app
from flask_restful import Resource
from tools.rewrite import Api, output_json

route_api = Api(app)
# 对正常结果封装一层信封
route_api.representation("application/json")(output_json)


@route_api.resource("/route")
class RouteResource(Resource):

    def get(self):
        """查看项目整个路由信息"""
        item_list = []
        for item in app.url_map.iter_rules():
            item_list.append({
                "name": item.endpoint,
                "path": item.rule
            })
        return {"api": item_list}
