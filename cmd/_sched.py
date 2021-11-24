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
    GetTelAlarm().start()


@_Job.job(cfg={'hour': '23', 'minute': '59', 'second': '58'}, name='alarm_site')
def alarm_site():
    GetSiteAlarm().start()


@_Job.job(cfg={'hour': '23', 'minute': '59', 'second': '58'}, name='alarm_pay')
def alarm_pay():
    GetPayAlarm().start()


@_Job.job(cfg={'hour': '23', 'minute': '59', 'second': '58'}, name='alarm_wanted')
def alarm_wanted():
    GetWantedAlarm().start()
