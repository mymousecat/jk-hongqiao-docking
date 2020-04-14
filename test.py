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

from app.db_op import get_pacs_following_by_id

from app.pacs_to_phexam import pacs_to_phexam

from app import appconfig

log = logging.getLogger(__name__)
load_my_logging_cfg('test')

if __name__ == '__main__':
   pacs = get_pacs_following_by_id(None)
   pacs_to_phexam(pacs,appconfig['YLJGMM'])
