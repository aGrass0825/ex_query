"""
-------------------------------------------------
   date：          2021/11/16
   Author :        aGrass
   File Name：     serv.py
   Description :   服务启动
-------------------------------------------------
   Change Activity:
                   2021/11/16
-------------------------------------------------
"""
import sys
from os import path
from ugly_code.cmd import CMDHolder

from ._typing import Runner
from .services import SchedulerService
from config import CMD_LOGGER, LOGFILE_DIR


@CMDHolder.command('serve', '中间库拉取数据服务')
def _original():
    Runner((SchedulerService,), CMD_LOGGER).serve()


def main():
    if CMD_LOGGER.get('filename') and len(sys.argv) > 1:
        filename = CMD_LOGGER['filename']
        base_name, ext = path.splitext(filename)
        CMD_LOGGER['filename'] = path.join(LOGFILE_DIR, "{}-{}{}".format(base_name, sys.argv[1], ext))
    CMDHolder(__name__).execute()
