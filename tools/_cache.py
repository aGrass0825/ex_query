"""
-------------------------------------------------
   date：          2021/11/16
   Author :        aGrass
   File Name：     _cache.py
   Description :   缓存处理业务
-------------------------------------------------
   Change Activity:
                   2021/11/16
-------------------------------------------------
"""
import json
import logging
from functools import wraps
from datetime import datetime
from redis import Redis, ConnectionPool

from config import RED_CONF


class ExRedCache(object):
    """缓存"""

    def __init__(self):
        pool = ConnectionPool(**RED_CONF, decode_responses=True)
        self._redis = Redis(connection_pool=pool)
        self.logger = logging.getLogger(self.__class__.__name__)

    redis = property(lambda self: self._redis)

    @staticmethod
    def get_today():
        """获取年月日"""
        return datetime.now().strftime('%Y-%m-%d')

    def save_result(self, type_ser: str, resp_result: list, count: int = 0):
        """保存数据"""
        if resp_result:
            key = "{}::{}".format(self.get_today(), type_ser)
            pipe = self.redis.pipeline()
            for res in resp_result:
                pipe.zadd(name=key, mapping={json.dumps(res): count})
                count += 1
            pipe.execute()
            self.redis.expire(key, 7 * 24 * 60 * 60)

    def get_result(self, key, form):
        """分页获取数据"""
        page = form.pagination()
        start = page.offset
        end = start + page.limit - 1
        result_list = self.redis.zrange(name=key, start=start, end=end)
        sum_num = self.redis.zcard(key)  # 统计总数
        result = list(map(lambda x: json.loads(x), result_list))
        return {"body": result, "count": sum_num}

    def cache_ex_data(self, func):
        """获取缓存中间库数据"""

        @wraps(func)
        def _wrap(obj, form):
            try:
                key = "{}::{}".format(self.get_today(), form.data_type.data)
                if self.redis.exists(key):
                    return self.get_result(key=key, form=form)
                ret = func(obj, form)
                self.save_result(type_ser=form.data_type.data, resp_result=ret)
                return self.get_result(key=key, form=form)
            except Exception as e:
                self.logger.error('Error:{}'.format(e))
                return dict(stats=507, message=e)

        return _wrap


red_cache = ExRedCache()
