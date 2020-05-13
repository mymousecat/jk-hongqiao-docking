# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     task_lis_to_phexam
   Description :
   Author :       wdh
   date：          2020-04-04
-------------------------------------------------
   Change Activity:
                   2020-04-04:
-------------------------------------------------
"""

import logging
from .param_config import CurPosParams
from .db_op import get_lis_following, save_lis_log
from .models import DockingLisLog
from .lis_to_phexam import lis_to_phexam
from . import appconfig
from .err import NotFoundException
from jktj.tjexception import TJException

log = logging.getLogger(__name__)


def _save_lis_log(r):
    log = DockingLisLog()
    log.ORDER_ID = r['orderId']
    log.ASSEMS = r['assems']
    log.ASSEM_NAME = r['assem_name']
    log.OP = r['op']
    log.IS_SUCCESS = r['is_success']
    log.MSG = r['msg']
    log.BARCODE = r['barcode']
    log.LIS_RESULT = r['lis_result']
    save_lis_log(log)


def lis_phexam():
    log.info('开始从配置文件中获取ID信息...')
    cur = CurPosParams('lis_to_phexam')
    id = cur.get()
    log.info('获取到当前的ID：{}'.format(id))
    dockingLisFollowing = None
    try:
        dockingLisFollowing = get_lis_following(id)
        if not dockingLisFollowing:
            log.info('没有在lis变动状态表中，发现比ID:{}大的新条码，程序将退出....'.format(id))
            return
        log.info('获取到id:{}  预约号:{}  条码号:{}'.format(dockingLisFollowing.id, dockingLisFollowing.BRID,
                                                   dockingLisFollowing.ZXTM))

        log.info('开始上传，，，')

        r_list = lis_to_phexam(appconfig['LIS_DEPARTMENT_ID'], dockingLisFollowing, appconfig['YLJGMM'])

        log.info('获取上传的日志为:{}'.format(r_list))

        for r in r_list:
            log.info('获取到上传的日志结果为:{}'.format(r))
            if (r['ex'] is not None) and (not isinstance(r['ex'], TJException)):
                raise r['ex']  # 则抛出这个异常，待上一层去处理

            # 将日志保存到数据表t_docking_lis_log中，便于以后查询
            _save_lis_log(r)

        cur.save(dockingLisFollowing.id)

    except (NotFoundException,TJException) as e:
        cur.save(dockingLisFollowing.id)
        log.error('接收Lis结果时发生错误,预约号为:{}'.format(dockingLisFollowing.BRID))
        log.error(e)

    except Exception as e:
        log.error('接收Lis结果时发生错误,预约号为:{}'.format(dockingLisFollowing.BRID))
        log.error(e)
