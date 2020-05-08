# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     task_pacs_to_phexam
   Description :
   Author :       wdh
   date：          2020-04-15
-------------------------------------------------
   Change Activity:
                   2020-04-15:
-------------------------------------------------
"""

import logging
from .param_config import CurPosParams
from .db_op import get_pacs_following_by_id, save_pacs_log
from .models import DockingPacsLog
from .pacs_to_phexam import pacs_to_phexam
from . import appconfig
from .err import InvalidParamException
from jktj.tjexception import TJException

log = logging.getLogger(__name__)


def _save_pacs_log(r):
    log = DockingPacsLog()
    log.ORDER_ID = r['orderId']
    log.ASSEMS = r['assems']
    log.ASSEM_NAME = r['assem_name']
    log.OP = r['op']
    log.IS_SUCCESS = r['is_success']
    log.MSG = r['msg']
    save_pacs_log(log)


def pacs_phexam():
    log.info('开始从配置文件中获取ID信息...')
    cur = CurPosParams('pacs_to_phexam')
    id = cur.get()
    log.info('获取到当前的ID：{}'.format(id))
    dockingPacsFollowing = None
    try:
        dockingPacsFollowing = get_pacs_following_by_id(id)
        if not dockingPacsFollowing:
            log.info('没有在pacs变动状态表中，发现比ID:{}大的新条码，程序将退出....'.format(id))
            return

        log.info('开始上传，，，')

        r_list = pacs_to_phexam(dockingPacsFollowing, appconfig['YLJGMM'])

        log.info('获取上传的日志为:{}'.format(r_list))

        for r in r_list:
            log.info('获取到上传的日志结果为:{}'.format(r))
            if (r['ex'] is not None) and (not isinstance(r['ex'], TJException)):
                raise r['ex']  # 则抛出这个异常，待上一层去处理

            # 将日志保存到数据表t_docking_pacs_log中，便于以后查询
            _save_pacs_log(r)

        cur.save(dockingPacsFollowing.id)

    except InvalidParamException as e:
        cur.save(dockingPacsFollowing.id)
        log.error('接收PACS结果时发生错误,预约号为:{}'.format(dockingPacsFollowing.BRID))
        log.error(e)

    except Exception as e:
        log.error('接收PACS结果时发生错误,预约号为:{}'.format(dockingPacsFollowing.BRID))
        log.error(e)