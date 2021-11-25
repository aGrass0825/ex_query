"""
-------------------------------------------------
   date：          2021/11/16
   Author :        aGrass
   File Name：     api.py
   Description :   定时任务逻辑处理
-------------------------------------------------
   Change Activity:
                   2021/11/16
-------------------------------------------------
"""
import abc
import time
import logging
import requests
from datetime import datetime
from urllib.parse import urlencode
from typing import Dict, Union, Sequence, NoReturn

from tools import red_cache
from config import REQUEST_PRO, ALARM_KEY


class GetAlarm(metaclass=abc.ABCMeta):

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    @abc.abstractmethod
    def service_type(self) -> str:
        pass

    @staticmethod
    def get_current_stamp():
        """获取当天零点的时间戳"""
        today = datetime.now().strftime('%Y-%m-%d')
        t_stamp = time.mktime(time.strptime(today, '%Y-%m-%d'))
        return int(t_stamp)

    @staticmethod
    def get_today():
        """获取年月日"""
        return datetime.now().strftime('%Y-%m-%d')

    @staticmethod
    def fmt_time(timestamp: int):
        """时间转换成标准时间"""
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    def get_alarm(self, params) -> Union[Sequence[Dict], NoReturn]:
        try:
            res = requests.get("{}/ketech/query".format(REQUEST_PRO),
                               params=urlencode(params, encoding='utf8'), timeout=10)
            _data = res.json(encoding='utf-8')
        except Exception as e:
            self.logger.error(f'{params.get("serviceType")}获取省平台预警数据失败 :{e}')
        else:
            if not _data['status']:
                self.logger.warning(f'{params.get("serviceType")}获取响应结果失败 :{_data["data"]}')
            return eval(_data['data'])

    def save_redis(self, today: str, type_ser: str, resp_result: list):
        try:
            red_cache.save_result(today=today, type_ser=type_ser, resp_result=resp_result)
        except Exception as e:
            self.logger.error(f"{type_ser}缓存失败:{e}")

    def start(self):
        end = int(time.time())
        start = self.get_current_stamp()
        today = self.get_today()
        type_ser = self.service_type
        condition = dict(startDate=self.fmt_time(start), endDate=self.fmt_time(end))
        params = {"serviceType": type_ser, "strCondition": condition}
        params.update(ALARM_KEY)
        resp_result = self.get_alarm(params)  # 耗时业务
        self.save_redis(today=today, type_ser=type_ser, resp_result=resp_result)


class GetTelAlarm(GetAlarm):
    """电话预警"""

    @property
    def service_type(self):
        return 'dhyj'


class GetPayAlarm(GetAlarm):
    """支付宝高危预警"""

    @property
    def service_type(self):
        return 'zfbgwyj'


class GetWantedAlarm(GetAlarm):
    """假通缉令预警"""

    @property
    def service_type(self):
        return 'jtjlyj'


class GetSiteAlarm(GetAlarm):
    """网站预警"""

    @property
    def service_type(self):
        return 'wzyj'
