"""
-------------------------------------------------
   date：          2021/11/16
   Author :        aGrass
   File Name：     config.py
   Description :   配置文件
-------------------------------------------------
   Change Activity:
                   2021/11/16
-------------------------------------------------
"""
import logging
from os import path, getcwd, getenv, makedirs
from ugly_code.ex import load_json_config

CWD_PATH = getcwd()
CONTENT_PATH = path.abspath(path.join(CWD_PATH, 'content'))
LOGFILE_DIR = path.join(CONTENT_PATH, 'logs')

_REQUIRE_DIRS = [CONTENT_PATH, LOGFILE_DIR]
for d in _REQUIRE_DIRS:
    if not path.exists(d):
        makedirs(d, 0o755)

CMD_LOGGER = {
    "level": logging.WARNING,
    "format": '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S',
    "filename": "cmd.log",
    "filemode": "w+"
}

LOG_CNF = {
    'level': logging.WARNING,
    'format': '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S',
    "filename": path.join(LOGFILE_DIR, 'web.log'),
    "filemode": "w+"
}

# 连接省平台接口认证
ALARM_KEY = ""
# 连接省平台URL
REQUEST_PRO = ""
# 密钥-盐
SECRET_KEY = ""

# Redis配置
RED_CONF = {
    "host": "localhost",
    "port": 6379,
    "db": 1
  }

# _local_cfg_path = path.join(CONTENT_PATH, getenv("EX_QUERY_CNF", "config.json"))
# if path.exists(_local_cfg_path):
#     load_json_config(globals(), _local_cfg_path)
