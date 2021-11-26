"""
-------------------------------------------------
   date：          2021/11/16
   Author :        aGrass
   File Name：     _sched.py
   Description :   定时任务配置
-------------------------------------------------
   Change Activity:
                   2021/11/16
-------------------------------------------------
"""
import logging
from datetime import datetime
from typing import Callable, Any, Iterable

from logic.api import GetTelAlarm, GetPayAlarm, GetWantedAlarm, GetSiteAlarm


class _Job:
    def __init__(self, func: Callable[[], Any], trigger: str = 'cron', name: str = '', cfg: dict = None):
        self.name = name
        self.func = func
        self.trigger = trigger
        self.cfg = cfg

    @classmethod
    def job(cls, cfg: dict, name: str = '', trigger: str = 'cron'):
        def _wrap(func: Callable[[], Any]) -> '_Job':
            return cls(func, trigger=trigger, name=name or func.__name__, cfg=cfg)

        return _wrap

    def __call__(self):
        return self.func()


def jobs() -> Iterable[_Job]:
    return (value for value in globals().values() if isinstance(value, _Job))


@_Job.job(cfg={'hour': '23', 'minute': '59', 'second': '58'}, name='alarm_tel')
def alarm_tel():
    logging.warning(f"电话预警：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    GetTelAlarm().start()


@_Job.job(cfg={'hour': '23', 'minute': '59', 'second': '58'}, name='alarm_site')
def alarm_site():
    logging.warning(f"网站预警：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    GetSiteAlarm().start()


@_Job.job(cfg={'hour': '23', 'minute': '59', 'second': '58'}, name='alarm_pay')
def alarm_pay():
    logging.warning(f"支付宝高危预警：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    GetPayAlarm().start()


@_Job.job(cfg={'hour': '23', 'minute': '59', 'second': '58'}, name='alarm_wanted')
def alarm_wanted():
    logging.warning(f"假通缉令预警：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    GetWantedAlarm().start()
