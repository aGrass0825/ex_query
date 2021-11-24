"""
-------------------------------------------------
   date：          2021/11/16
   Author :        aGrass
   File Name：     ex_handler.py
   Description :   业务查询处理
-------------------------------------------------
   Change Activity:
                   2021/11/16
-------------------------------------------------
"""
import time
import logging
import requests
from wtforms import Form
from flask import current_app
from datetime import datetime
from urllib.parse import urlencode
from typing import Dict, Union, Sequence, NoReturn

from tools import red_cache


class ExHandler:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def fmt_time(timestamp: int):
        """时间转换成标准时间"""
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    def _alarm(self, params) -> Union[Sequence[Dict], NoReturn]:
        try:
            res = requests.get("{}/ketech/query".format(current_app.config.get("REQUEST_PRO")),
                               params=urlencode(params, encoding='utf8'), timeout=10)
            _data = res.json(encoding='utf-8')
        except Exception as e:
            self.logger.error(f'{params.get("serviceType")}获取省平台预警数据失败 :{e}')
        else:
            if not _data['status']:
                self.logger.warning(f'{params.get("serviceType")}获取响应结果失败 :{_data["data"]}')
            return eval(_data['data'])

    def get_alarm(self, form: Form):
        end = int(time.time())
        start = end - form.data_time.data * 60 * 60
        condition = dict(startDate=self.fmt_time(start), endDate=self.fmt_time(end))
        params = {"serviceType": form.data_type.data, "strCondition": condition}
        params.update(current_app.config.get("ALARM_KEY"))
        return self._alarm(params)

    @red_cache.cache_ex_data
    def handler(self, form: Form):
        return self.get_alarm(form=form)


handler_ex = ExHandler()
