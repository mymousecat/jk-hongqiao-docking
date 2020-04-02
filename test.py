# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     test
   Description :
   Author :       wdh
   date：          2020-03-03
-------------------------------------------------
   Change Activity:
                   2020-03-03:
-------------------------------------------------
"""

import logging
from logconf import load_my_logging_cfg

from app.db_op import get_lis_following
from app.lis_to_phexam import lis_to_phexam

from app import appconfig

log = logging.getLogger(__name__)
load_my_logging_cfg('test')

if __name__ == '__main__':
    log.info('测试日志')
    dockLisfollowing = get_lis_following(13)
    r = lis_to_phexam(3,dockLisfollowing, appconfig['YLJGMM'])
    log.info(r)
