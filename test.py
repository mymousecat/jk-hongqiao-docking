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
from app import redis
import datetime

log = logging.getLogger(__name__)
load_my_logging_cfg('test')

if __name__ == '__main__':
    log.info('测试日志')

    # from app.request_lis import request_to_lis
    # from app.utils import to_xml, get_init_dict
    #
    # r = get_init_dict()
    # request_to_lis(barcode=331228, YLJGDM='121121', YLJGMM='43463423423', SYSDM='232323', SQJGDM='ACDDE@@@',
    #                build_dict=r)
    # log.info(to_xml(r))

    from app.utils import get_barcode_from_webservice

    from app.task_to_pacs import to_pacs
    to_pacs()

