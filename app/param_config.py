# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     param_config
   Description :
   Author :       wdh
   date：          2020-03-08
-------------------------------------------------
   Change Activity:
                   2020-03-08:
-------------------------------------------------
"""

import os
import json
from . import app


class CurPosParams:
    """
      记录和读取当前位置信息
    """

    def __init__(self, conf_name):
        self._filename = os.path.join(app.config['CONF_PATH'], '{}.json'.format(conf_name))
        self._r = {'curPos': None}

    def save(self, pos):
        self._r['curPos'] = pos
        with open(self._filename, 'w') as f:
            json.dump(self._r, f)

    def get(self):
        if not os.path.exists(self._filename):
            return None
        with open(self._filename, 'r') as f:
            try:
                r = json.load(f)
                return r['curPos']
            except:
                return None
