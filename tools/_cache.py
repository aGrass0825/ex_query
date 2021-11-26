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
from wtforms import Form
from functools import wraps
from redis import Redis, ConnectionPool
from datetime import datetime, timedelta

from config import RED_CONF


class ExRedCache(object):
    """缓存操作"""

    def __init__(self):
        pool = ConnectionPool(**RED_CONF, decode_responses=True)
        self._redis = Redis(connection_pool=pool)
        self.logger = logging.getLogger(self.__class__.__name__)

    redis = property(lambda self: self._redis)

    def resp_handler(self, type_ser: str, result: dict):
        """序列化保存缓存"""
        if type_ser == "dhyj":
            tel = result.get("shrhm")
        elif type_ser == "wzyj":
            tel = result.get("sjhm")
        elif type_ser == "zfbgwyj":
            tel = result.get("telephone")
        else:
            sfzh = result.get("sfzh")
            ret = {
                "citycode": result.get("citycode"), "cityname": result.get("cityname"), "tel": sfzh,
                "fkzt": result.get("fkzt"), "fksj": result.get("fksj", ""), "yjid": result.get("yjid")
            }
            return sfzh, ret
        ret = {
            "citycode": result.get("citycode"), "cityname": result.get("cityname").strip(),
            "tel": tel, "fkzt": result.get("fkzt"), "fksj": result.get("fksj", ""),
            "yjsj": result.get("yjsj", ""), "yjid": result.get("yjid")
        }
        return tel, ret

    def save_result(self, today: str, type_ser: str, save_time: int, resp_result: list) -> None:
        """保存数据"""
        if resp_result:
            key = "{}::{}".format(today, type_ser)
            pipe = self.redis.pipeline()
            for res in resp_result:
                score, res = self.resp_handler(type_ser=type_ser, result=res)
                pipe.zadd(name=key, mapping={json.dumps(res): score})
            pipe.execute()
            self.redis.expire(key, save_time)

    def get_result(self, key: str, form: Form) -> dict:
        """分页获取数据"""
        page = form.pagination()
        start = page.offset
        end = start + page.limit - 1
        result_list = self.redis.zrange(name=key, start=start, end=end)
        sum_num = self.redis.zcard(key)  # 统计总数
        result = list(map(lambda x: json.loads(x), result_list))
        return {"body": result, "count": sum_num}

    def get_between_day(self, begin_date: str, end_date: str) -> list:
        """获取范围内天数"""
        date_list = []
        begin_date = datetime.strptime(begin_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        while begin_date <= end_date:
            date_str = begin_date.strftime('%Y-%m-%d')
            date_list.append(date_str)
            begin_date += timedelta(days=1)
        return date_list

    def merge(self, short_time: int, day_list: list, form: Form) -> dict:
        """汇聚"""
        end_time = form.end.data.strftime('%Y-%m-%d')
        key_new = "{}::{}::{}".format(end_time, len(day_list), form.data_type.data)
        if self.redis.exists(key_new):
            return self.get_result(key=key_new, form=form)
        pipe = self.redis.pipeline()
        for item in day_list:
            key = "{}::{}".format(item, form.data_type.data)
            result_list = self.redis.zrange(name=key, start=0, end=-1)
            for res in result_list:
                pipe.zadd(name=key_new, mapping={res: json.loads(res).get("tel")})
            pipe.execute()
        self.redis.expire(key_new, short_time)
        return self.get_result(key=key_new, form=form)

    def kernel_show(self, form: Form, func, obj) -> dict:
        """展示逻辑"""
        try:
            start_time = form.start.data.strftime('%Y-%m-%d')
            end_time = form.end.data.strftime('%Y-%m-%d')
            now_time = datetime.now().strftime('%Y-%m-%d')

            if end_time == now_time and start_time == now_time:
                """查当天的"""
                key = "{}::{}".format(end_time, form.data_type.data)
                if self.redis.exists(key):
                    return self.get_result(key=key, form=form)
                ret = func(obj, form)
                if isinstance(ret, dict):
                    return ret
                self.save_result(today=end_time, type_ser=form.data_type.data,
                                 save_time=2 * 60, resp_result=ret)
                return self.get_result(key=key, form=form)

            elif start_time != end_time and end_time != now_time:
                """查前某几天"""
                day_list = self.get_between_day(begin_date=start_time, end_date=end_time)
                if len(day_list) > 6:
                    return dict(status=0, message="超出规定日期范围，请重新选择!")
                return self.merge(short_time=30 * 60, day_list=day_list, form=form)

            elif start_time != end_time and end_time == now_time:
                """查从当天至前几天"""
                day_list = self.get_between_day(begin_date=start_time, end_date=end_time)
                if len(day_list) > 7:
                    return dict(status=0, message="超出规定日期范围，请重新选择!")
                key = "{}::{}".format(end_time, form.data_type.data)
                if self.redis.exists(key):
                    return self.merge(short_time=4 * 60, day_list=day_list, form=form)
                ret = func(obj, form)
                if isinstance(ret, dict):
                    return ret
                self.save_result(today=end_time, type_ser=form.data_type.data,
                                 save_time=2 * 60, resp_result=ret)
                return self.merge(short_time=4 * 60, day_list=day_list, form=form)

            elif start_time == end_time and end_time != now_time:
                """查前某一天"""
                key = "{}::{}".format(end_time, form.data_type.data)
                return self.get_result(key=key, form=form)

        except Exception as e:
            self.logger.error('Error:{}'.format(e))
            return dict(stats=507, message="数据库操作失败，请联系技术人员!")

    def kernel_search(self, form: Form, func, obj, tel: str) -> dict:
        """搜索逻辑"""
        init_list = []
        start_time = form.start.data.strftime('%Y-%m-%d')
        end_time = form.end.data.strftime('%Y-%m-%d')
        now_time = datetime.now().strftime('%Y-%m-%d')
        day_list = self.get_between_day(begin_date=start_time, end_date=end_time)
        if len(day_list) > 7:
            return dict(status=0, message="超出规定日期范围，请重新选择!")
        for item in day_list:
            key = "{}::{}".format(item, form.data_type.data)
            if self.redis.exists(key):
                score_list = self.redis.zrangebyscore(name=key, min=tel, max=tel)
                init_list.extend(score_list)
            elif item == now_time:
                ret = func(obj, form)
                if isinstance(ret, dict):
                    return ret
                self.save_result(today=item, type_ser=form.data_type.data,
                                 save_time=2 * 60, resp_result=ret)
                score_list = self.redis.zrangebyscore(name=key, min=tel, max=tel)
                init_list.extend(score_list)
        if init_list:
            result = list(map(lambda x: json.loads(x), init_list))
            return {"body": result, "count": len(result)}
        else:
            return dict(status=0, message="未同步到中间库，请联系技术人员!")

    def cache_ex_data(self, func):
        """展示与搜索功能"""

        @wraps(func)
        def _wrap(obj, form):
            tel = form.callee.data
            if not tel:
                return self.kernel_show(form=form, func=func, obj=obj)
            else:
                return self.kernel_search(form=form, func=func, obj=obj, tel=tel)

        return _wrap


red_cache = ExRedCache()
