"""
-------------------------------------------------
   date：          2021/11/16
   Author :        aGrass
   File Name：     page.py
   Description :   请求参数校验
-------------------------------------------------
   Change Activity:
                   2021/11/16
-------------------------------------------------
"""
from collections import namedtuple
from wtforms import IntegerField, StringField, Form, DateTimeField

from ._validators import validators

Pagin = namedtuple('Pagin', ('offset', 'limit'))
AtypicalProcessState = {'unset': None, 'done': True, 'pending': False}


class Pagination(Form):
    """分页表单"""
    start = DateTimeField('start_time', validators=(validators.require,))
    end = DateTimeField('end_time', validators=(validators.require,))
    data_type = StringField("type", validators=(validators.require,))
    callee = StringField("tel", validators=(validators.optional, validators.regex('\d{5,11}')))
    pg = IntegerField('offset', validators=(validators.num_range(min_value=1), validators.require), default=1)
    limit = IntegerField('limit', validators=(validators.num_range(100, 10), validators.optional), default=10)

    def pagination(self) -> Pagin:
        return Pagin(offset=(self.pg.data - 1) * self.limit.data, limit=self.limit.data)
