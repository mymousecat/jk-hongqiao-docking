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
    # log.info(redis_store.set('ho'))
    # redis.getset('wdh.ho', 'token', ex=20)
    # redis.expireat('wdh.ho','2020-03-03 18:33:00');
    # redis.set('wdh.ho', 'token')
    # redis.expireat('wdh.ho', datetime.datetime.now() + datetime.timedelta(seconds=30))
    # redis.pexpireat()

    # log.info(datetime.datetime.now().timetuple())

    # now = datetime.datetime(year=2020, month=3, day=3)
    # log.info((now.time().max - now.time()).seconds)

    # log.info(now.time().max.hour - now.time().second)
    # max = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    # max = datetime.datetime.combine(now.today(), now.time().max)

    # log.info(max)
    #
    # log.info((max - now).seconds)

    # redis.expireat()

    # print(d)

    # ex = (max - now).seconds
    #
    # mex = (max - now).seconds
    #
    # log.info('ex={}'.format(mex))
    #
    # redis.set('wdh.ho', 'hello world', ex=ex)

    # log.info(redis.get('wdh.ho'))

    from app.websrv import check_params

    from app.request_lis import request_to_lis
    from app.utils import to_xml,get_init_dict

    r = get_init_dict()
    request_to_lis(331228, '121121', '43463423423', '232323', 'ACDDE@@@', '111111',r)
    log.info(to_xml(r))
