"""
-------------------------------------------------
   date：          2021/11/16
   Author :        aGrass
   File Name：     _tool.py
   Description :
-------------------------------------------------
   Change Activity:
                   2021/11/16
-------------------------------------------------
"""
import sys
import time
import random
from typing import Any


def _rand_sleep():
    time.sleep(random.randint(1000, 3000) / 1000)


def _println(message: str, *args: Any):
    if args:
        message = message.format(*args)
    sys.stderr.write("{}\n".format(message))
