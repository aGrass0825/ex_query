"""
-------------------------------------------------
   date：          2021/11/16
   Author :        aGrass
   File Name：     field.py
   Description :   wtforms_json校验初始化
-------------------------------------------------
   Change Activity:
                   2021/11/16
-------------------------------------------------
"""
import json
from wtforms import Form
from wtforms_json import MultiDict, flatten_json, is_missing, \
    field_list_is_missing, patch_data, monkey_patch_process_formdata, monkey_patch_field_process

try:
    from wtforms_sqlalchemy.fields import (QuerySelectField, QuerySelectMultipleField)

    HAS_SQLALCHEMY_SUPPORT = True
except ImportError:
    try:
        from wtforms.ext.sqlalchemy.fields import (QuerySelectField, QuerySelectMultipleField)

        HAS_SQLALCHEMY_SUPPORT = True
    except ImportError:
        HAS_SQLALCHEMY_SUPPORT = False
from wtforms.fields import (_unset_value, BooleanField, Field, FieldList, FileField, FormField, StringField)


@classmethod
def from_json(cls, formdata=None, obj=None, prefix='', data=None, meta=None, skip_unknown_keys=True, **kwargs):
    formdata = _fix(formdata)
    form = cls(
        formdata=MultiDict(
            flatten_json(cls, formdata, skip_unknown_keys=skip_unknown_keys)
        ) if formdata else None,
        obj=obj,
        prefix=prefix,
        data=data,
        meta=meta,
        **kwargs
    )
    return form


def _fix(formdata):
    _js = json.dumps(formdata)
    _data = _js.replace('class', 'class_')
    return json.loads(_data)


def init():
    Form.is_missing = is_missing
    FieldList.is_missing = field_list_is_missing
    Form.from_json = from_json
    Form.patch_data = patch_data
    FieldList.patch_data = patch_data
    if HAS_SQLALCHEMY_SUPPORT:
        QuerySelectField.process_formdata = monkey_patch_process_formdata(
            QuerySelectField.process_formdata
        )
        QuerySelectMultipleField.process_formdata = \
            monkey_patch_process_formdata(
                QuerySelectMultipleField.process_formdata
            )
    Field.process = monkey_patch_field_process(Field.process)
    FormField.process = monkey_patch_field_process(FormField.process)
    BooleanField.false_values = BooleanField.false_values + (False,)