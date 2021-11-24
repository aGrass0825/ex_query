"""
-------------------------------------------------
   date：          2021/11/16
   Author :        aGrass
   File Name：     _validators.py
   Description :   验证参数
-------------------------------------------------
   Change Activity:
                   2021/11/16
-------------------------------------------------
"""
from typing import Any
from functools import lru_cache
from wtforms.validators import Optional, DataRequired, NumberRange


class Singleton(type):
    """
    单例工具metaclass
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Validators(metaclass=Singleton):
    __slots__ = ("require", "optional")

    def __init__(self):
        self.optional = Optional()
        self.require = DataRequired('必填字段')

    @lru_cache(maxsize=20)
    def num_range(self, max_value: Any = None, min_value: Any = None) -> NumberRange:
        return NumberRange(min=min_value, max=max_value, message="数据范围必须在  ({}~{})".format(min_value, max_value))


validators = Validators()
